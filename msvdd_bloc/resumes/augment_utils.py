import random

from cytoolz import itertoolz


class Augmenter:
    """
    Randomly apply one or many data-augmentation transform functions to labeled tokens
    to produce new sequences with additional variety and/or noise in the data.

    Args:
        transforms (Sequence[Callable]): Ordered sequence of callables that must take
            List[Tuple[str, str]] as their first positional argument and return a new
            List[Tuple[str, str]].

            .. note:: Although the particular transforms applied may vary per call,
               they are applied *in order* as listed here.

        num (int or float or List[float]): If int, number of transforms to randomly select
            from ``transforms`` each time :meth:`Augmenter.apply()` is called. If float,
            probability that any given transform will be selected. If List[float],
            probability that the corresponding transform in ``transforms`` will be
            selected (these must be the same length). If None (default), num is set to
            ``len(transforms)``, which means that all transforms are always applied.
    """

    def __init__(self, transforms, *, num=None):
        self.tfs = self._validate_transforms(transforms)
        self.num = self._validate_num(num)

    def apply(self, labeled_tokens, **kwargs):
        """
        Sequentially apply some subset of augmentation transforms to ``labeled_tokens``,
        returning a new, modified sequence of labeled tokens.

        Args:
            labeled_tokens (List[Tuple[str, str]])

        Returns:
            List[Tuple[str, str]]
        """
        for transform in self._get_random_transforms():
            labeled_tokens = transform(labeled_tokens)
        return labeled_tokens

    def _validate_transforms(self, transforms):
        transforms = tuple(transforms)
        if not transforms:
            raise ValueError("at least one transform callable must be specified")
        elif not all(callable(transform) for transform in transforms):
            raise TypeError("all transforms must be callable")
        else:
            return transforms

    def _validate_num(self, num):
        if num is None:
            return len(self.tfs)
        elif isinstance(num, int) and 0 <= num <= len(self.tfs):
            return num
        elif isinstance(num, float) and 0.0 <= num <= 1.0:
            return num
        elif (
            isinstance(num, (tuple, list)) and
            len(num) == len(self.tfs) and
            all(isinstance(n, float) and 0.0 <= n <= 1.0 for n in num)
        ):
            return tuple(num)
        else:
            raise ValueError(
                "num={} is invalid; must be an int >= 1, a float in [0.0, 1.0], "
                "or a list of floats of length equal to given transforms".format(num)
            )

    def _get_random_transforms(self):
        num = self.num
        if isinstance(num, int):
            rand_idxs = random.sample(range(len(self.tfs)), min(num, len(self.tfs)))
            rand_tfs = [self.tfs[idx] for idx in sorted(rand_idxs)]
        elif isinstance(num, float):
            rand_tfs = [tf for tf in self.tfs if random.random() < num]
        else:
            rand_tfs = [
                tf for tf, tf_num in zip(self.tfs, self.num)
                if random.random() < tf_num
            ]
        return rand_tfs


def change_case_token_text(tok_labels, *, case="upper", target_labels=None):
    """
    Change token text to ``case`` case for those whose label is in ``target_labels``.

    Args:
        tok_labels (List[Tuple[str, str]])
        case ({"upper", "title", "lower"})
        target_labels (str or Set[str])

    Returns:
        List[Tuple[str, str]]
    """
    _case_to_func = {"upper": str.upper, "title": str.capitalize, "lower": str.lower}
    func = _case_to_func[case]
    if target_labels is None:
        return [(func(tok), label) for tok, label in tok_labels]
    else:
        if isinstance(target_labels, str):
            target_labels = {target_labels}
        return [
            (func(tok), label) if label in target_labels else (tok, label)
            for tok, label in tok_labels
        ]


def delete_token(tok_labels, *, prob=0.01,  target_labels=None):
    """
    Randomly delete any given token with a probability of ``prob`` for those whose
    label is in ``target_labels``.

    Args:
        tok_labels (List[Tuple[str, str]])
        prob (float)
        target_labels (str or Set[str])

    Returns:
        List[Tuple[str, str]]
    """
    if target_labels is None:
        return [tok_label for tok_label in tok_labels if random.random() >= prob]
    else:
        return [
            tok_label
            for tok_label in tok_labels
            if tok_label[1] in target_labels and random.random() >= prob
        ]


def insert_whitespace_token(
    tok_labels, *,
    prob=0.01,
    nrange=(1, 2),
    field_labels=("field_sep", "item_sep"),
):
    """
    Randomly insert a whitespace token between any given two tokens with a probability
    of ``prob``, provided neither token is already whitespace.

    Args:
        tok_labels (List[Tuple[str, str]])
        prob (float)
        ngrange (Tuple[int, int])
        field_labels (Tuple[str, str])

    Returns:
        List[Tuple[str, str]]
    """
    aug_tok_labels = []
    for tl1, tl2 in itertoolz.sliding_window(2, tok_labels):
        aug_tok_labels.append(tl1)
        if random.random() < prob and not (tl1[0].isspace() or tl2[0].isspace()):
            ws_label = field_labels[tl1[1] == tl2[1]]
            aug_tok_labels.append((" " * random.randint(*nrange), ws_label))
    return aug_tok_labels
