import itertools
import logging
import operator
import re

from toolz import itertoolz

from msvdd_bloc.resumes import constants
from msvdd_bloc.resumes import parse_utils
from msvdd_bloc.resumes import skills


LOGGER = logging.getLogger(__name__)

#######################
## CRF-BASED PARSING ##
#######################

GROUP_SEP_TEXTS = set(
    skills.constants.GROUP_SEPS_WITH_WS +
    skills.constants.GROUP_SEPS_WITH_WS_RIGHT
)
ITEM_SEP_TEXTS = set(constants.ANDS + skills.constants.ITEM_SEPS)
# HACK: we generally don't want features that depend on belonging to a set
# of manually-curated words; but this is a somewhat special case,
# and it improves performance on those fields, so... :shrug:
LEVEL_TEXTS = set(skills.constants.LEVELS)


def parse_lines(lines, tagger=None):
    """
    Parse a sequence of text lines belonging to the "skills" section of a résumé
    to produce structured data in the form of :class:`schemas.ResumeSkillSchema`
    using a trained Conditional Random Field (CRF) tagger.

    Args:
        lines (List[str])
        tagger (:class:`pycrfsuite.Tagger`)

    Returns:
        List[Dict[str, obj]]
    """
    if tagger is None:
        tagger = parse_utils.load_tagger(skills.FPATH_TAGGER)

    tokens = parse_utils.tokenize("\n".join(lines).strip())
    features = featurize(tokens)
    labeled_tokens = parse_utils.tag(tokens, features, tagger=tagger)
    data = _parse_labeled_tokens(labeled_tokens)
    return data


