import functools as fnc
import math
import random as rnd

import faker

from msvdd_bloc.resumes.education import constants as c
from msvdd_bloc.resumes import generate_utils

###################################
## random field value generators ##

class Provider(generate_utils.ResumeProvider):
    """Class for providing randomly-generated field values."""

    _area_detail_templates = (
        ("{subunit} {field_sep} {area_of_study}", 1.0),
        ("{area_of_study} {subunit}", 0.25),
    )
    _city_state_templates = (
        ("{city}, {state_abbr}", 1.0),
        ("{city}, {state}", 0.2),
    )
    _course_templates = (
        ("{subject}", 1.0),
        ("{prefix} {subject}", 0.5),
        ("{subject} {suffix}", 0.2),
        ("{subject} & {subject2}", 0.1),
    )
    _date_approx_templates = (
        ("{month} {year}", 1.0),
        ("{month_abbr} {year}", 1.0),
        ("{month_abbr}. {year}", 0.25),
        ("{season} {year}", 0.25),
        ("{year}", 0.25),
    )
    _gpa_templates = (
        ("{gpa:.{prec}f}", 1.0),
        ("{gpa:.{prec}f}{ws}/{ws}{max_gpa:.{prec}f}", 0.5),
    )
    _school_templates = (
        ("{school_name}", 1.0),
        ("{school_name} {field_sep_sm} {city_state}", 0.5),
        ("{school_name} {field_sep_dt} {city_state}", 0.25),
    )
    _school_name_templates = (
        "{person_name} {school_type}",
        "{place_name} {school_type}",
    )
    _university_templates = (
        ("{university_name}", 1.0),
        ("{university_name} {field_sep_sm} {city_state}", 0.5),
        ("{university_name} {field_sep_dt} {city_state}", 0.25),
    )
    _university_name_templates = (
        ("{person_name} {uni_type}", 1.0),
        ("{place_name} {uni_type}", 1.0),
        ("{uni_type} of {place_name}", 1.0),
        ("{uni_type} of {place_name_full}", 0.5),
        ("{uni_type} of {place_name}, {uni_subunit} of {area_of_study}", 0.25),
    )
    _university_name_place_name_templates = (
        ("{state}", 1.0),
        ("{city}", 1.0),
        ("{direction}{ern} {state}", 0.5),
    )

    def area_of_study(self):
        return rnd.choice(c.AREAS_OF_STUDY)

    def area_detail(self):
        template = self.generator.random_template_weighted(self._area_detail_templates)
        return template.format(
            area_of_study=self.area_of_study(),
            field_sep=rnd.choice(c.FIELD_SEP_SMS + c.FIELD_SEP_PREPS + (":",)),
            subunit=rnd.choices(c.STUDY_SUBUNITS, weights=[1.0, 1.0, 0.1, 0.1], k=1)[0],
        )

    def city_state(self):
        template = self.generator.random_template_weighted(self._city_state_templates)
        return template.format(
            city=self.generator.city(),
            state=self.generator.state(),
            state_abbr=self.generator.state_abbr(),
        )

    def course_title(self):
        template = self.generator.random_template_weighted(self._course_templates)
        # add a course code?
        if rnd.random() < 0.05:
            template += " ({dep_code} {num_code})".format(
                dep_code=self.generator.lexify("?" * rnd.randrange(2, 5)).upper(),
                num_code=self.generator.numerify("#" * rnd.randrange(2, 5)),
            )
        return template.format(
            prefix=rnd.choice(c.COURSE_PREFIXES),
            subject=rnd.choice(c.COURSE_SUBJECTS),
            subject2=rnd.choice(c.COURSE_SUBJECTS),
            suffix=rnd.choice(c.COURSE_SUFFIXES),
        )

    def date_approx(self):
        template = self.generator.random_template_weighted(self._date_approx_templates)
        month = self.generator.month_name()
        return template.format(
            month=month,
            month_abbr=month[:3],
            season=rnd.choice(c.SEASONS),
            year=self.generator.year(),
        )

    def field_sep(self):
        return self.generator.sep_with_ws(c.FIELD_SEPS, weights=None, ws_nrange=(1, 4))

    def field_sep_dt(self):
        return self.generator.sep_with_ws(
            c.FIELD_SEP_DTS, weights=[1.0, 0.5, 0.1], ws_nrange=(1, 3),
        )

    def field_sep_prep(self):
        return self.generator.sep_with_ws(
            c.FIELD_SEP_PREPS, weights=None, ws_nrange=(1, 3),
        )

    def field_sep_sm(self):
        return self.generator.sep_with_ws_right(
            c.FIELD_SEP_SMS, weights=[1.0, 0.5], ws_nrange=(1, 3),
        )

    def gpa(self):
        template = self.generator.random_template_weighted(self._gpa_templates)
        gpa, max_gpa = sorted(rnd.uniform(1.0, 4.0) for _ in range(2))
        return template.format(
            gpa=gpa,
            max_gpa=max_gpa,
            prec=rnd.randrange(1, 3),
            ws=rnd.choice(["", " "]),
        )

    def item_sep(self):
        return self.generator.sep_with_ws_right(
            c.FIELD_SEP_SMS, weights=[1.0, 0.25], ws_nrange=(1, 3),
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
        template = self.generator.random_template_weighted(self._school_templates)
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
        template = self.generator.random_template_weighted(self._university_templates)
        return template.format(
            university_name=self.university_name(),
            field_sep_dt=self.field_sep_dt(),
            field_sep_sm=self.field_sep_sm(),
            city_state=self.city_state(),
        )

    def university_degree(self):
        return rnd.choice(c.UNIVERSITY_DEGREES)

    def university_name(self):
        template = self.generator.random_template_weighted(self._university_name_templates)
        place_name_template = self.generator.random_template_weighted(self._university_name_place_name_templates)
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
            uni_type=self.generator.random_element_weighted(
                c.UNIVERSITY_TYPES, [1.0, 1.0, 0.5, 0.5, 0.25, 0.25]
            ),
        )


