#!/usr/bin/env python
"""
Script for generating a résumés dataset. From a directory of résumé .pdf, extract and
clean up texts, then save the collection of .txt files in a compressed .zip archive.

To reproduce the two datasets used in the Microsoft Virtual Data Dive (2019-10-06):

.. code-block::

    $ python scripts/generate_resume_dataset.py --in_dirpath /path/to/data/resumes/fellows --out_filepath ./data/resumes/fellows_resumes.zip --fname_prefix fellows --min_text_len 150 --locale en_US --remove_pii
    $ python scripts/generate_resume_dataset.py --in_dirpath /path/to/data/resumes/bonus --out_filepath ./data/resumes/bonus_resumes.zip --fname_prefix bonus --min_text_len 150 --locale en_US --remove_pii
"""
import argparse
import logging
import pathlib
import sys

from faker import Faker

import msvdd_bloc
from msvdd_bloc import regexes


logging.basicConfig(
    format="%(name)s : %(asctime)s : %(levelname)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
LOGGER = logging.getLogger("generate_resumes_dataset")
logging.getLogger("pdfminer").setLevel(logging.WARNING)  # shush, pdfminer


def main():
    parser = argparse.ArgumentParser(
        description=(
            "From a directory of résumé .pdf files, extract and clean up texts, "
            "then save the collection of .txt files in a compressed .zip archive."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    add_arguments(parser)
    args = parser.parse_args()

    filepaths = msvdd_bloc.fileio.get_filepaths(args.in_dirpath, ".pdf")
    LOGGER.info("found %s PDF files in %s", len(filepaths), args.in_dirpath)

    faker = Faker(locale=args.locale)

    text_files = []
    for i, filepath in enumerate(filepaths):
        text = msvdd_bloc.resumes.extract_text_from_pdf(filepath, min_len=args.min_text_len)
        if not text:
            LOGGER.warning("unable to extract text from %s", filepath)
            continue

        text = msvdd_bloc.resumes.clean_fellows_text(text)
        if args.remove_pii is True:
            text = replace_pii(text, faker=faker)
        if args.fname_prefix:
            fname = "{prefix}_resume_{i}.txt".format(prefix=args.fname_prefix, i=i)
        else:
            fname = "resume_{i}.txt".format(i=i)
        text_files.append((fname, text))

    msvdd_bloc.fileio.save_text_files_to_zip(args.out_filepath, text_files)
    LOGGER.info("saved %s text files to %s", len(text_files), args.out_filepath)
    return 0


def add_arguments(parser):
    """
    Add arguments to ``parser``, modifying it in-place.

    Args:
        parser (:class:`argparse.ArgumentParser`)
    """
    parser.add_argument(
        "--in_dirpath", type=pathlib.Path, required=True,
        help="path to directory on disk in which résumé PDFs are saved",
    )
    parser.add_argument(
        "--out_filepath", type=pathlib.Path, required=True,
        help="path to zip file on disk into which extracted text files are saved",
    )
    parser.add_argument(
        "--fname_prefix", type=str, default=None,
        help="if specified, a prefix added to the filename of each extracted text file",
    )
    parser.add_argument(
        "--min_text_len", type=int, default=150,
        help="minimum number of characters in an extracted text for it to be accepted",
    )
    parser.add_argument(
        "--remove_pii", action="store_true", default=False,
        help="if specified, remove personally-identifying information from extracted texts "
             "and replace it with fake data appropriate for ``locale``",
    )
    parser.add_argument(
        "--locale", type=str, default="en_US",
        help="locale in which fake data for replacing PII is localized",
    )


def replace_pii(text, *, faker=None):
    """
    Replace personally-identifying information in ``text``
    with randomly generated fake equivalents.

    Args:
        text (str)
        faker (:class:`Faker`)

    Returns:
        str
    """
    if faker is None:
        faker = Faker(locale="en_US")
    # let's start with names, which are usually on the first line
    first_line, *the_rest = text.split("\n", maxsplit=1)
    first_line = regexes.RE_NAME.sub(faker.name(), first_line.strip())
    text = "\n".join([first_line] + the_rest)
    # next, let's replace emails, urls, and addresses
    # which are usually in the first "chunk" of info
    first_chunk = text[:150]
    the_rest = text[150:]
    first_chunk = regexes.RE_PHONE_NUMBER.sub(faker.phone_number(), first_chunk)
    first_chunk = regexes.RE_EMAIL.sub(faker.email(), first_chunk)
    first_chunk = regexes.RE_URL.sub(faker.url(), first_chunk)
    first_chunk = regexes.RE_STREET_ADDRESS.sub(faker.address().replace("\n", " "), first_chunk)
    text = first_chunk + the_rest
    return text


if __name__ == "__main__":
    sys.exit(main())
