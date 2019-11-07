import random as rnd

from msvdd_bloc.resumes.generate_utils import FAKER


_SKILL_GROUP_SEPS = (":", "-", "")
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


def generate_field_and():
    return rnd.choices(["and", "&"], weights=[1.0, 0.2], k=1)[0]


def generate_field_bracket_left():
    return "("


def generate_field_bracket_right():
    return ")"


def generate_field_database():
    return rnd.choice(_DATABASES)


def generate_field_dev_mix():
    return rnd.choice(_DEV_MIX)


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


def generate_field_skill_group_sep():
    return "{ws1}{sep}".format(
        ws1="" if rnd.random() < 0.9 else " ",
        sep=rnd.choices(_SKILL_GROUP_SEPS, weights=[1.0, 0.5, 0.1], k=1)[0],
    )


def generate_field_software():
    return rnd.choice(_SOFTWARE)


def generate_field_whitespace():
    return " " * rnd.randint(0, 3)


FIELDS = {
    "and": (generate_field_and, "item_sep"),
    "bullet": (lambda : "- ", "bullet"),
    "db": (generate_field_database, "name"),
    "dev_mix": (generate_field_dev_mix, "name"),
    "in": (generate_field_level_prep, "field_sep"),
    "is": (generate_field_item_sep, "item_sep"),
    "grp_name": (generate_field_skill_group_name, "name"),
    "grp_name_sep": (generate_field_skill_group_sep, "field_sep"),
    "hobby": (generate_field_hobby, "other"),
    "lang": (generate_field_human_language, "name"),  # TODO: should this be "other"?
    "level": (generate_field_level, "level"),
    "lb": (generate_field_bracket_left, "field_sep"),
    "nl": (generate_field_newline, "field_sep"),
    "plang": (generate_field_programming_language, "name"),
    "rb": (generate_field_bracket_right, "field_sep"),
    "sent": (generate_field_sentence, "other"),
    "sw": (generate_field_software, "name"),
    "ws": (generate_field_whitespace, "field_sep"),
}
"""
Dict[str, Tuple[Callable, str]]: Mapping of field key string to a function that generates
a random field value and the default field label assigned to the value.
"""

_LNTMPLTS = {
    "grp_name_and_sep": lambda: "{grp_name} {grp_name_sep}",
    "dev_mixes": lambda: " {is} ".join("{dev_mix}" for _ in range(rnd.randint(3, 9))) + " {is} {and::0.1} {dev_mix}",
    "dev_mixes_bulleted": lambda: "{bullet} " + " {is} ".join("{dev_mix}" for _ in range(rnd.randint(3, 9))) + " {is} {and::0.1} {dev_mix}",
    "dev_mixes_grped": lambda: "{grp_name} {grp_name_sep} {ws} " + " {is} ".join("{dev_mix:keyword}" for _ in range(rnd.randint(3, 9))) + " {is} {and::0.1} {dev_mix:keyword}",
    "dev_mixes_kw": lambda: " {is} ".join("{dev_mix:keyword}" for _ in range(rnd.randint(3, 10))),
    "dev_mixes_level": lambda: " {is} ".join("{dev_mix} {lb} {level} {rb}" for _ in range(rnd.randint(3, 8))),
    "dev_mixes_level_grped": lambda: "{level} {in::0.5} {grp_name_sep::0.25}" + " {is} ".join("{dev_mix}" for _ in range(rnd.randint(3, 8))),
    "plangs": lambda: " {is} ".join("{plang}" for _ in range(rnd.randint(3, 8))),
    "plangs_bulleted": lambda: "{bullet} " + " {is} ".join("{plang}" for _ in range(rnd.randint(3, 8))),
    "plangs_grped": lambda: "{grp_name} {grp_name_sep} {ws} " + " {is} ".join("{plang:keyword}" for _ in range(rnd.randint(3, 8))),
    "plangs_kw": lambda: " {is} ".join("{plang:keyword}" for _ in range(rnd.randint(3, 8))),
    "dbs": lambda: " {is} ".join("{db}" for _ in range(rnd.randint(3, 6))),
    "dbs_bulleted": lambda: "{bullet} " + " {is} ".join("{db}" for _ in range(rnd.randint(3, 6))),
    "dbs_grped": lambda: "{grp_name} {grp_name_sep} {ws} " + " {is} ".join("{db:keyword}" for _ in range(rnd.randint(3, 6))),
    "dbs_kw": lambda: " {is} ".join("{db:keyword}" for _ in range(rnd.randint(3, 6))),
    "langs": lambda: " {is} ".join("{lang}" for _ in range(rnd.randint(2, 4))),
    "langs_bulleted": lambda: "{bullet} " + " {is} ".join("{lang}" for _ in range(rnd.randint(2, 4))),
    "langs_grped": lambda: "{grp_name} {grp_name_sep} {ws} " + " {is} ".join("{lang:keyword}" for _ in range(rnd.randint(2, 4))),
    "langs_kw": lambda: " {is} ".join("{lang:keyword}" for _ in range(rnd.randint(2, 4))),
}

TEMPLATES = [
    lambda: " {nl} ".join(_LNTMPLTS["dev_mixes"]() for _ in range(rnd.randint(1, 4))),
    lambda: " {nl} ".join(_LNTMPLTS["dev_mixes_bulleted"]() for _ in range(rnd.randint(1, 4))),
    lambda: " {nl} ".join(_LNTMPLTS["dev_mixes_grped"]() for _ in range(rnd.randint(1, 4))),
    lambda: " {nl} ".join(_LNTMPLTS["dev_mixes_level"]() for _ in range(rnd.randint(1, 2))),
    lambda: " {nl} ".join(_LNTMPLTS["dev_mixes_level_grped"]() for _ in range(rnd.randint(1, 3))),
    lambda: " {nl} ".join([_LNTMPLTS["plangs_bulleted"](), _LNTMPLTS["dbs_bulleted"](), _LNTMPLTS["dev_mixes_bulleted"]()]),
    lambda: " {nl} ".join([_LNTMPLTS["plangs_grped"](), _LNTMPLTS["dbs_grped"]()]),
    lambda: " {nl} ".join([_LNTMPLTS["grp_name_and_sep"](), _LNTMPLTS["dev_mixes"](), _LNTMPLTS["grp_name_and_sep"](), _LNTMPLTS["dev_mixes"]()]),
    lambda: " {nl} ".join(" {nl} ".join("{dev_mix}" for _ in range(rnd.randint(3, 10))) for _ in range(rnd.randint(1, 2))),
    lambda: "{bullet::0.25} " + _LNTMPLTS["dev_mixes_level_grped"]() + " {grp_name_sep} " + _LNTMPLTS["dev_mixes_level_grped"](),
    lambda: "{bullet} " + _LNTMPLTS["dev_mixes_grped"]() + " {nl} ".join("{bullet} {sent}" for i in range(rnd.randint(1, 3))),
]