FAKER = faker.Faker()
FAKER.add_provider(Provider)


FIELDS = {
    "area": (FAKER.area_of_study, "area"),
    "area_detail": (FAKER.area_detail, "area"),
    "bullet": (FAKER.bullet_point, "field_sep"),
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
    "nl": (fnc.partial(FAKER.newline, nrange=(1, 3), weights=[1.0, 0.1]), "field_sep"),
    "nls": (fnc.partial(FAKER.newline, nrange=(1, 3), weights=[0.1, 1.0]), "field_sep"),
    "rb": (FAKER.right_bracket, "field_sep"),
    "school": (FAKER.school, "institution"),
    "uni": (FAKER.university, "institution"),
    "ws": (FAKER.whitespace, "field_sep"),
}
"""
Dict[str, Tuple[Callable, str]]: Mapping of field key string to a function that generates
a random field value and the default field label assigned to the value.
"""

######################################
## random field template generators ##

def course_list_template():
    """
    Generate a template for a group of course fields, consisting of a label and
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
            for i in range(rnd.randrange(minn, maxn))),
    )


def course_block_template():
    """
    Generate a template for a group of course fields formatted as a sub-headered
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
        course_lines=" {bullet} ".join("{course}" for _ in range(rnd.randrange(3, 6))),
        course_list=course_list_sep.join(
            "{course}" if i != newline_idx else "{nl} {course}"
            for i in range(rnd.randrange(minn, maxn))),
    )


def date_group_template():
    """
    Generate a template for a group of date fields, consisting of an end date,
    possibly preceded by a label and/or a start date.
    """
    templates = (
        "{label_dt::0.4} {dt}",
        "{label_dt::0.1} {dt:start_dt} {fsep_dt} {dt|dt_now}",
        "{lb} {dt:start_dt} {fsep_dt} {dt|dt_now} {rb}",
    )
    return rnd.choices(templates, weights=[1.0, 0.5, 0.1], k=1)[0]


def study_group_template():
    """
    Generate a template for a group of study fields, consisting of a degree,
    a primary area of study, and possibly a secondary area of study.
    """
    templates = (
        "{deg_uni} {fsep_sm|fsep_prep|ws::0.5} {area}",
        "{deg_uni} {fsep_sm|fsep_prep|ws::0.5} {area} {fsep_sm:area} {area_detail}",
        "{deg_uni}",
    )
    return rnd.choices(templates, weights=[1.0, 0.5, 0.2], k=1)[0]


_EXPERIENCES = [
    lambda: "{uni} {nl}" + study_group_template() + "{fsep_sm|ws|nl}" + date_group_template(),
    lambda: "{uni} {fsep_sm|ws}" + date_group_template() + "{nl}" + study_group_template(),
    lambda: "{uni} {fsep_sm|ws}" + date_group_template() + "{nl}" + study_group_template() + "{nl}" + rnd.choice([course_list_template(), course_block_template()]),
    lambda: study_group_template() + "{nl} {uni} {fsep_sm|ws|nl}" + date_group_template(),
    lambda: (
        "{uni} {fsep_sm|ws}" + date_group_template() +
        "{nl}" + study_group_template() +
        "{nl|fsep_sm} {label_gpa::0.75} {gpa}"
    ),
    lambda: " {nl} {bullet} ".join(
        ["{uni}"] + rnd.sample(
            ["{label_gpa} {gpa}", "{area_detail}", study_group_template(), date_group_template(), course_list_template()],
            rnd.randrange(2, 4)
        )
    ),
    lambda: " {nl} ".join(
        ["{uni}"] + rnd.sample(
            ["{label_gpa} {gpa}", "{area_detail}", study_group_template(), date_group_template(), course_list_template()],
            rnd.randrange(2, 4)
        )
    ),
    lambda: " {nl} ".join(
        ["{uni}"] + rnd.sample(
            ["{label_gpa} {gpa}", study_group_template(), date_group_template()],
            rnd.randrange(2, 4)
        ) + [course_block_template()]
    ),
    lambda: "{school} {fsep_sm|ws} {label_dt::0.5} {dt} {fsep_sm|nl|ws} {deg_school}",
]
"""
List[Callable]: Set of functions that generate a single educational experience,
in a variety of formats and with a variety of constituent fields.
"""


TEMPLATES = [
    # 1 or 2 of the same experience
    lambda: " {nls} {nl::0.25} ".join(
        exp()
        for exp in [rnd.choice(_EXPERIENCES)] * rnd.choices([1, 2], weights=[1.0, 0.33], k=1)[0]
    ),
    # 1 or 2 of different experiences
    lambda: " {nls} {nl::0.25} ".join(
        exp()
        for exp in rnd.sample(_EXPERIENCES, rnd.choices([1, 2], weights=[1.0, 0.33], k=1)[0])
    ),
]
"""
List[Callable]: Set of functions that generate one or 2 educational experiences, either
of the same type or of different types, separated by newlines.
"""
