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


def get_token_features_base(token):
    """
    Get base per-token features, independent of other tokens within its sequence.
    Specific sections should add to / remove from these features, as needed.

    Args:
        token (:class:`spacy.tokens.Token`)

    Returns:
        Dict[str, obj]
    """
    return {
        "i": token.i,
        "len": len(token),
        "shape": token.shape_,
        "prefix": token.prefix_,
        "suffix": token.suffix_,
        "is_alnum": token.text.isalnum(),
        "is_alpha": token.is_alpha,
        "is_digit": token.is_digit,
        "is_lower": token.is_lower,
        "is_upper": token.is_upper,
        "is_title": token.is_title,
        "is_punct": token.is_punct,
        "is_left_punct": token.is_left_punct,
        "is_right_punct": token.is_right_punct,
        "is_bracket": token.is_bracket,
        "is_space": token.is_space,
        "like_num": token.like_num,
        "like_url": token.like_url,
        "like_email": token.like_email,
        "is_stop": token.is_stop,
    }


def tag(*, tokens, features, tagger):
    """
    Tag each token in ``tokens`` with a section-specific label based on its features.

    Args:
        tokens (List[:class:`spacy.tokens.Token`]): As output by :func:`tokenize()`.
        features (List[Dict[str, obj]]): As output by a section-specific ``featurize()``.
        tagger (:class:`pycrfsuite.Tagger`): Trained, section-specific CRF tagger.

    Returns:
        List[Tuple[:class:`spacy.tokens.Token`, str]]: Ordered sequence of
        (token, tag) pairs.
    """
    tags = tagger.tag(features)
    return list(zip(tokens, tags))


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
