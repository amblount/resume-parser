import functools as fnc
import math
import random as rnd

import faker

from msvdd_bloc.resumes.work import constants as c
from msvdd_bloc.resumes import generate_utils

###################################
## random field value generators ##

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

    _date_approx_templates = (
        ("{month} {year}", 1.0),
        ("{month_abbr} {year}", 1.0),
        ("{month_abbr}. {year}", 0.5),
        ("{season} {year}", 0.25),
        ("{year}", 0.25),
    )
    _job_title_templates = (
        ("{job}", 1.0),
        ("{level} {job}", 0.2),
        ("{job}{sep}{level}", 0.2),
        ("{level}{sep}{job}", 0.1),
    )
    _location_templates = (
        ("{city}, {state_abbr}", 1.0),
        ("{city}, {state}", 0.25),
        ("{city}", 0.1),
    )

    def company_name(self):
        if rnd.random() < 0.75:
            return rnd.choice(c.COMPANY_NAMES)
        else:
            return self.generator.company()

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
        return self.generator.sep_with_ws(
            c.FIELD_SEPS, weights=[1.0, 1.0, 0.5, 0.1], ws_nrange=(1, 4),
        )

    def field_sep_dt(self):
        sep = self.generator.random_element_weighted(c.FIELD_SEP_DTS, [1.0, 0.5, 0.1])
        # word-like separators need at least 1 space
        if sep.isalpha():
            ws = self.generator.whitespace(nrange=(1, 3), weights=[1.0, 0.25])
        # but punct-like separators do not
        else:
            ws = self.generator.whitespace(nrange=(0, 3), weights=[0.1, 1.0, 0.25])
        return "{ws}{sep}{ws}".format(ws=ws, sep=sep)

    def field_sep_prep(self):
        return self.generator.sep_with_ws(
            c.FIELD_SEP_PREPS, weights=None, ws_nrange=(1, 2),
        )

    def field_sep_sm(self):
        return self.generator.sep_with_ws_right(
            c.FIELD_SEP_SMS, weights=None, ws_nrange=(1, 3),
        )

    def job_title(self):
        template = self.generator.random_template_weighted(self._job_title_templates)
        sep = self.generator.random_element_weighted([", ", " - "], [1.0, 0.25])
        return template.format(
            job=self.generator.job(),
            level=rnd.choice(c.POSITION_LEVELS),
            sep=sep,
        )

    def location(self):
        template = self.generator.random_template_weighted(self._location_templates)
        return template.format(
            city=self.generator.city(),
            state=self.generator.state(),
            state_abbr=self.generator.state_abbr(),
        )

    def text_line(self, nrange=(50, 100), prob_capitalize=0.9):
        n_chars = rnd.randrange(*nrange)
        text_line = self.markov_model.generate(n_chars)
        if rnd.random() < prob_capitalize:
            text_line = text_line[0].capitalize() + text_line[1:]
        return text_line.strip()


FAKER = faker.Faker()
FAKER.add_provider(Provider)


FIELDS = {
    "bullet": (FAKER.bullet_point, "field_sep"),
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
    "nl": (fnc.partial(FAKER.newline, nrange=(1, 3), weights=[1.0, 0.1]), "field_sep"),
    "nls": (fnc.partial(FAKER.newline, nrange=(1, 3), weights=[0.1, 1.0]), "field_sep"),
    "punct_end": (lambda: ".", "highlight"),
    "rb": (FAKER.right_bracket, "field_sep"),
    "site": (FAKER.website, "website"),
    "subheader": (FAKER.subheader, "other"),
    "text_line": (FAKER.text_line, "highlight"),
    "text_line_trailing": (fnc.partial(FAKER.text_line, nrange=(25, 75), prob_capitalize=0.25), "highlight"),
    "ws": (FAKER.whitespace, "field_sep"),
    "ws_lg": (fnc.partial(FAKER.whitespace, nrange=(1, 5), weights=[0.4, 0.6, 0.8, 1.0]), "field_sep"),
}
"""
Dict[str, Tuple[Callable, str]]: Mapping of field key string to a function that generates
a random field value and the default field label assigned to the value.
"""

######################################
## random field template generators ##

