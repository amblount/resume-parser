import itertools
import logging
import operator
import re


LOGGER = logging.getLogger(__name__)

#######################
## CRF-BASED PARSING ##
#######################

# NOTE: required objects are as follows
# - TRAINING_DATA_FPATH (:class:`pathlib.Path`)
# - MODEL_FPATH (:class:`pathlib.Path`)
# - TAGGER (:class:`pycrfsuite.Tagger`)
# - LABELS (List[str])
# - featurize (func)

import pycrfsuite
from toolz import itertoolz

import msvdd_bloc
from . import utils

TRAINING_DATA_FPATH = msvdd_bloc.MODELS_DIR.joinpath("resumes", "resume-skills-training-data.jsonl")
MODEL_FPATH = msvdd_bloc.MODELS_DIR.joinpath("resumes", "resume-skills.crfsuite")


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


def parse_skills_section(lines):
    """
    Parse a sequence of text lines belonging to the "skills" section of a résumé
    to produce structured data in the form of :class:`schemas.ResumeSkillSchema`
    using a trained Conditional Random Field (CRF) tagger.

    Args:
        lines (List[str])

    Returns:
        List[Dict[str, obj]]
    """
    if TAGGER is None:
        raise IOError(
            "model file '{}' is missing; have you trained one yet? "
            "if not, use the `label_parser_training_data.py` script.".format(MODEL_FPATH)
        )

    skills = []
    for line in lines:
        tokens = utils.tokenize(line)
        if not tokens:
            continue
        else:
            features = featurize(tokens)
            tok_labels = tag(tokens, features)
            skills.extend(_parse_skills_from_labeled_tokens(tok_labels))
    return skills


