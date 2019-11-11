import itertools
import logging
import operator

import probablepeople
import usaddress
from toolz import itertoolz

from msvdd_bloc import regexes
from msvdd_bloc.providers import resume_basics
from msvdd_bloc.resumes import basics
from msvdd_bloc.resumes import parse_utils


LOGGER = logging.getLogger(__name__)

_LOCATION_TAG_MAPPING = {
   'Recipient': 'recipient',
   'AddressNumber': 'address',
   'AddressNumberPrefix': 'address',
   'AddressNumberSuffix': 'address',
   'StreetName': 'address',
   'StreetNamePreDirectional': 'address',
   'StreetNamePreModifier': 'address',
   'StreetNamePreType': 'address',
   'StreetNamePostDirectional': 'address',
   'StreetNamePostModifier': 'address',
   'StreetNamePostType': 'address',
   'CornerOf': 'address',
   'IntersectionSeparator': 'address',
   'LandmarkName': 'address',
   'USPSBoxGroupID': 'address',
   'USPSBoxGroupType': 'address',
   'USPSBoxID': 'address',
   'USPSBoxType': 'address',
   'BuildingName': 'address',
   'OccupancyType': 'address',
   'OccupancyIdentifier': 'address',
   'SubaddressIdentifier': 'address',
   'SubaddressType': 'address',
   'PlaceName': 'city',
   'StateName': 'region',
   'ZipCode': 'postal_code',
}
"""
Dict[str, str]: Mapping of ``usaddress` location tag to corresponding résumé schema field.
"""

#######################
## CRF-BASED PARSING ##
#######################

FIELD_SEP_CHARS = set(resume_basics._FIELD_SEPS)
ITEM_SEP_CHARS = set(resume_basics._ITEM_SEPS)


def parse_basics_section(lines, tagger=None):
    """
    Parse a sequence of text lines belonging to the "basics" section of a résumé
    to produce structured data in the form of :class:`schemas.ResumeBasicsSchema`
    using trained Conditional Random Field (CRF) taggers.

    Args:
        lines (List[str])
        tagger (:class:`pycrfsuite.Tagger`)

    Returns:
        Dict[str, obj]
    """
    if tagger is None:
        tagger = parse_utils.load_tagger(basics.FPATH_TAGGER)

    tokens = parse_utils.tokenize("\n".join(lines).strip())
    features = featurize(tokens)
    tok_labels = parse_utils.tag(tokens, features, tagger=tagger)
    basics_data = _parse_basics_from_labeled_tokens(tok_labels)
    return basics_data


def _parse_basics_from_labeled_tokens(tok_labels):
    """
    Args:
        tok_labels (List[Tuple[:class:`spacy.tokens.Token`, str]])

    Returns:
        Dict[str, obj]
    """
    excluded_labels = {"other", "field_sep", "item_sep", "field_label"}
    basics_data = {}
    profiles = []
    for label, tls in itertools.groupby(tok_labels, key=operator.itemgetter(1)):
        field_text = "".join(tok.text_with_ws for tok, _ in tls).strip()
        if label in excluded_labels:
            continue
        elif label == "location":
            try:
                location, location_type = usaddress.tag(
                    field_text.replace("\n", " "),
                    tag_mapping=_LOCATION_TAG_MAPPING,
                )
            except usaddress.RepeatedLabelError as e:
                LOGGER.debug("'location' parsing error:\n%s", e)
                continue
            if location_type == "Street Address":
                location = dict(location)
                if "recipient" in location:
                    basics_data["name"] = location.pop("recipient")
                basics_data["location"] = location
        # HACK: social profiles are not handled well by the parser or this function
        # bc it wasn't clear how best to identify the network and/or url based on
        # the fragments + icons typically included in résumés, *especially* since
        # the PDF extractor can't turn those social icons into unicode chars
        elif label == "profile":
            profiles.append({"username": field_text})
        else:
            basics_data[label] = field_text
    if profiles:
        basics_data["profiles"] = profiles
    return basics_data


