import random as rnd

import faker


_FIELD_SEPS = (":", ";", ",", "|")
_FIELD_SEP_DTS = ("-", "–")
_FIELD_SEP_PREPS = ("in",)
_FIELD_SEP_SMS = (",", ";")
_FIELD_LABEL_SEPS = (":", "-")
_LEFT_BRACKETS = ("(", "[")
_RIGHT_BRACKETS = (")", "]")

_DIRECTIONS = (
    "North", "South", "East", "West",
    "Northeast", "Northwest", "Southeast", "Southwest",
)
_SEASONS = ("Spring", "Summer", "Fall", "Winter")

_SCHOOL_DEGREES = (
    "Diploma", "High School Diploma", "Honor's Diploma",
    "GED", "G.E.D.",
)
_SCHOOL_TYPES = (
    "Academy",
    "High",
    "High School",
    "Institute",
    "School",
    "School of Fine Arts",
    "Secondary School",
)

_UNIVERSITY_DEGREES = (
    "Associate", "Associate Degree",
    "AA", "A.A.", "Associate of Arts",
    "AE", "A.E.", "Associate of Engineering",
    "APS", "A.P.S.", "Associate of Political Science",
    "AS", "A.S.", "Associate of Science",
    "AAS", "A.A.S.", "Associate of Applied Science",
    "Bachelor", "Bachelor's", "Bachelor's Degree",
    "B.Arch.", "Bachelor of Architecture",
    "BA", "B.A.", "Bachelor of Arts",
    "BBA", "B.B.A.", "Bachelor of Business Administration",
    "BCS", "BS CS", "B.Sc. CS", "BCompSc", "Bachelor of Computer Science",
    "BFA", "B.F.A.", "Bachelor of Fine Arts",
    "BS", "B.S.", "B.Sc.", "BSc", "Bachelor of Science",
    "Master", "Master's", "Master's Degree",
    "MA", "M.A.", "Master of Arts",
    "MBA", "M.B.A.", "Master of Business Administration",
    "MFA", "M.F.A.", "Master of Fine Arts",
    "M.Phil.", "Master of Philosophy",
    "MS", "M.S.",  "Master of Science",
    "Doctorate", "Doctorate Degree",
    "Ed.D.", "Doctor of Education",
    "JD", "J.D.", "Juris Doctor",
    "MD", "M.D.", "Doctor of Medicine",
    "PhD", "Ph.D.", "Doctor of Philosophy",
)
_UNIVERSITY_SUBUNITS = ("College", "Institute", "School", "Department", "Dept.")
_UNIVERSITY_SUFFIXES = (
    "Institute of Technology",
)
_UNIVERSITY_TYPES = (
    "University", "College",
    "State University", "State College",
    "Polytechnic University", "Community College"
)

_AREAS_OF_STUDY = (
    "Humanities",
    "Anthropology",
    "Archaeology",
    "History",
    "Linguistics and Languages",
    "Philosophy",
    "Religion",
    "The Arts",
    "Culinary Arts",
    "Literature",
    "Performing Arts",
    "Visual Arts",
    "Social Sciences",
    "Economics",
    "Geography",
    "Interdisciplinary Studies",
    "Area Studies",
    "Ethnic and Cultural Studies",
    "Gender and Sexuality Studies",
    "Organizational Studies",
    "Political Science",
    "Psychology",
    "Sociology",
    "Natural Sciences",
    "Biology",
    "Chemistry",
    "Earth Sciences",
    "Physics",
    "Space Sciences",
    "Astronomy",
    "Formal Sciences",
    "Computer Sciences", "Computer Science",  # HACK: add singular CS
    "Logic",
    "Mathematics",
    "Pure Mathematics",
    "Applied Mathematics",
    "Statistics",
    "Systems Science",
    "Professions and Applied Sciences",
    "Agriculture",
    "Architecture and Design",
    "Business",
    "Divinity",
    "Education",
    "Engineering and Technology",
    "Environmental Studies and Forestry",
    "Family and Consumer Science",
    "Human Physical Performance and Recreation",
    "Journalism, Media Studies and Communication",
    "Law",
    "Library and Museum Studies",
    "Medicine",
    "Military Sciences",
    "Public Administration",
    "Public Policy",
    "Social Work",
    "Transportation",
)
_AREA_SUBUNITS = ("Minor", "Concentration", "Emphasis")

