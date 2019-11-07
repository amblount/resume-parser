import functools as fnc
import random as rnd

from msvdd_bloc.resumes.generate_utils import FAKER


_GROUP_SEPS = (":", "-", "")
_ITEM_SEPS = (",", ";")
_PROFICIENCY_LEVEL_PREPS = ("in", "with", "to", "of")

_LEVELS = (
    "advanced", "intermediate", "beginner",
    "experienced", "proficient", "exposed", "exposure",
    "basic", "familiar", "fluent", "native",
)
_SKILL_GROUP_NAMES = (
    "Programming Languages", "Languages", "Programming",
    "Web Frameworks", "Web Frameworks/Tools", "Tools",
    "Frameworks and Tools", "Tools & Frameworks", "Frameworks & Tools",
    "Software", "Databases", "Technologies",
    "Technical Skills", "Domain Knowledge",
    "Interests", "Hobbies",
)

_PROGRAMMING_LANGUAGES = (
    "Java", "Python", "C", "C++", "C/C++", "C#", "Objective-C", "Objective C",
    "SQL", "Ruby", "MATLAB", "Go", "Swift", "Perl", "R", "Visual Basic", "Scala", "PHP",
    "HTML", "HTML5", "CSS", "HTML/CSS", "JavaScript", "TypeScript", "Groovy",
    "Processing", "Sass", "OCaml",
)
_DATABASES = (
    "PostgreSQL", "Postgres", "MongoDB", "Mongo DB",
    "Redshift", "MySQL", "SQLite", "NoSQL", "GraphQL",
    "SQLAlchemy", "DynamoDB", "Elasticsearch",
)

_DEV_BE = (
    "Airflow", "Bash", "Docker", "Kafka", "Apache Kafka", "Chef", "Kubernetes", "Hadoop",
    "Kibana", "Data Structures", "Data Architecture",
)
_DEV_DS = (
    "TensorFlow", "OpenCV", "PyTorch", "ArcGIS", "Spark", "PyData",
    "Machine Learning", "Supervised Machine Learning", "Unsupervised Machine Learning",
    "Deep Learning", "Big Data", "Forecasting", "Web Analytics",
    "Time Series Analysis", "TSA", "Natural Language Processing", "NLP",
    "Network Analysis", "Algorithms", "Data Analysis", "Data Pipelines",
)
_DEV_FE = (
    "React", "ReactJS", "React Native", "Node.js", "Node JS", "Angular", "Angular JS",
    "Express JS", "jQuery", "LESS", "AJAX", "Electron", "Selenium",
    "Rest APIs", "CRUD", "Ruby on Rails", "Django", "Flask",
)
_DEV_TECHNIQUES = (
    "agile development", "parallel programming", "networking", "web development",
    "unit testing", "cyber security", "SEO",
)
_DEV_TOOLS = (
    "Git", "GitHub", "Version Control",
    "Sublime", "Atom", "VS Code", "Eclipse", "IDE", "Shell", "Terminal",
    "IPython Notebooks", "Jupyter Notebooks", "RStudio",
    "LaTeX", "Markdown", "JSON", "XML",
    "AWS", "WordPress", "Heroku", "Jenkins", "VMWare", "Google Cloud",
)
_DEV_MIX = (
    _DEV_BE + _DEV_DS + _DEV_FE
    + _DEV_TECHNIQUES + _DEV_TOOLS
    + _DATABASES + _PROGRAMMING_LANGUAGES
)

_SOFTWARE = (
    "Linux", "Unix", "Windows", "Mac OS", "macOS", "Android", "iOS", "Arduino",
    "Adobe Photoshop", "Adobe Illustrator", "Adobe InDesign", "Autodesk Maya",
    "Microsoft Office", "Microsoft Word", "Microsoft Excel",
    "JIRA", "Trello", "Asana",
)
_HUMAN_LANGUAGES = (
    "English", "Spanish", "French", "German", "Chinese", "Japanese", "Dutch",
)
_HOBBIES = (
    "Bowling", "Karaoke", "Kayaking", "Swimming", "Fishing", "Rock Climbing",
)

#############################
## random field generators ##
#############################

def generate_field_and():
    return rnd.choices(["and", "&"], weights=[1.0, 0.2], k=1)[0]


def generate_field_database():
    return rnd.choice(_DATABASES)


def generate_field_dev_mix():
    return rnd.choice(_DEV_MIX)


def generate_field_group_sep():
    return "{ws1}{sep}".format(
        ws1="" if rnd.random() < 0.9 else " ",
        sep=rnd.choices(_GROUP_SEPS, weights=[1.0, 0.5, 0.1], k=1)[0],
    )


def generate_field_hobby():
    return rnd.choice(_HOBBIES)


def generate_field_human_language():
    return rnd.choice(_HUMAN_LANGUAGES)


def generate_field_item_sep():
    return "{sep}{ws}".format(
        sep=rnd.choices(_ITEM_SEPS, weights=[1.0, 0.2], k=1)[0],
        ws=" " * rnd.randint(1, 2),
    )


def generate_field_newline():
    if rnd.random() < 0.8:
        return "\n"
    else:
        return "\n\n"


def generate_field_level():
    return rnd.choice(_LEVELS)


def generate_field_level_prep():
    return rnd.choices(_PROFICIENCY_LEVEL_PREPS, weights=[1.0, 0.4, 0.2, 0.1], k=1)[0]


def generate_field_programming_language():
    return rnd.choice(_PROGRAMMING_LANGUAGES)


