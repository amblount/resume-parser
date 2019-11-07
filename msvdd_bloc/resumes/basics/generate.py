import functools
import random

from msvdd_bloc.resumes import noise_utils
from msvdd_bloc.resumes.generate_utils import FAKER


_FIELD_LABEL_SEPS = (":", "-", "")
_FIELD_SEPS = ("|", "–", "-", ":", "•", "·", "Ÿ", "�", "⇧")
_ITEM_SEPS = (",", ";")

_FIELD_LABEL_ADDRS = ("Address", "Current Address")
_FIELD_LABEL_EMAILS = ("Email", "E-mail")
_FIELD_LABEL_PHONES = ("Phone", "Mobile", "Cell", "Tel.")
_FIELD_LABEL_PROFILES = ("GitHub", "Twitter", "LinkedIn")

_PHONE_FORMATS = (
    "###-###-####", "###.###.####", "(###) ###-####", "### ###-####",
)
_URL_SCHEMES = ("www.", "http://", "http://www.", "")


def generate_field_address():
    return FAKER.address().replace("\n", " ")


def generate_field_address_city_state():
    return "{city}, {state_abbr}".format(
        city=FAKER.city(),
        state_abbr=FAKER.state_abbr(),
    )


def generate_field_address_city_state_zip():
    return "{city}, {state_abbr} {postcode}".format(
        city=FAKER.city(),
        state_abbr=FAKER.state_abbr(),
        postcode=FAKER.postcode(),
    )


def generate_field_address_street():
    return FAKER.street_address()


def generate_field_email():
    return FAKER.email()


def generate_field_field_sep():
    return "{ws}{sep}{ws}".format(
        ws=" " * random.randint(1, 4),
        sep=random.choices(
            _FIELD_SEPS,
            weights=[1.0, 0.5, 0.5, 0.25, 0.1, 0.05, 0.05, 0.05, 0.05],
            k=1,
        )[0],
    )


def generate_field_item_sep():
    return "{sep}{ws}".format(
        sep=random.choices(_ITEM_SEPS, weights=[1.0, 0.2], k=1)[0],
        ws=" " * random.randint(1, 2),
    )


def generate_field_label_addr():
    return "{label}{ws}{sep}".format(
        label=random.choices(_FIELD_LABEL_ADDRS , weights=[1.0, 0.1], k=1)[0],
        ws="" if random.random() < 0.9 else " ",
        sep=random.choices(_FIELD_LABEL_SEPS, weights=[1.0, 0.2, 0.2], k=1)[0],
    )


def generate_field_label_email():
    return "{label}{ws}{sep}".format(
        label=random.choice(_FIELD_LABEL_EMAILS),
        ws="" if random.random() < 0.9 else " ",
        sep=random.choices(_FIELD_LABEL_SEPS, weights=[1.0, 0.2, 0.2], k=1)[0],
    )


def generate_field_label_phone():
    return "{label}{ws}{sep}".format(
        label=random.choice(_FIELD_LABEL_PHONES),
        ws="" if random.random() < 0.9 else " ",
        sep=random.choices(_FIELD_LABEL_SEPS, weights=[1.0, 0.2, 0.2], k=1)[0],
    )


def generate_field_label_profile():
    return "{label}{ws}{sep}".format(
        label=random.choice(_FIELD_LABEL_PROFILES),
        ws="" if random.random() < 0.9 else " ",
        sep=random.choices(_FIELD_LABEL_SEPS, weights=[1.0, 0.2, 0.2], k=1)[0],
    )


def generate_field_name():
    return FAKER.name()


def generate_field_newline():
    if random.random() < 0.8:
        return "\n"
    else:
        return "\n\n"


def generate_field_phone():
    if random.random() < 0.25:
        return FAKER.phone_number()
    else:
        return FAKER.numerify(random.choice(_PHONE_FORMATS))


def generate_field_resume_label():
    if random.random() > 0.8:
        return FAKER.job()
    else:
        return FAKER.catch_phrase()


