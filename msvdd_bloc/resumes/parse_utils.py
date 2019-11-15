import importlib
import logging
import string
import sys

import pycrfsuite
import spacy
from spacy.tokens import Doc


LOGGER = logging.getLogger(__name__)
_PUNCT_CHARS = set(string.punctuation)


def tokenize(line):
    """
    Split ``line`` into a sequence of spaCy tokens to be featurized.

    Args:
        line (List[str] or str)

    Returns:
        List[:class:`spacy.tokens.Token`]
    """
    if isinstance(line, str):
        return [tok for tok in TOKENIZER(line)]
    elif isinstance(line, (list, tuple)):
        return [tok for tok in Doc(TOKENIZER.vocab, words=line)]
    else:
        raise TypeError("`line` must be a str or List[str], not {}".format(type(line)))


def get_token_features_base(token):
    """
    Get base per-token features, independent of other tokens within its sequence.
    Specific sections should add to / remove from these features, as needed.

    Args:
        token (:class:`spacy.tokens.Token`)

    Returns:
        Dict[str, obj]
    """
    text = token.text
    return {
        "idx": token.i,
        "len": len(token),
        "shape": token.shape_,
        "prefix": token.prefix_,
        "suffix": token.suffix_,
        "is_alpha": token.is_alpha,
        "is_digit": token.is_digit,
        "is_lower": token.is_lower,
        "is_upper": token.is_upper,
        "is_title": token.is_title,
        "is_punct": token.is_punct,
        "is_left_punct": token.is_left_punct,
        "is_right_punct": token.is_right_punct,
        "is_bracket": token.is_bracket,
        "is_quote": token.is_quote,
        "is_space": token.is_space,
        "like_num": token.like_num,
        "like_url": token.like_url,
        "like_email": token.like_email,
        "is_stop": token.is_stop,
        "is_alnum": text.isalnum(),
        "is_partial_digit": any(c.isdigit() for c in text) and not all(c.isdigit() for c in text),
        "is_partial_punct": any(c in _PUNCT_CHARS for c in text) and not all(c in _PUNCT_CHARS for c in text),
    }


def pad_tokens_features(tokens_features, *, n_left=1, n_right=1):
    """
    Pad list of tokens' features on the left and/or right with a configurable number of
    dummy feature dicts.

    Args:
        tokens_features (List[Dict[str, obj]])
        n_left (int): Number of dummy feature dicts to prepend.
        n_right (int): Number of dummy feature dicts to append.

    Returns:
        List[Dict[str, obj]]
    """
    return (
        [{"_start": True} for _ in range(n_left)]
        + tokens_features
        + [{"_end": True} for _ in range(n_right)]
    )


def tag(tokens, features, *, tagger):
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


def load_tagger(fpath):
    """
    Args:
        fpath (str or :class:`pathlib.Path`)

    Returns:
        :class:`pycrfsuite.Tagger`
    """
    try:
        tagger = pycrfsuite.Tagger()
        tagger.open(str(fpath))
        return tagger
    except IOError:
        LOGGER.warning(
            "tagger model file '%s' is missing; have you trained one yet? "
            "if not, use the `label_parser_training_data.py` script to do so.",
            fpath,
        )
        raise


class PhoneNumberMerger:
    """
    Custom spaCy pipeline component that merges contiguous tokens matching
    typical phone number patterns into a single token.
    """

    def __init__(self, nlp):
        self.matcher = spacy.matcher.Matcher(nlp.vocab)
        self.matcher.add(
            "phone",
            None,
            [{"SHAPE": "ddd"}, {"SHAPE": "ddd"}, {"SHAPE": "dddd"}],
            [{"SHAPE": "ddd"}, {"TEXT": "-", "OP": "?"}, {"SHAPE": "ddd"}, {"TEXT": "-"}, {"SHAPE": "dddd"}],
            [{"SHAPE": "ddd"}, {"TEXT": ".", "OP": "?"}, {"SHAPE": "ddd"}, {"TEXT": "."}, {"SHAPE": "dddd"}],
            [{"TEXT": "("}, {"SHAPE": "ddd"}, {"TEXT": ")"}, {"SHAPE": "ddd"}, {"TEXT": "-"}, {"SHAPE": "dddd"}],
            [{"TEXT": "("}, {"SHAPE": "ddd"}, {"TEXT": ")"}, {"SHAPE": "ddd"}, {"TEXT": {"REGEX": "[.-]"}}, {"SHAPE": "dddd"}],
            [{"SHAPE": "+d"}, {"TEXT": "("}, {"SHAPE": "ddd"}, {"TEXT": ")"}, {"SHAPE": "ddd"}, {"TEXT": "-"}, {"SHAPE": "dddd"}],
            [{"TEXT": "("}, {"SHAPE": "ddd)ddd"}, {"TEXT": {"REGEX": "[.-]"}}, {"SHAPE": "dddd"}],
        )

    def __call__(self, doc):
        matches = spacy.util.filter_spans(
            [doc[start:end] for _, start, end in self.matcher(doc)]
        )
        with doc.retokenize() as retokenizer:
            for match in matches:
                retokenizer.merge(match)
        return doc


TOKENIZER = spacy.blank("en")
TOKENIZER.add_pipe(PhoneNumberMerger(TOKENIZER), last=True)
