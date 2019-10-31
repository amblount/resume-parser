import functools
import random

from msvdd_bloc.resumes.generate import generators
from msvdd_bloc.resumes.generate import noise


_COMMON_FIELD_LABEL_SEPS = (":", "-", "")
_COMMON_FIELD_SEPS = ("|", "–", "-", ":", "•", "·", "Ÿ", "�", "⇧")
_COMMON_ITEM_SEPS = (",", ";")


def generate_field_sep():
    return "{ws}{sep}{ws}".format(
        ws=" " * random.randint(1, 4),
        sep=random.choices(
            _COMMON_FIELD_SEPS,
            weights=[1.0, 0.5, 0.5, 0.25, 0.1, 0.05, 0.05, 0.05, 0.05],
            k=1,
        )[0],
    )


def generate_item_sep():
    return "{sep}{ws}".format(
        sep=random.choices(_COMMON_ITEM_SEPS, weights=[1.0, 0.2], k=1)[0],
        ws=" " * random.randint(1, 2),
    )


def generate_label_addr():
    return "{label}{ws}{sep}".format(
        label=random.choices(["Address", "Current Address"], weights=[1.0, 0.1], k=1)[0],
        ws="" if random.random() < 0.9 else " ",
        sep=random.choices(_COMMON_FIELD_LABEL_SEPS, weights=[1.0, 0.2, 0.2], k=1)[0],
    )


def generate_label_email():
    return "{label}{ws}{sep}".format(
        label=random.choice(["Email", "E-mail"]),
        ws="" if random.random() < 0.9 else " ",
        sep=random.choices(_COMMON_FIELD_LABEL_SEPS, weights=[1.0, 0.2, 0.2], k=1)[0],
    )


def generate_label_phone():
    return "{label}{ws}{sep}".format(
        label=random.choice(["Phone", "Mobile", "Cell", "Tel."]),
        ws="" if random.random() < 0.9 else " ",
        sep=random.choices(_COMMON_FIELD_LABEL_SEPS, weights=[1.0, 0.2, 0.2], k=1)[0],
    )


def generate_label_profile():
    return "{label}{ws}{sep}".format(
        label=random.choice(["GitHub", "Twitter", "LinkedIn"]),
        ws="" if random.random() < 0.9 else " ",
        sep=random.choices(_COMMON_FIELD_LABEL_SEPS, weights=[1.0, 0.2, 0.2], k=1)[0],
    )


def generate_whitespace():
    return " " * random.randint(1, 4)


FIELDS = {
    "addr": (generators.address, "location"),
    "addr_city_state": (generators.address_city_state, "location"),
    "addr_city_state_zip": (generators.address_city_state_zip, "location"),
    "addr_street": (generators.address_street, "location"),
    "email": (generators.email, "email"),
    "fs": (generate_field_sep, "field_sep"),
    "is": (generate_item_sep, "item_sep"),
    "job_title": (generators.job_title, "label"),
    "label_addr": (generate_label_addr, "field_label"),
    "label_email": (generate_label_email, "field_label"),
    "label_phone": (generate_label_phone, "field_label"),
    "label_profile": (generate_label_profile, "field_label"),
    "name": (generators.person_name, "name"),
    "nl": (generators.newline, "field_sep"),
    "phone": (generators.phone, "phone"),
    "sent_short": (generators.sentence_short, "other"),
    "user_name": (generators.user_name, "profile"),
    "website": (generators.website, "website"),
    "website_profile": (generators.website_profile, "website"),  # TODO: is this best?
    "ws": (generate_whitespace, "field_sep"),
}
"""
Dict[str, Tuple[Callable, str]]: Mapping of field key string to a function that generates
a random field value and the default field label assigned to the value.
"""

