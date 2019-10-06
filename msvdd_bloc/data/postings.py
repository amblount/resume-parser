import logging

import requests

from . import utils

LOGGER = logging.getLogger(__name__)


_THEMUSE_CATEGORIES = (
    "Account Management",
    "Business & Strategy",
    "Creative & Design",
    "Customer Service",
    "Data Science",
    "Editorial",
    "Education",
    "Engineering",
    "Finance",
    "Fundraising & Development",
    "Healthcare & Medicine",
    "HR & Recruiting",
    "Legal",
    "Marketing & PR",
    "Operations",
    "Project & Product Management",
    "Retail",
    "Sales",
    "Social Media & Community",
)


def fetch_from_github(*, query, location=None, limit=None):
    """
    Args:
        query (str): A search term, such as "ruby" or "java".
        location (str): A place name, like "New York, NY".
        limit (int): Maximum number of results to return.

    Returns:
        List[dict]
    """
    base_url = "https://jobs.github.com/positions.json"
    params = {"description": query}
    if location:
        params["location"] = location
    results = []
    i = 0
    while True:
        page_params = params.copy()
        page_params["page"] = i
        try:
            response = requests.get(base_url, params=page_params)
            response.raise_for_status()
        except requests.RequestException:
            LOGGER.exception("unable to fetch github jobs")
            break
        page_results = response.json()
        results.extend(page_results)
        i += 1
        if len(page_results) < 50:
            break
        elif limit is not None and len(results) > limit:
            break
    if limit is not None:
        return results[:limit]
    else:
        return results


def fetch_from_indeed(publisher_id, user_ip, *, query, location=None, limit=None):
    """
    Args:
        publisher_id (str)
        user_ip (str)
        query (str): A search term, such as "ruby" or "java".
        location (str): A place name, like "New York, NY".
        limit (int): Maximum number of results to return.

    Returns:
        List[dict]
    """
    base_url = "http://api.indeed.com/ads/apisearch"
    results_per_page = 25
    params = {
        "publisher": publisher_id,
        "userip": user_ip,
        "useragent": "blocbot python/v1",
        "v": 2,
        "format": "json",
        "filter": 1,
        "limit": results_per_page,  # not the same as `limit` kwarg
    }
    params["q"] = query
    if location:
        params["l"] = location
    start = 0
    results = []
    while True:
        page_params = params.copy()
        page_params["start"] = start
        try:
            response = requests.get(base_url, params=page_params)
            response.raise_for_status()
        except requests.RequestException:
            LOGGER.exception("unable to fetch indeed jobs")
            break
        page_results = response.json().get("results", [])
        results.extend(page_results)
        start += results_per_page
        if len(page_results) < results_per_page:
            break
        elif limit is not None and len(results) > limit:
            break
    if limit is not None:
        results = results[:limit]

    detailed_results = []
    job_keys = [result["jobkey"] for result in results]
    base_url = "http://api.indeed.com/ads/apigetjobs"
    params = {
        "publisher": publisher_id,
        "userip": user_ip,
        "v": 2,
        "format": "json",
    }
    for job_keys_chunk in utils.chunk_items(job_keys, 10):
        chunk_params = params.copy()
        chunk_params["jobkeys"] = ",".join(job_key for job_key in job_keys_chunk)
        try:
            response = requests.get(base_url, params=chunk_params)
            response.raise_for_status()
        except requests.RequestException:
            LOGGER.exception("unable to fetch indeed jobs details")
            break
        chunk_results = response.json().get("results", [])
        detailed_results.extend(chunk_results)
    return detailed_results


def fetch_from_themuse(*, category, location=None, limit=None):
    """
    Args:
        category (str): Job category for which to search.
        location (str): A place name, like "New York, NY".
        limit (int): Maximum number of results to return.

    Returns:
        List[dict]
    """
    if category not in _THEMUSE_CATEGORIES:
        raise ValueError(
            "category={} is invalid; valid values are {}".format(
                category, _THEMUSE_CATEGORIES)
        )
    base_url = "https://www.themuse.com/api/public/jobs"
    params = {"category": category}
    if location:
        params["location"] = location
    results = []
    i = 0
    while True:
        page_params = params.copy()
        page_params["page"] = i
        try:
            response = requests.get(base_url, params=page_params)
            response.raise_for_status()
        except requests.RequestException:
            LOGGER.exception("unable to fetch themuse jobs")
            break
        data = response.json()
        page_results = data.get("results", [])
        results.extend(page_results)
        i += 1
        if len(page_results) < data["items_per_page"]:
            break
        elif limit is not None and len(results) > limit:
            break
    if limit is not None:
        return results[:limit]
    else:
        return results
