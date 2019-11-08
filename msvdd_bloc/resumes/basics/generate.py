import functools as fnc
import random as rnd

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

#############################
## random field generators ##
#############################

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
        ws=" " * rnd.randint(1, 4),
        sep=rnd.choices(
            _FIELD_SEPS,
            weights=[1.0, 0.5, 0.5, 0.25, 0.1, 0.05, 0.05, 0.05, 0.05],
            k=1,
        )[0],
    )


def generate_field_item_sep():
    return "{sep}{ws}".format(
        sep=rnd.choices(_ITEM_SEPS, weights=[1.0, 0.2], k=1)[0],
        ws=" " * rnd.randint(1, 2),
    )


def generate_field_label_addr():
    return "{label}{ws}{sep}".format(
        label=rnd.choices(_FIELD_LABEL_ADDRS , weights=[1.0, 0.1], k=1)[0],
        ws="" if rnd.random() < 0.9 else " ",
        sep=rnd.choices(_FIELD_LABEL_SEPS, weights=[1.0, 0.2, 0.2], k=1)[0],
    )


def generate_field_label_email():
    return "{label}{ws}{sep}".format(
        label=rnd.choice(_FIELD_LABEL_EMAILS),
        ws="" if rnd.random() < 0.9 else " ",
        sep=rnd.choices(_FIELD_LABEL_SEPS, weights=[1.0, 0.2, 0.2], k=1)[0],
    )


def generate_field_label_phone():
    return "{label}{ws}{sep}".format(
        label=rnd.choice(_FIELD_LABEL_PHONES),
        ws="" if rnd.random() < 0.9 else " ",
        sep=rnd.choices(_FIELD_LABEL_SEPS, weights=[1.0, 0.2, 0.2], k=1)[0],
    )


def generate_field_label_profile():
    return "{label}{ws}{sep}".format(
        label=rnd.choice(_FIELD_LABEL_PROFILES),
        ws="" if rnd.random() < 0.9 else " ",
        sep=rnd.choices(_FIELD_LABEL_SEPS, weights=[1.0, 0.2, 0.2], k=1)[0],
    )


def generate_field_name():
    return FAKER.name()


def generate_field_newline():
    if rnd.random() < 0.8:
        return "\n"
    else:
        return "\n\n"


def generate_field_phone():
    if rnd.random() < 0.25:
        return FAKER.phone_number()
    else:
        return FAKER.numerify(rnd.choice(_PHONE_FORMATS))


def generate_field_resume_label():
    if rnd.random() > 0.8:
        return FAKER.job()
    else:
        return FAKER.catch_phrase()


def generate_field_sentence():
    return FAKER.sentence(nb_words=rnd.randint(5, 15))


def generate_field_user_name():
    return "{at}{name}".format(
        at="@" if rnd.random() < 0.33 else "",
        name=FAKER.user_name(),
    )


def generate_field_website():
    if rnd.random() < 0.5:
        return FAKER.url()
    else:
        return FAKER.domain_name(levels=rnd.randint(1, 2))


def generate_field_website_profile():
    if rnd.random() < 0.5:
        return "{scheme}linkedin.com/in/{slug}".format(
            scheme=rnd.choice(_URL_SCHEMES),
            slug=FAKER.slug(value=FAKER.name()),
        )
    else:
        return "{scheme}github.com/{user}".format(
            scheme=rnd.choice(_URL_SCHEMES),
            user=FAKER.user_name(),
        )


def generate_field_whitespace():
    return " " * rnd.randint(1, 4)


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
    "profile": (generate_field_website_profile, "website"),  # TODO: improve this?
    "sent": (generate_field_sentence, "other"),
    "user_name": (generate_field_user_name, "profile"),
    "website": (generate_field_website, "website"),
    "ws": (generate_field_whitespace, "field_sep"),
}
"""
Dict[str, Tuple[Callable, str]]: Mapping of field key string to a function that generates
a random field value and the default field label assigned to the value.
"""

