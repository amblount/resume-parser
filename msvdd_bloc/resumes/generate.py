import functools
import random
import re

import faker
import spacy

from msvdd_bloc.resumes.parse.utils import TOKENIZER


FAKER = faker.Faker(locale="en_US")
_FAKERS = {
    locale: faker.Faker(locale=locale)
    for locale in ("en_US", "en_GB", "en_NZ", "es_ES", "es_MX", "fr_FR")
}

CONST_FIELD_KEYS = {"field_sep", "item_sep"}

RE_TEMPLATE_FIELD = re.compile(
    r"{(?P<key>[\w|]+)(?::(?P<label>\w+)?(?::(?P<prob>\d\.\d+)?)?)?}",
    flags=re.UNICODE,
)

FIELD_SEPS = ("|", "–", "-", ":", "•", "·", "Ÿ", "�")
ITEM_SEPS = (",", ";")

_PERSON_NAMES = [_faker.name() for _faker in _FAKERS.values() for _ in range(500)]


def _generate_field_sep():
    return "{ws}{sep}{ws}".format(
        ws=" " * random.randint(1, 4),
        sep=random.choices(
            FIELD_SEPS,
            weights=[1.0, 0.5, 0.5, 0.25, 0.1, 0.05, 0.05, 0.05],
            k=1
        )[0],
    )


def _generate_item_sep():
    return "{sep}{ws}".format(
        sep=random.choices(ITEM_SEPS, weights=[1.0, 0.2], k=1)[0],
        ws=" " * random.randint(1, 2),
    )


FIELDS = {
    "any": {
        "addr": [
            lambda: FAKER.address().replace("\n", " "),
            lambda: "{city}, {state_abbr}".format(
                city=FAKER.city(),
                state_abbr=FAKER.state_abbr(),
            ),
            lambda: "{city}, {state_abbr} {postcode}".format(
                city=FAKER.city(),
                state_abbr=FAKER.state_abbr(),
                postcode=FAKER.postcode(),
            ),
        ],
        "addr_street": FAKER.street_address,
        "addr_city_state": lambda: "{city}, {state_abbr}".format(
            city=FAKER.city(),
            state_abbr=FAKER.state_abbr(),
        ),
        "email": FAKER.email,
        "field_sep": _generate_field_sep,
        "item_sep": _generate_item_sep,
        "job_title": [
            FAKER.job,
            lambda: random.choice(["Web Developer", "Data Scientist", "Data Engineer", "Software Engineer", "Back-end engineer", "Front-end engineer"]),
        ],
        "nl": lambda: random.choices(["\n", "\n\n"], weights=[1.0, 0.25], k=1)[0],
        "phone": [
            FAKER.phone_number,
            lambda: FAKER.numerify("###-###-####"),
            lambda: FAKER.numerify("###.###.####"),
            lambda: FAKER.numerify("(###) ###-####"),
        ],
        "sent": lambda: FAKER.sentence(nb_words=random.randint(10, 20)),
        "sent_short": lambda: FAKER.sentence(nb_words=10),
        "sent_long": lambda: FAKER.sentence(nb_words=20),
        "user_name": lambda: "{at}{name}".format(
            at="@" if random.random() < 0.33 else "",
            name=FAKER.user_name(),
        ),
        "website": [
            FAKER.url,
            lambda: FAKER.domain_name(levels=random.randint(1, 2)),
        ],
        "ws": lambda: " " * random.randint(1, 4),
    },
    "basics": {
        "name": lambda: random.choice(_PERSON_NAMES),
        "field_label_addr": lambda: "Address{sep}".format(
            sep=random.choice([":", " - "]) if random.random() < 0.75 else "",
        ),
        "field_label_email": lambda: "{label}{ws}{sep}".format(
            label=random.choice(["Email", "E-mail"]),
            ws="" if random.random() < 0.9 else " ",
            sep=random.choice([":", " - "]) if random.random() < 0.75 else "",
        ),
        "field_label_phone": lambda: "{label}{ws}{sep}".format(
            label=random.choice(["Phone", "Mobile", "Cell", "Tel."]),
            ws="" if random.random() < 0.9 else " ",
            sep=random.choice([":", " - "]) if random.random() < 0.75 else "",
        ),
        "field_label_profile": lambda: "{label}{ws}{sep}".format(
            label=random.choice(["GitHub", "Twitter", "LinkedIn"]),
            ws="" if random.random() < 0.9 else " ",
            sep=random.choice([":", " - "]) if random.random() < 0.75 else "",
        ),
        "website": [
            FAKER.url,
            lambda: FAKER.domain_name(levels=random.randint(1, 2)),
            lambda: "{scheme}linkedin.com/in/{slug}".format(
                scheme=random.choice(["www.", "http://", "http://www."]) if random.random() > 0.75 else "",
                slug=FAKER.slug(value=FAKER.name()),
            ),
            lambda: "{scheme}github.com/{user}".format(
                scheme=random.choice(["www.", "http://", "http://www."]) if random.random() > 0.75 else "",
                user=FAKER.user_name()
            ),
        ],
    }
}


FIELD_TO_LABEL = {
    "basics": {
        "addr": "location",
        "addr_street": "location",
        "addr_city_state": "location",
        "field_label_addr": "field_label",
        "field_label_email": "field_label",
        "field_label_phone": "field_label",
        "field_label_profile": "field_label",
        "job_title": "label",
        "nl": "field_sep",
        "user_name": "profile",
        "ws": "field_sep",
    },
}


