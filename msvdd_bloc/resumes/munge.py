import re

import ftfy

# TODO: figure out what we want to do here

def clean_fellows_text(text):
    """
    Correct any encoding / mojibake / unicode weirdness, and remove
    superfluous numbering at the end of the résumé.

    Args:
        text (str)

    Returns:
        str
    """
    text = ftfy.fix_text(text)
    text = re.sub(r"\s+\d+\s*?$", "", text)
    return text


def clean_bonus_text(text):
    """
    Correct any encoding / mojibake / unicode weirdness, and remove
    superfluous "resumes (in)" lines at the end of the résumé.

    Args:
        text (str)

    Returns:
        str
    """
    text = ftfy.fix_text(text)
    text = re.sub(r"([\w]+ ?){1,3}resumes( in ([\w,]+ ?){1,3})?\n", "", text)
    return text
