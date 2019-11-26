import pytest
from spacy.tokens import Token

from msvdd_bloc import tokenize


class TestTokenize:

    def test_line_str(self):
        line = "This is an example line."
        exp_texts = ["This", "is", "an", "example", "line", "."]
        tokens = tokenize.tokenize(line)
        assert tokens
        assert (
            isinstance(tokens, list) and
            all(isinstance(tok, Token) for tok in tokens)
        )
        assert [tok.text for tok in tokens] == exp_texts

    def test_line_list(self):
        line = ["This", "is", "an", "example", "line", "."]
        tokens = tokenize.tokenize(line)
        assert tokens
        assert (
            isinstance(tokens, list) and
            all(isinstance(tok, Token) for tok in tokens)
        )
        assert [tok.text for tok in tokens] == line

    def test_phone_number_merge(self):
        line = "Call me at 555-123-4567 ASAP."
        exp_texts = ["Call", "me", "at", "555-123-4567", "ASAP", "."]
        tokens = tokenize.tokenize(line)
        assert tokens
        assert (
            isinstance(tokens, list) and
            all(isinstance(tok, Token) for tok in tokens)
        )
        assert [tok.text for tok in tokens] == exp_texts

    def test_date_range_split(self):
        line = "I worked there 2012–2015."
        exp_texts = ["I", "worked", "there", "2012", "–", "2015", "."]
        tokens = tokenize.tokenize(line)
        assert tokens
        assert (
            isinstance(tokens, list) and
            all(isinstance(tok, Token) for tok in tokens)
        )
        assert [tok.text for tok in tokens] == exp_texts