def date_group_template():
    """
    Generate a template for a group of date fields, consisting of an end date,
    possibly preceded by a start date.
    """
    templates = (
        "{dt:start_date} {fsep_dt} {dt|dt_now}",
        "{dt}",
        "{lb} {dt:start_date} {fsep_dt} {dt|dt_now} {rb}",
    )
    return rnd.choices(templates, weights=[1.0, 0.5, 0.1], k=1)[0]


def summary_group_template():
    """
    Generate a template for a group of text lines labeled as a "summary",
    consisting of one or more text lines separated by newlines and optionally
    ending with a period.
    """
    n_lines = rnd.randrange(1, 4)
    if n_lines == 1:
        return "{text_line:summary} {punct_end:summary:0.33}"
    else:
        return (
            " {nl:item_sep} ".join("{text_line:summary}" for _ in range(n_lines - 1)) +
            " {nl:item_sep} {text_line_trailing:summary} {punct_end:summary:0.33}"
        )


def highlights_group_template():
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
        for template in rnd.choices(templates, weights=[1.0, 0.33], k=rnd.randrange(1, 4))
    )


_EXPERIENCES = [
    lambda: (
        "{comp} {fsep_sm|nl|ws_lg} {job} {nl} {location} {fsep|ws_lg}" +
        date_group_template() + "{nl}" +
        highlights_group_template()
    ),
    lambda: (
        "{job} {fsep_sm|ws_lg} {lb} {comp} {rb} {nl}" +
        date_group_template() + "{fsep|ws_lg}" +
        "{location} {nl}" +
        highlights_group_template()
    ),
    lambda: (
        "{comp} {fsep|fsep_sm|nl|ws_lg} {job} {fsep|ws_lg}" +
        date_group_template() + "{nl}" +
        highlights_group_template()
    ),
    lambda: (
        "{comp} {fsep_sm|ws_lg} {job} {fsep|nl|ws_lg}" +
        date_group_template()
    ),
    lambda: (
        "{comp} {fsep|ws_lg}" +
        date_group_template() + "{nl}" +
        "{job} {nl}" +
        highlights_group_template()
    ),
    lambda: (
        "{job} {fsep_prep} {comp} {fsep|ws_lg}" +
        date_group_template() + "{nl}" +
        highlights_group_template()
    ),
    lambda: (
        "{bullet::0.25} {comp} {fsep_sm|ws_lg} {location} {nl} {job} {fsep|fsep_sm|ws_lg}" +
        date_group_template() + "{nl}" +
        highlights_group_template()
    ),
    lambda: (
        "{job} {nl} {comp} {nl}" +
        " {fsep} ".join(rnd.sample([date_group_template(), "{location}"], 2)) + "{nl}" +
        highlights_group_template()
    ),
    lambda: "{job} {fsep_sm} {comp} {fsep_sm} {location} {nl}" + summary_group_template(),
    lambda: (
        " {fsep} ".join(rnd.sample(["{job}", "{comp}", date_group_template()], 3)) + "{nl}" +
        rnd.choice([highlights_group_template(), summary_group_template()])
    ),
    lambda: "{comp} {nl}" + highlights_group_template(),
    lambda: (
        "{comp} {fsep|fsep_sm|ws_lg} {location} {nl} {job} {fsep|ws_lg}" +
        date_group_template() + "{nl}" +
        highlights_group_template()
    ),
]
"""
List[Callable]: Set of functions that generate a single educational experience,
in a variety of formats and with a variety of constituent fields.
"""


def _multiple_experiences_template():
    """
    Generate a template for 1–3 work experiences, delimited by newlines and (optionally)
    a subheader.
    """
    n_experiences = rnd.choices([1, 2, 3], weights=[1.0, 0.75, 0.25], k=1)[0]
    experience = rnd.choice(_EXPERIENCES)
    sep = rnd.choices(
        [" {nls} {nl::0.5} ", " {nl} {nl::0.5} {subheader} {nl} {nl::0.5} "],
        weights=[1.0, 0.05],
        k=1,
    )[0]
    return sep.join(experience() for _ in range(n_experiences))


TEMPLATES = [_multiple_experiences_template]
"""
List[Callable]: Set of functions that generate one or multiple work experiences with
the same overall formatting.
"""
