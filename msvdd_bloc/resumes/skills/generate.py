import functools as fnc
import random as rnd

import faker

from msvdd_bloc.resumes.skills import constants as c
from msvdd_bloc.resumes import generate_utils


class Provider(generate_utils.ResumeProvider):
    """Class for providing randomly-generated field values."""

    def database(self):
        return rnd.choice(c.DATABASES)

    def dev_mix(self):
        return rnd.choice(c.DEV_MIX)

    def group_name(self):
        return rnd.choice(c.GROUP_NAMES)

    def group_sep(self):
        return "{ws}{sep}".format(
            ws="" if rnd.random() < 0.9 else " ",
            sep=(
                rnd.choices(c.GROUP_SEPS, weights=[1.0, 0.5, 0.25], k=1)[0] if rnd.random() < 0.9
                else ""
            ),
        )

    def hobby(self):
        return rnd.choice(c.HOBBIES)

    def human_language(self):
        return rnd.choice(c.HUMAN_LANGUAGES)

    def item_sep(self):
        return "{sep}{ws}".format(
            sep=rnd.choices(c.ITEM_SEPS, weights=[1.0, 0.2], k=1)[0],
            ws=" " * rnd.randint(1, 2),
        )

    def item_sep_and(self):
        return rnd.choices(c.ITEM_SEP_ANDS, weights=[1.0, 0.2], k=1)[0]

    def level(self):
        return rnd.choice(c.LEVELS)

    def level_prep(self):
        return rnd.choices(c.LEVEL_PREPS, weights=[1.0, 0.4, 0.2, 0.1], k=1)[0]

    def programming_language(self):
        return rnd.choice(c.PROGRAMMING_LANGUAGES)

    def software(self):
        return rnd.choice(c.SOFTWARE)


FAKER = faker.Faker()
FAKER.add_provider(Provider)


FIELDS = {
    "bullet": (lambda : "- ", "bullet"),
    "db": (FAKER.database, "name"),
    "dev_mix": (FAKER.dev_mix, "name"),
    "isep": (FAKER.item_sep, "item_sep"),
    "isep_and": (FAKER.item_sep_and, "item_sep"),
    "grp_name": (FAKER.group_name, "name"),
    "grp_sep": (FAKER.group_sep, "field_sep"),
    "hobby": (FAKER.hobby, "other"),
    "lang": (FAKER.human_language, "name"),
    "level": (FAKER.level, "level"),
    "level_prep": (FAKER.level_prep, "field_sep"),
    "lb": (FAKER.left_bracket, "field_sep"),
    "nl": (FAKER.newline, "field_sep"),
    "plang": (FAKER.programming_language, "name"),
    "rb": (FAKER.right_bracket, "field_sep"),
    "sent": (fnc.partial(FAKER.sentence, nb_words=10, variable_nb_words=True), "other"),
    "sw": (FAKER.software, "name"),
    "ws": (FAKER.whitespace, "field_sep"),
}
"""
Dict[str, Tuple[Callable, str]]: Mapping of field key string to a function that generates
a random field value and the default field label assigned to the value.
"""

############################
## random line generators ##
############################

def generate_line_fields(*, key, nrange, bullet=False):
    """
    Generate line template for a list of fields, formatted as
    ``{key} {isep} {key} {isep} {isep_and::0.1} {key}``.

    Args:
        key (str)
        nrange (Tuple[int, int])
        bullet (bool)

    Returns:
        str
    """
    nmin, nmax = nrange
    return "{blt} {fields} {field_end}".format(
        blt="" if bullet is False else "{bullet}",
        fields=" {isep} ".join(
            "{{{key}}}".format(key=key)
            for _ in range(rnd.randint(nmin - 1, nmax - 1))
        ),
        field_end="{{isep}} {{isep_and::0.1}} {{{key}}}".format(key=key),
    ).strip()


