import pytest
from spacy.tokens import Token

from msvdd_bloc import schemas
from msvdd_bloc.resumes import parse


@pytest.fixture(scope="module")
def lines():
    return [
        "Burton DeWilde",
        "Dr. Burton J. DeWilde",
        "robert03@gmail.com | +1-397-533-1394 | https://www.howell.org/",
        "1968 Autumn Mews Suite 545 West Derekville, CA 59587",
        "Kelly Knapp  Email: xjones@pennington.net",
        "boonesteven@hammond.com - @jonesrobert - http://www.tucker.com",
    ]


@pytest.fixture(scope="module")
def tokenized_lines(lines):
    return [parse.utils.tokenize(line) for line in lines]


@pytest.fixture(scope="module")
def featurized_lines(tokenized_lines):
    return [parse.basics.featurize(tokens) for tokens in tokenized_lines]


@pytest.fixture(scope="module")
def tagged_lines(tokenized_lines, featurized_lines):
    return [
        parse.utils.tag(tokens=tokens, features=features, tagger=parse.basics.TAGGER)
        for tokens, features in zip(tokenized_lines, featurized_lines)
    ]


@pytest.fixture(scope="module")
def parsed_lines(tagged_lines):
    return [
        parse.basics._parse_basics_from_labeled_tokens(tok_labels)
        for tok_labels in tagged_lines
    ]


@pytest.fixture(scope="module")
def parsed_section(lines):
    return parse.basics.parse_basics_section(lines)


def test_tokenize(tokenized_lines):
    expected_token_texts = [
        ['Burton', 'DeWilde'],
        ['Dr.', 'Burton', 'J.', 'DeWilde'],
        ['robert03@gmail.com', '|', '+1', '-', '397', '-', '533', '-', '1394', '|', 'https://www.howell.org/'],
        ['1968', 'Autumn', 'Mews', 'Suite', '545', 'West', 'Derekville', ',', 'CA', '59587'],
        ['Kelly', 'Knapp', ' ', 'Email', ':', 'xjones@pennington.net'],
        ['boonesteven@hammond.com', '-', '@jonesrobert', '-', 'http://www.tucker.com']
    ]
    observed_token_texts = [[tok.text for tok in tokens] for tokens in tokenized_lines]
    for exp_tt, obs_tt in zip(expected_token_texts, observed_token_texts):
        assert exp_tt == obs_tt


def test_featurize(featurized_lines):
    assert featurized_lines
    assert all(
        isinstance(featurized_line, list)
        for featurized_line in featurized_lines
    )
    assert all(
        isinstance(features, dict)
        for featurized_line in featurized_lines
        for features in featurized_line
    )
    # let's test for features not produced by generic utils token featurizer
    first_features = featurized_lines[0][0]
    assert all(key in first_features for key in ("prev", "next"))
    assert all(key in first_features for key in ("is_field_sep_char", "like_profile_username"))


def test_tag(tagged_lines):
    assert tagged_lines
    assert all(isinstance(tok_labels, list) for tok_labels in tagged_lines)
    assert all(isinstance(tl, tuple) for tok_labels in tagged_lines for tl in tok_labels)
    assert all(
        isinstance(tok, Token) and isinstance(label, str)
        for tok_labels in tagged_lines
        for tok, label in tok_labels
    )
    first_item = [(tok.text, label) for tok, label in tagged_lines[0]]
    assert first_item == [("Burton", "name"), ("DeWilde", "name")]


def test_parse_line(parsed_lines):
    assert parsed_lines
    assert all(parsed_line for parsed_line in parsed_lines)
    assert all(isinstance(parsed_line, dict) for parsed_line in parsed_lines)
    first_item = parsed_lines[0]
    assert first_item == {"name": "Burton DeWilde"}


def test_parsed_section(parsed_section):
    expected_section = {
        "name": "Kelly Knapp",
        "email": "boonesteven@hammond.com",
        "phone": "+1-397-533-1394",
        "website": "http://www.tucker.com",
        "location": {
            "address": "1968 Autumn Mews Suite 545",
            "city": "West Derekville",
            "region": "CA",
            "postal_code": "59587",
        },
        "profiles": [{"username": "@jonesrobert"}],
    }
    assert parsed_section == expected_section
    assert schemas.ResumeBasicsSchema().load(parsed_section)
