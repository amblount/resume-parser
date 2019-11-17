import pathlib

ROOT_DIR = pathlib.Path(__file__).parent.parent.resolve()
DATA_DIR = ROOT_DIR.joinpath("data")
MODELS_DIR = ROOT_DIR.joinpath("models")

from .about import __version__
from . import fileio
from . import job_postings
from . import regexes
from . import resumes
from . import schemas
from . import utils