def generate_field_sentence():
    return FAKER.sentence(nb_words=random.randint(5, 15))


def generate_field_user_name():
    return "{at}{name}".format(
        at="@" if random.random() < 0.33 else "",
        name=FAKER.user_name(),
    )


def generate_field_website():
    if random.random() < 0.5:
        return FAKER.url()
    else:
        return FAKER.domain_name(levels=random.randint(1, 2))


def generate_field_website_profile():
    if random.random() < 0.5:
        return "{scheme}linkedin.com/in/{slug}".format(
            scheme=random.choice(_URL_SCHEMES),
            slug=FAKER.slug(value=FAKER.name()),
        )
    else:
        return "{scheme}github.com/{user}".format(
            scheme=random.choice(_URL_SCHEMES),
            user=FAKER.user_name(),
        )


def generate_field_whitespace():
    return " " * random.randint(1, 4)


FIELDS = {
    "addr": (generate_field_address, "location"),
    "addr_city_state": (generate_field_address_city_state, "location"),
    "addr_city_state_zip": (generate_field_address_city_state_zip, "location"),
    "addr_street": (generate_field_address_street, "location"),
    "email": (generate_field_email, "email"),
    "fs": (generate_field_field_sep, "field_sep"),
    "is": (generate_field_item_sep, "item_sep"),
    "label": (generate_field_resume_label, "label"),
    "label_addr": (generate_field_label_addr, "field_label"),
    "label_email": (generate_field_label_email, "field_label"),
    "label_phone": (generate_field_label_phone, "field_label"),
    "label_profile": (generate_field_label_profile, "field_label"),
    "name": (generate_field_name, "name"),
    "nl": (generate_field_newline, "field_sep"),
    "phone": (generate_field_phone, "phone"),
    "sent_short": (generate_field_sentence, "other"),
    "user_name": (generate_field_user_name, "profile"),
    "website": (generate_field_website, "website"),
    "website_profile": (generate_field_website_profile, "website"),  # TODO: improve this?
    "ws": (generate_field_whitespace, "field_sep"),
}
"""
Dict[str, Tuple[Callable, str]]: Mapping of field key string to a function that generates
a random field value and the default field label assigned to the value.
"""

