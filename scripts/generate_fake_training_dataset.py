#!/usr/bin/env python
"""
Script to generate fake training datasets for a particular résumé section,
for use in training a parser via the ``train_parser.py`` script.

Examples:

.. code-block::

    $ python scripts/generate_fake_training_dataset.py --module_name "msvdd_bloc.resumes.basics" --n 5000 --augment --fixed_val_field_keys fsep isep ws
    $ python scripts/generate_fake_training_dataset.py --module_name "msvdd_bloc.resumes.education" --n 5000 --augment --fixed_val_field_keys fsep isep ws
    $ python scripts/generate_fake_training_dataset.py --module_name "msvdd_bloc.resumes.skills" --n 5000 --augment --fixed_val_field_keys grp_name_sep isep isep_and ws
"""
import argparse
import importlib
import logging
import sys

from msvdd_bloc import fileio
from msvdd_bloc.resumes import generate_utils


logging.basicConfig(
    format="%(name)s : %(asctime)s : %(levelname)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
LOGGER = logging.getLogger("generate_fake_training_dataset")


def main():
    parser = argparse.ArgumentParser(
        description="Script to generate a fake training dataset for a particular section.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    add_arguments(parser)
    args = parser.parse_args()

    LOGGER.setLevel(args.loglevel)

    module = importlib.import_module(args.module_name)

    fixed_val_field_keys = (
        set(args.fixed_val_field_keys) if args.fixed_val_field_keys else None
    )
    all_labeled_tokens = list(
        generate_utils.generate_labeled_tokens(
            module.generate.TEMPLATES,
            module.generate.FIELDS,
            n=args.n,
            fixed_val_field_keys=fixed_val_field_keys,
        )
    )
    LOGGER.info(
        "%s fake '%s' examples generated:\n%s ...",
        args.n, args.module_name, all_labeled_tokens[:1],
    )
    if args.augment is True:
        try:
            all_labeled_tokens = [
                module.augment.AUGMENTER.apply(labeled_tokens)
                for labeled_tokens in all_labeled_tokens
            ]
            LOGGER.info("data augmentation applied added to fake examples...")
        except AttributeError:
            LOGGER.warning(
                "no augmenter found at module '%s.augment.AUGMENTER'; "
                "no data augmentation applied to fake examples...",
                module,
            )
    fileio.save_json(module.FPATH_TRAINING_DATA, all_labeled_tokens, lines=True)
    LOGGER.info("fake examples saved to '%s'", module.FPATH_TRAINING_DATA)


def add_arguments(parser):
    """
    Add arguments to ``parser``, modifying it in-place.

    Args:
        parser (:class:`argparse.ArgumentParser`)
    """
    parser.add_argument(
        "--module_name", type=str, required=True,
        help="absolute name of module with functionality for featurizing tokens, "
        "as well as filepaths to training data and trained model settings, "
        "e.g. 'msvdd_bloc.resumes.basics'",
    )
    parser.add_argument(
        "--n", type=int, default=1000,
        help="number of fake examples to generate",
    )
    parser.add_argument(
        "--fixed_val_field_keys", type=str, nargs="+", default=None,
        help="one or more field keys for which a fixed (randomly-generated) value "
        "is used throughout a given fake example",
    )
    parser.add_argument(
        "--augment", action="store_true", default=False,
        help="if specified, apply data augmentation to fake examples, as specified in "
        "an `Augmenter` class, e.g. `msvdd_bloc.resumes.basics.augment.AUGMENTER()`",
    )
    parser.add_argument(
        "--loglevel", type=int, default=logging.INFO,
        help="numeric value of logging level above which you want to see messages; "
        "see: https://docs.python.org/3/library/logging.html#logging-levels",
    )


if __name__ == "__main__":
    sys.exit(main())
