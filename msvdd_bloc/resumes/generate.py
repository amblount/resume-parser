import random
import re

import faker
import spacy


FAKER = faker.Faker(locale="en_US")
TOKENIZER = spacy.blank("en")

CONST_FIELD_KEYS = {"field_sep", "item_sep"}

RE_TEMPLATE_FIELD = re.compile(r"{(\w+)}")

FIELD_SEPS = (":", "|", "-", "–", "•")
ITEM_SEPS = (",", ";")


def _generate_field_sep():
    return "{ws}{field_sep}{ws}".format(
        ws=" " * random.randint(1, 4),
        field_sep=random.choice(FIELD_SEPS),
    )


def _generate_field_sep_colon():
    return ":{ws}".format(ws=" " * random.randint(1, 2))


FIELDS = {
    "any": {
        "address": [
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
        "address_street": FAKER.street_address,
        "address_city_state": lambda: "{city}, {state_abbr}".format(
            city=FAKER.city(),
            state_abbr=FAKER.state_abbr(),
        ),
        "field_sep_colon": _generate_field_sep_colon,
        "email": FAKER.email,
        "field_sep": _generate_field_sep,
        "job_title": FAKER.job,
        "phone": [
            FAKER.phone_number,
            lambda: FAKER.numerify("###-###-####"),
            lambda: FAKER.numerify("###.###.####"),
            lambda: FAKER.numerify("(###) ###-####"),
        ],
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
        "name": FAKER.name,
        "field_label_profile": lambda: random.choice(["GitHub", "Twitter", "LinkedIn"]),
        "field_label_email": lambda: random.choice(["Email", "e-mail"]),
        "field_label_phone": lambda: random.choice(["Phone", "Mobile"]),
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
        "address": "location",
        "address_street": "location",
        "address_city_state": "location",
        "field_sep_colon": "field_sep",
        "field_label_email": "field_label",
        "field_label_phone": "field_label",
        "field_label_profile": "field_label",
        "job_title": "label",
        "user_name": "profile",
        "ws": "field_sep",
    },
}

TEMPLATES = {
    "basics": [
        ("{name}", "{address}{field_sep}{phone}{field_sep}{email}"),
        ("{name}", "{address_street}{field_sep}{address_city_state}{field_sep}{email}{field_sep}{phone}"),
        ("{name}", "{phone}{field_sep}{email}{field_sep}{address}"),
        ("{name}", "{field_label_email}{field_sep_colon} {email}", "{field_label_phone}{field_sep_colon} {phone}"),
        ("{name}{ws}{email}{ws}{phone}{ws}{website}{ws}{address_city_state}",),
        ("{name}{field_sep}{email}{field_sep}{website}",),
        ("{name}", "{job_title}", "{email}{field_sep}{address_street}{field_sep}{address_city_state}", "{website}{field_sep}{user_name}"),
        ("{name}", "{address_city_state}{field_sep}{phone}{field_sep}{email}"),
        ("{name}", "{website}", "{phone}{ws}{email}"),
        ("{name}", "{field_label_email}{ws}{email}{field_sep}{field_label_phone}{ws}{phone}{field_sep}{website}"),
        ("{name}", "{email}{ws}{phone}{ws}{website}{ws}{address_city_state}"),
        ("{name}", "{address}", "{phone}{field_sep}{field_label_profile}{field_sep_colon}{user_name}{field_sep}{email}"),
        ("{name}", "{field_label_email}{field_sep_colon}{email}{field_sep}{field_label_phone}{field_sep_colon}{phone}{field_sep}{field_label_profile}{field_sep_colon}{user_name}"),
        ("{name}{field_sep}{email}", "{website}{field_sep}{phone}", "{field_label_profile}{user_name}{field_sep}{field_label_profile}{user_name}"),
        ("{name}", "{email}", "{phone}", "{website}"),
        ("{name}{field_sep}{email}", "{website}{field_sep}{website}"),
        ("{name}", "{job_title}", "{email}{ws}{phone}{ws}{website}"),
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
        for line in template:
            field_keys = RE_TEMPLATE_FIELD.findall(line)
            field_labels = [
                FIELD_TO_LABEL[section].get(field_key, field_key)
                for field_key in field_keys
            ]
            # some fields should be the same for all occurrences in a given line
            const_field_vals = {}
            for cfk in CONST_FIELD_KEYS:
                if any(fl == cfk for fl in field_labels):
                    const_field_vals[cfk] = _get_random_field_value(section, cfk)
            field_vals = [
                const_field_vals.get(field_key) or _get_random_field_value(section, field_key)
                for field_key in field_keys
            ]
            tok_labels = [
                (tok.text, label)
                for val, label in zip(field_vals, field_labels)
                for tok in TOKENIZER(val)
            ]
            yield tok_labels


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
