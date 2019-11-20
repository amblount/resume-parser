"""
generate utils
--------------

Functionality for generating fake examples of labeled tokens for training a parser
in a résumé section-agnostic manner. Section subpackages use and build upon these utils
in their respective ``generate.py`` modules.
"""
import collections
import logging
import random as rnd
import re

import faker

from msvdd_bloc import regexes
from msvdd_bloc import utils
from msvdd_bloc.resumes import constants as c
from msvdd_bloc.resumes.parse_utils import TOKENIZER


LOGGER = logging.getLogger(__name__)


class ResumeProvider(faker.providers.BaseProvider):
    """
    Class for providing randomized field values in a résumé, regardless of section.
    """

    _subheader_templates = (
        "{word1}",
        "{word1} {word2}",
        "{word1} {sep} {word2}",
        "{word1} {word2} {sep} {word3}",
    )

    def address_inline(self):
        sep = rnd.choice([", ", " "])
        return self.generator.address().replace("\n", sep)

    def and_rand(self, weights=None):
        return (
            rnd.choices(c.ANDS, weights=weights, k=1)[0] if weights else
            rnd.choice(c.ANDS)
        )

    def date_present(self):
        return rnd.choices(c.DATE_PRESENTS, weights=[1.0, 0.25], k=1)[0]

    def field_label(self, labels, seps, label_weights=None, sep_weights=None):
        # TODO: figure out if this is actually how we want to structure field labels...
        # specifically: do we *want* to tag the separator as part of the field label??
        label = (
            rnd.choices(labels, weights=label_weights, k=1)[0] if label_weights else
            rnd.choice(labels)
        )
        return "{label}{ws}{sep}".format(
            label=label,
            # TODO: figure out if this ws matters, if we want two spaces, etc.
            ws="" if rnd.random() < 0.9 else " ",
            sep=rnd.choices(seps, weights=sep_weights, k=1)[0] if rnd.random() < 0.9 else "",
        ).strip()

    def left_bracket(self):
        return rnd.choice(c.LEFT_BRACKETS)

    def newline(self):
        return "\n" if rnd.random() < 0.8 else "\n\n"

    def right_bracket(self):
        return rnd.choice(c.RIGHT_BRACKETS)

    def sep_with_ws(self, seps, weights=None, ws_nrange=(1, 4)):
        sep = (
            rnd.choices(seps, weights=weights, k=1)[0] if weights else
            rnd.choice(seps)
        )
        return "{ws}{sep}{ws}".format(sep=sep, ws=self.whitespace(nrange=ws_nrange))

    def sep_with_ws_right(self, seps, weights=None, ws_nrange=(1, 2)):
        sep = (
            rnd.choices(seps, weights=weights, k=1)[0] if weights else
            rnd.choice(seps)
        )
        return "{sep}{ws}".format(sep=sep, ws=self.whitespace(nrange=ws_nrange))

    def subheader(self):
        template = rnd.choices(
            self._subheader_templates, weights=[1.0, 0.5, 0.25, 0.1], k=1,
        )[0]
        word1, word2, word3 = rnd.sample(c.SUBHEADERS, 3)
        sep = self.and_rand()
        if rnd.random() < 0.75:
            template_fmt = template.format(
                word1=word1, word2=word2, word3=word3, sep=sep,
            ).upper()
        else:
            template_fmt = template.format(
                word1=word1.capitalize(),
                word2=word2.capitalize(),
                word3=word3.capitalize(),
                sep=sep,
            )
        return template_fmt

    def website(self):
        if rnd.random() < 0.5:
            return self.generator.url()
        else:
            return self.generator.domain_name(levels=rnd.randint(1, 2))

    def whitespace(self, nrange=(1, 4)):
        return " " * rnd.randint(*nrange)


class MarkovModel:
    """
    Class to generate fake text using a Markov model trained on data. It's not fancy,
    but it's a big improvement over totally-random "lorem ipsum"!
    """

    def __init__(self, state_len=4):
        self.state_len = state_len
        self.model = None

    def train(self, text):
        """
        Args:
            text (str)
        """
        model = collections.defaultdict(collections.Counter)
        state_len = self.state_len
        for i in range(len(text) - state_len):
            state = text[i : i + state_len]
            next_char = text[i + state_len]
            model[state][next_char] += 1
        LOGGER.debug("trained markov model has %s states", len(model))
        self.model = model

    def generate(self, n_chars, state=None):
        """
        Args:
            n_chars (int)
            state (str)

        Returns:
            str
        """
        if self.model is None:
            raise Exception("model has not yet been trained")
        if state and len(state) != self.state_len:
            raise ValueError("invalid state; must be of length {}".format(self.state_len))
        elif state is None:
            state = rnd.choice(list(self.model))

        chars = list(state)
        for _ in range(n_chars):
            next_chars = self.model[state]
            if not next_chars:
                LOGGER.warning(
                    "markov model state '%s' only occurred once at the end of training, "
                    "so no next chars available; bailing...", state,
                )
                break
            next_char = rnd.choices(list(next_chars), weights=next_chars.values())
            chars.extend(next_char)
            state = state[1:] + next_char[0]

        return "".join(chars)


def generate_labeled_tokens(templates, fields, *, n=1, fixed_val_field_keys=None):
    """
    Generate one or many fake examples by combining fields arranged as in ``templates``
    with values and default labels specified by ``fields``.

    Args:
        templates (List[str] or List[Callable])
        fields (Dict[str, Tuple[Callable, str]])
        section (str)
        n (int)
        fixed_val_field_keys (str or Set[str])

    Yields:
        List[Tuple[str, str]]
    """
    fixed_val_field_keys = utils.to_collection(fixed_val_field_keys, str, set)
    for template in rnd.choices(templates, k=n):
        if callable(template):
            template = template()
        template_fields = regexes.RE_TEMPLATE_FIELD.findall(template)
        field_keys = []
        field_labels = []
        field_vals = []
        const_field_vals = {}
        for key, label, prob in template_fields:
            if prob and rnd.random() > float(prob):
                continue
            field_key = key if "|" not in key else rnd.choice(key.split("|"))
            field_label = label or fields[field_key][1]
            if fixed_val_field_keys and field_key in fixed_val_field_keys:
                field_value = const_field_vals.setdefault(
                    field_label, fields[field_key][0](),
                )
            else:
                field_value = fields[field_key][0]()
            field_keys.append(field_key)
            field_labels.append(field_label)
            field_vals.append(field_value)
        tok_labels = [
            (tok.text, label)
            for val, label in zip(field_vals, field_labels)
            for tok in TOKENIZER(val)
        ]
        yield tok_labels
