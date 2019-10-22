import logging
import re


LOGGER = logging.getLogger(__name__)

#########################
## RULES-BASED PARSING ##
#########################

RE_SKILL_NAME_DELIM = re.compile(r"(?:: +| +[-–] +)")
RE_SKILL_KEYWORD_DELIM = re.compile(r"[,;] +(?:(?:and|&) +)?")
RE_SKILL_LEVEL = re.compile(
    r"\(?(?P<level>advanced|intermediate|beginner|basic|proficient|exposed)\)? ?(in )?",
    flags=re.UNICODE | re.IGNORECASE,
)
RE_SKILL_CLEAN = re.compile(r"[.,;]$")


def parse_skills_section(lines):
    """
    Parse a sequence of text lines belonging to the "skills" section of a résumé
    to produce structured data in the form of :class:`schemas.ResumeSkillSchema`.

    Args:
        lines (List[str])

    Returns:
        List[Dict[str, str]]
    """
    all_skills = []
    for line in lines:
        if not line:
            continue
        line = line.lstrip("- ")
        split_line = RE_SKILL_NAME_DELIM.split(line)
        if len(split_line) == 1:
            names = RE_SKILL_KEYWORD_DELIM.split(line)
            if len(names) == 1:
                names = line.split()
            skills = []
            for name in names:
                match = RE_SKILL_LEVEL.search(name)
                if match:
                    skill = {
                        "name": RE_SKILL_CLEAN.sub("", RE_SKILL_LEVEL.sub("", name).strip()),
                        "level": match.group("level"),
                    }
                else:
                    skill = {"name": RE_SKILL_CLEAN.sub("", name.strip())}
                skills.append(skill)
            all_skills.extend(skills)
        elif len(split_line) == 2:
            name, keywords = split_line
            keywords_split = RE_SKILL_KEYWORD_DELIM.split(keywords)
            if len(keywords_split) == 1:
                keywords_split = keywords.split()
            skill = {
                "name": RE_SKILL_CLEAN.sub("", name.strip()),
                "keywords": [RE_SKILL_CLEAN.sub("", kw) for kw in keywords_split]
            }
            all_skills.append(skill)
    return all_skills


#######################
## CRF-BASED PARSING ##
#######################

# NOTE: required objects are as follows
# - TRAINING_DATA_FPATH (:class:`pathlib.Path`)
# - MODEL_FPATH (:class:`pathlib.Path`)
# - TAGGER (:class:`pycrfsuite.Tagger`)
# - LABELS (List[str])
# - tokenize (func)
# - featurize (func)

import pycrfsuite
import spacy
from toolz import itertoolz

import msvdd_bloc

TRAINING_DATA_FPATH = msvdd_bloc.MODELS_DIR.joinpath("resumes", "resume-skills-training-data.jsonl")
MODEL_FPATH = msvdd_bloc.MODELS_DIR.joinpath("resumes", "resume-skills.crfsuite")

TOKENIZER = spacy.blank("en")
try:
    TAGGER = pycrfsuite.Tagger()
    TAGGER.open(str(MODEL_FPATH))
except IOError:
    TAGGER = None

LABELS = (
    "bullet",
    "name",
    "keyword",
    "level",
    "field_sep",
    "item_sep",
    "other",
)

LEVEL_WORDS = {
    "advanced", "intermediate", "beginner",
    "experienced", "proficient", "exposed", "exposure",
    "basic", "familiar",
}
FIELD_SEP_CHARS = {":", "-", "–", "(", ")"}
ITEM_SEP_CHARS = {",", ";", "/", "&"}


def parse_skills_section_crf(lines):
    """
    Args:
        lines (List[str])

    Returns:
        List[List[Tuple[str, str]]]
    """
    if TAGGER is None:
        raise IOError(
            "model file '{}' is missing; have you trained one yet? "
            "if not, use the `label_parser_training_data.py` script.".format(MODEL_FPATH)
        )

    parsed_lines = []
    for line in lines:
        tokens = tokenize(line)
        if not tokens:
            parsed_lines.append([])
            continue
        else:
            features = featurize(tokens)
            tok_tags = tag(tokens, features)
            # TODO: Apply logic to sequence of (token, tag) pairs!
            parsed_lines.append(tok_tags)
    return parsed_lines


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


def featurize(tokens):
    """
    Extract features from individual tokens as well as those that are dependent on
    the sequence thereof.

    Args:
        tokens (List[:class:`spacy.tokens.Token`])

    Returns:
        List[Dict[str, obj]]
    """
    tokens_features = [get_token_features(token) for token in tokens]
    if len(tokens_features) == 1:
        tokens_features[0]["_singleton"] = True
        return tokens_features
    else:
        feature_sequence = []
        tokens_features = [{"_start": True}] + tokens_features + [{"_end": True}]
        for prev_tf, curr_tf, next_tf in itertoolz.sliding_window(3, tokens_features):
            tf = curr_tf.copy()
            tf["prev"] = prev_tf
            tf["next"] = next_tf
            # NOTE: add features here that depend upon tokens elsewhere in the sequence
            # e.g. whether or not a particular word appeared earlier in the sequence
            if any(_tf.get("prefix") in FIELD_SEP_CHARS for _tf in feature_sequence):
                tf["after_field_sep"] = True
            else:
                tf["after_field_sep"] = False
            feature_sequence.append(tf)
        return feature_sequence


def get_token_features(token):
    """
    Get per-token features, independent of other tokens within its sequence.

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
        "is_alpha": token.is_alpha,
        "is_digit": token.is_digit,
        "is_lower": token.is_lower,
        "is_upper": token.is_upper,
        "is_title": token.is_title,
        "is_punct": token.is_punct,
        "is_left_punct": token.is_left_punct,
        "is_right_punct": token.is_right_punct,
        "is_space": token.is_space,
        "like_num": token.like_num,
        "like_url": token.like_url,
        "like_email": token.like_email,
        "is_stop": token.is_stop,
        "is_level_word": token.lower_ in LEVEL_WORDS,
        "is_field_sep_char": token.text in FIELD_SEP_CHARS,
        "is_item_sep_char": token.text in ITEM_SEP_CHARS,
    }


def tag(tokens, features):
    """
    Tag each token in ``tokens`` with a label from ``LABELS`` based on its features.

    Args:
        tokens (List[:class:`spacy.tokens.Token`]): As output by :func:`tokenize()`
        features (List[Dict[str, obj]]): As output by :func:`featurize()`

    Returns:
        List[Tuple[str, str]]: Ordered sequence of (token, tag) pairs.
    """
    tags = TAGGER.tag(features)
    return list(zip(tokens, tags))