def _parse_skills_from_labeled_tokens(tok_labels):
    """
    Args:
        tok_labels (List[Tuple[:class:`spacy.tokens.Token`, str]])

    Returns:
        List[Dict[str, obj]]
    """
    skills = []

    # get rid of leading bullets
    if tok_labels[0][1] == "bullet":
        tok_labels = tok_labels[1:]
    # get rid of leading / trailing item_seps
    if tok_labels[0][1] == "item_sep":
        tok_labels = tok_labels[1:]
    if tok_labels[-1][1] == "item_sep":
        tok_labels = tok_labels[:-1]
    # and all other tokens
    tok_labels = [(tok, label) for tok, label in tok_labels if label != "other"]
    if not tok_labels:
        return []

    labels_str = "".join(label for _, label in tok_labels)

    # a junk line, with key content probably split onto the next line
    # nbd, that line's skills will likely get parsed as names instead of keywords
    if re.search(r"^(name|level)+field_sep$", labels_str):
        pass
    # space-delimited list of skill names (or keywords)
    # note: this is a parser error -- they shouldn't be keywords -- but we can correct it
    # note: this is an ambiguous way to list skills; we assume each token is separate
    elif re.search(r"^(name|keyword)+$", labels_str):
        skills.extend({"name": tok.text} for tok, _ in tok_labels)
    # a name separated by a level
    elif re.search(r"^(name)+field_sep(level)+$", labels_str):
        skills.append({
            "name": "".join(tok.text_with_ws for tok, label in tok_labels if label == "name"),
            "level": "".join(tok.text_with_ws for tok, label in tok_labels if label == "level"),
        })
    # char-delimited list of skill names
    elif re.search(r"^(name)+((item_sep)+(name)+)+$", labels_str):
        skills.extend([
            {"name": "".join(tok.text_with_ws for tok, label in tls)}
            for label, tls in itertools.groupby(tok_labels, key=operator.itemgetter(1))
            if label != "item_sep"
        ])
    # char-delimited list of skill names (or keywords)
    # note: this is a parser error -- they shouldn't be keywords -- but we can correct it
    elif re.search(r"^(name)+((item_sep)+(name|keyword)+)+$", labels_str):
        skills.extend([
            {"name": "".join(tok.text_with_ws for tok, label in tls)}
            for label, tls in itertools.groupby(tok_labels, key=operator.itemgetter(1))
            if label != "item_sep"
        ])
    # char-delimited list of skill names with levels
    elif re.search(r"^((name)+((field_sep)+(level)+(field_sep)+)?(item_sep)*?)+$", labels_str):
        for is_item_sep, tls in itertools.groupby(tok_labels, key=lambda tl: tl[1] == "item_sep"):
            if not is_item_sep:
                tls = list(tls)
                skills.append({
                    "name": "".join(tok.text_with_ws for tok, label in tls if label == "name"),
                    "level": "".join(tok.text_with_ws for tok, label in tls if label == "level"),
                })
    # skill name explicitly separated from one or more keywords,
    # either by a leading separator (e.g. ":") or bracketed separators (e.g. "(...)")
    elif re.search(r"^(name)+field_sep(keyword)+((item_sep)+(keyword)+)*?field_sep?$", labels_str):
        field_sep_idx = [label for _, label in tok_labels].index("field_sep")
        skills.append({
            "name": "".join(tok.text_with_ws for tok, _ in tok_labels[:field_sep_idx]),
            "keywords": [
                "".join(tok.text_with_ws for tok, label in tls)
                for label, tls in itertools.groupby(tok_labels[field_sep_idx + 1:], key=operator.itemgetter(1))
                if label != "item_sep"
            ],
        })
    # level explicitly separated from one or more names/keywords
    # note: the parser assigning all items as keywords after level + field_sep is an error
    # but we can catch it and fix it post-parse
    elif re.search(r"^(level)+field_sep(name|keyword)+((item_sep)+(name|keyword)+)*?$", labels_str):
        field_sep_idx = [label for _, label in tok_labels].index("field_sep")
        level = "".join(tok.text_with_ws for tok, label in tok_labels[:field_sep_idx] if label == "level")
        skills.extend([
            {"level": level, "name": "".join(tok.text_with_ws for tok, label in tls)}
            for label, tls in itertools.groupby(tok_labels[field_sep_idx + 1:], key=operator.itemgetter(1))
            if label != "item_sep"
        ])
    # level implicitly separated from one or more names/keywords
    # note: the parser assigning all items as keywords after level + field_sep is an error
    # but we can catch it and fix it post-parse
    elif re.search(r"^(level)+(name)+((item_sep)+(name|keyword)+)*?$", labels_str):
        name_idx = [label for _, label in tok_labels].index("name")
        level = "".join(tok.text_with_ws for tok, label in tok_labels[:name_idx] if label == "level")
        skills.extend([
            {"level": level, "name": "".join(tok.text_with_ws for tok, label in tls)}
            for label, tls in itertools.groupby(tok_labels[name_idx + 1:], key=operator.itemgetter(1))
            if label != "item_sep"
        ])
    # skill name explicitly separated from one or more names/keywords with levels
    # note: this isn't permitted by our resume schema, so we'll drop the leading name
    # and convert the keywords into their own names
    elif re.search(r"^(name)+field_sep((name|keyword)+((field_sep)+(level)+(field_sep)+)?(item_sep)*?)+$", labels_str):
        field_sep_idx = [label for _, label in tok_labels].index("field_sep")
        for is_item_sep, tls in itertools.groupby(tok_labels[field_sep_idx + 1:], key=lambda tl: tl[1] == "item_sep"):
            if not is_item_sep:
                tls = list(tls)
                skills.append({
                    "name": "".join(tok.text_with_ws for tok, label in tls if label in {"name", "keyword"}),
                    "level": "".join(tok.text_with_ws for tok, label in tls if label == "level"),
                })
    else:
        LOGGER.warning("unable to parse skills from labeled tokens: {}".format(tok_labels))
    return skills


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
        tokens (List[:class:`spacy.tokens.Token`]): As output by :func:`utils.tokenize()`
        features (List[Dict[str, obj]]): As output by :func:`featurize()`

    Returns:
        List[Tuple[str, str]]: Ordered sequence of (token, tag) pairs.
    """
    tags = TAGGER.tag(features)
    return list(zip(tokens, tags))


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


def parse_skills_section_alt(lines):
    """
    Parse a sequence of text lines belonging to the "skills" section of a résumé
    to produce structured data in the form of :class:`schemas.ResumeSkillSchema`
    using logical rules based on regular expressions.

    Args:
        lines (List[str])

    Returns:
        List[Dict[str, str]]

    Note:
        This function is not as flexible as :func:`parse_skills_section()`,
        but its errors are probably more consistent and easier to understand.
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
