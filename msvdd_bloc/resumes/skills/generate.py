import functools as fnc
import math
import random as rnd

import faker

from msvdd_bloc.resumes.skills import constants as c
from msvdd_bloc.resumes import generate_utils

###################################
## random field value generators ##

class Provider(generate_utils.ResumeProvider):
    """Class for providing randomly-generated field values."""

    def database(self):
        return rnd.choice(c.DATABASES)

    def dev_mix(self):
        return rnd.choice(c.DEV_MIX)

    def group_name(self):
        return rnd.choice(c.GROUP_NAMES)

    def group_sep(self):
        if rnd.random() < 0.75:
            return self.generator.sep_with_ws_right(
                c.GROUP_SEPS_WITH_WS_RIGHT,
                ws_nrange=(1, 5), ws_weights=(1.0, 0.8, 0.6, 0.4),
            )
        else:
            return self.generator.sep_with_ws(
                c.GROUP_SEPS_WITH_WS,
                ws_nrange=(1, 5), ws_weights=(1.0, 0.8, 0.6, 0.4),
            )

    def hobby(self):
        return rnd.choice(c.HOBBIES)

    def human_language(self):
        return rnd.choice(c.HUMAN_LANGUAGES)

    def item_sep(self):
        return self.generator.sep_with_ws_right(
            c.ITEM_SEPS, weights=[1.0, 0.2], ws_nrange=(1, 3),
        )

    def item_sep_and(self):
        return self.generator.and_rand(weights=[1.0, 0.2])

    def level(self):
        return rnd.choice(c.LEVELS)

    def level_prep(self):
        return self.generator.random_element_weighted(c.LEVEL_PREPS, [1.0, 0.4, 0.2, 0.1])

    def programming_language(self):
        return rnd.choice(c.PROGRAMMING_LANGUAGES)

    def software(self):
        return rnd.choice(c.SOFTWARE)


FAKER = faker.Faker()
FAKER.add_provider(Provider)