_COURSE_SUBJECTS = (
    "Accounting and Informational Systems",
    "Acting",
    "Aeronautics and Astronautics",
    "Agricultural Science",
    "Animal Science",
    "Anthropology",
    "Applied Math",
    "Applied Mathematical Sciences",
    "Aquatic and Fishery Sciences",
    "Architectural Design",
    "Art",
    "Art History",
    "Astronomy",
    "Astronomy",
    "Atmospheric Sciences",
    "Biochemistry",
    "Bioengineering",
    "Bioengineering",
    "Biology",
    "Biology",
    "Bioresource Science and Engineering",
    "Botany",
    "Business Administration",
    "Chemical Engineering",
    "Chemistry",
    "Cinematography",
    "City Planning",
    "Civil and Environmental Engineering",
    "Classics",
    "Communication*",
    "Comparative Literature",
    "Comparative Literature",
    "Computer Engineering and Computer Science",
    "Construction Management",
    "Costume Design",
    "Criminal Science and Forensics",
    "Criminology",
    "Dance",
    "Design",
    "Digital Arts",
    "Drama",
    "Earth and Space Science",
    "Earth and Space Sciences",
    "Ecology",
    "Economics",
    "Economics",
    "Education",
    "Electrical Engineering",
    "English",
    "Entomology",
    "Entrepreneurship",
    "Environmental Science",
    "Environmental Studies",
    "Environmental Studies and Policy",
    "Ethnic and Gender Studies",
    "Ethnomusicology",
    "Film Studies",
    "Finance",
    "Food Science",
    "Foreign Language and Literature",
    "Forestry and Wildlife Management",
    "Genetics",
    "Geography",
    "Geology",
    "Geology",
    "Graphic Design",
    "Health Informatics",
    "History",
    "History Of Music",
    "Industrial Engineering",
    "Informatics",
    "Informatics",
    "International Business",
    "International Studies",
    "Kinesiology",
    "Library Science",
    "Linguistics",
    "Management",
    "Marine Biology",
    "Marketing",
    "Materials Science and Engineering",
    "Mathematics",
    "Mechanical Engineering",
    "Medical Technology",
    "Microbiology",
    "Molecular Biology",
    "Music",
    "Music Composition",
    "Music Education",
    "Music Performance",
    "Neurobiology",
    "Nursing",
    "Nutrition Science",
    "Oceanography",
    "Oceanography and Marine Biology",
    "Philosophy",
    "Physics",
    "Physiology",
    "Political Science",
    "Prop Production",
    "Psychology",
    "Psychology",
    "Recording Technology",
    "Religious Studies",
    "Resource Management",
    "Rhetoric",
    "Social Justice",
    "Social Welfare",
    "Sociology",
    "Speech and Hearing Sciences",
    "Sports Medicine",
    "Stage Design",
    "Statistics",
    "Technical Communication",
    "Theater Management",
    "Video Game Design",
    "Viticulture and Enology",
    "Writing",
)
_COURSE_PREFIXES = (
    "Introductory", "Intro to", "Intermediate", "Advanced", "Elementary",
    "Contemporary", "Modern", "21st Century", "20th Century", "Classical",
    "Perspectives on",
)
_COURSE_SUFFIXES = (
    "1", "2", "I", "II", "101", "201",
)

_FIELD_LABEL_COURSES = (
    "Courses", "Relevant Courses",
    "Coursework", "Relevant Coursework",
    "Course Work", "Relevant Course Work",
)
_FIELD_LABEL_GRAD_DATES = (
    "Graduation", "Graduating",
    "Graduated", "Expected Graduation", "Expected",
    "Class of",
)
_FIELD_LABEL_GPAS = (
    "GPA", "Cumulative GPA", "Current GPA", "Grade Point Average",
)