TEMPLATES = {
    "basics": [
        "{addr_street} {nl:item_sep} {addr_city_state} {nl} {name} {nl} {phone} {nl} {email} {nl} {website}",
        "{name} {field_sep|nl|ws} {field_label_email::0.1} {email} {field_sep|nl|ws} {field_label_phone::0.1} {phone} {field_sep|nl|ws} {field_label_profile::0.1} {website}",
        "{name} {field_sep|nl|ws} {field_label_email::0.1} {email} {field_sep|nl|ws} {field_label_profile::0.1} {website} {field_sep|nl|ws} {field_label_profile::0.1} {user_name}",
        "{name} {field_sep|nl|ws} {field_label_addr::0.1} {addr} {nl} {field_label_phone::0.1} {phone} {field_sep|nl|ws} {field_label_email::0.1} {email}",
        "{name} {field_sep|nl|ws} {field_label_phone::0.1} {phone} {field_sep|nl|ws} {field_label_email::0.1} {email} {field_sep|nl|ws} {addr|addr_city_state}",
        "{name} {nl} {email} {field_sep|ws} {website}",
        "{name} {nl} {field_label_addr::0.1} {addr}",
        "{name} {nl} {addr|addr_city_state} {field_sep|nl} {phone} {field_sep|nl} {email}",
        "{name} {nl} {addr_street} {ws:item_sep} {addr_city_state} {field_sep} {email} {field_sep} {phone}",
        "{name} {nl} {email}",
        "{name} {nl} {email} {field_sep} {addr}",
        "{name} {nl} {email} {nl} {field_label_phone::0.1} {phone}",
        "{name} {nl} {email} {nl} {phone} {nl} {website}",
        "{name} {nl|ws} {email} {ws} {phone} {ws} {website} {ws::0.5} {addr_city_state}",
        "{name} {nl} {field_label_email::0.1} {email} {field_sep|nl|ws:field_sep} {field_label_phone::0.1} {phone} {field_sep|nl|ws:field_sep} {field_label_profile::0.1} {website}",
        "{name} {nl} {job_title} {nl} {email} {field_sep} {phone} {field_sep} {addr} {nl} {user_name} {field_sep} {website} {field_sep} {website}",
        "{name} {nl} {job_title} {nl} {email} {ws} {phone} {ws} {website}",
        "{name} {nl} {phone} {field_sep} {email} {field_sep} {addr_city_state}",
        "{name} {nl} {phone} {field_sep} {email} {nl} {website} {ws:item_sep} {website}",
        "{name} {nl} {phone} {nl} {email} {nl} {website}"
        "{name} {nl} {sent_short:other}",
        "{name} {nl} {website}",
        "{name} {nl} {website} {nl} {phone} {field_sep|ws} {email}",
        "{name} {ws} {addr} {nl} {user_name} {user_name} {ws:item_sep} {email} {ws:item_sep} {phone}",
        "{name} {ws} {field_label_email::0.1} {email} {nl} {field_label_profile::0.1} {website} {ws} {field_label_phone::0.1} {phone}",
    ],
}


def generate_labeled_tokens(section, n=1):
    """
    Args:
        section (str)
        n (int)

    Yields:
        List[Tuple[:class:`spacy.token.Token`, str]]
    """
    for template in random.choices(TEMPLATES[section], k=n):
        fields = RE_TEMPLATE_FIELD.findall(template)
        field_keys = []
        field_labels = []
        field_vals = []
        const_field_vals = {}
        for key, label, prob in fields:
            if prob and random.random() > float(prob):
                continue
            field_key = key if "|" not in key else random.choice(key.split("|"))
            field_label = label or FIELD_TO_LABEL[section].get(field_key) or field_key
            if field_label in CONST_FIELD_KEYS:
                field_value = const_field_vals.setdefault(
                    field_label, _get_random_field_value(section, field_label)
                )
            else:
                field_value = _get_random_field_value(section, field_key)
            field_keys.append(field_key)
            field_labels.append(field_label)
            field_vals.append(field_value)
        tok_labels = [
            (tok.text, label)
            for val, label in zip(field_vals, field_labels)
            for tok in TOKENIZER(val)
        ]
        yield tok_labels


def add_noise_to_tok_labels(tok_labels):
    noise_funcs = []
    # noise_funcs.append(functools.partial(_delete_chars, 0.01))
    if random.random() < 0.05:
        noise_funcs.append(functools.partial(_uppercase_token, "name"))
    for noise_func in noise_funcs:
        tok_labels = noise_func(tok_labels)
    return tok_labels


def _uppercase_token(label_to_change, tok_labels):
    return [
        (tok.upper(), label) if label == label_to_change else (tok, label)
        for tok, label in tok_labels
    ]


# def _delete_chars(prob, tok_labels):
#     return [
#         ("".join(c for c in tok if random.random() > prob), label)
#         for tok, label in tok_labels
#     ]


def _get_random_field_value(section, field_key):
    """
    Args:
        section (str)
        field_key (str)

    Returns:
        obj
    """
    generator = FIELDS.get(section, {}).get(field_key) or FIELDS["any"][field_key]
    if isinstance(generator, (list, tuple)):
        generator = random.choice(generator)
    return generator()