TEMPLATES = [
    "{addr_city_state} {nl} {phone} {nl} {name} {nl} {website_profile} {nl} {email} {nl} {website_profile}",
    "{addr_street} {nl} {addr_city_state_zip} {nl} {name} {nl} {phone} {nl} {email} {nl} {website}",
    "{name}",
    "{name} {fs} {email} {fs} {website_profile}",
    "{name} {fs} {email} {nl} {website} {fs} {phone} {nl} {user_name} {fs:item_sep} {user_name}",
    "{name} {nl} {addr} {fs} {email} {fs} {phone}",
    "{name} {nl} {addr} {fs} {phone} {fs} {email} {fs} {nl} {website_profile}",
    "{name} {nl} {addr} {nl} {phone} {nl} {email}",
    "{name} {nl} {addr} {nl} {phone} {nl} {email} {fs} {website_profile}",
    "{name} {nl} {addr} {ws} {phone} {ws} {email}",
    "{name} {nl} {addr_city_state} {fs} {phone} {fs} {email}",
    "{name} {nl} {addr_city_state} {nl} {email} {nl} {website_profile}",
    "{name} {nl} {addr_street} {fs:item_sep} {addr_city_state_zip} {fs} {email} {fs} {phone}",
    "{name} {nl} {addr_street} {fs:item_sep} {addr_city_state_zip} {fs} {phone} {fs} {email} {nl} {website_profile} {fs:item_sep} {website_profile}",
    "{name} {nl} {email}",
    "{name} {nl} {email} {fs} {addr}",
    "{name} {nl} {email} {fs} {phone}",
    "{name} {nl} {email} {fs} {phone} {fs} {addr}",
    "{name} {nl} {email} {fs} {phone} {fs} {addr} {nl} {website} {fs} {website_profile}",
    "{name} {nl} {email} {fs} {phone} {fs} {website_profile}",
    "{name} {nl} {email} {fs} {phone} {fs} {website_profile} {fs:item_sep} {website_profile}",
    "{name} {nl} {email} {fs} {phone} {nl} {sent_short}",
    "{name} {nl} {email} {nl} {label_phone} {ws} {phone}",
    "{name} {nl} {email} {nl} {phone} {nl} {label_addr} {ws} {addr}",
    "{name} {nl} {email} {ws} {phone} {website} {addr_city_state}",
    "{name} {nl} {label} {nl} {email} {fs} {phone} {fs} {addr_street} {fs:item_sep} {addr_city_state} {nl} {website} {fs} {user_name} {fs} {website_profile} {fs} {website_profile}",
    "{name} {nl} {label} {nl} {email} {ws} {phone} {ws} {website_profile} {ws:item_sep} {website_profile}",
    "{name} {nl} {label} {nl} {sent_short}",
    "{name} {nl} {label_addr} {ws} {addr} {nl} {phone} {fs} {label_profile} {ws} {ws} {user_name} {fs} {email} {fs} {website_profile}",
    "{name} {nl} {label_email} {ws} {email} {fs} {label_phone} {ws} {phone} {fs} {label_profile} {ws} {website}",
    "{name} {nl} {label_email} {ws} {email} {fs} {label_phone} {ws} {phone} {fs} {label_profile} {ws} {website_profile}",
    "{name} {nl} {label_phone} {ws} {phone} {fs} {label_email} {ws} {email} {fs} {label_profile} {ws} {website_profile}",
    "{name} {nl} {label_phone} {ws} {phone} {fs} {website_profile} {fs} {label_email} {ws} {email}",
    "{name} {nl} {label_phone} {ws} {phone} {nl} {label_email} {ws} {email} {label_profile} {ws} {website_profile} {nl} {label_profile} {ws} {website_profile}",
    "{name} {nl} {label_phone} {ws} {phone} {ws} {label_email} {ws} {email} {nl} {label_profile} {ws} {website_profile} {ws} {label_profile} {ws} {user_name}",
    "{name} {nl} {phone} {fs} {email} {fs} {addr}",
    "{name} {nl} {phone} {fs} {email} {nl} {website_profile} {fs} {website_profile}",
    "{name} {nl} {phone} {nl} {email} {nl} {website_profile} {nl} {addr}",
    "{name} {nl} {phone} {nl} {website} {nl} {email}",
    "{name} {nl} {phone} {ws} {email}",
    "{name} {nl} {website} {nl} {email} {fs} {phone}",
    "{name} {nl} {website_profile} {nl} {phone} {ws} {email}",
    "{name} {ws} {addr} {nl} {user_name} {ws} {website_profile} {ws} {phone}",
    "{name} {ws} {addr} {nl} {website_profile} {ws} {email} {nl} {phone}",
    "{name} {ws} {label_email} {ws} {email} {nl} {website} {ws} {label_phone} {ws} {phone}",
    "{name} {ws} {email} {fs} {phone} {fs} {addr_city_state} {fs} {website_profile} {fs:item_sep} {website_profile}",
    "{name} {ws} {email} {phone} {ws} {website_profile} {ws} {addr_city_state}",
]


def add_noise(tok_labels):
    """
    Args:
        tok_labels (List[Tuple[str, str]])

    Returns:
        List[Tuple[str, str]]
    """
    noise_funcs = []
    # noise_funcs.append(functools.partial(noise_utils.delete_token_chars, 0.001))
    if random.random() < 0.05:
        noise_funcs.append(functools.partial(noise_utils.uppercase_token_text, {"name"}))
    for noise_func in noise_funcs:
        tok_labels = noise_func(tok_labels)
    return tok_labels
