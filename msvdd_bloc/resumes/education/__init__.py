"""
education
---------
"""
from msvdd_bloc import MODELS_DIR as _MDIR
from . import augment
from . import constants
from . import generate
from . import parse


FPATH_TRAINING_DATA = _MDIR.joinpath("resumes", "resume-education-training-data.jsonl")
FPATH_TAGGER = _MDIR.joinpath("resumes", "resume-education-tagger.crfsuite")
LABELS = (
    "institution",
    "area",
    "study_type",
    "start_date",
    "end_date",
    "gpa",
    "course",
    "field_sep",
    "item_sep",
    "field_label",
    "bullet",
    "other",
)
"""
Tuple[str]: Collection of labels applied to field values when parsing "education" section.
"""
