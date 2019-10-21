import argparse
import logging
import pathlib
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
        description=(
            "TODO"
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    add_arguments(parser)
    args = parser.parse_args()

    LOGGER.setLevel(args.loglevel)

    trainer = pycrfsuite.Trainer(verbose=True)  # , params=params_to_set)

    parser_module = msvdd_bloc.resumes.parse.utils.load_module_from_path(
        name="parser_module", fpath=args.module_filepath.resolve())
    training_data_fpath = parser_module.TRAINING_DATA_FPATH
    model_fpath = parser_module.MODEL_FPATH

    labeled_lines = msvdd_bloc.fileio.load_json(training_data_fpath, lines=True)
    for labeled_line in labeled_lines:
        labels = [label for _, label in labeled_line]
        token_strs = [token for token, _ in labeled_line]
        tokens = parser_module.tokenize(token_strs)
        features = parser_module.featurize(tokens)
        trainer.append(features, labels)

    trainer.train(str(model_fpath))
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
        "--loglevel", type=int, default=logging.INFO,
        help="numeric value of logging level above which you want to see messages"
        "see: https://docs.python.org/3/library/logging.html#logging-levels",
    )


if __name__ == "__main__":
    sys.exit(main())