def generate_line_fields_grped(*, key, nrange, bullet=False):
    """
    Generate line template for a list of fields with a group name, formatted as
    ``{grp_name} {grp_sep} {ws} {key:keyword} {isep} {key:keyword} {isep} {isep_and::0.1} {key:keyword}``.

    Args:
        key (str)
        nrange (Tuple[int, int])
        bullet (bool)

    Returns:
        str
    """
    nmin, nmax = nrange
    return "{blt} {grp} {fields} {field_end}".format(
        blt="" if bullet is False else "{bullet}",
        grp="{grp_name} {grp_sep} {ws}",
        fields=" {isep} ".join(
            "{{{key}:keyword}}".format(key=key)
            for _ in range(rnd.randint(nmin - 1, nmax - 1))
        ),
        field_end="{{isep}} {{isep_and::0.1}} {{{key}:keyword}}".format(key=key),
    ).strip()


def generate_line_fields_levels(*, key, nrange, bullet=False):
    """
    Generate line template for a list of fields with individual levels, formatted as
    ``{key} {lb} {level} {rb} {isep} {key} {lb} {level} {rb} {isep} {isep_and::0.1} {key} {lb} {level} {rb}``.

    Args:
        key (str)
        nrange (Tuple[int, int])
        bullet (bool)

    Returns:
        str
    """
    nmin, nmax = nrange
    return "{blt} {fields} {field_end}".format(
        blt="" if bullet is False else "{bullet}",
        fields=" {isep} ".join(
            "{{{key}}} {{lb}} {{level}} {{rb}}".format(key=key)
            for _ in range(rnd.randint(nmin - 1, nmax - 1))
        ),
        field_end="{{isep}} {{isep_and::0.1}} {{{key}}} {{lb}} {{level}} {{rb}}".format(key=key),
    ).strip()


def generate_line_fields_level_grped(*, key, nrange, bullet=False):
    """
    Generate line template for a list of fields with a group-wide level, formatted as
    ``{level} {level_prep::0.5} {grp_sep::0.25} {key} {isep} {key} {isep} {isep_and::0.1} {key}``.

    Args:
        key (str)
        nrange (Tuple[int, int])
        bullet (bool)

    Returns:
        str
    """
    nmin, nmax = nrange
    return "{blt} {lvl} {fields} {field_end}".format(
        blt="" if bullet is False else "{bullet}",
        lvl="{level} {level_prep::0.5} {grp_sep::0.25}",
        fields=" {isep} ".join(
            "{{{key}}}".format(key=key)
            for _ in range(rnd.randint(nmin - 1, nmax - 1))
        ),
        field_end="{{isep}} {{isep_and::0.1}} {{{key}}}".format(key=key),
    ).strip()


LINES = {
    "grp_name_and_sep": lambda: "{grp_name} {grp_sep}",
    "dev_mixes": fnc.partial(generate_line_fields, key="dev_mix", nrange=(3, 10)),
    "dev_mixes_bulleted": fnc.partial(generate_line_fields, key="dev_mix", nrange=(3, 10), bullet=True),
    "dev_mixes_grped": fnc.partial(generate_line_fields_grped, key="dev_mix", nrange=(3, 10)),
    "dev_mixes_level": fnc.partial(generate_line_fields_levels, key="dev_mix", nrange=(3, 10)),
    "dev_mixes_level_grped": fnc.partial(generate_line_fields_level_grped, key="dev_mix", nrange=(3, 10)),
    "plangs": fnc.partial(generate_line_fields, key="plang", nrange=(3, 8)),
    "plangs_bulleted": fnc.partial(generate_line_fields, key="plang", nrange=(3, 8), bullet=True),
    "plangs_grped": fnc.partial(generate_line_fields_grped, key="plang", nrange=(3, 8)),
    "dbs": fnc.partial(generate_line_fields, key="db", nrange=(3, 6)),
    "dbs_bulleted": fnc.partial(generate_line_fields, key="db", nrange=(3, 6), bullet=True),
    "dbs_grped": fnc.partial(generate_line_fields_grped, key="db", nrange=(3, 6)),
    "langs": fnc.partial(generate_line_fields, key="lang", nrange=(2, 4)),
    "langs_bulleted": fnc.partial(generate_line_fields, key="lang", nrange=(2, 4), bullet=True),
    "langs_grped": fnc.partial(generate_line_fields_grped, key="lang", nrange=(2, 4)),
    "langs_level": fnc.partial(generate_line_fields_levels, key="lang", nrange=(2, 4)),
    "hobbies": fnc.partial(generate_line_fields, key="hobby", nrange=(2, 6)),
    "hobbies_grped": fnc.partial(generate_line_fields_grped, key="hobby", nrange=(2, 6)),
}
"""
Dict[str, Callable]: Intermediate mapping of line type name to a function that generates
a random corresponding value.
"""


