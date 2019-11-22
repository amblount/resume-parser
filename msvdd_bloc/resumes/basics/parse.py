import itertools
import logging
import operator

import probablepeople
import usaddress
from toolz import itertoolz

from msvdd_bloc import regexes
from msvdd_bloc.resumes import basics
from msvdd_bloc.resumes import parse_utils


LOGGER = logging.getLogger(__name__)

#######################
## CRF-BASED PARSING ##
#######################

FIELD_SEP_TEXTS = set(basics.constants.FIELD_SEPS)
ITEM_SEP_TEXTS = set(basics.constants.ITEM_SEPS)


def parse_lines(lines, tagger=None):
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
    labeled_tokens = parse_utils.tag(tokens, features, tagger=tagger)
    data = _parse_labeled_tokens(labeled_tokens)
    return data


def _parse_labeled_tokens(labeled_tokens):
    """
    Args:
        labeled_tokens (List[Tuple[:class:`spacy.tokens.Token`, str]])

    Returns:
        Dict[str, obj]
    """
    excluded_labels = {"other", "field_sep", "item_sep", "field_label"}
    data = {}
    profiles = []
    summary_lines = []
    for label, tls in itertools.groupby(labeled_tokens, key=operator.itemgetter(1)):
        field_text = "".join(tok.text_with_ws for tok, _ in tls).strip()
        if label in excluded_labels:
            continue
        elif label == "location":
            try:
                location, location_type = usaddress.tag(
                    field_text.replace("\n", " "),
                    tag_mapping=basics.constants.LOCATION_TAG_MAPPING,
                )
            except usaddress.RepeatedLabelError as e:
                LOGGER.debug("'location' parsing error:\n%s", e)
                continue
            if location_type == "Street Address":
                location = dict(location)
                if "recipient" in location:
                    data["name"] = location.pop("recipient")
                data["location"] = location
        # HACK: social profiles are not handled well by the parser or this function
        # bc it wasn't clear how best to identify the network and/or url based on
        # the fragments + icons typically included in résumés, *especially* since
        # the PDF extractor can't turn those social icons into unicode chars
        elif label == "profile":
            profiles.append({"username": field_text})
        elif label == "summary":
            summary_lines.append(field_text)
        else:
            data[label] = field_text
    if profiles:
        data["profiles"] = profiles
    if summary_lines:
        data["summary"] = "\n".join(summary_lines)
    return data


def featurize(tokens):
    """
    Get features from individual tokens as well as those that are dependent on
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
        tokens_features = parse_utils.pad_tokens_features(
            tokens_features, n_left=2, n_right=2)
        idx_last_newline = 0
        follows_bullet = False
        tf_windows = itertoolz.sliding_window(5, tokens_features)
        for pprev_tf, prev_tf, tf, next_tf, nnext_tf in tf_windows:
            tf = tf.copy()
            tf["pprev"] = pprev_tf
            tf["prev"] = prev_tf
            tf["next"] = next_tf
            tf["nnext"] = nnext_tf
            # NOTE: add features here that depend upon tokens elsewhere in the sequence
            # e.g. whether or not a particular word appeared earlier in the sequence
            if all(char == "\n" for char in tf["shape"]):
                idx_last_newline = tf["idx"]
                follows_bullet = False
            tf["n_toks_since_newline"] = tf["idx"] - idx_last_newline
            tf["follows_bullet"] = follows_bullet
            # is this token a bullet? i.e. "- " token starting a new line
            if tf["shape"] == "-" and tf["n_toks_since_newline"] == 1:
                follows_bullet = True
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
    text = token.text
    features = parse_utils.get_token_features_base(token)
    features.update(
        {
            "is_field_sep_text": text in FIELD_SEP_TEXTS,
            "is_item_sep_text": text in ITEM_SEP_TEXTS,
            "like_profile_username": regexes.RE_USER_HANDLE.match(text) is not None,
            "like_phone_number": regexes.RE_PHONE_NUMBER.match(text) is not None,
        }
    )
    return features


#########################
## RULES-BASED PARSING ##
#########################

def parse_lines_rules_based_version(lines):
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
    data = {}
    for line in lines:
        if not line:
            continue
        for line_chunk in regexes.RE_LINE_DELIM.split(line):
            if not line_chunk:
                continue
            if "email" not in data:
                match = regexes.RE_EMAIL.search(line_chunk)
                if match:
                    data["email"] = match.group()
                    start, end = match.span()
                    if start == 0 and end == len(line_chunk):
                        continue
                    else:
                        line_chunk = line_chunk[:start] + line_chunk[end:]
            if "phone" not in data:
                match = regexes.RE_PHONE_NUMBER.search(line_chunk)
                if match:
                    data["phone"] = match.group()
                    start, end = match.span()
                    if start == 0 and end == len(line_chunk):
                        continue
                    else:
                        line_chunk = line_chunk[:start] + line_chunk[end:]
            if "website" not in data:
                match = regexes.RE_URL.search(line_chunk)
                if match:
                    data["website"] = match.group()
                    start, end = match.span()
                    if start == 0 and end == len(line_chunk):
                        continue
                    else:
                        line_chunk = line_chunk[:start] + line_chunk[end:]
            if "profiles" not in data:
                match = regexes.RE_USER_HANDLE.search(line_chunk)
                if match:
                    data["profiles"] = [{"username": match.group()}]
                    start, end = match.span()
                    if start == 0 and end == len(line_chunk):
                        continue
                    else:
                        line_chunk = line_chunk[:start] + line_chunk[end:]
            if "location" not in data:
                try:
                    location, location_type = usaddress.tag(
                        line_chunk, tag_mapping=basics.constants.LOCATION_TAG_MAPPING)
                except usaddress.RepeatedLabelError as e:
                    LOGGER.debug("'location' parsing error:\n%s", e)
                    continue
                if location_type == "Street Address":
                    location = dict(location)
                    if "recipient" in location:
                        data["name"] = location.pop("recipient")
                    data["location"] = location
            if "name" not in data:
                try:
                    name, name_type = probablepeople.tag(line_chunk)
                except probablepeople.RepeatedLabelError as e:
                    LOGGER.debug("'name' parsing error:\n%s", e)
                    continue
                if name_type == "Person":
                    data["name"] = " ".join(name.values())
    return data
