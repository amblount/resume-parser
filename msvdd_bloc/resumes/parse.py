import collections
import logging
import re

import probablepeople
import usaddress
from toolz import itertoolz

from .. import regexes


LOGGER = logging.getLogger(__name__)

SECTION_HEADERS = {
    "summary": {
        "career summary",
        "objective",
        "summary",
    },
    "work": {
        "additional experience",
        "experience",
        "experiences",
        "leadership",
        "leadership experience",
        "leadership and service",
        "professional experience",
        "relevant experience",
        "work experience",
        "work & research experience",
    },
    "volunteer": {
        "volunteering",
    },
    "education": {
        "academic qualifications",
        "education",
    },
    "awards": {
        "achievements",
        "awards",
        "awards and certifications",
        "fellowships & awards",
        "honors",
        "honors & awards",
        "honors, awards, and memberships",
    },
    "publications": {
        "publications",
    },
    "skills": {
        "languages and technologies",
        "language and technologies",
        "programming languages",
        "skills",
        "skills & expertise",
        "technical skills",
        "technical skillset",
        "technological skills",
        "tools",
    },
    "languages": {
        "languages",
    },
    "interests": {
        "activities",
        "activities and student groups",
        "github projects",
        "interests",
        "other projects",
        "programming projects",
        "projects",
        "side projects",
        "technical projects",
    },
}


LOCATION_TAG_MAPPING = {
   'Recipient': 'recipient',
   'AddressNumber': 'address',
   'AddressNumberPrefix': 'address',
   'AddressNumberSuffix': 'address',
   'StreetName': 'address',
   'StreetNamePreDirectional': 'address',
   'StreetNamePreModifier': 'address',
   'StreetNamePreType': 'address',
   'StreetNamePostDirectional': 'address',
   'StreetNamePostModifier': 'address',
   'StreetNamePostType': 'address',
   'CornerOf': 'address',
   'IntersectionSeparator': 'address',
   'LandmarkName': 'address',
   'USPSBoxGroupID': 'address',
   'USPSBoxGroupType': 'address',
   'USPSBoxID': 'address',
   'USPSBoxType': 'address',
   'BuildingName': 'address',
   'OccupancyType': 'address',
   'OccupancyIdentifier': 'address',
   'SubaddressIdentifier': 'address',
   'SubaddressType': 'address',
   'PlaceName': 'city',
   'StateName': 'region',
   'ZipCode': 'postal_code',
}


def get_section_idxs(lines):
    """
    Args:
        lines (List[str])

    Returns:
        List[Tuple[str, int]]
    """
    section_idxs = [("START", 0)]
    for idx, line in enumerate(lines):
        for section, headers in SECTION_HEADERS.items():
            if (
                any(line.lower() == header for header in headers) or
                any(line.lower().startswith(header + ":") for header in headers)
            ):
                section_idxs.append((section, idx))
    section_idxs.append(("END", len(lines)))
    return section_idxs


def get_section_lines(lines, section_idxs):
    """
    Args:
        lines (List[str])
        section_idxs (List[Tuple[str, int]])

    Returns:
        Dict[str, List[str]]
    """
    section_lines = collections.defaultdict(list)
    for (section, idx1), (_, idx2) in itertoolz.sliding_window(2, section_idxs):
        section_lines[section].extend(lines[idx1 : idx2])
    return dict(section_lines)


def parse_basics_section(lines):
    """
    Args:
        lines (List[str])

    Returns:
        Dict[str, obj]
    """
    basics = {}
    for line in lines:
        if not line:
            continue
        for line_chunk in regexes.RE_LINE_DELIM.split(line):
            if not line_chunk:
                continue
            if "email" not in basics:
                match = regexes.RE_EMAIL.search(line_chunk)
                if match:
                    basics["email"] = match.group()
                    start, end = match.span()
                    if start == 0 and end == len(line_chunk):
                        continue
                    else:
                        line_chunk = line_chunk[:start] + line_chunk[end:]
            if "phone" not in basics:
                match = regexes.RE_PHONE_NUMBER.search(line_chunk)
                if match:
                    basics["phone"] = match.group()
                    start, end = match.span()
                    if start == 0 and end == len(line_chunk):
                        continue
                    else:
                        line_chunk = line_chunk[:start] + line_chunk[end:]
            if "website" not in basics:
                match = regexes.RE_URL.search(line_chunk)
                if match:
                    basics["website"] = match.group()
                    start, end = match.span()
                    if start == 0 and end == len(line_chunk):
                        continue
                    else:
                        line_chunk = line_chunk[:start] + line_chunk[end:]
            if "profiles" not in basics:
                match = regexes.RE_USER_HANDLE.search(line_chunk)
                if match:
                    basics["profiles"] = [{"username": match.group()}]
                    start, end = match.span()
                    if start == 0 and end == len(line_chunk):
                        continue
                    else:
                        line_chunk = line_chunk[:start] + line_chunk[end:]
            if "location" not in basics:
                try:
                    location, location_type = usaddress.tag(
                        line_chunk, tag_mapping=LOCATION_TAG_MAPPING)
                except usaddress.RepeatedLabelError as e:
                    LOGGER.debug("'location' parsing error:\n%s", e)
                    continue
                if location_type == "Street Address":
                    location = dict(location)
                    if "recipient" in location:
                        basics["name"] = location.pop("recipient")
                    basics["location"] = location
            if "name" not in basics:
                try:
                    name, name_type = probablepeople.tag(line_chunk)
                except probablepeople.RepeatedLabelError as e:
                    LOGGER.debug("'name' parsing error:\n%s", e)
                    continue
                if name_type == "Person":
                    basics["name"] = " ".join(name.values())
    return basics


def parse_skills_section(lines):
    """
    Args:
        lines (List[str])

    Returns:
        List[Dict[str, str]]

    Example:

        [{
            "name": "Web Development",
            "level": "Master",
            "keywords": ["HTML", "CSS", "Javascript"]
        }]
    """
    # TODO: parse out level, e.g. "Python (proficient)"
    skills = [
        {"name": skill.lstrip("- ")}
        for line in lines
        for skill in re.split(r"[,;] +", line)
        if skill.strip() and
        skill.strip().lower() not in SECTION_HEADERS["skills"]
    ]
    return skills
