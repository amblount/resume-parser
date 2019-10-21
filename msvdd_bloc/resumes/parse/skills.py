import logging
import re


LOGGER = logging.getLogger(__name__)

RE_SKILL_NAME_DELIM = re.compile(r"(?:: +| +[-–] +)")
RE_SKILL_KEYWORD_DELIM = re.compile(r"[,;] +(?:(?:and|&) +)?")
RE_SKILL_LEVEL = re.compile(
    r"\(?(?P<level>advanced|intermediate|beginner|basic|proficient|exposed)\)? ?(in )?",
    flags=re.UNICODE | re.IGNORECASE,
)
RE_SKILL_CLEAN = re.compile(r"[.,;]$")


def parse_skills_section(lines):
    """
    Parse a sequence of text lines belonging to the "skills" section of a résumé
    to produce structured data in the form of :class:`schemas.ResumeSkillSchema`.

    Args:
        lines (List[str])

    Returns:
        List[Dict[str, str]]
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
