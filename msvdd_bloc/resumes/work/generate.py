import functools as fnc
import math
import random as rnd

import faker

from msvdd_bloc.resumes.work import constants as c
from msvdd_bloc.resumes import generate_utils


class Provider(generate_utils.ResumeProvider):
    """Class for providing randomly-generated field values."""

    _markov_model = None

    @property
    def markov_model(self):
        """
        :class:`generate_utils.MarkovModel`: Markov model used to generate text in
        :meth:`Provider.text_lines()` and :meth:`Provider.text_lines_trailing()`.
        It's trained and assigned at the instance- rather than class-level to avoid
        having to train the model every time this module is imported. It's fast, but
        not *that* fast.
        """
        if self._markov_model is None:
            self._markov_model = generate_utils.MarkovModel(state_len=4).fit(c.TEXT_SAMPLES)
        return self._markov_model

    _location_templates = (
        "{city}, {state_abbr}",
        "{city}, {state}",
        "{city}",
    )
    _date_approx_templates = (
        "{month} {year}",
        "{month_abbr} {year}",
        "{month_abbr}. {year}",
        "{season} {year}",
        "{year}",
    )
    _job_title_templates = (
        "{job}",
        "{level} {job}",
        "{job}{sep}{level}",
        "{level}{sep}{job}",
    )

    def company_name(self):
        if rnd.random() < 0.75:
            return rnd.choice(c.COMPANY_NAMES)
        else:
            return self.generator.company()

    def date_approx(self):
        template = rnd.choices(
            self._date_approx_templates, weights=[1.0, 1.0, 0.5, 0.25, 0.25], k=1,
        )[0]
        month = self.generator.month_name()
        return template.format(
            month=month,
            month_abbr=month[:3],
            season=rnd.choice(c.SEASONS),
            year=self.generator.year(),
        )

    def field_sep(self):
        return self.generator.sep_with_ws(
            c.FIELD_SEPS, weights=[1.0, 1.0, 0.5, 0.1], ws_nrange=(1, 4),
        )

    def field_sep_dt(self):
        sep = rnd.choices(c.FIELD_SEP_DTS, weights=[1.0, 0.5, 0.1], k=1)[0]
        # word-like separators need at least 1 space
        if sep.isalpha():
            ws = " " * rnd.choices([1, 2], weights=[1.0, 0.25], k=1)[0]
        # but punct-like separators do not
        else:
            ws = " " * rnd.choices([1, 2, 0], weights=[1.0, 0.25, 0.1], k=1)[0]
        return "{ws}{sep}{ws}".format(ws=ws, sep=sep)

    def field_sep_prep(self):
        return self.generator.sep_with_ws(
            c.FIELD_SEP_PREPS, weights=None, ws_nrange=(1, 2),
        )

    def field_sep_sm(self):
        return self.generator.sep_with_ws_right(
            c.FIELD_SEP_SMS, weights=None, ws_nrange=(1, 2),
        )

    def job_title(self):
        template = rnd.choices(
            self._job_title_templates, weights=[1.0, 0.2, 0.2, 0.1], k=1,
        )[0]
        return template.format(
            job=self.generator.job(),
            level=rnd.choice(c.POSITION_LEVELS),
            sep=rnd.choices([", ", " - "], weights=[1.0, 0.25], k=1)[0],
        )

    def location(self):
        template = rnd.choices(
            self._location_templates, weights=[1.0, 0.25, 0.1], k=1)[0]
        return template.format(
            city=self.generator.city(),
            state=self.generator.state(),
            state_abbr=self.generator.state_abbr(),
        )

    def text_line(self, nrange=(50, 100), prob_capitalize=0.9):
        n_chars = rnd.randint(*nrange)
        text_line = self.markov_model.generate(n_chars)
        if rnd.random() < prob_capitalize:
            text_line = text_line[0].capitalize() + text_line[1:]
        return text_line.strip()


FAKER = faker.Faker()
FAKER.add_provider(Provider)


FIELDS = {
    "bullet": (lambda : "- ", "bullet"),
    "comp": (FAKER.company_name, "company"),
    "dt": (FAKER.date_approx, "end_date"),
    "dt_now": (FAKER.date_present, "end_date"),
    "fsep": (FAKER.field_sep, "field_sep"),
    "fsep_dt": (FAKER.field_sep_dt, "field_sep"),
    "fsep_prep": (FAKER.field_sep_prep, "field_sep"),
    "fsep_sm": (FAKER.field_sep_sm, "field_sep"),
    "lb": (FAKER.left_bracket, "field_sep"),
    "location": (FAKER.location, "location"),
    "job": (FAKER.job_title, "position"),
    "nl": (FAKER.newline, "field_sep"),
    "punct_end": (lambda: ".", "highlight"),
    "rb": (FAKER.right_bracket, "field_sep"),
    "site": (FAKER.website, "website"),
    "subheader": (FAKER.subheader, "other"),
    "text_line": (FAKER.text_line, "highlight"),
    "text_line_trailing": (fnc.partial(FAKER.text_line, nrange=(25, 75), prob_capitalize=0.25), "highlight"),
    "ws": (FAKER.whitespace, "field_sep"),
}
"""
Dict[str, Tuple[Callable, str]]: Mapping of field key string to a function that generates
a random field value and the default field label assigned to the value.
"""

