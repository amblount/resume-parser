import functools as fnc
import random as rnd

import faker

from msvdd_bloc.resumes.basics import constants as c
from msvdd_bloc.resumes import generate_utils


class Provider(generate_utils.ResumeProvider):
    """Class for providing randomly-generated field values."""

    _address_city_state_templates = (
        "{city}, {state_abbr}",
        "{city}, {state}",
    )
    _address_city_state_zip_templates = (
        "{city}, {state_abbr} {postcode}",
        "{city}, {state} {postcode}",
    )
    _user_name_templates = (
        "{user_name}",
        "@{user_name}",
    )
    _website_profile_templates = (
        "{scheme}linkedin.com/in/{slug}",
        "{scheme}github.com/{user}",
    )

    def address_city_state(self):
        template = rnd.choices(
            self._address_city_state_templates, weights=[0.9, 0.1], k=1)[0]
        return template.format(
            city=self.generator.city(),
            state=self.generator.state(),
            state_abbr=self.generator.state_abbr(),
        )

    def address_city_state_zip(self):
        template = rnd.choices(
            self._address_city_state_zip_templates, weights=[0.9, 0.1], k=1)[0]
        return template.format(
            city=self.generator.city(),
            state=self.generator.state(),
            state_abbr=self.generator.state_abbr(),
            postcode=self.generator.postcode(),
        )

    def field_sep(self):
        return self.generator.sep_with_ws(
            c.FIELD_SEPS,
            weights=[1.0, 0.5, 0.5, 0.25, 0.1, 0.05, 0.05, 0.05, 0.05],
            ws_nrange=(1, 4),
        )

    def item_sep(self):
        return self.generator.sep_with_ws_right(
            c.ITEM_SEPS, weights=[1.0, 0.2], ws_nrange=(1, 2),
        )

    def label_addr(self):
        return self.generator.field_label(
            c.FIELD_LABEL_ADDRS, c.FIELD_LABEL_SEPS,
            label_weights=[1.0, 0.1], sep_weights=[1.0, 0.2],
        )

    def label_email(self):
        return self.generator.field_label(
            c.FIELD_LABEL_EMAILS, c.FIELD_LABEL_SEPS,
            label_weights=[1.0, 0.5], sep_weights=[1.0, 0.2],
        )

    def label_phone(self):
        return self.generator.field_label(
            c.FIELD_LABEL_PHONES, c.FIELD_LABEL_SEPS,
            label_weights=None, sep_weights=[1.0, 0.2],
        )

    def label_profile(self):
        return self.generator.field_label(
            c.FIELD_LABEL_PROFILES, c.FIELD_LABEL_SEPS,
            label_weights=None, sep_weights=[1.0, 0.2],
        )

    def phone(self):
        if rnd.random() < 0.25:
            return self.generator.phone_number()
        else:
            return self.numerify(rnd.choice(c.PHONE_FORMATS))

    def person_label(self):
        if rnd.random() > 0.8:
            return self.generator.job()
        else:
            return self.generator.catch_phrase()

    def user_name_rand_at(self):
        template = rnd.choices(self._user_name_templates, weights=[1.0, 0.33], k=1)[0]
        return template.format(user_name=self.generator.user_name())

    def website_profile(self):
        template = rnd.choice(self._website_profile_templates)
        return template.format(
            scheme=rnd.choice(c.URL_SCHEMES) if rnd.random() < 0.75 else "",
            slug=self.generator.slug(value=self.generator.name()),
            user=self.generator.user_name(),
        )


FAKER = faker.Faker()
FAKER.add_provider(Provider)


FIELDS = {
    "addr": (FAKER.address_inline, "location"),
    "addr_city_state": (FAKER.address_city_state, "location"),
    "addr_city_state_zip": (FAKER.address_city_state_zip, "location"),
    "addr_street": (FAKER.street_address, "location"),
    "email": (FAKER.email, "email"),
    "fsep": (FAKER.field_sep, "field_sep"),
    "isep": (FAKER.item_sep, "item_sep"),
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
                sep_key="fsep",
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
                sep_key="fsep",
                n=2,
            ),
            generate_line_fields_shuffle(
                field_keys=["email", "user_name", "website", "profile"],
                sep_key="fsep",
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
                sep_key="fsep|nl",
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
                sep_key="fsep",
                n=rnd.randint(2, 4),
            ),
            "{sent::0.05}",
        ]
    ),
    lambda: " {nl|fsep} ".join(
        [
            "{name}",
            "{addr_street} {fsep:item_sep} {addr_city_state_zip}",
            generate_line_fields_shuffle(
                field_keys=["email", "phone", "profile", "website"],
                sep_key="fsep",
                n=rnd.randint(2, 4),
            ),
        ]
    ),
]
"""
List[Callable]: Collection of functions that generate randomized "basics" résumé sections
when passed with :obj:`FIELDS` into :func:`msvdd_bloc.resumes.generate_utils.generate_labeled_tokens()`.
"""