def featurize(tokens):
    """
    Extract features from individual tokens as well as those that are dependent on
    the sequence thereof.

    Args:
        tokens (List[:class:`spacy.tokens.Token`])

    Returns:
        List[Dict[str, obj]]
    """
    tokens_features = [get_token_features(token) for token in tokens]
    if len(tokens_features) == 1:
        tokens_features[0]["_singleton"] = True
        return tokens_features
    else:
        feature_sequence = []
        tokens_features = (
            [{"_start": True}, {"_start": True}]
            + tokens_features
            + [{"_end": True}]
        )
        idx_last_newline = 0
        for pprev_tf, prev_tf, curr_tf, next_tf in itertoolz.sliding_window(4, tokens_features):
            tf = curr_tf.copy()
            tf["pprev"] = pprev_tf
            tf["prev"] = prev_tf
            tf["next"] = next_tf
            # NOTE: add features here that depend upon tokens elsewhere in the sequence
            # e.g. whether or not a particular word appeared earlier in the sequence
            if all(char == "\n" for char in tf["shape"]):
                idx_last_newline = tf["idx"]
            tf["n_toks_since_newline"] = tf["idx"] - idx_last_newline
            feature_sequence.append(tf)
        return feature_sequence


def get_token_features(token):
    """
    Get per-token features, independent of other tokens within its sequence.

    Args:
        token (:class:`spacy.tokens.Token`)

    Returns:
        Dict[str, obj]
    """
    features = parse_utils.get_token_features_base(token)
    features.update(
        {
            "is_field_sep_char": token.text in FIELD_SEP_CHARS,
            "is_item_sep_char": token.text in ITEM_SEP_CHARS,
            "like_profile_username": regexes.RE_USER_HANDLE.match(token.text) is not None,
            "like_phone_number": regexes.RE_PHONE_NUMBER.match(token.text) is not None,
        }
    )
    return features


#########################
## RULES-BASED PARSING ##
#########################

def parse_basics_section_alt(lines):
    """
    Parse a sequence of text lines belonging to the "basics" section of a résumé
    to produce structured data in the form of :class:`schemas.ResumeBasicsSchema`
    using logical rules based on regular expressions,
    *PLUS* some pre-trained CRF parsers.

    Args:
        lines (List[str])

    Returns:
        Dict[str, obj]
    """
    basics = {}
    for line in lines:
        if not line:
            continue
        for line_chunk in regexes.RE_LINE_DELIM.split(line):
            if not line_chunk:
                continue
            if "email" not in basics:
                match = regexes.RE_EMAIL.search(line_chunk)
                if match:
                    basics["email"] = match.group()
                    start, end = match.span()
                    if start == 0 and end == len(line_chunk):
                        continue
                    else:
                        line_chunk = line_chunk[:start] + line_chunk[end:]
            if "phone" not in basics:
                match = regexes.RE_PHONE_NUMBER.search(line_chunk)
                if match:
                    basics["phone"] = match.group()
                    start, end = match.span()
                    if start == 0 and end == len(line_chunk):
                        continue
                    else:
                        line_chunk = line_chunk[:start] + line_chunk[end:]
            if "website" not in basics:
                match = regexes.RE_URL.search(line_chunk)
                if match:
                    basics["website"] = match.group()
                    start, end = match.span()
                    if start == 0 and end == len(line_chunk):
                        continue
                    else:
                        line_chunk = line_chunk[:start] + line_chunk[end:]
            if "profiles" not in basics:
                match = regexes.RE_USER_HANDLE.search(line_chunk)
                if match:
                    basics["profiles"] = [{"username": match.group()}]
                    start, end = match.span()
                    if start == 0 and end == len(line_chunk):
                        continue
                    else:
                        line_chunk = line_chunk[:start] + line_chunk[end:]
            if "location" not in basics:
                try:
                    location, location_type = usaddress.tag(
                        line_chunk, tag_mapping=_LOCATION_TAG_MAPPING)
                except usaddress.RepeatedLabelError as e:
                    LOGGER.debug("'location' parsing error:\n%s", e)
                    continue
                if location_type == "Street Address":
                    location = dict(location)
                    if "recipient" in location:
                        basics["name"] = location.pop("recipient")
                    basics["location"] = location
            if "name" not in basics:
                try:
                    name, name_type = probablepeople.tag(line_chunk)
                except probablepeople.RepeatedLabelError as e:
                    LOGGER.debug("'name' parsing error:\n%s", e)
                    continue
                if name_type == "Person":
                    basics["name"] = " ".join(name.values())
    return basics
