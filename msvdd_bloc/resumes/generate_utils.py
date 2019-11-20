"""
generate utils
--------------

Functionality for generating fake examples of labeled tokens for training a parser
in a résumé section-agnostic manner. Section subpackages use and build upon these utils
in their respective ``generate.py`` modules.
"""
import random as rnd
import re

import faker

from msvdd_bloc import regexes
from msvdd_bloc import utils
from msvdd_bloc.resumes import constants as c
from msvdd_bloc.resumes.parse_utils import TOKENIZER


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

    def and_rand(self):
        return rnd.choice(c.ANDS)

    def left_bracket(self):
        return rnd.choice(c.LEFT_BRACKETS)

    def newline(self):
        return "\n" if rnd.random() < 0.8 else "\n\n"

    def right_bracket(self):
        return rnd.choice(c.RIGHT_BRACKETS)

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

    def whitespace(self):
        return " " * rnd.randint(1, 4)


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