def generate_multiline_singletons(*, keys, nrange, bullet_prob=0.25):
    """
    Generate a newline-delimited list of singleton skills, with a key from ``keys``
    and optional leading bullet, for n items within ``nrange``, formatted like
    ``{bullet} {key1|key2} {lb} {level} {rb} {nl} ...``.

    Args:
        keys (List[str])
        nrange (Tuple[int, int])
        bullet_prob (float)

    Returns:
        str
    """
    templates = (
        "{blt} {{{keys}}}",
        "{blt} {{{keys}}} {{ws}} {{level}}",
        "{blt} {{{keys}}} {{lb}} {{level}} {{rb}}",
    )
    bullet = True if rnd.random() < bullet_prob else False
    template = rnd.choices(templates, weights=[1.0, 0.5, 0.5], k=1)[0]
    template_fmt = template.format(
        blt="" if bullet is False else "{bullet}",
        keys="|".join(keys),
    ).strip()
    return " {nl} ".join(template_fmt for _ in range(rnd.randint(*nrange)))


TEMPLATES = [
    lambda: " {nl} ".join(LINES["dev_mixes"]() for _ in range(rnd.randint(1, 4))),
    lambda: " {nl} ".join(LINES["dev_mixes_bulleted"]() for _ in range(rnd.randint(1, 4))),
    lambda: " {nl} ".join(LINES["dev_mixes_grped"]() for _ in range(rnd.randint(1, 4))),
    lambda: " {nl} ".join(LINES["dev_mixes_level"]() for _ in range(rnd.randint(1, 2))),
    lambda: " {nl} ".join(LINES["dev_mixes_level_grped"]() for _ in range(rnd.randint(1, 3))),
    lambda: " {nl} ".join(LINES[key]() for key in rnd.sample(["dev_mixes_grped", "plangs_grped", "dbs_grped", "langs_grped", "hobbies_grped"], rnd.randint(3, 4))),
    lambda: " {nl} ".join([LINES["plangs_bulleted"](), LINES["dbs_bulleted"](), LINES["dev_mixes_bulleted"]()]),
    lambda: " {nl} ".join([LINES["plangs_grped"](), LINES["dbs_grped"]()]),
    lambda: " {nl} ".join([LINES["langs_grped"](), LINES["plangs_grped"]()]),
    lambda: " {nl} ".join([LINES["grp_name_and_sep"](), LINES["dev_mixes"](), LINES["grp_name_and_sep"](), LINES["dev_mixes"]()]),
    lambda: " {nl} ".join(["{level} {grp_sep::0.5}", LINES["dev_mixes"](), "{level} {grp_sep::0.5}", LINES["dev_mixes"]()]),
    lambda: " {nl} ".join(" {nl} ".join("{dev_mix}" for _ in range(rnd.randint(3, 10))) for _ in range(rnd.randint(1, 2))),
    lambda: "{bullet::0.25} " + LINES["dev_mixes_level_grped"]() + " {grp_sep} " + LINES["dev_mixes_level_grped"](),
    lambda: "{bullet} " + LINES["dev_mixes_grped"]() + " {nl} ".join("{bullet} {sent}" for i in range(rnd.randint(1, 3))),
    lambda: generate_multiline_singletons(keys=["db", "dev_mix", "plang", "lang"], nrange=(3, 8), bullet_prob=0.25),
]
"""
List[Callable]: Collection of functions that generate random skills section templates,
by combining individual field generators defined in :obj:`FIELDS` plus line generators
defined in :obj:`LINES`.
"""
