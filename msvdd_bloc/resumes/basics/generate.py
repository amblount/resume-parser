import functools as fnc
import random as rnd

import faker

from msvdd_bloc.providers import resume_basics
from msvdd_bloc.resumes import noise_utils


FAKER = faker.Faker()
FAKER.add_provider(resume_basics.Provider)


FIELDS = {
    "addr": (FAKER.address_inline, "location"),
    "addr_city_state": (FAKER.address_city_state, "location"),
    "addr_city_state_zip": (FAKER.address_city_state_zip, "location"),
    "addr_street": (FAKER.street_address, "location"),
    "email": (FAKER.email, "email"),
    "fs": (FAKER.field_sep, "field_sep"),
    "is": (FAKER.item_sep, "item_sep"),
    "label": (FAKER.person_label, "label"),
    "label_addr": (FAKER.label_addr, "field_label"),
    "label_email": (FAKER.label_email, "field_label"),
    "label_phone": (FAKER.label_phone, "field_label"),
    "label_profile": (FAKER.label_profile, "field_label"),
    "name": (FAKER.name, "name"),
    "nl": (FAKER.newline, "field_sep"),
    "phone": (FAKER.phone, "phone"),
    "profile": (FAKER.website_profile, "website"),  # TODO: improve this?
    "sent": (fnc.partial(FAKER.sentence, nb_words=10, variable_nb_words=True), "other"),
    "user_name": (FAKER.user_name_rand_at, "profile"),
    "website": (FAKER.website, "website"),
    "ws": (FAKER.whitespace, "field_sep"),
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
