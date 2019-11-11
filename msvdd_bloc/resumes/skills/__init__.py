from msvdd_bloc import MODELS_DIR as _MDIR
from . import constants
from . import generate
from . import parse


FPATH_TRAINING_DATA = _MDIR.joinpath("resumes", "resume-skills-training-data.jsonl")
FPATH_TAGGER = _MDIR.joinpath("resumes", "resume-skills-tagger.crfsuite")
LABELS = (
    "bullet",
    "name",
    "keyword",
    "level",
    "field_sep",
    "item_sep",
    "other",
)
