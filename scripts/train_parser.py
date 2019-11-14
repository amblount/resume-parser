#!/usr/bin/env python
"""
Script to train a CRF parser based on labeled, tokenized training data -- either fake
data generated via ``generate_fake_training_dataset.py``, or real data labeled via
``label_training_dataset.py``.

Examples:

.. code-block::

    $ python scripts/generate_fake_training_dataset.py --module_name "msvdd_bloc.resumes.basics" --test_size 0.1 --params_filepath "./models/resumes/crf-model-params.json" --verbose
    $ python scripts/generate_fake_training_dataset.py --module_name "msvdd_bloc.resumes.education" --test_size 0.1 --params_filepath "./models/resumes/crf-model-params.json" --verbose
    $ python scripts/generate_fake_training_dataset.py --module_name "msvdd_bloc.resumes.skills" --test_size 0.1 --params_filepath "./models/resumes/crf-model-params.json" --verbose
"""
import argparse
import importlib
import logging
import pathlib
import random
import re
import sys

import pycrfsuite

import msvdd_bloc
from msvdd_bloc.resumes import parse_utils


logging.basicConfig(
    format="%(name)s : %(asctime)s : %(levelname)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
LOGGER = logging.getLogger("train_parser")


def main():
    parser = argparse.ArgumentParser(
        description="Script to train a CRF parser on section-specific texts.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    add_arguments(parser)
    args = parser.parse_args()

    LOGGER.setLevel(args.loglevel)

    if args.params_filepath:
        params = next(
            msvdd_bloc.fileio.load_json(args.params_filepath.resolve(), lines=False)
        )
    else:
        params = {}
    trainer = pycrfsuite.Trainer(
        algorithm=args.algorithm, params=params, verbose=args.verbose)

    module = importlib.import_module(args.module_name)

    all_feature_label_pairs = []
    labeled_lines = msvdd_bloc.fileio.load_json(module.FPATH_TRAINING_DATA, lines=True)
    for labeled_line in labeled_lines:
        labels = [label for _, label in labeled_line]
        token_strs = [token for token, _ in labeled_line]
        tokens = parse_utils.tokenize(token_strs)
        features = module.parse.featurize(tokens)
        all_feature_label_pairs.append((features, labels))

    if args.test_size == 0.0:
        holdout = -1
        for features, labels in all_feature_label_pairs:
            trainer.append(features, labels, group=0)
    else:
        holdout = 1
        for features, labels in all_feature_label_pairs:
            group = 0 if random.random() >= args.test_size else 1
            trainer.append(features, labels, group=group)

    LOGGER.info("training CRF model with the following params:\n%s", trainer.get_params())
    trainer.train(str(module.FPATH_TAGGER), holdout=holdout)
    LOGGER.info("saved trained model settings to %s", module.FPATH_TAGGER)


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
        "--test_size", type=float, default=0.1,
        help="fraction of the available training data to use as a test set, i.e. "
        "hold out from training for model evaluation purposes",
    )
    parser.add_argument(
        "--algorithm", type=str,
        choices=("lbfgs", "l2sgd", "ap", "pa", "arow"), default="lbfgs",
        help="name of the training algorithm to use when training the CRF model",
    )
    parser.add_argument(
        "--params_filepath", type=pathlib.Path, default=None,
        help="path to .json file on disk with CRF model params to replace defaults; "
        "see: https://python-crfsuite.readthedocs.io/en/latest/pycrfsuite.html#pycrfsuite.Trainer",
    )
    parser.add_argument(
        "--verbose", action="store_true", default=False,
        help="if specified, print out a lot of extra information from model training; "
        "note that this is independent of `loglevel`",
    )
    parser.add_argument(
        "--loglevel", type=int, default=logging.INFO,
        help="numeric value of logging level above which you want to see messages"
        "see: https://docs.python.org/3/library/logging.html#logging-levels",
    )


if __name__ == "__main__":
    sys.exit(main())
