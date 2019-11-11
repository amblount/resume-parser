import random


def upper_case_token_text(target_label, tok_labels):
    """
    Change token text to upper case for those whose label is in ``target_label``.

    Args:
        target_label (str or Set[str])
        tok_labels (List[Tuple[str, str]])

    Returns:
        List[Tuple[str, str]]
    """
    if isinstance(target_label, str):
        target_label = {target_label}
    return [
        (tok.upper(), label) if label in target_label else (tok, label)
        for tok, label in tok_labels
    ]


def title_case_token_text(target_label, tok_labels):
    """
    Change token text to title case for those whose label is in ``target_label``.

    Args:
        target_label (str or Set[str])
        tok_labels (List[Tuple[str, str]])

    Returns:
        List[Tuple[str, str]]
    """
    if isinstance(target_label, str):
        target_label = {target_label}
    return [
        (tok.title(), label) if label in target_label else (tok, label)
        for tok, label in tok_labels
    ]


def delete_token(prob, tok_labels):
    """
    Randomly delete any given token with a probability of ``prob``.

    Args:
        prob (float)
        tok_labels (List[Tuple[str, str]])

    Returns:
        List[Tuple[str, str]]
    """
    return [
        tok_label
        for tok_label in tok_labels
        if random.random() >= prob
    ]


def delete_token_chars(prob, tok_labels):
    """
    Randomly delete any given character in token texts with a probability of ``prob``.

    Args:
        prob (float)
        tok_labels (List[Tuple[str, str]])

    Returns:
        List[Tuple[str, str]]
    """
    return [
        ("".join(c for c in tok if random.random() >= prob), label)
        for tok, label in tok_labels
    ]