def generate_field_sentence():
    return FAKER.sentence(nb_words=rnd.randint(5, 15))


def generate_field_skill_group_name():
    return rnd.choice(_SKILL_GROUP_NAMES)


def generate_field_software():
    return rnd.choice(_SOFTWARE)


def generate_field_whitespace():
    return " " * rnd.randint(0, 3)


FIELDS = {
    "and": (generate_field_and, "item_sep"),
    "bullet": (lambda : "- ", "bullet"),
    "db": (generate_field_database, "name"),
    "dev_mix": (generate_field_dev_mix, "name"),
    "is": (generate_field_item_sep, "item_sep"),
    "grp_name": (generate_field_skill_group_name, "name"),
    "grp_sep": (generate_field_group_sep, "field_sep"),
    "hobby": (generate_field_hobby, "other"),
    "lang": (generate_field_human_language, "name"),  # TODO: should this be "other"?
    "level": (generate_field_level, "level"),
    "level_prep": (generate_field_level_prep, "field_sep"),
    "lb": (lambda: "(", "field_sep"),
    "nl": (generate_field_newline, "field_sep"),
    "plang": (generate_field_programming_language, "name"),
    "rb": (lambda: ")", "field_sep"),
    "sent": (generate_field_sentence, "other"),
    "sw": (generate_field_software, "name"),
    "ws": (generate_field_whitespace, "field_sep"),
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
    ``{key} {is} {key} {is} {and::0.1} {key}``.

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
        fields=" {is} ".join(
            "{{{key}}}".format(key=key)
            for _ in range(rnd.randint(nmin - 1, nmax - 1))
        ),
        field_end="{{is}} {{and::0.1}} {{{key}}}".format(key=key),
    ).strip()


def generate_line_fields_grped(*, key, nrange, bullet=False):
    """
    Generate line template for a list of fields with a group name, formatted as
    ``{grp_name} {grp_sep} {ws} {key:keyword} {is} {key:keyword} {is} {and::0.1} {key:keyword}``.

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
        fields=" {is} ".join(
            "{{{key}:keyword}}".format(key=key)
            for _ in range(rnd.randint(nmin - 1, nmax - 1))
        ),
        field_end="{{is}} {{and::0.1}} {{{key}:keyword}}".format(key=key),
    ).strip()


def generate_line_fields_levels(*, key, nrange, bullet=False):
    """
    Generate line template for a list of fields with individual levels, formatted as
    ``{key} {lb} {level} {rb} {is} {key} {lb} {level} {rb} {is} {and::0.1} {key} {lb} {level} {rb}``.

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
        fields=" {is} ".join(
            "{{{key}}} {{lb}} {{level}} {{rb}}".format(key=key)
            for _ in range(rnd.randint(nmin - 1, nmax - 1))
        ),
        field_end="{{is}} {{and::0.1}} {{{key}}} {{lb}} {{level}} {{rb}}".format(key=key),
    ).strip()


def generate_line_fields_level_grped(*, key, nrange, bullet=False):
    """
    Generate line template for a list of fields with a group-wide level, formatted as
    ``{level} {level_prep::0.5} {grp_sep::0.25} {key} {is} {key} {is} {and::0.1} {key}``.

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
        fields=" {is} ".join(
            "{{{key}}}".format(key=key)
            for _ in range(rnd.randint(nmin - 1, nmax - 1))
        ),
        field_end="{{is}} {{and::0.1}} {{{key}}}".format(key=key),
    ).strip()


_LINES = {
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
}


TEMPLATES = [
    lambda: " {nl} ".join(_LINES["dev_mixes"]() for _ in range(rnd.randint(1, 4))),
    lambda: " {nl} ".join(_LINES["dev_mixes_bulleted"]() for _ in range(rnd.randint(1, 4))),
    lambda: " {nl} ".join(_LINES["dev_mixes_grped"]() for _ in range(rnd.randint(1, 4))),
    lambda: " {nl} ".join(_LINES["dev_mixes_level"]() for _ in range(rnd.randint(1, 2))),
    lambda: " {nl} ".join(_LINES["dev_mixes_level_grped"]() for _ in range(rnd.randint(1, 3))),
    lambda: " {nl} ".join([_LINES["plangs_bulleted"](), _LINES["dbs_bulleted"](), _LINES["dev_mixes_bulleted"]()]),
    lambda: " {nl} ".join([_LINES["plangs_grped"](), _LINES["dbs_grped"]()]),
    lambda: " {nl} ".join([_LINES["langs_grped"](), _LINES["plangs_grped"]()]),
    lambda: " {nl} ".join([_LINES["grp_name_and_sep"](), _LINES["dev_mixes"](), _LINES["grp_name_and_sep"](), _LINES["dev_mixes"]()]),
    lambda: " {nl} ".join(["{level} {grp_sep::0.5}", _LINES["dev_mixes"](), "{level} {grp_sep::0.5}", _LINES["dev_mixes"]()]),
    lambda: " {nl} ".join(" {nl} ".join("{dev_mix}" for _ in range(rnd.randint(3, 10))) for _ in range(rnd.randint(1, 2))),
    lambda: "{bullet::0.25} " + _LINES["dev_mixes_level_grped"]() + " {grp_sep} " + _LINES["dev_mixes_level_grped"](),
    lambda: "{bullet} " + _LINES["dev_mixes_grped"]() + " {nl} ".join("{bullet} {sent}" for i in range(rnd.randint(1, 3))),
]
