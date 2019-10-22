import re
import unicodedata

import ftfy
from toolz import itertoolz

from .. import regexes


def normalize_text(text):
    """
    Correct any encoding / mojibake / unicode weirdness, standardize list bullets, etc.

    Args:
        text (str)

    Returns:
        str
    """
    norm_text = text
    # normalize unicode and fix encoding/mojibake
    norm_text = ftfy.fix_text(norm_text)
    norm_text = unicodedata.normalize("NFC", norm_text)
    # standardize bullets
    norm_text = regexes.RE_BULLETS.sub("-", norm_text)
    # normalize whitespace
    norm_text = norm_text.replace("\u200b", "")
    norm_text = regexes.RE_NONBREAKING_SPACE.sub(" ", norm_text).strip()
    norm_text = regexes.RE_BREAKING_SPACE.sub(r"\n", norm_text)
    return norm_text


def get_filtered_text_lines(text, *, delim=r" ?\n"):
    """
    Split ``text`` into lines, filtering out some superfluous lines if context allows.

    Args:
        text (str)
        delim (str)

    Returns:
        List[str]

    Note:
        This should be applied to normalized text -- see :func:`normalize_text()`.
    """
    lines = []
    all_lines = ["<START>"] + re.split(delim, text) + ["<END>"]
    for prev_line, line, next_line in itertoolz.sliding_window(3, all_lines):
        line = line.strip()
        # ignore empty lines between bulleted list items -- probably just a parsing error
        if not line and prev_line.startswith("- ") and next_line.startswith("- "):
            continue
        # ignore resume-ending numbers -- probably just page numbering
        elif line.isdigit() and next_line == "<END>":
            continue
        lines.append(line)
    return lines