def _parse_labeled_tokens(labeled_tokens):
    """
    Args:
        labeled_tokens (List[Tuple[:class:`spacy.tokens.Token`, str]])

    Returns:
        List[Dict[str, obj]]
    """
    skills_data = []

    def _is_line_group_sep(tok_label):
        """
        Groups of related skills don't necessarily stick to a single line; only split
        them if there's a newline labeled specifically as a field separator, rather than
        an item separator.
        """
        return (
            tok_label[1] == "field_sep" and
            re.match(r"^\n+$", tok_label[0].text) is not None
        )

    grped_tok_labels = itertools.groupby(labeled_tokens, key=_is_line_group_sep)
    for key, tok_labels in grped_tok_labels:
        # skip newline field separators
        if key is True:
            continue

        tok_labels = list(tok_labels)

        # get rid of leading / trailing field_seps and item_seps
        if tok_labels[0][1] in ("item_sep", "field_sep"):
            tok_labels = tok_labels[1:]
        if tok_labels[-1][1] == "item_sep":
            tok_labels = tok_labels[:-1]
        # get rid of all "other" tokens
        tok_labels = [(tok, label) for tok, label in tok_labels if label != "other"]
        if not tok_labels:
            return []

        labels_str = "".join(label for _, label in tok_labels)

        # junk lines, with key content probably split onto the next line
        # nbd, next line's skills will probably get parsed just fine
        if (
            re.search(r"^(level)+(field_sep)*?$", labels_str) or
            re.search(r"^(name)+(field_sep)+$", labels_str)
        ):
            pass
        # space-delimited list of names (or keywords)
        # note: this is a parser error -- they shouldn't be keywords -- but we can correct it
        # note: this is an ambiguous way to list skills; we assume each token is separate
        elif re.search(r"^(name|keyword)+$", labels_str):
            skills_data.extend({"name": tok.text} for tok, _ in tok_labels)
        # name separated from a level
        elif re.search(r"^(name)+(field_sep)+(level)+(field_sep)*?$", labels_str):
            skills_data.append({
                "name": "".join(tok.text_with_ws for tok, label in tok_labels if label == "name").strip(),
                "level": "".join(tok.text_with_ws for tok, label in tok_labels if label == "level").strip(),
            })
        # char-delimited list of names (or keywords)
        elif re.search(r"^(name)+((item_sep)+(name|keyword)+)+$", labels_str):
            skills_data.extend([
                {"name": "".join(tok.text_with_ws for tok, label in tls).strip()}
                for label, tls in itertools.groupby(tok_labels, key=operator.itemgetter(1))
                if label != "item_sep"
            ])
        # char-delimited list of names with (optional) levels
        elif re.search(r"^((name)+((field_sep)+(level)+(field_sep)+)?(item_sep)*?)+$", labels_str):
            for is_item_sep, tls in itertools.groupby(tok_labels, key=lambda tl: tl[1] == "item_sep"):
                if not is_item_sep:
                    tls = list(tls)
                    skills_data.append({
                        "name": "".join(tok.text_with_ws for tok, label in tls if label == "name").strip(),
                        "level": "".join(tok.text_with_ws for tok, label in tls if label == "level"),
                    })
        # name explicitly separated from list of keywords (or names)
        elif re.search(r"^(name)+(field_sep)+(keyword)+((item_sep)+(keyword|name)+)*?$", labels_str):
            field_sep_idx = [label for _, label in tok_labels].index("field_sep")
            skills_data.append({
                "name": "".join(tok.text_with_ws for tok, _ in tok_labels[:field_sep_idx]).strip(),
                "keywords": [
                    "".join(tok.text_with_ws for tok, label in tls).strip()
                    for label, tls in itertools.groupby(tok_labels[field_sep_idx + 1:], key=operator.itemgetter(1))
                    if label != "item_sep"
                ],
            })
        # level explicitly separated from list of names/keywords
        # note: tagging keywords after level + field_sep is an error
        # but we can catch it and fix it post-parse
        elif re.search(r"^(level)+(field_sep)+(name|keyword)+((item_sep)+(name|keyword)+)*?$", labels_str):
            field_sep_idx = [label for _, label in tok_labels].index("field_sep")
            level = "".join(
                tok.text_with_ws
                for tok, label in tok_labels[:field_sep_idx]
                if label == "level"  # TODO: is this if statement necessary?
            ).strip()
            skills_data.extend([
                {"level": level, "name": "".join(tok.text_with_ws for tok, _ in tls).strip()}
                for label, tls in itertools.groupby(tok_labels[field_sep_idx + 1:], key=operator.itemgetter(1))
                if label != "item_sep"
            ])
        # level implicitly separated from list of names/keywords
        elif re.search(r"^(level)+(name)+((item_sep)+(name|keyword)+)*?$", labels_str):
            name_idx = [label for _, label in tok_labels].index("name")
            level = "".join(
                tok.text_with_ws
                for tok, label in tok_labels[:name_idx]
                if label == "level"  # TODO: is this if statement necessary?
            ).strip()
            skills_data.extend([
                {"level": level, "name": "".join(tok.text_with_ws for tok, _ in tls).strip()}
                for label, tls in itertools.groupby(tok_labels[name_idx + 1:], key=operator.itemgetter(1))
                if label != "item_sep"
            ])
        # name explicitly separated from one or more names/keywords with levels
        # note: this isn't permitted by our resume schema, so we'll drop the leading name
        # and convert the keywords into their own names
        elif re.search(r"^(name)+(field_sep)+((name|keyword)+((field_sep)+(level)+(field_sep)*?)?(item_sep)*?)+$", labels_str):
            field_sep_idx = [label for _, label in tok_labels].index("field_sep")
            for is_item_sep, tls in itertools.groupby(tok_labels[field_sep_idx + 1:], key=lambda tl: tl[1] == "item_sep"):
                if not is_item_sep:
                    tls = list(tls)
                    level = "".join(
                        tok.text_with_ws for tok, label in tls if label == "level"
                    ).strip()
                    labels = {"name", "keyword"}
                    item = {
                        "name": "".join(
                            tok.text_with_ws for tok, label in tls if label in labels
                        ).strip()
                    }
                    if level:
                        item["level"] = level
                    skills_data.append(item)
        else:
            LOGGER.warning("unable to parse skills from labeled tokens: {}".format(tok_labels))
    return skills_data


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
        line_idx_windows = parse_utils.get_line_token_idxs(tokens_features)
        prev_line_idx, next_line_idx = next(line_idx_windows)
        follows_bullet = False
        n_pad_l, n_pad_r = 3, 2
        tokens_features = parse_utils.pad_tokens_features(
            tokens_features, n_left=n_pad_l, n_right=n_pad_r)
        tf_windows = itertoolz.sliding_window(n_pad_l + n_pad_r + 1, tokens_features)
        for ppprev_tf, pprev_tf, prev_tf, curr_tf, next_tf, nnext_tf in tf_windows:
            tf = curr_tf.copy()
            # add features from surrounding tokens, for context
            tf["ppprev"] = ppprev_tf
            tf["pprev"] = pprev_tf
            tf["prev"] = prev_tf
            tf["next"] = next_tf
            tf["nnext"] = nnext_tf
            # add features dependent on this token's position within the sequence
            # and its relationship to other tokens
            tok_idx = tf["idx"]
            if tf["is_newline"] and tf["idx"] > 0:
                prev_line_idx, next_line_idx = next(line_idx_windows)
                follows_bullet = False
            tf["tok_line_idx"] = tok_idx - prev_line_idx
            tf["follows_bullet"] = follows_bullet
            # bullets have is_group_sep_text, but they aren't group separators
            # at least not in the sense we want here; so, +2 to the previous newline idx
            # ensures that bullets are not counted in this feature
            line_tfs_so_far = tokens_features[prev_line_idx + n_pad_l + 2: tok_idx + n_pad_l]
            if any(_tf["is_group_sep_text"] for _tf in line_tfs_so_far):
                tf["follows_group_sep"] = True
            else:
                tf["follows_group_sep"] = False
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
    text = token.text
    features = parse_utils.get_token_features_base(token)
    features.update(
        {
            "is_group_sep_text": text in GROUP_SEP_TEXTS,
            "is_item_sep_text": text in ITEM_SEP_TEXTS,
            "is_level_text": text.lower() in LEVEL_TEXTS,
        }
    )
    return features


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
