import functools
import random
import re

import faker

from msvdd_bloc.resumes.parse_utils import TOKENIZER


FAKER = faker.Faker(locale="en_US")

RE_TEMPLATE_FIELD = re.compile(
    r"{(?P<key>[\w|]+)(?::(?P<label>\w+)?(?::(?P<prob>\d\.\d+)?)?)?}",
    flags=re.UNICODE,
)


def generate_labeled_tokens(templates, fields, *, n=1, const_field_keys=None):
    """
    Args:
        templates (List[str] or List[Callable])
        fields (Dict[str, Tuple[Callable, str]])
        section (str)
        n (int)
        const_field_keys (Set[str])

    Yields:
        List[Tuple[:class:`spacy.token.Token`, str]]
    """
    for template in random.choices(templates, k=n):
        if callable(template):
            template = template()
        template_fields = RE_TEMPLATE_FIELD.findall(template)
        field_keys = []
        field_labels = []
        field_vals = []
        const_field_vals = {}
        for key, label, prob in template_fields:
            if prob and random.random() > float(prob):
                continue
            field_key = key if "|" not in key else random.choice(key.split("|"))
            field_label = label or fields[field_key][1]
            if const_field_keys and field_key in const_field_keys:
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
