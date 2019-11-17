"""
schemas
-------
"""
import marshmallow as ma

from msvdd_bloc import regexes


class ResumeSchema(ma.Schema):
    """
    Standard schema for representing résumés as structured JSON data.

    Example::

        {
            "basics": {
                "name": "John Doe",
                "label": "Programmer",
                "email": "john@gmail.com",
                "phone": "(912) 555-4321",
                "website": "http://johndoe.com",
                "summary": "A summary of John Doe...",
                "location": {
                    "address": "2712 Broadway St",
                    "postalCode": "CA 94115",
                    "city": "San Francisco",
                    "countryCode": "US",
                    "region": "California"
                },
                "profiles": [{
                    "network": "Twitter",
                    "username": "john",
                    "url": "http://twitter.com/john"
                }]
            },
            "work": [{
                "company": "Company",
                "position": "President",
                "website": "http://company.com",
                "startDate": "2013-01-01",
                "endDate": "2014-01-01",
                "summary": "Description...",
                "highlights": [
                    "Started the company"
                ]
            }],
            "volunteer": [{
                "organization": "Organization",
                "position": "Volunteer",
                "website": "http://organization.com/",
                "startDate": "2012-01-01",
                "endDate": "2013-01-01",
                "summary": "Description...",
                "highlights": [
                    "Awarded 'Volunteer of the Month'"
                ]
            }],
            "education": [{
                "institution": "University",
                "area": "Software Development",
                "studyType": "Bachelor",
                "startDate": "2011-01-01",
                "endDate": "2013-01-01",
                "gpa": "4.0",
                "courses": [
                    "DB1101 - Basic SQL"
                ]
            }],
            "awards": [{
                "title": "Award",
                "date": "2014-11-01",
                "awarder": "Company",
                "summary": "There is no spoon."
            }],
            "publications": [{
                "name": "Publication",
                "publisher": "Company",
                "releaseDate": "2014-10-01",
                "website": "http://publication.com",
                "summary": "Description..."
            }],
            "skills": [{
                "name": "Web Development",
                "level": "Master",
                "keywords": [
                    "HTML",
                    "CSS",
                    "Javascript"
                ]
            }],
            "languages": [{
                "language": "English",
                "fluency": "Native speaker"
            }],
            "interests": [{
                "name": "Wildlife",
                "keywords": [
                    "Ferrets",
                    "Unicorns"
                ]
            }],
            "references": [{
                "name": "Jane Doe",
                "reference": "Reference..."
            }]
        }

    References:
        Based on https://jsonresume.org/schema/
    """
    basics = ma.fields.Nested("ResumeBasicsSchema")
    work = ma.fields.Nested("ResumeWorkSchema", many=True)
    volunteer = ma.fields.Nested("ResumeVolunteerSchema", many=True)
    education = ma.fields.Nested("ResumeEducationSchema", many=True)
    awards = ma.fields.Nested("ResumeAwardSchema", many=True)
    publications = ma.fields.Nested("ResumePublicationSchema", many=True)
    skills = ma.fields.Nested("ResumeSkillSchema", many=True)
    languages = ma.fields.Nested("ResumeLanguageSchema", many=True)
    interests = ma.fields.Nested("ResumeInterestSchema", many=True)
    references = ma.fields.Nested("ResumeReferenceSchema", many=True)

    class Meta:
        # ignore any unknown keys
        unknown = ma.EXCLUDE


class ResumeBasicsSchema(ma.Schema):
    """
    Example::

        {
            "name": "John Doe",
            "label": "Programmer",
            "email": "john@gmail.com",
            "phone": "(912) 555-4321",
            "website": "http://johndoe.com",
            "summary": "A summary of John Doe...",
            "location": {
                "address": "2712 Broadway St",
                "postalCode": "CA 94115",
                "city": "San Francisco",
                "countryCode": "US",
                "region": "California"
            },
            "profiles": [{
                "network": "Twitter",
                "username": "john",
                "url": "http://twitter.com/john"
            }]
        }
    """
    name = ma.fields.String()
    label = ma.fields.String()
    email = ma.fields.String(validate=ma.validate.Email())
    phone = ma.fields.String()
    # marshmallow's built-in URL validation is *strict*
    website = ma.fields.String(validate=ma.validate.URL(relative=True, require_tld=True))
    # website = ma.fields.String(
    #     validate=lambda s: regexes.RE_URL.match(s) is not None or regexes.RE_SHORT_URL.match(s) is not None)
    summary = ma.fields.String()
    location = ma.fields.Nested("ResumeBasicsLocationSchema")
    profiles = ma.fields.Nested("ResumeBasicsProfileSchema", many=True)


class ResumeBasicsLocationSchema(ma.Schema):
    """
    Example::

        {
            "address": "2712 Broadway St",
            "postalCode": "CA 94115",
            "city": "San Francisco",
            "countryCode": "US",
            "region": "California"
        }
    """
    address = ma.fields.String()
    postal_code = ma.fields.String()
    city = ma.fields.String()
    country_code = ma.fields.String()
    region = ma.fields.String()


class ResumeBasicsProfileSchema(ma.Schema):
    """
    Example::

        {
            "network": "Twitter",
            "username": "john",
            "url": "http://twitter.com/john"
        }
    """
    network = ma.fields.String()
    username = ma.fields.String()
    url = ma.fields.String(validate=ma.validate.URL())