FIELDS = {
    "bullet": (FAKER.bullet_point, "field_sep"),
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
    "nl": (fnc.partial(FAKER.newline, nrange=(1, 3), weights=[1.0, 0.1]), "field_sep"),
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

######################################
## random field template generators ##


def _get_nl_idx(nl_nmax):
    if nl_nmax is not None:
        return rnd.choices(
            range(nl_nmax),
            weights=[math.pow(i / nl_nmax, 2) for i in range(nl_nmax)],
            k=1,
        )[0]
    else:
        return -1


def fields_list_template(key, *, nrange, nl_nmax=None, bullet=False):
    """
    Generate template for a list of fields, formatted as
    ``{bullet} {key} {isep} {key} {isep} {isep_and} {key}``.

    Args:
        key (str)
        nrange (Tuple[int, int])
        nl_nmax (int)
        bullet (bool)

    Returns:
        str
    """
    nl_idx = _get_nl_idx(nl_nmax)
    nmin, nmax = nrange
    return "{blt} {fields} {field_end}".format(
        blt="" if bullet is False else "{bullet}",
        fields=" {isep} ".join(
            "{nl}{{{key}}}".format(key=key, nl="" if i != nl_idx else "{nl:item_sep} ")
            for i in range(rnd.randrange(nmin - 1, nmax))
        ),
        field_end="{{isep}} {{isep_and::0.05}} {{{key}}}".format(key=key),
    ).strip()


def grped_fields_list_template(key, *, nrange, nl_nmax=None, bullet=False):
    """
    Generate line template for a list of fields with a group name, formatted as
    ``{grp_name} {grp_sep} {key:keyword} {isep} {key:keyword} {isep} {isep_and} {key:keyword}``.

    Args:
        key (str)
        nrange (Tuple[int, int])
        nl_nmax (int)
        bullet (bool)

    Returns:
        str
    """
    nl_idx = _get_nl_idx(nl_nmax)
    nmin, nmax = nrange
    return "{blt} {grp} {fields} {field_end}".format(
        blt="" if bullet is False else "{bullet}",
        grp="{grp_name} {grp_sep}",
        fields=" {isep} ".join(
            "{nl}{{{key}:keyword}}".format(key=key, nl="" if i != nl_idx else "{nl:item_sep} ")
            for i in range(rnd.randrange(nmin - 1, nmax))
        ),
        field_end="{{isep}} {{isep_and::0.05}} {{{key}:keyword}}".format(key=key),
    ).strip()


def fields_levels_list_template(key, *, nrange, nl_nmax=None, bullet=False):
    """
    Generate line template for a list of fields with individual levels, formatted as
    ``{key} {lb} {level} {rb} {isep} {key} {lb} {level} {rb} {isep} {isep_and} {key} {lb} {level} {rb}``.

    Args:
        key (str)
        nrange (Tuple[int, int])
        nl_nmax (int)
        bullet (bool)

    Returns:
        str
    """
    nl_idx = _get_nl_idx(nl_nmax)
    nmin, nmax = nrange
    return "{blt} {fields} {field_end}".format(
        blt="" if bullet is False else "{bullet}",
        fields=" {isep} ".join(
            "{nl}{{{key}}} {{lb}} {{level}} {{rb}}".format(key=key, nl="" if i != nl_idx else "{nl:item_sep} ")
            for i in range(rnd.randrange(nmin - 1, nmax))
        ),
        field_end="{{isep}} {{isep_and::0.05}} {{{key}}} {{lb}} {{level}} {{rb}}".format(key=key),
    ).strip()


def grped_fields_levels_list_template(key, *, nrange, nl_nmax=None, bullet=False):
    """
    Generate line template for a list of fields with a group-wide level, formatted as
    ``{level} {level_prep} {grp_sep} {key} {isep} {key} {isep} {isep_and} {key}``.

    Args:
        key (str)
        nrange (Tuple[int, int])
        nl_nmax (int)
        bullet (bool)

    Returns:
        str
    """
    nl_idx = _get_nl_idx(nl_nmax)
    nmin, nmax = nrange
    return "{blt} {lvl} {fields} {field_end}".format(
        blt="" if bullet is False else "{bullet}",
        lvl="{level} {level_prep::0.5} {grp_sep::0.25}",
        fields=" {isep} ".join(
            "{nl}{{{key}}}".format(key=key, nl="" if i != nl_idx else "{nl:item_sep} ")
            for i in range(rnd.randrange(nmin - 1, nmax))
        ),
        field_end="{{isep}} {{isep_and::0.05}} {{{key}}}".format(key=key),
    ).strip()


LINES = {
    "grp_name_and_sep": lambda: "{grp_name} {grp_sep}",
    "dev_mixes": fnc.partial(fields_list_template, "dev_mix", nrange=(3, 10), nl_nmax=12),
    "dev_mixes_bulleted": fnc.partial(fields_list_template, "dev_mix", nrange=(3, 10), nl_nmax=12, bullet=True),
    "dev_mixes_grped": fnc.partial(grped_fields_list_template, "dev_mix", nrange=(3, 10), nl_nmax=12),
    "dev_mixes_level": fnc.partial(fields_levels_list_template, "dev_mix", nrange=(3, 10), nl_nmax=12),
    "dev_mixes_level_grped": fnc.partial(grped_fields_levels_list_template, "dev_mix", nrange=(3, 10), nl_nmax=12),
    "plangs": fnc.partial(fields_list_template, "plang", nrange=(3, 8)),
    "plangs_bulleted": fnc.partial(fields_list_template, "plang", nrange=(3, 8), bullet=True),
    "plangs_grped": fnc.partial(grped_fields_list_template, "plang", nrange=(3, 8)),
    "dbs": fnc.partial(fields_list_template, "db", nrange=(3, 6)),
    "dbs_bulleted": fnc.partial(fields_list_template, "db", nrange=(3, 6), bullet=True),
    "dbs_grped": fnc.partial(grped_fields_list_template, "db", nrange=(3, 6)),
    "langs": fnc.partial(fields_list_template, "lang", nrange=(2, 4)),
    "langs_bulleted": fnc.partial(fields_list_template, "lang", nrange=(2, 4), bullet=True),
    "langs_grped": fnc.partial(grped_fields_list_template, "lang", nrange=(2, 4)),
    "langs_level": fnc.partial(fields_levels_list_template, "lang", nrange=(2, 4)),
    "hobbies": fnc.partial(fields_list_template, "hobby", nrange=(2, 6)),
    "hobbies_grped": fnc.partial(grped_fields_list_template, "hobby", nrange=(2, 6)),
}
"""
Dict[str, Callable]: Intermediate mapping of line type name to a function that generates
a random corresponding value.
"""


def singleton_line_list_template(keys, *, nrange, bullet_prob=0.25):
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
        "{blt} {{{keys}}} {{grp_sep|ws}} {{level}}",
        "{blt} {{{keys}}} {{lb}} {{level}} {{rb}}",
    )
    bullet = "{bullet}" if rnd.random() < bullet_prob else ""
    template = rnd.choices(templates, weights=[1.0, 0.5, 0.5], k=1)[0]
    template_fmt = template.format(blt=bullet, keys="|".join(keys)).strip()
    return " {nl} ".join(template_fmt for _ in range(rnd.randrange(*nrange)))


