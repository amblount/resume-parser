"""
tokenize
--------

Segment text into its constituent tokens using spaCy.
"""
import spacy
from spacy.tokens import Doc


def tokenize(line):
    """
    Split ``line`` into a sequence of spaCy tokens, to be featurized.

    Args:
        line (List[str] or str): If str, text to be split into tokens. If List[str],
            it's assumed that ``line`` was already tokenized at some point,
            so each str element is transformed into a token.

    Returns:
        List[:class:`spacy.tokens.Token`]
    """
    if isinstance(line, str):
        return [tok for tok in TOKENIZER(line)]
    elif isinstance(line, (list, tuple)):
        return [tok for tok in Doc(TOKENIZER.vocab, words=line)]
    else:
        raise TypeError("`line` must be a str or List[str], not {}".format(type(line)))


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
            doc[start : end] for _, start, end in self.matcher(doc)
        )
        if matches:
            with doc.retokenize() as retokenizer:
                for match in matches:
                    retokenizer.merge(match)
        return doc


class DateRangeSplitter:
    """
    Custom spaCy pipeline component that splits tokens matching a date range like
    YYYY–YYYY into separate tokens, which sneaks through the default tokenization rules.
    """

    def __init__(self, nlp):
        self.matcher = spacy.matcher.Matcher(nlp.vocab)
        self.matcher.add("date_range", None, [{"SHAPE": "dddd–dddd"}])

    def __call__(self, doc):
        matches = spacy.util.filter_spans(
            doc[start : end] for _, start, end in self.matcher(doc)
        )
        if matches:
            with doc.retokenize() as retokenizer:
                for match in matches:
                    tok = match[0]
                    text = match.text
                    orths = [text[:4], text[4], text[5:]]
                    heads = [(tok, 0), (tok, 1), (tok, 2)]
                    retokenizer.split(tok, orths, heads=heads)
        return doc


TOKENIZER = spacy.blank("en")
TOKENIZER.add_pipe(PhoneNumberMerger(TOKENIZER), last=True)
TOKENIZER.add_pipe(DateRangeSplitter(TOKENIZER), last=True)