TEMPLATES = [
    ("{addr_city_state} {nl} {phone} {nl} {name} {nl} {website_profile} {nl} {email} {nl} {website_profile}", 1),
    ("{addr_street} {nl} {addr_city_state_zip} {nl} {name} {nl} {phone} {nl} {email} {nl} {website}", 1),
    ("{name}", 2),
    ("{name} {fs} {email} {fs} {website_profile}", 1),
    ("{name} {fs} {email} {nl} {website} {fs} {phone} {nl} {user_name} {fs:item_sep} {user_name}", 1),
    ("{name} {nl} {addr} {fs} {email} {fs} {phone}", 1),
    ("{name} {nl} {addr} {fs} {phone} {fs} {email} {fs} {nl} {website_profile}", 1),
    ("{name} {nl} {addr} {nl} {phone} {nl} {email}", 1),
    ("{name} {nl} {addr} {nl} {phone} {nl} {email} {fs} {website_profile}", 1),
    ("{name} {nl} {addr} {ws} {phone} {ws} {email}", 1),
    ("{name} {nl} {addr_city_state} {fs} {phone} {fs} {email}", 1),
    ("{name} {nl} {addr_city_state} {nl} {email} {nl} {website_profile}", 1),
    ("{name} {nl} {addr_street} {fs:item_sep} {addr_city_state_zip} {fs} {email} {fs} {phone}", 1),
    ("{name} {nl} {addr_street} {fs:item_sep} {addr_city_state_zip} {fs} {phone} {fs} {email} {nl} {website_profile} {fs:item_sep} {website_profile}", 1),
    ("{name} {nl} {email}", 1),
    ("{name} {nl} {email} {fs} {addr}", 1),
    ("{name} {nl} {email} {fs} {phone}", 1),
    ("{name} {nl} {email} {fs} {phone} {fs} {addr}", 1),
    ("{name} {nl} {email} {fs} {phone} {fs} {addr} {nl} {website} {fs} {website_profile}", 1),
    ("{name} {nl} {email} {fs} {phone} {fs} {website_profile}", 4),
    ("{name} {nl} {email} {fs} {phone} {fs} {website_profile} {fs:item_sep} {website_profile}", 1),
    ("{name} {nl} {email} {fs} {phone} {nl} {sent_short}", 1),
    ("{name} {nl} {email} {nl} {label_phone} {ws} {phone}", 1),
    ("{name} {nl} {email} {nl} {phone} {nl} {label_addr} {ws} {addr}", 1),
    ("{name} {nl} {email} {ws} {phone} {website} {addr_city_state}", 1),
    ("{name} {nl} {job_title} {nl} {email} {fs} {phone} {fs} {addr_street} {fs:item_sep} {addr_city_state} {nl} {website} {fs} {user_name} {fs} {website_profile} {fs} {website_profile}", 1),
    ("{name} {nl} {job_title} {nl} {email} {ws} {phone} {ws} {website_profile} {ws:item_sep} {website_profile}", 1),
    ("{name} {nl} {job_title} {nl} {sent_short}", 1),
    ("{name} {nl} {label_addr} {ws} {addr} {nl} {phone} {fs} {label_profile} {ws} {ws} {user_name} {fs} {email} {fs} {website_profile}", 1),
    ("{name} {nl} {label_email} {ws} {email} {fs} {label_phone} {ws} {phone} {fs} {label_profile} {ws} {website}", 1),
    ("{name} {nl} {label_email} {ws} {email} {fs} {label_phone} {ws} {phone} {fs} {label_profile} {ws} {website_profile}", 1),
    ("{name} {nl} {label_phone} {ws} {phone} {fs} {label_email} {ws} {email} {fs} {label_profile} {ws} {website_profile}", 1),
    ("{name} {nl} {label_phone} {ws} {phone} {fs} {website_profile} {fs} {label_email} {ws} {email}", 1),
    ("{name} {nl} {label_phone} {ws} {phone} {nl} {label_email} {ws} {email} {label_profile} {ws} {website_profile} {nl} {label_profile} {ws} {website_profile}", 1),
    ("{name} {nl} {label_phone} {ws} {phone} {ws} {label_email} {ws} {email} {nl} {label_profile} {ws} {website_profile} {ws} {label_profile} {ws} {user_name}", 1),
    ("{name} {nl} {phone} {fs} {email} {fs} {addr}", 1),
    ("{name} {nl} {phone} {fs} {email} {nl} {website_profile} {fs} {website_profile}", 1),
    ("{name} {nl} {phone} {nl} {email} {nl} {website_profile} {nl} {addr}", 1),
    ("{name} {nl} {phone} {nl} {website} {nl} {email}", 1),
    ("{name} {nl} {phone} {ws} {email}", 1),
    ("{name} {nl} {website} {nl} {email} {fs} {phone}", 1),
    ("{name} {nl} {website_profile} {nl} {phone} {ws} {email}", 1),
    ("{name} {ws} {addr} {nl} {user_name} {ws} {website_profile} {ws} {phone}", 1),
    ("{name} {ws} {addr} {nl} {website_profile} {ws} {email} {nl} {phone}", 1),
    ("{name} {ws} {label_email} {ws} {email} {nl} {website} {ws} {label_phone} {ws} {phone}", 1),
    ("{name} {ws} {email} {fs} {phone} {fs} {addr_city_state} {fs} {website_profile} {fs:item_sep} {website_profile}", 1),
    ("{name} {ws} {email} {phone} {ws} {website_profile} {ws} {addr_city_state}", 1),
]


def add_noise(tok_labels):
    """
    Args:
        tok_labels (List[Tuple[str, str]])

    Returns:
        List[Tuple[str, str]]
    """
    noise_funcs = []
    # noise_funcs.append(functools.partial(noise.delete_token_chars, 0.001))
    if random.random() < 0.05:
        noise_funcs.append(functools.partial(noise.uppercase_token_text, {"name"}))
    for noise_func in noise_funcs:
        tok_labels = noise_func(tok_labels)
    return tok_labels
