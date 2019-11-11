import collections
import re

# NOTE: the last item within the <text> group MUST NOT have a "|" operator
# otherwise it will match anything and bork matching for all sections below it
SECTION_HEADERS = {
    "basics": re.compile(
        r"^(?P<text>"
        "about|"
        "contacts?|"
        "(contact|personal) info"
        ")(?P<end>:?$)",
        flags=re.IGNORECASE,
    ),
    # "summary" section becomes a field in "basics" section
    "summary": re.compile(
        r"^(?P<text>"
        "career objective|"
        "(career|professional) summary|"
        "objective|"
        "summary"
        ")(?P<end>: |:?$)",
        flags=re.IGNORECASE,
    ),
    "work": re.compile(
        r"^(?P<text>"
        "(additional|leadership|professional|relevant|work) experiences?|"
        "employment|"
        "experiences?|"
        "leadership|"
        "leadership (and|&) service|"
        "professional development|"
        "work (and|&) (research|technical) experiences?"
        ")(?P<end>:?$)",
        flags=re.IGNORECASE,
    ),
    "volunteer": re.compile(
        r"^(?P<text>"
        "community service|"
        "volunteer experiences?|"
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
    # "courses" section becomes a field in "education" section
    "courses": re.compile(
        r"^(?P<text>"
        "course ?work|"
        "courses completed|"
        "(recent|related|relevant|undergraduate) courses|"
        "(recent|related|relevant) course ?work"
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
        "(relevant|soft|special|technical|technological) skills(et)?|"
        "technical strengths|"
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
        "extracurriculars|"
        "extracurricular activities|"
        "fellowships (and|&) clubs|"
        "(github|other|programming|recent|side|technical) projects|"
        "interests|"
        "projects"
        ")(?P<end>:?$)",
        flags=re.IGNORECASE,
    ),
    "ambiguous": re.compile(
        r"^(?P<text>"
        "activities (and|&) honors|"
        "affiliations|"
        "awards, activities,? (and|&) additional skills|"
        "campus involvement|"
        "certifications|"
        "community involvement|"
        "involvement|"
        "involvement (and|&) achievements|"
        "leadership (and|&) activities|"
        "leadership (and|&) affiliations|"
        "miscellaneous|"
        "organizations|"
        "organizations (and|&) awards|"
        "programs (and|&) affiliations|"
        "skills (and|&) activities|"
        "skills (and|&) interests|"
        "skills, activities,? (and|&) interests|"
        "technical skills (and|&) interests|"
        "unique qualities"
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
"""
Dict[str, :class:`re.Pattern`]: Mapping of section name to compiled regex pattern
that matches header lines indicating the start of the corresponding section.
"""


def get_section_lines(lines):
    """
    Parse a sequence of text lines from a résumé into a mapping of section name
    to corresponding lines.

    Args:
        List[str]: Cleaned and filtered résumé text lines, as output by
            :func:`resumes.munge.get_filtered_text_lines()`.

    Returns:
        Dict[str, List[str]]
    """
    section_lines = collections.defaultdict(list)
    curr_section = "start"
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
