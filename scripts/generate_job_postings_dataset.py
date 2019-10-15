#!/usr/bin/env python
"""
Script for generating a job postings dataset.

To reproduce (something close to) the three datasets used in the Microsoft Virtual
Data Dive (2019-10-06):

.. code-block::

    $ python scripts/generate_job_postings_dataset.py --source github --out_filepath ./data/postings/test_github_jobs.json --limit 100 --queries "web developer" "front-end developer" "back-end developer" "full-stack developer" "python" "data scientist" "data engineer" --locations "New York, NY" "Chicago, IL" "San Francisco, CA" "San Jose, CA" "Los Angeles, CA" "Seattle, WA" "Austin, TX" "Washington, DC" "Baltimore, MD" "Boston, MA"
    $ python scripts/generate_job_postings_dataset.py --source indeed --out_filepath ./data/postings/test_indeed_jobs.json --limit 100 --queries "web developer" "front-end developer" "back-end developer" "full-stack developer" "python" "data scientist" "data engineer" --locations "New York, NY" "Chicago, IL" "San Francisco, CA" "San Jose, CA" "Los Angeles, CA" "Seattle, WA" "Austin, TX" "Washington, DC" "Baltimore, MD" "Boston, MA" --publisher_id PUBLISHER_ID
    $ python scripts/generate_job_postings_dataset.py --source themuse --out_filepath ./data/postings/test_themuse_jobs.json --limit 100 --queries "Engineering" "Data Science" --locations "New York, NY" "Chicago, IL" "San Francisco, CA" "San Jose, CA" "Los Angeles, CA" "Seattle, WA" "Austin, TX" "Washington, DC" "Baltimore, MD" "Boston, MA"
"""
import argparse
import itertools
import logging
import pathlib
import re
import sys
import time

import requests

import msvdd_bloc


logging.basicConfig(
    format="%(name)s : %(asctime)s : %(levelname)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
LOGGER = logging.getLogger("generate_job_postings_dataset")

DUPE_KEYS = {
    "github": "id",
    "indeed": "jobkey",
    "themuse": "id",
}
"""Dict[str, str]: Keys on job postings used to deduplicate results."""


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Fetch job postings from a specified source matching query criteria, "
            "then save the deduplicated set of results in a .json file."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    add_arguments(parser)
    args = parser.parse_args()

    args.out_filepath = args.out_filepath.resolve()
    if args.source == "indeed" and args.user_ip is None:
        args.user_ip = requests.get("https://api.ipify.org").text

    LOGGER.info("fetching job postings from %s...", args.source)

    all_job_postings = []
    for query, location in itertools.product(args.queries, args.locations or [None]):
        LOGGER.info("query=%s, location=%s", query, location)
        try:
            if args.source == "github":
                results = msvdd_bloc.job_postings.fetch_from_github(
                    query=query, location=location, limit=args.limit)
            elif args.source == "indeed":
                results = msvdd_bloc.job_postings.fetch_from_indeed(
                    args.publisher_id, args.user_id,
                    query=query, location=location, limit=args.limit,
                )
            elif args.source == "themuse":
                results = msvdd_bloc.job_postings.fetch_from_themuse(
                    category=query, location=location, limit=args.limit)
            else:
                raise ValueError("source='{}' is invalid".format(args.source))
            all_job_postings.extend(results)
            time.sleep(0.1)
        except Exception:
            break

    job_postings = msvdd_bloc.utils.dedupe_results(all_job_postings, DUPE_KEYS[args.source])
    LOGGER.info("fetched %s job postings", len(job_postings))
    msvdd_bloc.fileio.save_json(args.out_filepath, job_postings)
    LOGGER.info("saved results to %s", args.out_filepath)


def add_arguments(parser):
    """
    Add arguments to ``parser``, modifying it in-place.

    Args:
        parser (:class:`argparse.ArgumentParser`)
    """
    parser.add_argument(
        "--source", type=str, required=True, choices=["github", "indeed", "themuse"],
        help="source from which job postings matching queries are fetched",
    )
    parser.add_argument(
        "--out_filepath", type=pathlib.Path, required=True,
        help="path to JSON file on disk into which fetched job postings are saved",
    )
    parser.add_argument(
        "--queries", type=str, nargs="+", required=True,
        help="search terms, like 'python' or 'data', by which to filter results",
    )
    parser.add_argument(
        "--locations", type=str, nargs="+", required=False,
        help="one or more place names, like 'New York, NY', by which to filter results",
    )
    parser.add_argument(
        "--limit", type=int, default=100,
        help="maximum number of results to fetch per (query, location) pair",
    )
    parser.add_argument(
        "--publisher_id", type=str, default=None,
        help="publisher ID (basically, an API key), required if ``source`` is 'indeed'",
    )
    parser.add_argument(
        "--user_ip", type=str, default=None,
        help="user's external IP address, required if ``source`` is 'indeed'. "
             "note: if not specified, IP address is fetched from https://api.ipify.org."
    )


if __name__ == "__main__":
    sys.exit(main())
