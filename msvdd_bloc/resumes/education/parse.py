import itertools
import logging
import operator

from toolz import itertoolz

from msvdd_bloc import regexes
from msvdd_bloc.resumes import education
from msvdd_bloc.resumes import parse_utils


LOGGER = logging.getLogger(__name__)

#######################
## CRF-BASED PARSING ##
#######################

FIELD_SEP_TEXTS = {
    sep for sep in itertoolz.concatv(
        education.constants.FIELD_SEPS,
        education.constants.FIELD_SEP_DTS,
        education.constants.FIELD_SEP_SMS,
        education.constants.LEFT_BRACKETS,
        education.constants.RIGHT_BRACKETS,
    )
}
ITEM_SEP_TEXTS = set(education.constants.FIELD_SEP_SMS)


def parse_lines(lines, tagger=None):
    """
    Parse a sequence of text lines belonging to the "education" section of a résumé
    to produce structured data in the form of :class:`schemas.ResumeEducationSchema`
    using a trained Conditional Random Field (CRF) tagger.

    Args:
        lines (List[str])
        tagger (:class:`pycrfsuite.Tagger`)

    Returns:
        List[Dict[str, obj]]
    """
    if tagger is None:
        tagger = parse_utils.load_tagger(education.FPATH_TAGGER)

    tokens = parse_utils.tokenize("\n".join(lines).strip())
    features = featurize(tokens)
    labeled_tokens = parse_utils.tag(tokens, features, tagger=tagger)
    datas = _parse_labeled_tokens(labeled_tokens)
    return datas


def _parse_labeled_tokens(labeled_tokens):
    """
    Args:
        labeled_tokens (List[Tuple[:class:`spacy.tokens.Token`, str]])

    Returns:
        List[Dict[str, obj]]
    """
    excluded_labels = {"other", "field_sep", "item_sep", "field_label", "bullet"}
    datas = []
    data = {}
    courses = []
    for label, tls in itertools.groupby(labeled_tokens, key=operator.itemgetter(1)):
        if label in excluded_labels:
            continue
        field_text = "".join(tok.text_with_ws for tok, _ in tls).strip()
        if label == "course":
            courses.append(field_text)
        # big assumption: only one institution per educational experience
        # and the appearance of a new one indicates another item
        elif label == "institution" and "institution" in data:
            if courses:
                data["courses"] = courses
            datas.append(data)
            # start a new educational experience
            data = {label: field_text}
            courses = []
        else:
            data[label] = field_text
    # add any remaining education experience to the list
    if data:
        if courses:
            data["courses"] = courses
        datas.append(data)
    return datas


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
        tokens_features = parse_utils.pad_tokens_features(
            tokens_features, n_left=2, n_right=2)
        idx_last_newline = 0
        tf_windows = itertoolz.sliding_window(5, tokens_features)
        for pprev_tf, prev_tf, curr_tf, next_tf, nnext_tf in tf_windows:
            tf = curr_tf.copy()
            tf["pprev"] = pprev_tf
            tf["prev"] = prev_tf
            tf["next"] = next_tf
            tf["nnext"] = nnext_tf
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
    text = token.text
    features = parse_utils.get_token_features_base(token)
    features.update(
        {
            "is_field_sep_text": text in FIELD_SEP_TEXTS,
            "is_item_sep_text": text in ITEM_SEP_TEXTS,
            "like_month_name": regexes.RE_MONTH.match(text) is not None,
            "like_year": regexes.RE_YEAR.match(text) is not None,
        }
    )
    return features