class Provider(faker.providers.BaseProvider):

    _area_minor_templates = (
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
        return rnd.choice(_AREAS_OF_STUDY)

    def area_minor(self):
        template = rnd.choices(self._area_minor_templates, weights=[1.0, 0.25], k=1)[0]
        return template.format(
            area_of_study=self.area_of_study(),
            field_sep=rnd.choice(_FIELD_SEP_SMS + _FIELD_SEP_PREPS + (":",)),
            subunit=rnd.choices(_AREA_SUBUNITS, weights=[1.0, 0.1, 0.1], k=1)[0],
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
        return template.format(
            prefix=rnd.choice(_COURSE_PREFIXES),
            subject=rnd.choice(_COURSE_SUBJECTS),
            subject2=rnd.choice(_COURSE_SUBJECTS),
            suffix=rnd.choice(_COURSE_SUFFIXES),
        )

    def date_approx(self):
        template = rnd.choices(
            self._date_approx_templates, weights=[1.0, 1.0, 0.25, 0.25, 0.25], k=1,
        )[0]
        month = self.generator.month_name()
        return template.format(
            month=month,
            month_abbr=month[:3],
            season=rnd.choice(_SEASONS),
            year=self.generator.year(),
        )

    def date_present(self):
        return rnd.choices(["Present", "Current"], weights=[1.0, 0.25], k=1)[0]

    def field_sep(self):
        return "{ws}{sep}{ws}".format(
            ws=" " * rnd.randint(1, 3),
            sep=rnd.choice(_FIELD_SEPS),
        )

    def field_sep_dt(self):
        return "{ws}{sep}{ws}".format(
            ws=" " * rnd.randint(1, 2),
            sep=rnd.choice(_FIELD_SEP_DTS),
        )

    def field_sep_prep(self):
        return "{ws}{sep}{ws}".format(
            ws=" " * rnd.randint(1, 2),
            sep=rnd.choice(_FIELD_SEP_PREPS),
        )

    def field_sep_sm(self):
        return "{sep}{ws}".format(
            ws=" " * rnd.randint(1, 2),
            sep=rnd.choices(_FIELD_SEP_SMS, weights=[1.0, 0.5], k=1)[0],
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
        return "{sep}{ws}".format(
            ws=" " * rnd.randint(1, 2),
            sep=rnd.choices(_FIELD_SEP_SMS, weights=[1.0, 0.25], k=1)[0],
        )

    def _label_field(self, label_values, label_weights):
        return "{label}{ws}{sep}".format(
            label=rnd.choices(label_values , weights=label_weights, k=1)[0],
            ws="" if rnd.random() < 0.9 else " ",
            sep=rnd.choices(_FIELD_LABEL_SEPS, weights=[1.0, 0.2], k=1)[0] if rnd.random() < 0.9 else "",
        )

    def label_courses(self):
        return self._label_field(_FIELD_LABEL_COURSES, None)

    def label_grad_date(self):
        return self._label_field(_FIELD_LABEL_GRAD_DATES, None)

    def label_gpa(self):
        return self._label_field(_FIELD_LABEL_GPAS, [1.0, 0.2, 0.2, 0.1])

    def left_bracket(self):
        return rnd.choice(_LEFT_BRACKETS)

    def newline(self):
        return "\n" if rnd.random() < 0.8 else "\n\n"

    def right_bracket(self):
        return rnd.choice(_RIGHT_BRACKETS)

    def school(self):
        template = rnd.choices(self._school_templates, weights=[1.0, 0.5, 0.25], k=1)[0]
        return template.format(
            school_name=self.school_name(),
            field_sep_dt=self.field_sep_dt(),
            field_sep_sm=self.field_sep_sm(),
            city_state=self.city_state(),
        )

    def school_degree(self):
        return rnd.choice(_SCHOOL_DEGREES)

    def school_name(self):
        template = rnd.choice(self._school_name_templates)
        return template.format(
            person_name=self.generator.last_name(),
            place_name=self.generator.city(),
            school_type=rnd.choice(_SCHOOL_TYPES),
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
        return rnd.choice(_UNIVERSITY_DEGREES)

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
                direction=rnd.choice(_DIRECTIONS),
                ern="ern" if rnd.random() < 0.5 else "",
                state=state,
            ),
            place_name_full="{state}{sep}{city}".format(
                city=city,
                state=state,
                sep=rnd.choice([", ", " – ", "-", "–", " ", " at "]),
            ),
            uni_subunit=rnd.choice(_UNIVERSITY_SUBUNITS),
            uni_type=rnd.choices(
                _UNIVERSITY_TYPES,
                weights=[1.0, 1.0, 0.5, 0.5, 0.25, 0.25],
                k=1,
            )[0],
        )

    def whitespace(self):
        return " " * rnd.randint(1, 4)
