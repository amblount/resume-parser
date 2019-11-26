import pycrfsuite
import pytest
from spacy.tokens import Token

from msvdd_bloc import tokenize
from msvdd_bloc.resumes import basics, education, skills
from msvdd_bloc.resumes import parse_utils


class TestLoadTagger:

    def test(self):
        for module in [basics, education, skills]:
            tagger = parse_utils.load_tagger(module.FPATH_TAGGER)
            assert isinstance(tagger, pycrfsuite.Tagger)

    def test_bad_path(self, tmp_path):
        with pytest.raises(IOError):
            parse_utils.load_tagger(tmp_path.joinpath("foo.crfsuite"))


class TestPadTokensFeatures:

    def test(self):
        tfs = [{"feat1": "val1"}, {"feat1": "val2"}]
        for n in [1, 2, 3]:
            tfs_padded = parse_utils.pad_tokens_features(tfs, n_left=n, n_right=0)
            assert tfs_padded
            assert (
                isinstance(tfs_padded, list) and
                all(isinstance(tf, dict) for tf in tfs_padded)
            )
            assert len(tfs_padded) == len(tfs) + n

    def test_padded_features(self):
        tfs = [{"feat1": "val1"}, {"feat1": "val2"}]
        tfs_padded = parse_utils.pad_tokens_features(tfs, n_left=2, n_right=1)
        assert all(tf == {"_start": True} for tf in tfs_padded[:2])
        assert all(tf == {"_end": True} for tf in tfs_padded[-1:])


class TestGetTokenFeaturesBase:

    def test_token(self):
        token = tokenize.tokenize(["test"])[0]
        obs_features = parse_utils.get_token_features_base(token)
        exp_features = {
            "idx": 0,
            "len": 4,
            "shape": "xxxx",
            "prefix": "t",
            "suffix": "est",
            "is_alpha": True,
            "is_digit": False,
            "is_lower": True,
            "is_upper": False,
            "is_title": False,
            "is_punct": False,
            "is_left_punct": False,
            "is_right_punct": False,
            "is_bracket": False,
            "is_quote": False,
            "is_space": False,
            "like_num": False,
            "like_url": False,
            "like_email": False,
            "is_stop": False,
            "is_alnum": True,
            "is_newline": False,
            "is_partial_digit": False,
            "is_partial_punct": False,
        }
        assert obs_features == exp_features

    def test_token_title_alnum(self):
        token = tokenize.tokenize(["Test0"])[0]
        obs_features = parse_utils.get_token_features_base(token)
        exp_features = {
            "idx": 0,
            "len": 5,
            "shape": "Xxxxd",
            "prefix": "T",
            "suffix": "st0",
            "is_alpha": False,
            "is_digit": False,
            "is_lower": False,
            "is_upper": False,
            "is_title": True,
            "is_punct": False,
            "is_left_punct": False,
            "is_right_punct": False,
            "is_bracket": False,
            "is_quote": False,
            "is_space": False,
            "like_num": False,
            "like_url": False,
            "like_email": False,
            "is_stop": False,
            "is_alnum": True,
            "is_newline": False,
            "is_partial_digit": True,
            "is_partial_punct": False,
        }
        assert obs_features == exp_features

    def test_token_upper_with_punct(self):
        token = tokenize.tokenize(["VICE-VERSA"])[0]
        obs_features = parse_utils.get_token_features_base(token)
        exp_features = {
            "idx": 0,
            "len": 10,
            "shape": "XXXX-XXXX",
            "prefix": "V",
            "suffix": "RSA",
            "is_alpha": False,
            "is_digit": False,
            "is_lower": False,
            "is_upper": True,
            "is_title": False,
            "is_punct": False,
            "is_left_punct": False,
            "is_right_punct": False,
            "is_bracket": False,
            "is_quote": False,
            "is_space": False,
            "like_num": False,
            "like_url": False,
            "like_email": False,
            "is_stop": False,
            "is_alnum": False,
            "is_newline": False,
            "is_partial_digit": False,
            "is_partial_punct": True,
        }
        assert obs_features == exp_features

    def test_token_number(self):
        token = tokenize.tokenize(["1.0"])[0]
        obs_features = parse_utils.get_token_features_base(token)
        exp_features = {
            "idx": 0,
            "len": 3,
            "shape": "d.d",
            "prefix": "1",
            "suffix": "1.0",
            "is_alpha": False,
            "is_digit": False,
            "is_lower": False,
            "is_upper": False,
            "is_title": False,
            "is_punct": False,
            "is_left_punct": False,
            "is_right_punct": False,
            "is_bracket": False,
            "is_quote": False,
            "is_space": False,
            "like_num": True,
            "like_url": False,
            "like_email": False,
            "is_stop": False,
            "is_alnum": False,
            "is_newline": False,
            "is_partial_digit": True,
            "is_partial_punct": True,
        }
        assert obs_features == exp_features

    def test_token_email(self):
        token = tokenize.tokenize(["foo@bar.com"])[0]
        obs_features = parse_utils.get_token_features_base(token)
        exp_features = {
            "idx": 0,
            "len": 11,
            "shape": "xxx@xxx.xxx",
            "prefix": "f",
            "suffix": "com",
            "is_alpha": False,
            "is_digit": False,
            "is_lower": True,
            "is_upper": False,
            "is_title": False,
            "is_punct": False,
            "is_left_punct": False,
            "is_right_punct": False,
            "is_bracket": False,
            "is_quote": False,
            "is_space": False,
            "like_num": False,
            "like_url": False,
            "like_email": True,
            "is_stop": False,
            "is_alnum": False,
            "is_newline": False,
            "is_partial_digit": False,
            "is_partial_punct": True,
        }
        assert obs_features == exp_features
