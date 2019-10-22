import argparse
import logging
import pathlib
import random
import re
import sys

import pycrfsuite

import msvdd_bloc


logging.basicConfig(
    format="%(name)s : %(asctime)s : %(levelname)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
LOGGER = logging.getLogger("train_parser")


def main():
    parser = argparse.ArgumentParser(
        description="Script to train a CRF parser on domain-specific texts.",
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

    parser_module = msvdd_bloc.resumes.parse.utils.load_module_from_path(
        name="parser_module", fpath=args.module_filepath.resolve())
    training_data_fpath = parser_module.TRAINING_DATA_FPATH
    model_fpath = parser_module.MODEL_FPATH

    all_feature_label_pairs = []
    labeled_lines = msvdd_bloc.fileio.load_json(training_data_fpath, lines=True)
    for labeled_line in labeled_lines:
        labels = [label for _, label in labeled_line]
        token_strs = [token for token, _ in labeled_line]
        tokens = parser_module.tokenize(token_strs)
        features = parser_module.featurize(tokens)
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

    trainer.train(str(model_fpath), holdout=holdout)
    LOGGER.info("saved trained model settings to %s", model_fpath)


def add_arguments(parser):
    """
    Add arguments to ``parser``, modifying it in-place.

    Args:
        parser (:class:`argparse.ArgumentParser`)
    """
    parser.add_argument(
        "--module_filepath", type=pathlib.Path, required=True,
        help="path to .py file on disk with functionality for tokenizing "
        "and featurizing items",
    )
    parser.add_argument(
        "--test_size", type=float, default=0.0,
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
