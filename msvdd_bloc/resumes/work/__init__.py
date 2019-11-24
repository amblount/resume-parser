"""
work
----
"""
from msvdd_bloc import MODELS_DIR as _MDIR
from . import augment
from . import constants
from . import generate
from . import parse


FPATH_TRAINING_DATA = _MDIR.joinpath("resumes", "resume-work-training-data.jsonl")
FPATH_TAGGER = _MDIR.joinpath("resumes", "resume-work-tagger.crfsuite")
LABELS = (
    "company",
    "position",
    "website",
    "start_date",
    "end_date",
    "summary",
    "highlights",
    "field_sep",
    "item_sep",
    "location",
    "other",
)
"""
Tuple[str]: Collection of labels applied to field values when parsing "work" section.
"""
