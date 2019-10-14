import logging
import re
import unicodedata

import bs4
import dateutil.parser
import ftfy

from .. import regexes

LOGGER = logging.getLogger(__name__)


def munge_job_posting_github(data):
    """
    Args:
        data (Dict[str, obj])

    Returns:
        Dict[str, obj]
    """
    return {
        "title": data.get("title"),
        "company": data.get("company"),
        "date_posted": munge_date_posted(data.get("created_at")),
        "location": munge_location_github(data.get("location")),
        "url": data.get("url"),
        "employment_type": munge_employment_type_github(data.get("type")),
        "description": munge_description(data.get("description"), html=True),
    }


def munge_job_posting_indeed(data):
    """
    Args:
        data (Dict[str, obj])

    Returns:
        Dict[str, obj]
    """
    return {
        "title": data.get("jobtitle"),
        "company": data.get("company"),
        "date_posted": munge_date_posted(data.get("date")),
        "location": munge_location_indeed(data.get("formattedLocation")),
        "url": data.get("url"),
        "description": munge_description(data.get("snippet"), html=False),
    }


def munge_job_posting_themuse(data):
    """
    Args:
        data (Dict[str, obj])

    Returns:
        Dict[str, obj]
    """
    return {
        "title": data.get("name"),
        "company": munge_company_themuse(data.get("company")),
        "date_posted": munge_date_posted(data.get("publication_date")),
        "location": munge_location_themuse(data.get("locations")),
        "url": munge_url_themuse(data.get("refs")),
        "description": munge_description(data.get("contents"), html=True),
        "industry": munge_industry_themuse(data.get("categories")),
    }


def munge_company_themuse(value):
    """
    Args:
        value (Dict[str, obj])

    Returns:
        str
    """
    if not value:
        return None
    else:
        return value.get("name")


def munge_date_posted(value):
    """
    Args:
        value (str)

    Returns:
        str
    """
    if not value:
        return None
    else:
        return dateutil.parser.parse(value).date().isoformat()


def munge_description(value, *, html=False):
    """
    Args:
        value (str)
        html (bool)

    Returns:
        str
    """
    if not value:
        return None
    else:
        if html is True:
            value = bs4.BeautifulSoup(value, "html.parser").get_text()
            value = unicodedata.normalize("NFKD", value)
        value = ftfy.fix_text(value).strip()
        return value


def munge_location_github(value):
    """
    Args:
        value (str)

    Returns:
        List[str]
    """
    if not value:
        return None
    else:
        # no zip codes, thanks!
        value = regexes.RE_ZIP_CODE.sub("", value).strip()
        # split multiple locations on common delimiters
        # punct-based delimiters
        if ";" in value:
            value = re.split(r" ?; +", value)
        # word-based delimiters
        elif " & " in value or " or " in value or " and " in value:
            value = re.split(r" +(?:or|and|&) +", value)
        # HACK: ambiguous comma usage?
        elif value.count(", ") > 1 and not value.endswith("USA"):
            value = re.split(", +", value)
        else:
            value = [value]
        return value


def munge_location_indeed(value):
    """
    Args:
        value (str)

    Returns:
        List[str]
    """
    if not value:
        return None
    else:
        return [value]


def munge_location_themuse(value):
    """
    Args:
        value (List[Dict[str, str]])

    Returns:
        List[str]
    """
    if not value:
        return None
    else:
        return [item["name"] for item in value if item.get("name")]


def munge_employment_type_github(value):
    """
    Args:
        value (str)

    Returns:
        str
    """
    if not value:
        return None
    else:
        value = value.lower().replace(" ", "-")
        return value


def munge_url_themuse(value):
    """
    Args:
        value (Dict[str, str])

    Returns:
        str
    """
    if not value:
        return None
    else:
        return value.get("landing_page")


def munge_industry_themuse(value):
    """
    Args:
        value (List[Dict[str, str]])

    Returns:
        str
    """
    if not value:
        return None
    else:
        return "; ".join(item["name"] for item in value if item.get("name"))