TEMPLATES = [
    lambda: " {nl} ".join(LINES["dev_mixes"]() for _ in range(rnd.randrange(1, 5))),
    lambda: " {nl} ".join(LINES["dev_mixes_bulleted"]() for _ in range(rnd.randrange(1, 5))),
    lambda: " {nl} ".join(LINES["dev_mixes_grped"]() for _ in range(rnd.randrange(1, 5))),
    lambda: " {nl} ".join(LINES["dev_mixes_level"]() for _ in range(rnd.randrange(1, 3))),
    lambda: " {nl} ".join(LINES["dev_mixes_level_grped"]() for _ in range(rnd.randrange(1, 4))),
    lambda: " {nl} ".join(LINES[key]() for key in rnd.sample(["dev_mixes_grped", "plangs_grped", "dbs_grped", "langs_grped", "hobbies_grped"], rnd.randrange(3, 5))),
    lambda: " {nl} ".join([LINES["plangs_bulleted"](), LINES["dbs_bulleted"](), LINES["dev_mixes_bulleted"]()]),
    lambda: " {nl} ".join([LINES["plangs_grped"](), LINES["dbs_grped"]()]),
    lambda: " {nl} ".join([LINES["langs_grped"](), LINES["plangs_grped"]()]),
    lambda: " {nl} ".join([LINES["grp_name_and_sep"](), LINES["dev_mixes"](), LINES["grp_name_and_sep"](), LINES["dev_mixes"]()]),
    lambda: " {nl} ".join(["{level} {grp_sep::0.5}", LINES["dev_mixes"](), "{level} {grp_sep::0.5}", LINES["dev_mixes"]()]),
    lambda: " {nl} ".join(" {nl} ".join("{dev_mix}" for _ in range(rnd.randrange(3, 10))) for _ in range(rnd.randrange(1, 3))),
    lambda: "{bullet} " + LINES["dev_mixes_grped"]() + " {nl} " + " {nl} ".join("{bullet} {sent}" for i in range(rnd.randrange(1, 4))),
    lambda: singleton_line_list_template(["db", "dev_mix", "plang", "lang"], nrange=(3, 8), bullet_prob=0.25),
    # NOTE: this next one is weird ... and there's currently no logic to parse it
    # lambda: "{bullet::0.25} " + LINES["dev_mixes_level_grped"]() + " {grp_sep} " + LINES["dev_mixes_level_grped"](),
]
"""
List[Callable]: Collection of functions that generate random skills section templates,
by combining individual field generators defined in :obj:`FIELDS` plus line generators
defined in :obj:`LINES`.
"""
