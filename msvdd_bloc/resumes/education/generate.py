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
    "item_sep": (FAKER.field_sep_sm, "item_sep"),
    "label_courses": (FAKER.label_courses, "field_label"),
    "label_gpa": (FAKER.label_gpa, "field_label"),
    "label_dt": (FAKER.label_grad_date, "field_label"),
    "lb": (lambda: "(", "field_sep"),
    "nl": (FAKER.newline, "field_sep"),
    "rb": (lambda: ")", "field_sep"),
    "school": (FAKER.school, "institution"),
    "uni": (FAKER.university, "institution"),
    "ws": (FAKER.whitespace, "field_sep"),
}
"""
Dict[str, Tuple[Callable, str]]: Mapping of field key string to a function that generates
a random field value and the default field label assigned to the value.
"""

def generate_group_courses():
    return "{label_courses::0.75}" + " {item_sep} ".join(
        "{course}" for _ in range(rnd.randint(3, 8))
    )


def generate_group_date():
    templates = (
        "{label_dt::0.4} {dt}",
        "{label_dt::0.1} {dt:start_dt} {fsep_dt} {dt|dt_now}",
        "{lb} {dt:start_dt} {fsep_dt} {dt|dt_now} {rb}",
    )
    return rnd.choices(templates, weights=[1.0, 0.5, 0.1], k=1)[0]


def generate_group_study():
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
    lambda: "{school} {fsep_sm|ws} {label_dt::0.5} {dt} {fsep_sm|nl|ws} {deg_school}",
]

TEMPLATES = [
    # 1 or 2 of the same experience
    lambda: " {nl} {nl} ".join(
        [rnd.choice(_EXPERIENCES)()] * rnd.choices([1, 2], weights=[1.0, 0.33], k=1)[0]
    ),
    # 1 or 2 of different experiences
    lambda: " {nl} {nl} ".join(
        exp()
        for exp in rnd.sample(_EXPERIENCES, rnd.choices([1, 2], weights=[1.0, 0.33], k=1)[0])
    ),
]
