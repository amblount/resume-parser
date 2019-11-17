"""
parse
-----
"""
import logging

import marshmallow as ma

from msvdd_bloc import schemas
from msvdd_bloc.resumes import munge, segment
from msvdd_bloc.resumes import basics, education, skills


LOGGER = logging.getLogger(__name__)
_RESUME_SCHEMA = schemas.ResumeSchema()


def parse(text):
    """
    Args:
        text (str)

    Returns:
        Dict[str, object]
    """
    data = {}

    norm_text = munge.normalize_text(text)
    text_lines = munge.get_filtered_text_lines(norm_text)
    section_lines = segment.get_section_lines(text_lines)

    # basics section
    basics_lines = section_lines.get("start", []) + section_lines.get("basics", [])
    basics_data = basics.parse.parse_lines(basics_lines)
    if section_lines.get("summary"):
        basics_data["summary"] = "\n".join(section_lines["summary"]).strip()
    data["basics"] = basics_data

    # education
    education_lines = section_lines.get("education", [])
    education_data = education.parse.parse_lines(education_lines)
    data["education"] = education_data
    # NOTE: uncomment if courses not directly included in main education lines
    # courses_lines = section_lines.get("courses", [])

    # skills
    skills_lines = section_lines.get("skills", [])
    skills_data = skills.parse.parse_lines(skills_lines)
    data["skills"] = skills_data

    # TODO: figure out what we want to do here
    # option 1: validate and warn, but return data as-is
    # validation = _RESUME_SCHEMA.validate(data)
    # if validation:
    #     LOGGER.warning("validation error: %s", validation)
    # option 2: validate and warn, but only return valid data
    try:
        data = _RESUME_SCHEMA.load(data)
    except ma.ValidationError as e:
        LOGGER.warning("validation error: %s", e.messages)
        data = e.valid_data

    return data
