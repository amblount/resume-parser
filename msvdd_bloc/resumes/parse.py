import collections
import logging
import re

import probablepeople
import usaddress
from toolz import itertoolz

from .. import regexes


LOGGER = logging.getLogger(__name__)

SECTION_HEADERS = {
    "summary": re.compile(
        r"^(?P<text>"
        "career summary|"
        "objective|"
        "summary"
        ")(?P<end>: |:?$)",
        flags=re.IGNORECASE,
    ),
    "work": re.compile(
        r"^(?P<text>"
        "additional experiences?|"
        "experiences?|"
        "leadership|"
        "leadership (and|&) service|"
        "leadership experiences?|"
        "professional experiences?|"
        "relevant experiences?|"
        "work experiences?|"
        "work (and|&) research experiences?"
        ")(?P<end>:?$)",
        flags=re.IGNORECASE,
    ),
    "volunteer": re.compile(
        r"^(?P<text>"
        "volunteering"
        ")(?P<end>:?$)",
        flags=re.IGNORECASE,
    ),
    "education": re.compile(
        r"^(?P<text>"
        "academic qualifications|"
        "education"
        ")(?P<end>:?$)",
        flags=re.IGNORECASE,
    ),
    "awards": re.compile(
        r"^(?P<text>"
        "achievements|"
        "awards|"
        "awards (and|&) certifications|"
        "fellowships (and|&) awards|"
        "honors|"
        "honors (and|&) awards|"
        "honors, awards, (and|&) memberships"
        ")(?P<end>: |:?$)",
        flags=re.IGNORECASE,
    ),
    "publications": re.compile(
        r"^(?P<text>"
        "publications"
        ")(?P<end>:?$)",
        flags=re.IGNORECASE,
    ),
    "skills": re.compile(
        r"^(?P<text>"
        "languages? (and|&) technologies|"
        "programming languages|"
        "skills|"
        "skills (and|&) expertise|"
        "technical skills(et)?|"
        "technological skills(et)?|"
        "tools"
        ")(?P<end>:?$)",
        flags=re.IGNORECASE,
    ),
    "languages": re.compile(
        r"^(?P<text>"
        "languages"
        ")(?P<end>:?$)",
        flags=re.IGNORECASE,
    ),
    "interests": re.compile(
        r"^(?P<text>"
        "activities|"
        "activities (and|&) student groups|"
        "extracurricular activities|"
        "github projects|"
        "interests|"
        "other projects|"
        "programming projects|"
        "projects|"
        "side projects|"
        "technical projects"
        ")(?P<end>:?$)",
        flags=re.IGNORECASE,
    ),
    "ambiguous": re.compile(
        r"^(?P<text>"
        "activities (and|&) honors"
        ")(?P<end>:?$)",
        flags=re.IGNORECASE,
    ),
    # this catches too many non-header lines, sorry
    # "other": re.compile(
    #     r"^(?P<text>"
    #     r"(\w+( |-| & )?){1,3})"
    #     r":?(?P<end>$)",
    # )
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


def get_section_lines(lines):
    """
    Args:
        List[str]

    Returns:
        Dict[str, List[str]]
    """
    section_lines = collections.defaultdict(list)
    curr_section = "START"
    for line in lines:
        for section, pattern in SECTION_HEADERS.items():
            match = pattern.match(line)
            if match:
                curr_section = section
                # if header is the start of a line with more content
                # append only the post-header content
                if match.group("end").endswith(": "):
                    section_lines[curr_section].append(line[match.end():])
                # if header is a whole line on its own, skip to the next line
                else:
                    pass
                # only one section header match permitted per line
                break
        # no new match, so add line to current section
        else:
            section_lines[curr_section].append(line)
    return section_lines


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


RE_SKILL_NAME_DELIM = re.compile(r"(?:: +| +[-–] +)")
RE_SKILL_KEYWORD_DELIM = re.compile(r"[,;] +(?:(?:and|&) +)?")
RE_SKILL_LEVEL = re.compile(
    r"\(?(?P<level>advanced|intermediate|beginner|basic|proficient|exposed)\)? ?(in )?",
    flags=re.UNICODE | re.IGNORECASE,
)
RE_SKILL_CLEAN = re.compile(r"[.,;]$")


def parse_skills_section(lines):
    """
    Args:
        lines (List[str])

    Returns:
        List[Dict[str, str]]

    Example:

        [{
            "name": "Web Development",
            "level": "advanced",
            "keywords": ["HTML", "CSS", "Javascript"]
        }]
    """
    all_skills = []
    for line in lines:
        if not line:
            continue
        line = line.lstrip("- ")
        split_line = RE_SKILL_NAME_DELIM.split(line)
        if len(split_line) == 1:
            names = RE_SKILL_KEYWORD_DELIM.split(line)
            if len(names) == 1:
                names = line.split()
            skills = []
            for name in names:
                match = RE_SKILL_LEVEL.search(name)
                if match:
                    skill = {
                        "name": RE_SKILL_CLEAN.sub("", RE_SKILL_LEVEL.sub("", name).strip()),
                        "level": match.group("level"),
                    }
                else:
                    skill = {"name": RE_SKILL_CLEAN.sub("", name.strip())}
                skills.append(skill)
            all_skills.extend(skills)
        elif len(split_line) == 2:
            name, keywords = split_line
            keywords_split = RE_SKILL_KEYWORD_DELIM.split(keywords)
            if len(keywords_split) == 1:
                keywords_split = keywords.split()
            skill = {
                "name": RE_SKILL_CLEAN.sub("", name.strip()),
                "keywords": [RE_SKILL_CLEAN.sub("", kw) for kw in keywords_split]
            }
            all_skills.append(skill)
    return all_skills
