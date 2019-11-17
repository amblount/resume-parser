import random as rnd

import pytest

from msvdd_bloc.resumes import generate_utils


@pytest.fixture(scope="module")
def fields():
    return {
        "field1": (lambda: "value1", "label1"),
        "field2": (lambda: "value2", "label2"),
        "fsep": (lambda: rnd.choice([":", ";", ",", "|", "-", "–"]), "field_sep"),
    }


@pytest.fixture(scope="module")
def templates_base():
    return [
        lambda: "{field1} {field2}",
    ]


def test_generate_labeled_tokens(fields):
    inputs_outputs = [
        (
            [lambda: "{field1} {field2}",],
            [("value1", "label1"), ("value2", "label2")],
        ),
        (
            [lambda: "{field2} {field1}",],
            [("value2", "label2"), ("value1", "label1")],
        ),
        (
            [lambda: "{field1:label_alt} {field2}",],
            [("value1", "label_alt"), ("value2", "label2")],
        ),
        (
            [lambda: "{field1::0.0} {field2}",],
            [("value2", "label2")],
        ),
    ]
    for templates, exp_lts in inputs_outputs:
        obs_lts = next(generate_utils.generate_labeled_tokens(templates, fields))
        assert obs_lts == exp_lts


def test_generate_labeled_tokens_n(templates_base, fields):
    for n in [1, 2, 3]:
        lts = list(generate_utils.generate_labeled_tokens(templates_base, fields, n=n))
        assert len(lts) == n


def test_generate_labeled_tokens_fixed_val_field_keys(fields):
    templates = [
        lambda: "{field1} {fsep} {field2} {fsep} {field1} {fsep} {field2}",
    ]
    lts = next(
        generate_utils.generate_labeled_tokens(
            templates, fields, fixed_val_field_keys="fsep",
        )
    )
    assert lts
    assert len(set(tok for tok, label in lts if label == "field_sep")) == 1