class ResumeWorkSchema(ma.Schema):
    """
    Example::

        {
            "company": "Company",
            "position": "President",
            "website": "http://company.com",
            "startDate": "2013-01-01",
            "endDate": "2014-01-01",
            "summary": "Description...",
            "highlights": [
                "Started the company"
            ]
        }
    """
    company = ma.fields.String()
    position = ma.fields.String()
    website = ma.fields.String(validate=ma.validate.URL())
    start_date = ma.fields.String()  # not necessarily a date
    end_date = ma.fields.String()  # not necessarily a date
    summary = ma.fields.String()
    highlights = ma.fields.List(ma.fields.String())


class ResumeVolunteerSchema(ma.Schema):
    """
    Example::

        {
            "organization": "Organization",
            "position": "Volunteer",
            "website": "http://organization.com/",
            "startDate": "2012-01-01",
            "endDate": "2013-01-01",
            "summary": "Description...",
            "highlights": [
                "Awarded 'Volunteer of the Month'"
            ]
        }
    """
    organization = ma.fields.String()
    position = ma.fields.String()
    website = ma.fields.String(validate=ma.validate.URL())
    start_date = ma.fields.String()  # not necessarily a date
    end_date = ma.fields.String()  # not necessarily a date
    summary = ma.fields.String()
    highlights = ma.fields.List(ma.fields.String())


class ResumeEducationSchema(ma.Schema):
    """
    Example::

        {
            "institution": "University",
            "area": "Software Development",
            "studyType": "Bachelor",
            "startDate": "2011-01-01",
            "endDate": "2013-01-01",
            "gpa": "4.0",
            "courses": [
                "DB1101 - Basic SQL"
            ]
        }
    """
    institution = ma.fields.String()
    area = ma.fields.String()
    study_type = ma.fields.String()
    start_date = ma.fields.String()  # not necessarily a date
    end_date = ma.fields.String()  # not necessarily a date
    gpa = ma.fields.String()  # not necessarily a number
    courses = ma.fields.List(ma.fields.String())


class ResumeAwardSchema(ma.Schema):
    """
    Example::

        {
            "title": "Award",
            "date": "2014-11-01",
            "awarder": "Company",
            "summary": "There is no spoon."
        }
    """
    title = ma.fields.String()
    date = ma.fields.Date()
    awarder = ma.fields.String()
    summary = ma.fields.String()


class ResumePublicationSchema(ma.Schema):
    """
    Example::

        {
            "name": "Publication",
            "publisher": "Company",
            "releaseDate": "2014-10-01",
            "website": "http://publication.com",
            "summary": "Description..."
        }
    """
    name = ma.fields.String()
    publisher = ma.fields.String()
    release_date = ma.fields.Date()
    # website = ma.fields.String(validate=ma.validate.URL())
    website = ma.fields.String(validate=ma.validate.URL())
    summary = ma.fields.String()


class ResumeSkillSchema(ma.Schema):
    """
    Example::

        {
            "name": "Web Development",
            "level": "Master",
            "keywords": [
                "HTML",
                "CSS",
                "Javascript"
            ]
        }
    """
    name = ma.fields.String()
    level = ma.fields.String()
    keywords = ma.fields.List(ma.fields.String())


class ResumeLanguageSchema(ma.Schema):
    """
    Example::

        {
            "language": "English",
            "fluency": "Native speaker"
        }
    """
    language = ma.fields.String()
    fluency = ma.fields.String()


class ResumeInterestSchema(ma.Schema):
    """
    Example::

        {
            "name": "Wildlife",
            "keywords": [
                "Ferrets",
                "Unicorns"
            ]
        }
    """
    name = ma.fields.String()
    keywords = ma.fields.List(ma.fields.String())


class ResumeReferenceSchema(ma.Schema):
    """
    Example::

        {
            "name": "Jane Doe",
            "reference": "Reference..."
        }
    """
    name = ma.fields.String()
    reference = ma.fields.String()


class JobPostingSchema(ma.Schema):
    """
    Standard schema for representing job postings as structured JSON data.

    References:
        Based on https://schema.org/JobPosting
    """
    title = ma.fields.String(required=True)
    company = ma.fields.String(required=True)
    date_posted = ma.fields.Date(required=True)
    location = ma.fields.List(ma.fields.String(), required=True)
    url = ma.fields.String(required=True, validate=ma.validate.URL())
    start_date = ma.fields.Date()
    employment_type = ma.fields.String(
        validate=ma.validate.OneOf(
            choices=["full-time", "part-time", "contract", "temporary", "seasonal", "internship"]
        )
    )
    description = ma.fields.String()
    responsibilities = ma.fields.String()
    education_requirements = ma.fields.String()
    experience_requirements = ma.fields.String()
    skills_requirements = ma.fields.String()
    industry = ma.fields.String()
    benefits = ma.fields.String()
    special_commitments = ma.fields.String()
    work_hours = ma.fields.String()
    base_salary = ma.fields.Number()
    expected_salary = ma.fields.Number()
    salary_currency = ma.fields.String()

    class Meta:
        # ignore any unknown keys
        unknown = ma.EXCLUDE