############################
## random line generators ##
############################

def generate_line_fields_shuffle(*, field_keys, sep_key, n):
    """
    Args:
        field_keys (List[str])
        sep_key (str)
        n (int)

    Returns:
        str
    """
    sep = " {{{key}}} ".format(key=sep_key)
    return sep.join(
        "{{{key}}}".format(key=key)
        for key in rnd.sample(field_keys, min(n, len(field_keys)))
    )


def generate_line_fields_labeled_shuffle(*, field_keys, sep_key, n):
    """
    Args:
        field_keys (List[str])
        sep_key (str)
        n (int)

    Returns:
        str
    """
    sep = " {{{key}}} ".format(key=sep_key)
    return sep.join(
        "{{label_{key}}} {{ws}} {{{key}}}".format(key=key)
        for key in rnd.sample(field_keys, min(n, len(field_keys)))
    )


TEMPLATES = [
    lambda: " {nl} ".join(
        [
            "{name}",
            "{label::0.05}",
            generate_line_fields_shuffle(
                field_keys=["addr|addr_city_state|addr_city_state_zip", "email", "phone", "user_name", "website", "profile"],
                sep_key="fs",
                n=rnd.randint(1, 5),
            ),
            "{sent::0.05}",
        ]
    ),
    lambda: " {nl} ".join(
        [
            "{name}",
            "{label::0.05}",
            generate_line_fields_shuffle(
                field_keys=["addr|addr_city_state|addr_city_state_zip", "email", "phone", "profile", "user_name", "website"],
                sep_key="nl",
                n=rnd.randint(1, 5),
            ),
        ]
    ),
    lambda: " {nl} ".join(
        [
            "{name}",
            "{label::0.05}",
            generate_line_fields_shuffle(
                field_keys=["addr|addr_city_state|addr_city_state_zip", "email", "phone", "profile", "user_name", "website"],
                sep_key="ws",
                n=rnd.randint(1, 5),
            ),
            "{sent::0.05}",
        ]
    ),
    lambda: " {nl} ".join(
        [
            "{name}",
            "{label::0.05}",
            generate_line_fields_shuffle(
                field_keys=["addr|addr_city_state|addr_city_state_zip", "phone"],
                sep_key="fs",
                n=2,
            ),
            generate_line_fields_shuffle(
                field_keys=["email", "user_name", "website", "profile"],
                sep_key="fs",
                n=rnd.randint(2, 4),
            ),
        ]
    ),
    lambda: " {nl} ".join(
        [
            "{addr|addr_city_state|addr_city_state_zip}",
            "{name}",
            generate_line_fields_shuffle(
                field_keys=["email", "profile", "user_name", "website"],
                sep_key="fs|nl",
                n=rnd.randint(2, 4),
            ),
        ]
    ),
    lambda: " {nl} ".join(
        [
            "{name}",
            "{label::0.05}",
            generate_line_fields_labeled_shuffle(
                field_keys=["addr", "email", "phone", "profile"],
                sep_key="fs",
                n=rnd.randint(2, 4),
            ),
            "{sent::0.05}",
        ]
    ),
    lambda: " {nl|fs} ".join(
        [
            "{name}",
            "{addr_street} {fs:item_sep} {addr_city_state_zip}",
            generate_line_fields_shuffle(
                field_keys=["email", "phone", "profile", "website"],
                sep_key="fs",
                n=rnd.randint(2, 4),
            ),
        ]
    ),
]


def add_noise(tok_labels):
    """
    Args:
        tok_labels (List[Tuple[str, str]])

    Returns:
        List[Tuple[str, str]]
    """
    noise_funcs = []
    # noise_funcs.append(fnc.partial(noise_utils.delete_token_chars, 0.001))
    if rnd.random() < 0.05:
        noise_funcs.append(fnc.partial(noise_utils.uppercase_token_text, {"name"}))
    for noise_func in noise_funcs:
        tok_labels = noise_func(tok_labels)
    return tok_labels
