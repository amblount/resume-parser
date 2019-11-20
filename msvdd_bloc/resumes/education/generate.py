import functools as fnc
import math
import random as rnd

import faker

from msvdd_bloc.resumes.education import constants as c
from msvdd_bloc.resumes import generate_utils


class Provider(generate_utils.ResumeProvider):
    """Class for providing randomly-generated field values."""

    _area_detail_templates = (
        "{subunit} {field_sep} {area_of_study}",
        "{area_of_study} {subunit}",
    )
    _city_state_templates = (
        "{city}, {state_abbr}",
        "{city}, {state}",
    )
    _course_templates = (
        "{subject}",
        "{prefix} {subject}",
        "{subject} {suffix}",
        "{subject} & {subject2}",
    )
    _date_approx_templates = (
        "{month} {year}",
        "{month_abbr} {year}",
        "{month_abbr}. {year}",
        "{season} {year}",
        "{year}",
    )
    _gpa_templates = (
        "{gpa:.{prec}f}",
        "{gpa:.{prec}f}{ws}/{ws}{max_gpa:.{prec}f}",
    )
    _school_templates = (
        "{school_name}",
        "{school_name} {field_sep_sm} {city_state}",
        "{school_name} {field_sep_dt} {city_state}",
    )
    _school_name_templates = (
        "{person_name} {school_type}",
        "{place_name} {school_type}",
    )
    _university_templates = (
        "{university_name}",
        "{university_name} {field_sep_sm} {city_state}",
        "{university_name} {field_sep_dt} {city_state}",
    )
    _university_name_templates = (
        "{person_name} {uni_type}",
        "{place_name} {uni_type}",
        "{uni_type} of {place_name}",
        "{uni_type} of {place_name_full}",
        "{uni_type} of {place_name}, {uni_subunit} of {area_of_study}",
    )
    _university_name_place_name_templates = (
        "{state}",
        "{city}",
        "{direction}{ern} {state}",
    )

    def area_of_study(self):
        return rnd.choice(c.AREAS_OF_STUDY)

    def area_detail(self):
        template = rnd.choices(self._area_detail_templates, weights=[1.0, 0.25], k=1)[0]
        return template.format(
            area_of_study=self.area_of_study(),
            field_sep=rnd.choice(c.FIELD_SEP_SMS + c.FIELD_SEP_PREPS + (":",)),
            subunit=rnd.choices(c.STUDY_SUBUNITS, weights=[1.0, 1.0, 0.1, 0.1], k=1)[0],
        )

    def city_state(self):
        template = rnd.choices(self._city_state_templates, weights=[1.0, 0.2], k=1)[0]
        return template.format(
            city=self.generator.city(),
            state=self.generator.state(),
            state_abbr=self.generator.state_abbr(),
        )

    def course_title(self):
        template = rnd.choices(
            self._course_templates, weights=[1.0, 0.5, 0.2, 0.1], k=1,
        )[0]
        # add a course code?
        if rnd.random() < 0.05:
            template += " ({dep_code} {num_code})".format(
                dep_code=self.generator.lexify("?" * rnd.randint(2, 4)).upper(),
                num_code=self.generator.numerify("#" * rnd.randint(2, 4)),
            )
        return template.format(
            prefix=rnd.choice(c.COURSE_PREFIXES),
            subject=rnd.choice(c.COURSE_SUBJECTS),
            subject2=rnd.choice(c.COURSE_SUBJECTS),
            suffix=rnd.choice(c.COURSE_SUFFIXES),
        )

    def date_approx(self):
        template = rnd.choices(
            self._date_approx_templates, weights=[1.0, 1.0, 0.25, 0.25, 0.25], k=1,
        )[0]
        month = self.generator.month_name()
        return template.format(
            month=month,
            month_abbr=month[:3],
            season=rnd.choice(c.SEASONS),
            year=self.generator.year(),
        )

    def field_sep(self):
        return self.generator.sep_with_ws(c.FIELD_SEPS, weights=None, ws_nrange=(1, 3))

    def field_sep_dt(self):
        return self.generator.sep_with_ws(
            c.FIELD_SEP_DTS, weights=[1.0, 0.5, 0.1], ws_nrange=(1, 2),
        )

    def field_sep_prep(self):
        return self.generator.sep_with_ws(
            c.FIELD_SEP_PREPS, weights=None, ws_nrange=(1, 2),
        )

    def field_sep_sm(self):
        return self.generator.sep_with_ws_right(
            c.FIELD_SEP_SMS, weights=[1.0, 0.5], ws_nrange=(1, 2),
        )

    def gpa(self):
        template = rnd.choices(self._gpa_templates, weights=[1.0, 0.5], k=1)[0]
        gpa, max_gpa = sorted(rnd.uniform(1.0, 4.0) for _ in range(2))
        return template.format(
            gpa=gpa,
            max_gpa=max_gpa,
            prec=rnd.randint(1, 2),
            ws=rnd.choice(["", " "]),
        )

    def item_sep(self):
        return self.generator.sep_with_ws_right(
            c.FIELD_SEP_SMS, weights=[1.0, 0.25], ws_nrange=(1, 2),
        )

    def label_courses(self):
        return self.generator.field_label(
            c.FIELD_LABEL_COURSES, c.FIELD_LABEL_SEPS,
            label_weights=None, sep_weights=[1.0, 0.2],
        )

    def label_grad_date(self):
        return self.generator.field_label(
            c.FIELD_LABEL_GRAD_DATES, c.FIELD_LABEL_SEPS,
            label_weights=None, sep_weights=[1.0, 0.2],
        )

    def label_gpa(self):
        return self.generator.field_label(
            c.FIELD_LABEL_GPAS, c.FIELD_LABEL_SEPS,
            label_weights=[1.0, 0.2, 0.2, 0.1], sep_weights=[1.0, 0.2],
        )

    def school(self):
        template = rnd.choices(self._school_templates, weights=[1.0, 0.5, 0.25], k=1)[0]
        return template.format(
            school_name=self.school_name(),
            field_sep_dt=self.field_sep_dt(),
            field_sep_sm=self.field_sep_sm(),
            city_state=self.city_state(),
        )

    def school_degree(self):
        return rnd.choice(c.SCHOOL_DEGREES)

    def school_name(self):
        template = rnd.choice(self._school_name_templates)
        return template.format(
            person_name=self.generator.last_name(),
            place_name=self.generator.city(),
            school_type=rnd.choice(c.SCHOOL_TYPES),
        )

    def university(self):
        template = rnd.choices(self._university_templates, weights=[1.0, 0.5, 0.25], k=1)[0]
        return template.format(
            university_name=self.university_name(),
            field_sep_dt=self.field_sep_dt(),
            field_sep_sm=self.field_sep_sm(),
            city_state=self.city_state(),
        )

    def university_degree(self):
        return rnd.choice(c.UNIVERSITY_DEGREES)

    def university_name(self):
        template = rnd.choices(
            self._university_name_templates,
            weights=[1.0, 1.0, 1.0, 0.5, 0.25],
            k=1,
        )[0]
        place_name_template = rnd.choices(
            self._university_name_place_name_templates,
            weights=[1.0, 1.0, 0.5],
            k=1,
        )[0]
        city = self.generator.city()
        state = self.generator.state()
        return template.format(
            area_of_study=self.area_of_study(),
            person_name=self.generator.last_name(),
            place_name=place_name_template.format(
                city=city,
                direction=rnd.choice(c.DIRECTIONS),
                ern="ern" if rnd.random() < 0.5 else "",
                state=state,
            ),
            place_name_full="{state}{sep}{city}".format(
                city=city,
                state=state,
                sep=rnd.choice([", ", " – ", "-", "–", " ", " at "]),
            ),
            uni_subunit=rnd.choice(c.UNIVERSITY_SUBUNITS),
            uni_type=rnd.choices(
                c.UNIVERSITY_TYPES,
                weights=[1.0, 1.0, 0.5, 0.5, 0.25, 0.25],
                k=1,
            )[0],
        )


