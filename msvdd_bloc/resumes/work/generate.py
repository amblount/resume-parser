import functools as fnc
import math
import random as rnd

import faker

from msvdd_bloc.resumes.work import constants as c


class Provider(faker.providers.BaseProvider):
    """Class for providing randomly-generated field values."""

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
    _subheader_templates = (
        "{word1}",
        "{word1} {word2}",
        "{word1} & {word2}",
        "{word1} and {word2}",
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

    def date_present(self):
        return rnd.choices(["Present", "Current"], weights=[1.0, 0.25], k=1)[0]

    def field_sep(self):
        return "{ws}{sep}{ws}".format(
            ws=" " * rnd.randint(1, 4),
            sep=rnd.choices(
                c.FIELD_SEPS,
                weights=[1.0, 1.0, 0.5, 0.1],
                k=1,
            )[0],
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
        return "{ws}{sep}{ws}".format(
            ws=" " * rnd.randint(1, 2),
            sep=rnd.choice(c.FIELD_SEP_PREPS),
        )

    def field_sep_sm(self):
        return "{sep}{ws}".format(
            ws=" " * rnd.randint(1, 2),
            sep=rnd.choice(c.FIELD_SEP_SMS),
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

    def left_bracket(self):
        return rnd.choice(c.LEFT_BRACKETS)

    def location(self):
        template = rnd.choices(
            self._location_templates, weights=[1.0, 0.25, 0.1], k=1)[0]
        return template.format(
            city=self.generator.city(),
            state=self.generator.state(),
            state_abbr=self.generator.state_abbr(),
        )

    def newline(self):
        return "\n" if rnd.random() < 0.8 else "\n\n"

    def punct_mid_sentence(self):
        return rnd.choices(c.PUNCT_MID_SENTENCE, weights=[1.0, 0.25, 0.1, 0.1], k=1)[0]

    def summary_paragraph(self):
        return " ".join(
            self.generator.sentence(nb_words=15)
            for _ in range(rnd.randint(2, 4))
        )

    def right_bracket(self):
        return rnd.choice(c.RIGHT_BRACKETS)

    def subheader(self):
        template = rnd.choices(
            self._subheader_templates, weights=[1.0, 0.25, 0.25, 0.1], k=1,
        )[0]
        if rnd.random() < 0.75:
            subheader_string = template.format(
                word1=self.generator.word(), word2=self.generator.word()
            ).upper()
        else:
            subheader_string = template.format(
                word1=self.generator.word().capitalize(),
                word2=self.generator.word().capitalize(),
            )
        return subheader_string

    def website(self):
        if rnd.random() < 0.5:
            return self.generator.url()
        else:
            return self.generator.domain_name(levels=rnd.randint(1, 2))

    def whitespace(self):
        return " " * rnd.randint(1, 4)

    def word_plus(self):
        if rnd.random() < 0.9:
            word = self.generator.word()
            if rnd.random() < 0.01:
                word = "{}'s".format(word)
            elif rnd.random() < 0.01:
                word = "{}-{}".format(word, self.generator.word())
            elif rnd.random() < 0.01:
                word = '"{}"'.format(word)
            return word
        elif rnd.random() < 0.75:
            return self.generator.bs()
        else:
            return str(self.generator.random_int(min=1, max=100))

    def word_title(self):
        return self.generator.word().capitalize()


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
    "para": (FAKER.summary_paragraph, "summary"),
    "punct_mid": (FAKER.punct_mid_sentence, "highlight"),
    "punct_end": (lambda: ".", "highlight"),
    "rb": (FAKER.right_bracket, "field_sep"),
    "sent": (fnc.partial(FAKER.sentence, nb_words=15, variable_nb_words=True), "highlight"),
    "site": (FAKER.website, "website"),
    "subheader": (FAKER.subheader, "other"),
    "word": (FAKER.word, "highlight"),
    "word_plus": (FAKER.word_plus, "highlight"),
    "word_title": (FAKER.word_title, "highlight"),
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


def generate_group_highlight():
    """
    Generate a template for a logical group of highlight fields, consisting of a single
    sentence spanning one or multiple lines, beginning with a bullet point.
    """
    maxn_newline = rnd.randint(15, 25)
    maxn_punct = rnd.randint(20, 40)
    n_words = rnd.randint(8, 22)

    all_fks = ["{bullet} {word_title}"]
    n_since_punct = 0
    n_since_newline = 0
    for i in range(n_words):
        fks = ["{word_plus}"]
        if i < 0.8 * n_words and rnd.random() < math.pow(n_since_punct / maxn_punct, 2):
            fks.append("{punct_mid}")
            n_since_punct = 0
        else:
            n_since_punct += 1
        if i < 0.8 * n_words and rnd.random() < math.pow(n_since_newline / maxn_newline, 2):
            fks.append("{nl:item_sep}")
            n_since_newline = 0
        else:
            n_since_newline += 1
        all_fks.extend(fks)
    all_fks.append("{punct_end::0.25}")
    return " ".join(all_fks)


def generate_group_highlights():
    """
    Generate a template for a logical group of highlight fields, consisting of one or more
    sentences as a list spanning multiple lines, each beginning with a bullet point.
    """
    return " {nl} ".join(generate_group_highlight() for _ in range(rnd.randint(1, 3)))


_EXPERIENCES = [
    lambda: (
        "{comp} {fsep_sm|nl|ws} {job} {nl} {city_state} {fsep|ws}" +
        generate_group_date() + "{nl}" +
        generate_group_highlights()
    ),
    lambda: (
        "{job} {fsep_sm|ws} {lb} {comp} {rb} {nl}" +
        generate_group_date() + "{fsep|ws}" +
        "{city_state} {nl}" +
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
        "{bullet::0.25} {comp} {fsep_sm|ws} {city_state} {nl} {job} {fsep|fsep_sm|ws}" +
        generate_group_date() + "{nl}" +
        generate_group_highlights()
    ),
    lambda: (
        "{job} {nl} {comp} {nl}" +
        " {fsep} ".join(rnd.sample([generate_group_date(), "{city_state}"], 2)) + "{nl}" +
        generate_group_highlights()
    ),
    lambda: "{job} {fsep_sm} {comp} {fsep_sm} {city_state} {nl} {para}",
    lambda: (
        " {fsep} ".join(rnd.sample(["{job}", "{comp}", generate_group_date()], 3)) + "{nl}" +
        rnd.choice([generate_group_highlights(), "{para}"])
    ),
    lambda: "{comp} {nl}" + generate_group_highlights(),
    lambda: (
        "{comp} {fsep|fsep_sm|ws} {city_state} {nl} {job} {fsep|ws}" +
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
