import itertools
import logging
import operator

from toolz import itertoolz

from msvdd_bloc import regexes
from msvdd_bloc.resumes import parse_utils
from msvdd_bloc.resumes import work


LOGGER = logging.getLogger(__name__)

FIELD_SEP_TEXTS = {
    sep for sep in itertoolz.concatv(
        work.constants.FIELD_SEPS,
        work.constants.FIELD_SEP_DTS,
        work.constants.FIELD_SEP_SMS,
        work.constants.LEFT_BRACKETS,
        work.constants.RIGHT_BRACKETS,
    )
}
COMPANY_TYPE_TEXTS = set(work.constants.COMPANY_TYPES)
POSITION_TEXTS = set(work.constants.POSITION_LEVELS + work.constants.POSITION_TYPES)


def parse_lines(lines, tagger=None):
    """
    Parse a sequence of text lines belonging to the "work" section of a résumé
    to produce structured data in the form of :class:`schemas.ResumeWorkSchema`
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
    return []


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
            tokens_features, n_left=3, n_right=2)
        idx_last_newline = 0
        idx_last_bullet = 0
        tf_windows = itertoolz.sliding_window(6, tokens_features)
        for ppprev_tf, pprev_tf, prev_tf, curr_tf, next_tf, nnext_tf in tf_windows:
            tf = curr_tf.copy()
            tf["ppprev"] = ppprev_tf
            tf["pprev"] = pprev_tf
            tf["prev"] = prev_tf
            tf["next"] = next_tf
            tf["nnext"] = nnext_tf
            # NOTE: add features here that depend upon tokens elsewhere in the sequence
            # e.g. whether or not a particular word appeared earlier in the sequence
            if all(char == "\n" for char in tf["shape"]):
                idx_last_newline = tf["idx"]
            tf["n_toks_since_newline"] = tf["idx"] - idx_last_newline
            if tf["shape"] == "-" and tf["n_toks_since_newline"] == 1:
                idx_last_bullet = tf["idx"]
            tf["n_toks_since_bullet"] = tf["idx"] - idx_last_bullet
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
            "is_company_type_text": text in COMPANY_TYPE_TEXTS,
            "is_position_text": text in POSITION_TEXTS,
            "like_month_name": regexes.RE_MONTH.match(text) is not None,
            "like_year": regexes.RE_YEAR.match(text) is not None,
        }
    )
    return features
