import random as rnd

import faker


_FIELD_LABEL_SEPS = (":", "-")
_FIELD_SEPS = ("|", "–", "-", ":", "•", "·", "Ÿ", "�", "⇧")
_ITEM_SEPS = (",", ";")

_FIELD_LABEL_ADDRS = ("Address", "Current Address")
_FIELD_LABEL_EMAILS = ("Email", "E-mail")
_FIELD_LABEL_PHONES = ("Phone", "Mobile", "Cell", "Tel.")
_FIELD_LABEL_PROFILES = ("GitHub", "Twitter", "LinkedIn")

_PHONE_FORMATS = (
    "###-###-####", "###.###.####", "(###) ###-####", "### ###-####",
)
_URL_SCHEMES = ("www.", "http://", "http://www.")


class Provider(faker.providers.BaseProvider):

    _address_city_state_templates = (
        "{city}, {state_abbr}",
        "{city}, {state}",
    )
    _address_city_state_zip_templates = (
        "{city}, {state_abbr} {postcode}",
        "{city}, {state} {postcode}",
    )
    _user_name_templates = (
        "{user_name}",
        "@{user_name}",
    )
    _website_profile_templates = (
        "{scheme}linkedin.com/in/{slug}",
        "{scheme}github.com/{user}",
    )

    def address_inline(self):
        sep = rnd.choice([", ", " "])
        return self.generator.address().replace("\n", sep)

    def address_city_state(self):
        template = rnd.choices(
            self._address_city_state_templates, weights=[0.9, 0.1], k=1)[0]
        return template.format(
            city=self.generator.city(),
            state=self.generator.state(),
            state_abbr=self.generator.state_abbr(),
        )

    def address_city_state_zip(self):
        template = rnd.choices(
            self._address_city_state_zip_templates, weights=[0.9, 0.1], k=1)[0]
        return template.format(
            city=self.generator.city(),
            state=self.generator.state(),
            state_abbr=self.generator.state_abbr(),
            postcode=self.generator.postcode(),
        )

    def field_sep(self):
        return "{ws}{sep}{ws}".format(
            ws=" " * rnd.randint(1, 4),
            sep=rnd.choices(
                _FIELD_SEPS,
                weights=[1.0, 0.5, 0.5, 0.25, 0.1, 0.05, 0.05, 0.05, 0.05],
                k=1,
            )[0],
        )

    def item_sep(self):
        return "{sep}{ws}".format(
            sep=rnd.choices(_ITEM_SEPS, weights=[1.0, 0.2], k=1)[0],
            ws=" " * rnd.randint(1, 2),
        )

    def _label_field(self, label_values, label_weights):
        return "{label}{ws}{sep}".format(
            label=rnd.choices(label_values , weights=label_weights, k=1)[0],
            ws="" if rnd.random() < 0.9 else " ",
            sep=rnd.choices(_FIELD_LABEL_SEPS, weights=[1.0, 0.2], k=1)[0] if rnd.random() < 0.9 else "",
        )

    def label_addr(self):
        return self._label_field(_FIELD_LABEL_ADDRS, [1.0, 0.1])

    def label_email(self):
        return self._label_field(_FIELD_LABEL_EMAILS, [1.0, 0.5])

    def label_phone(self):
        return self._label_field(_FIELD_LABEL_PHONES, None)

    def label_profile(self):
        return self._label_field(_FIELD_LABEL_PROFILES, None)

    def newline(self):
        return "\n" if rnd.random() < 0.8 else "\n\n"

    def phone(self):
        if rnd.random() < 0.25:
            return self.generator.phone_number()
        else:
            return self.numerify(rnd.choice(_PHONE_FORMATS))

    def person_label(self):
        if rnd.random() > 0.8:
            return self.generator.job()
        else:
            return self.generator.catch_phrase()

    def user_name_rand_at(self):
        template = rnd.choices(self._user_name_templates, weights=[1.0, 0.33], k=1)[0]
        return template.format(user_name=self.generator.user_name())

    def website(self):
        if rnd.random() < 0.5:
            return self.generator.url()
        else:
            return self.generator.domain_name(levels=rnd.randint(1, 2))

    def website_profile(self):
        template = rnd.choice(self._website_profile_templates)
        return template.format(
            scheme=rnd.choice(_URL_SCHEMES) if rnd.random() < 0.75 else "",
            slug=self.generator.slug(value=self.generator.name()),
            user=self.generator.user_name(),
        )

    def whitespace(self):
        return " " * rnd.randint(1, 4)
