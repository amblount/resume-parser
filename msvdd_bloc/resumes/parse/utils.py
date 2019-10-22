import importlib
import sys

import spacy


TOKENIZER = spacy.blank("en")


def tokenize(line):
    """
    Split ``line`` into a sequence of spaCy tokens to be featurized.

    Args:
        line (List[str] or str)

    Returns:
        List[:class:`spacy.tokens.Token`]
    """
    if isinstance(line, str):
        line_str = line
    elif isinstance(line, (list, tuple)):
        line_str = " ".join(line)
    else:
        raise TypeError("`line` must be a str or List[str], not {}".format(type(line)))

    return [tok for tok in TOKENIZER(line_str)]


def load_module_from_path(*, name, fpath):
    """
    Args:
        name (str)
        fpath (str of :class:`pathlib.Path`)
    """
    if name in sys.modules:
        return sys.modules[name]
    else:
        spec = importlib.util.spec_from_file_location(name, fpath)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module
