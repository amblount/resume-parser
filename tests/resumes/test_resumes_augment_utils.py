import pytest

from msvdd_bloc.resumes import augment_utils


@pytest.fixture(scope="module")
def labeled_tokens():
    return [
        ('State', 'institution'),
        ('University', 'institution'),
        ('of', 'institution'),
        ('New', 'institution'),
        ('York', 'institution'),
        (',', 'institution'),
        ('New', 'institution'),
        ('Jonathanshire', 'institution'),
        (',', 'institution'),
        ('  ', 'institution'),
        ('Pruittbury', 'institution'),
        (',', 'institution'),
        ('AZ', 'institution'),
        ('\n', 'field_sep'),
        ('Graduated', 'field_label'),
        (':', 'field_label'),
        ('Sep', 'start_dt'),
        ('1994', 'start_dt'),
        (' ', 'field_sep'),
        ('-', 'field_sep'),
        ('March', 'end_date'),
        ('1996', 'end_date'),
        ('\n', 'field_sep'),
        ('Cumulative', 'field_label'),
        ('GPA', 'field_label'),
        ('1.63', 'gpa'),
        ('\n', 'field_sep'),
        ('Entomology', 'course'),
        (',', 'item_sep'),
        ('Atmospheric', 'course'),
        ('Sciences', 'course'),
        (',', 'item_sep'),
        ('Sociology', 'course')
    ]


class TestTransforms:

    def test_change_case_token_text(self, labeled_tokens):
        case_meths = [
            ("upper", str.isupper),
            ("lower", str.islower),
            ("title", str.istitle),
        ]
        for case, meth in case_meths:
            aug_lts = augment_utils.change_case_token_text(
                labeled_tokens, case=case, target_labels=None)
            assert aug_lts
            assert (
                isinstance(aug_lts, list) and
                all(isinstance(aug_lt, tuple) for aug_lt in aug_lts)
            )
            assert all(meth(tok) or not tok.isalpha() for tok, _ in aug_lts)

    def test_change_case_token_text_targeted(self, labeled_tokens):
        for target_label in ["institution", "field_label"]:
            aug_lts = augment_utils.change_case_token_text(
                labeled_tokens, case="upper", target_labels=target_label)
            assert aug_lts
            assert all(
                tok.isupper() or not tok.isalpha()
                for tok, label in aug_lts
                if label == target_label
            )
            assert any(
                tok.isupper() is False and tok.isalpha() is True
                for tok, label in aug_lts
                if label != target_label
            )

    def test_delete_token(self, labeled_tokens):
        for prob in [0.25, 0.5]:
            aug_lts = augment_utils.delete_token(
                labeled_tokens, prob=prob, target_labels=None)
            assert aug_lts
            assert (
                isinstance(aug_lts, list) and
                all(isinstance(aug_lt, tuple) for aug_lt in aug_lts)
            )
            assert len(aug_lts) < len(labeled_tokens)
        # test extreme cases where we delete *all* tokens and *no* tokens
        assert len(augment_utils.delete_token(labeled_tokens, prob=1.0)) == 0
        assert len(augment_utils.delete_token(labeled_tokens, prob=0.0)) == len(labeled_tokens)

    def test_delete_token_targeted(self, labeled_tokens):
        for target_label in ["institution", "field_label"]:
            aug_lts = augment_utils.delete_token(
                labeled_tokens, prob=0.75, target_labels=target_label)
            assert (
                sum(1 for tok, label in aug_lts if label == target_label) <
                sum(1 for tok, label in labeled_tokens if label == target_label)
            )

    def test_insert_whitespace_token(self, labeled_tokens):
        aug_lts = augment_utils.insert_whitespace_token(
            labeled_tokens,
            prob=0.25, nrange=(1, 2), field_labels=("field_sep", "item_sep"),
        )
        assert aug_lts
        assert (
            isinstance(aug_lts, list) and
            all(isinstance(aug_lt, tuple) for aug_lt in aug_lts)
        )
        assert len(aug_lts) > len(labeled_tokens)
        assert (
            sum(1 for tok, _ in aug_lts if tok.isspace()) >
            sum(1 for tok, _ in labeled_tokens if tok.isspace())
        )
