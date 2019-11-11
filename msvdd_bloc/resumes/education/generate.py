import functools as fnc
import random as rnd

import faker

from msvdd_bloc.providers import resume_education
from msvdd_bloc.resumes import noise_utils


FAKER = faker.Faker()
FAKER.add_provider(resume_education.Provider)


FIELDS = {
    "area": (FAKER.area_of_study, "area"),
    "area_minor": (FAKER.area_minor, "area"),
    "bullet": (lambda: "- ", "other"),  # TODO: should it be other, or bullet?
    "city_state": (FAKER.city_state, "institution"),
    "course": (FAKER.course_title, "course"),
    "deg_school": (FAKER.school_degree, "study_type"),
    "deg_uni": (FAKER.university_degree, "study_type"),
    "dt": (FAKER.date_approx, "end_date"),
    "dt_now": (FAKER.date_present, "end_date"),
    "fsep": (FAKER.field_sep, "field_sep"),
    "fsep_dt": (FAKER.field_sep_dt, "field_sep"),
    "fsep_prep": (FAKER.field_sep_prep, "field_sep"),
    "fsep_sm": (FAKER.field_sep_sm, "field_sep"),
    "gpa": (FAKER.gpa, "gpa"),
    "item_sep": (FAKER.item_sep, "item_sep"),
    "label_courses": (FAKER.label_courses, "field_label"),
    "label_gpa": (FAKER.label_gpa, "field_label"),
    "label_dt": (FAKER.label_grad_date, "field_label"),
    "lb": (FAKER.left_bracket, "field_sep"),
    "nl": (FAKER.newline, "field_sep"),
    "rb": (FAKER.right_bracket, "field_sep"),
    "school": (FAKER.school, "institution"),
    "uni": (FAKER.university, "institution"),
    "ws": (FAKER.whitespace, "field_sep"),
}
"""
Dict[str, Tuple[Callable, str]]: Mapping of field key string to a function that generates
a random field value and the default field label assigned to the value.
"""

#############################
## random group generators ##
#############################

def generate_group_courses():
    """
    Generate a template for a logical group of course fields, consisting of a label and
    a variable number of course titles separated by appropriate punctuation,
    possibly split over two lines.
    """
    templates = (
        "{{label_courses::0.75}} {courses}",
        "{{label_courses::0.75}} {courses} {{nl}} {courses2}",
    )
    template = rnd.choices(templates, weights=[1.0, 0.25], k=1)[0]
    return template.format(
        courses=" {item_sep} ".join("{course}" for _ in range(rnd.randint(3, 5))),
        courses2=" {item_sep} ".join("{course}" for _ in range(rnd.randint(1, 3))),
    )


def generate_group_date():
    """
    Generate a template for a logical group of date fields, consisting of an end date,
    possibly preceded by a label and/or a start date.
    """
    templates = (
        "{label_dt::0.4} {dt}",
        "{label_dt::0.1} {dt:start_dt} {fsep_dt} {dt|dt_now}",
        "{lb} {dt:start_dt} {fsep_dt} {dt|dt_now} {rb}",
    )
    return rnd.choices(templates, weights=[1.0, 0.5, 0.1], k=1)[0]


def generate_group_study():
    """
    Generate a template for a logical group of study fields, consisting of a degree,
    a primary area of study, and possibly a secondary area of study.
    """
    templates = (
        "{deg_uni} {fsep_sm|fsep_prep|ws::0.5} {area}",
        "{deg_uni} {fsep_sm|fsep_prep|ws::0.5} {area} {fsep_sm:area} {area_minor}",
        "{deg_uni}",
    )
    return rnd.choices(templates, weights=[1.0, 0.5, 0.2], k=1)[0]


_EXPERIENCES = [
    lambda: "{uni} {nl}" + generate_group_study() + "{fsep_sm|ws|nl}" + generate_group_date(),
    lambda: "{uni} {fsep_sm|ws}" + generate_group_date() + "{nl}" + generate_group_study(),
    lambda: generate_group_study() + "{nl} {uni} {fsep_sm|ws|nl}" + generate_group_date(),
    lambda: (
        "{uni} {fsep_sm|ws}" + generate_group_date() +
        "{nl}" + generate_group_study() +
        "{nl|fsep_sm} {label_gpa::0.75} {gpa}"
    ),
    lambda: " {nl} {bullet} ".join(
        ["{uni}"] + rnd.sample(
            ["{label_gpa} {gpa}", "{area_minor}", generate_group_study(), generate_group_date(), generate_group_courses()],
            rnd.randint(2, 3)
        )
    ),
    lambda: " {nl} ".join(
        ["{uni}"] + rnd.sample(
            ["{label_gpa} {gpa}", "{area_minor}", generate_group_study(), generate_group_date(), generate_group_courses()],
            rnd.randint(2, 3)
        )
    ),
    lambda: "{school} {fsep_sm|ws} {label_dt::0.5} {dt} {fsep_sm|nl|ws} {deg_school}",
]
"""
List[Callable]: Set of functions that generate a single educational experience,
in a variety of formats and with a variety of constituent fields.
"""


TEMPLATES = [
    # 1 or 2 of the same experience
    lambda: " {nl} {nl} ".join(
        exp()
        for exp in [rnd.choice(_EXPERIENCES)] * rnd.choices([1, 2], weights=[1.0, 0.33], k=1)[0]
    ),
    # 1 or 2 of different experiences
    lambda: " {nl} {nl} ".join(
        exp()
        for exp in rnd.sample(_EXPERIENCES, rnd.choices([1, 2], weights=[1.0, 0.33], k=1)[0])
    ),
]
"""
List[Callable]: Set of functions that generate one or 2 educational experiences, either
of the same type or of different types, separated by newlines.
"""
