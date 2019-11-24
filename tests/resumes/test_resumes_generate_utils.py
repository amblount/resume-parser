import random as rnd

import pytest
from faker import Faker

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

@pytest.fixture(scope="module")
def faker():
    fkr = Faker()
    fkr.add_provider(generate_utils.ResumeProvider)
    return fkr


@pytest.fixture(scope="module")
def training_text():
    return (
        "Here is some example text from which new text may be generated. "
        "Markov Models are pretty cool, although their outputs are often nonsense. "
        "This last bit's ending has to be found previously to avoid an annoying edge case: nonsense."
    )


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


class TestResumeProvider:

    def test_random_element_weighted(self, faker):
        assert faker.random_element_weighted(["a", "b", "c"], None) in {"a", "b", "c"}
        assert faker.random_element_weighted(["a", "b", "c"], [1.0, 0.5, 0.25]) in {"a", "b", "c"}
        assert faker.random_element_weighted(["a", "b", "c"], [1.0, 0.0, 0.0]) == "a"

    def test_random_n_weighted(self, faker):
        assert faker.random_n_weighted((1, 4), None) in {1, 2, 3}
        assert faker.random_n_weighted((1, 4), [1.0, 0.5, 0.25]) in {1, 2, 3}
        assert faker.random_n_weighted((1, 4), [1.0, 0.0, 0.0]) == 1

    def test_random_template_weighted(self, faker):
        templates_weights = (
            ("{word1}", 1.0),
            ("{word1} {word2}", 0.5),
        )
        templates = tuple(template for template, _ in templates_weights)
        assert faker.random_template_weighted(templates_weights) in templates


class TestMarkovModel:

    def test_init(self):
        state_len = 4
        mm = generate_utils.MarkovModel(state_len=state_len)
        assert mm.state_len == state_len
        assert mm.model is None

    def test_fit(self, training_text):
        mm = generate_utils.MarkovModel(state_len=4)
        mm.fit(training_text)
        assert isinstance(mm.model, dict)
        assert len(mm.model) > 1

    def test_generate(self, training_text):
        mm = generate_utils.MarkovModel(state_len=4)
        mm.fit(training_text)
        result = mm.generate(10)
        assert isinstance(result, str)
        assert len(result) == 10
        result = mm.generate(10, state="Here")
        assert isinstance(result, str)
        assert len(result) == 10
        assert result.startswith("Here")

    def test_generate_error(self, training_text):
        mm = generate_utils.MarkovModel(state_len=4)
        with pytest.raises(RuntimeError):
            mm.generate(10)
        mm.fit(training_text)
        with pytest.raises(ValueError):
            mm.generate(10, state="foo")
