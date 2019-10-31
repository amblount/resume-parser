import random

import faker


FAKER = faker.Faker(locale="en_US")
_FAKERS = {
    locale: faker.Faker(locale=locale)
    for locale in ("en_US", "en_GB", "en_NZ", "es_ES", "es_MX", "fr_FR")
}


_COMMON_PERSON_NAMES = [_faker.name() for _faker in _FAKERS.values() for _ in range(500)]
_COMMON_PHONE_FORMATS = [
    "###-###-####", "###.###.####", "(###) ###-####", "### ###-####",
]
_COMMON_HTTP_SCHEMES = ["www.", "http://", "http://www.", ""]


def address():
    return FAKER.address().replace("\n", " ")


def address_city_state():
    return "{city}, {state_abbr}".format(
        city=FAKER.city(),
        state_abbr=FAKER.state_abbr(),
    )


def address_city_state_zip():
    return "{city}, {state_abbr} {postcode}".format(
        city=FAKER.city(),
        state_abbr=FAKER.state_abbr(),
        postcode=FAKER.postcode(),
    )


def address_street():
    return FAKER.street_address()


def email():
    return FAKER.email()


def job_title():
    return FAKER.job()


def month_year():
    return "{month} {year}".format(
        month=FAKER.month_name() if random.random() < 0.75 else FAKER.month_name()[:3],
        year=FAKER.year(),
    )


def month_year_range():
    return "{my1}{sep}{my2}".format(
        my1=month_year(),
        sep=random.choice([" – ", " - ", "–", "-"]),
        my2=month_year() if random.random() < 0.8 else random.choice(["Present", "Current"]),
    )


def newline():
    if random.random() < 0.8:
        return "\n"
    else:
        return "\n\n"


def person_name():
    return random.choice(_COMMON_PERSON_NAMES)


def phone():
    if random.random() < 0.25:
        return FAKER.phone_number()
    else:
        return FAKER.numerify(random.choice(_COMMON_PHONE_FORMATS))


def sentence():
    return FAKER.sentence(nb_words=random.randint(5, 25))


def sentence_short():
    return FAKER.sentence(nb_words=random.randint(5, 15))


def sentence_long():
    return FAKER.sentence(nb_words=random.randint(15, 25))


def user_name():
    return "{at}{name}".format(
        at="@" if random.random() < 0.33 else "",
        name=FAKER.user_name(),
    )


def website():
    if random.random() < 0.5:
        return FAKER.url()
    else:
        return FAKER.domain_name(levels=random.randint(1, 2))


def website_profile():
    if random.random() < 0.5:
        return "{scheme}linkedin.com/in/{slug}".format(
            scheme=random.choice(_COMMON_HTTP_SCHEMES),
            slug=FAKER.slug(value=FAKER.name()),
        )
    else:
        return "{scheme}github.com/{user}".format(
            scheme=random.choice(_COMMON_HTTP_SCHEMES),
            user=FAKER.user_name(),
        )
