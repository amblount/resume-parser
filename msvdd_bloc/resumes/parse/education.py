import itertools
import logging
import operator

import probablepeople
import pycrfsuite
import usaddress
from toolz import itertoolz

import msvdd_bloc
from msvdd_bloc import regexes
from msvdd_bloc.resumes.parse import utils


LOGGER = logging.getLogger(__name__)

#######################
## CRF-BASED PARSING ##
#######################

# NOTE: required objects are as follows
# - TRAINING_DATA_FPATH (:class:`pathlib.Path`)
# - MODEL_FPATH (:class:`pathlib.Path`)
# - TAGGER (:class:`pycrfsuite.Tagger`)
# - LABELS (List[str])
# - featurize (func)

TRAINING_DATA_FPATH = msvdd_bloc.MODELS_DIR.joinpath("resumes", "resume-education-training-data.jsonl")
MODEL_FPATH = msvdd_bloc.MODELS_DIR.joinpath("resumes", "resume-education.crfsuite")

try:
    TAGGER = pycrfsuite.Tagger()
    TAGGER.open(str(MODEL_FPATH))
except IOError:
    TAGGER = None

LABELS = (
    "other",        # 0
    "institution",  # 1
    "area",         # 2
    "study_type",   # 3
    "start_date",   # 4
    "end_date",     # 5
    "gpa",          # 6
    "course",       # 7
    "field_sep",    # 8
    "item_sep",     # 9
    "field_label",  # 10
)

FIELD_SEP_CHARS = {",", ";", ":", "|", "-", "–"}
STUDY_TYPES = {
    "BA", "B.A.", "BS", "B.S.", "B.Sc.", "Bachelor", "Bachelors",
    "MA", "M.A.", "MS", "M.S.", "MBA", "M.B.A.", "Masters",
    "PhD", "Ph.D.", "Doctorate", "Doctor",
    "MD", "M.D.", "JD", "J.D.",
}
SEASON_NAMES = {"spring", "summer", "fall", "winter"}


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
        tokens_features = [{"_start": True}] + tokens_features + [{"_end": True}]
        for prev_tf, curr_tf, next_tf in itertoolz.sliding_window(3, tokens_features):
            tf = curr_tf.copy()
            tf["prev"] = prev_tf
            tf["next"] = next_tf
            # NOTE: add features here that depend upon tokens elsewhere in the sequence
            # e.g. whether or not a particular word appeared earlier in the sequence
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
    features = utils.get_token_features_base(token)
    features.update(
        {
            "is_field_sep_char": token.text in FIELD_SEP_CHARS,
            "is_study_type": token.text in STUDY_TYPES,
            "is_month_name": regexes.RE_MONTH.match(token.text) is not None,
            "is_season_name": token.lower_ in SEASON_NAMES,
            "is_year": regexes.RE_YEAR.match(token.text) is not None,
        }
    )
    return features
