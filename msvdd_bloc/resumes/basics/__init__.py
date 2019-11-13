from msvdd_bloc import MODELS_DIR as _MDIR
from . import augment
from . import constants
from . import generate
from . import parse


FPATH_TRAINING_DATA = _MDIR.joinpath("resumes", "resume-basics-training-data.jsonl")
FPATH_TAGGER = _MDIR.joinpath("resumes", "resume-basics-tagger.crfsuite")
LABELS = (
    "other",
    "name",
    "label",
    "email",
    "phone",
    "website",
    "location",
    "profile",
    "field_sep",
    "item_sep",
    "field_label",
)
