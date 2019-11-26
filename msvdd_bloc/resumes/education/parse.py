import itertools
import logging
import operator

from toolz import itertoolz

from msvdd_bloc import regexes, tokenize
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
INSTITUTION_TEXTS = {
    "university", "college", "institute", "department", "dept.",
    "high", "school", "academy",
}


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

    tokens = tokenize.tokenize("\n".join(lines).strip())
    features = featurize(tokens)
    labeled_tokens = parse_utils.tag(tokens, features, tagger=tagger)
    results = _parse_labeled_tokens(labeled_tokens)
    return results


def _parse_labeled_tokens(labeled_tokens):
    """
    Args:
        labeled_tokens (List[Tuple[:class:`spacy.tokens.Token`, str]])

    Returns:
        List[Dict[str, obj]]
    """
    one_per_result_labels = {"institution", "study_type", "end_date"}
    excluded_labels = {"other", "field_sep", "item_sep", "field_label", "bullet"}
    results = []
    result = {}
    result_courses = []
    for label, tls in itertools.groupby(labeled_tokens, key=operator.itemgetter(1)):
        if label in excluded_labels:
            continue
        field_text = "".join(tok.text_with_ws for tok, _ in tls).strip()
        if label == "course":
            result_courses.append(field_text)
        # key assumption: results can only have one of certain fields
        # and the appearance of another such field indicates a new result
        elif label in one_per_result_labels and result.get(label):
            # add current result to results list
            if result_courses:
                result["courses"] = result_courses
            results.append(result)
            # start a new result
            result = {label: field_text}
            result_courses = []
        else:
            result[label] = field_text
    # add leftover result to the list
    if result:
        if result_courses:
            result["courses"] = result_courses
        results.append(result)
    return results


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
        line_idx_windows = parse_utils.get_line_token_idxs(tokens_features)
        prev_line_idx, next_line_idx = next(line_idx_windows)
        follows_bullet = False
        n_pad_l, n_pad_r = 3, 2
        tokens_features = parse_utils.pad_tokens_features(
            tokens_features, n_left=n_pad_l, n_right=n_pad_r)
        tf_windows = itertoolz.sliding_window(n_pad_l + n_pad_r + 1, tokens_features)
        for ppprev_tf, pprev_tf, prev_tf, curr_tf, next_tf, nnext_tf in tf_windows:
            tf = curr_tf.copy()
            # add features from surrounding tokens, for context
            tf["ppprev"] = ppprev_tf
            tf["pprev"] = pprev_tf
            tf["prev"] = prev_tf
            tf["next"] = next_tf
            tf["nnext"] = nnext_tf
            # add features dependent on this token's position within the sequence
            # and its relationship to other tokens
            tok_idx = tf["idx"]
            line_tfs = tokens_features[prev_line_idx + n_pad_l : next_line_idx + n_pad_l]
            if tf["is_newline"] and tf["idx"] > 0:
                prev_line_idx, next_line_idx = next(line_idx_windows)
                follows_bullet = False
            tf["tok_line_idx"] = tok_idx - prev_line_idx
            tf["follows_bullet"] = follows_bullet
            # is this token a bullet? i.e. "- " token starting a new line
            if tf["shape"] == "-" and tf["tok_line_idx"] == 1:
                follows_bullet = True
            if tf["like_year"] is True:
                year = int(curr_tf["prefix"] + curr_tf["suffix"])
                other_years = [
                    int(_tf["prefix"] + _tf["suffix"])
                    for _tf in line_tfs
                    if _tf["like_year"] is True and _tf["idx"] != tok_idx
                ]
                if other_years:
                    tf["is_max_line_year"] = all(year > oyr for oyr in other_years)
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
            "is_institution_text": text.lower() in INSTITUTION_TEXTS,
            "like_month_name": regexes.RE_MONTH.match(text) is not None,
            "like_year": regexes.RE_YEAR.match(text) is not None,
        }
    )
    return features