FAKER = faker.Faker()
FAKER.add_provider(Provider)


FIELDS = {
    "area": (FAKER.area_of_study, "area"),
    "area_detail": (FAKER.area_detail, "area"),
    "bullet": (lambda: "- ", "bullet"),
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
    "isep": (FAKER.item_sep, "item_sep"),
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
    template = "{{label_courses::0.75}} {course_list}"
    minn, maxn = (3, 8)
    newline_idx = rnd.choices(
        range(maxn),
        weights=[math.pow(i / maxn, 2) for i in range(maxn)],
        k=1,
    )[0]
    return template.format(
        course_list=" {isep} ".join(
            "{course}" if i != newline_idx else "{nl} {course}"
            for i in range(rnd.randint(minn, maxn))),
    )


def generate_group_courses_block():
    """
    Generate a template for a logical group of course fields formatted as a sub-headered
    block, consisting of a header (label) and a variable number of course titles,
    either as an optionally bulletted list split over one or multiple lines.
    """
    templates = (
        "{{label_courses::0.9}} {{nl}} {{bullet::0.5}} {course_list}",
        "{{label_courses::0.9}} {{nl}} {course_lines}",
    )
    template = rnd.choices(templates, weights=[1.0, 0.5], k=1)[0]
    minn, maxn = (4, 10)
    newline_idx = rnd.choices(
        range(maxn),
        weights=[math.pow(i / maxn, 2) for i in range(maxn)],
        k=1,
    )[0]
    course_list_sep = rnd.choices([" {isep} ", " {ws} "], weights=[1.0, 0.2], k=1)[0]
    return template.format(
        course_lines=" {bullet} ".join("{course}" for _ in range(rnd.randint(3, 5))),
        course_list=course_list_sep.join(
            "{course}" if i != newline_idx else "{nl} {course}"
            for i in range(rnd.randint(minn, maxn))),
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
        "{deg_uni} {fsep_sm|fsep_prep|ws::0.5} {area} {fsep_sm:area} {area_detail}",
        "{deg_uni}",
    )
    return rnd.choices(templates, weights=[1.0, 0.5, 0.2], k=1)[0]


_EXPERIENCES = [
    lambda: "{uni} {nl}" + generate_group_study() + "{fsep_sm|ws|nl}" + generate_group_date(),
    lambda: "{uni} {fsep_sm|ws}" + generate_group_date() + "{nl}" + generate_group_study(),
    lambda: "{uni} {fsep_sm|ws}" + generate_group_date() + "{nl}" + generate_group_study() + "{nl}" + rnd.choice([generate_group_courses(), generate_group_courses_block()]),
    lambda: generate_group_study() + "{nl} {uni} {fsep_sm|ws|nl}" + generate_group_date(),
    lambda: (
        "{uni} {fsep_sm|ws}" + generate_group_date() +
        "{nl}" + generate_group_study() +
        "{nl|fsep_sm} {label_gpa::0.75} {gpa}"
    ),
    lambda: " {nl} {bullet} ".join(
        ["{uni}"] + rnd.sample(
            ["{label_gpa} {gpa}", "{area_detail}", generate_group_study(), generate_group_date(), generate_group_courses()],
            rnd.randint(2, 3)
        )
    ),
    lambda: " {nl} ".join(
        ["{uni}"] + rnd.sample(
            ["{label_gpa} {gpa}", "{area_detail}", generate_group_study(), generate_group_date(), generate_group_courses()],
            rnd.randint(2, 3)
        )
    ),
    lambda: " {nl} ".join(
        ["{uni}"] + rnd.sample(
            ["{label_gpa} {gpa}", generate_group_study(), generate_group_date()],
            rnd.randint(2, 3)
        ) + [generate_group_courses_block()]
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
