import marshmallow as ma

from .data.resumes import RE_PHONE_NUMBER


class ResumeBasicsLocationSchema(ma.Schema):
    address = ma.fields.String()
    postal_code = ma.fields.String()
    city = ma.fields.String()
    country_code = ma.fields.String()
    region = ma.fields.String()


class ResumeBasicsProfileSchema(ma.Schema):
    network = ma.fields.String()
    username = ma.fields.String()
    url = ma.fields.String(validate=ma.validate.URL())


class ResumeBasicsSchema(ma.Schema):
    name = ma.fields.String()
    label = ma.fields.String()
    # picture = ma.fields.Raw()
    email = ma.fields.String(validate=ma.validate.Email())
    phone = ma.fields.String(validate=ma.validate.Regexp(RE_PHONE_NUMBER))
    website = ma.fields.String(validate=ma.validate.URL())
    summary = ma.fields.String()
    location = ma.fields.Nested(ResumeBasicsLocationSchema)
    profiles = ma.fields.Nested(ResumeBasicsProfileSchema, many=True)


class ResumeWorkSchema(ma.Schema):
    company = ma.fields.String()
    position = ma.fields.String()
    website = ma.fields.String(validate=ma.validate.URL())
    start_date = ma.fields.Date()
    end_date = ma.fields.Date()
    summary = ma.fields.String()
    highlights = ma.fields.List(ma.fields.String())


class ResumeVolunteerSchema(ma.Schema):
    organization = ma.fields.String()
    position = ma.fields.String()
    website = ma.fields.String(validate=ma.validate.URL())
    start_date = ma.fields.Date()
    end_date = ma.fields.Date()
    summary = ma.fields.String()
    highlights = ma.fields.List(ma.fields.String())


class ResumeEducationSchema(ma.Schema):
    institution = ma.fields.String()
    area = ma.fields.String()
    study_type = ma.fields.String()
    start_date = ma.fields.Date()
    end_date = ma.fields.Date()
    gpa = ma.fields.Number()
    course = ma.fields.List(ma.fields.String())


class ResumeAwardSchema(ma.Schema):
    title = ma.fields.String()
    date = ma.fields.Date()
    awarder = ma.fields.String()
    summary = ma.fields.String()


class ResumePublicationSchema(ma.Schema):
    name = ma.fields.String()
    publisher = ma.fields.String()
    release_date = ma.fields.Date()
    website = ma.fields.String(validate=ma.validate.URL())
    summary = ma.fields.String()


class ResumeSkillSchema(ma.Schema):
    name = ma.fields.String()
    level = ma.fields.String()
    keywords = ma.fields.List(ma.fields.String())


class ResumeLanguageSchema(ma.Schema):
    language = ma.fields.String()
    fluency = ma.fields.String()


class ResumeInterestSchema(ma.Schema):
    name = ma.fields.String()
    keywords = ma.fields.List(ma.fields.String())


class ResumeReferenceSchema(ma.Schema):
    name = ma.fields.String()
    reference = ma.fields.String()


class ResumeSchema(ma.Schema):
    """
    Standard schema for representing résumés as structured JSON data.

    References:
        Based on https://jsonresume.org/schema/
    """
    basics = ma.fields.Nested(ResumeBasicsSchema)
    work = ma.fields.Nested(ResumeWorkSchema, many=True)
    volunteer = ma.fields.Nested(ResumeVolunteerSchema, many=True)
    education = ma.fields.Nested(ResumeEducationSchema, many=True)
    awards = ma.fields.Nested(ResumeAwardSchema, many=True)
    publications = ma.fields.Nested(ResumePublicationSchema, many=True)
    skills = ma.fields.Nested(ResumeSkillSchema, many=True)
    languages = ma.fields.Nested(ResumeLanguageSchema, many=True)
    interests = ma.fields.Nested(ResumeInterestSchema, many=True)
    references = ma.fields.Nested(ResumeReferenceSchema, many=True)

    class Meta:
        # ignore any unknown keys
        unknown = ma.EXCLUDE


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
