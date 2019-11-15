from msvdd_bloc import MODELS_DIR as _MDIR
from . import augment
from . import constants
from . import generate
from . import parse


FPATH_TRAINING_DATA = _MDIR.joinpath("resumes", "resume-skills-training-data.jsonl")
FPATH_TAGGER = _MDIR.joinpath("resumes", "resume-skills-tagger.crfsuite")
LABELS = (
    "name",
    "keyword",
    "level",
    "field_sep",
    "item_sep",
    "bullet",
    "other",
)
"""
Tuple[str]: Collection of labels applied to field values when parsing "skills" section.
"""