#############################
## random group generators ##
#############################

def generate_group_date():
    """
    Generate a template for a logical group of date fields, consisting of an end date,
    possibly preceded by a start date.
    """
    templates = (
        "{dt}",
        "{dt:start_date} {fsep_dt} {dt|dt_now}",
        "{lb} {dt:start_date} {fsep_dt} {dt|dt_now} {rb}",
    )
    return rnd.choices(templates, weights=[1.0, 0.5, 0.1], k=1)[0]


def generate_group_summary():
    """
    Generate a template for a logical group of text lines labeled as a "summary",
    consisting of one or more text lines separated by newlines and optionally
    ending with a period.
    """
    n_lines = rnd.randint(1, 3)
    if n_lines == 1:
        return "{text_line:summary} {punct_end:summary:0.33}"
    else:
        return (
            " {nl:item_sep} ".join("{text_line:summary}" for _ in range(n_lines - 1)) +
            " {nl:item_sep} {text_line_trailing:summary} {punct_end:summary:0.33}"
        )


def generate_group_highlights():
    """
    Generate a template for a logical group of bulleted text lines labeled as "highlights",
    consisting of 1 or 2 text lines separated by newlines and optionally
    ending with a period.
    """
    templates = (
        "{bullet} {text_line} {punct_end::0.25}",
        "{bullet} {text_line} {nl:item_sep} {text_line_trailing} {punct_end::0.25}",
    )
    return " {nl} ".join(
        template
        for template in rnd.choices(templates, weights=[1.0, 0.33], k=rnd.randint(1, 3))
    )


_EXPERIENCES = [
    lambda: (
        "{comp} {fsep_sm|nl|ws} {job} {nl} {location} {fsep|ws}" +
        generate_group_date() + "{nl}" +
        generate_group_highlights()
    ),
    lambda: (
        "{job} {fsep_sm|ws} {lb} {comp} {rb} {nl}" +
        generate_group_date() + "{fsep|ws}" +
        "{location} {nl}" +
        generate_group_highlights()
    ),
    lambda: (
        "{comp} {fsep|fsep_sm|nl|ws} {job} {fsep|ws}" +
        generate_group_date() + "{nl}" +
        generate_group_highlights()
    ),
    lambda: (
        "{comp} {fsep_sm|ws} {job} {fsep|nl|ws}" +
        generate_group_date()
    ),
    lambda: (
        "{comp} {fsep|ws}" +
        generate_group_date() + "{nl}" +
        "{job} {nl}" +
        generate_group_highlights()
    ),
    lambda: (
        "{job} {fsep_prep} {comp} {fsep|ws}" +
        generate_group_date() + "{nl}" +
        generate_group_highlights()
    ),
    lambda: (
        "{bullet::0.25} {comp} {fsep_sm|ws} {location} {nl} {job} {fsep|fsep_sm|ws}" +
        generate_group_date() + "{nl}" +
        generate_group_highlights()
    ),
    lambda: (
        "{job} {nl} {comp} {nl}" +
        " {fsep} ".join(rnd.sample([generate_group_date(), "{location}"], 2)) + "{nl}" +
        generate_group_highlights()
    ),
    lambda: "{job} {fsep_sm} {comp} {fsep_sm} {location} {nl}" + generate_group_summary(),
    lambda: (
        " {fsep} ".join(rnd.sample(["{job}", "{comp}", generate_group_date()], 3)) + "{nl}" +
        rnd.choice([generate_group_highlights(), generate_group_summary()])
    ),
    lambda: "{comp} {nl}" + generate_group_highlights(),
    lambda: (
        "{comp} {fsep|fsep_sm|ws} {location} {nl} {job} {fsep|ws}" +
        generate_group_date() + "{nl}" +
        generate_group_highlights()
    ),
]
"""
List[Callable]: Set of functions that generate a single educational experience,
in a variety of formats and with a variety of constituent fields.
"""


def generate_experiences():
    n_experiences = rnd.choices([1, 2, 3], weights=[1.0, 0.75, 0.25], k=1)[0]
    experience = rnd.choice(_EXPERIENCES)
    sep = rnd.choices(
        [" {nl} {nl::0.5} ", " {nl} {nl::0.5} {subheader} {nl} {nl::0.5} "],
        weights=[1.0, 0.05],
        k=1,
    )[0]
    return sep.join(experience() for _ in range(n_experiences))


TEMPLATES = [generate_experiences]
"""
List[Callable]: Set of functions that generate one or multiple work experiences with
the same overall formatting.
"""
