import argparse
import logging
import pathlib
import re
import sys

import msvdd_bloc
from msvdd_bloc.resumes.parse import utils


logging.basicConfig(
    format="%(name)s : %(asctime)s : %(levelname)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
LOGGER = logging.getLogger("label_parser_training_data")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Manually label distinct lines of tokenized text by a specified labeling scheme, "
            "then save the collection of labeled lines in a .jsonl file."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    add_arguments(parser)
    args = parser.parse_args()

    LOGGER.setLevel(args.loglevel)

    parser_module = utils.load_module_from_path(
        name="parser_module", fpath=args.module_filepath.resolve())
    training_data_fpath = parser_module.TRAINING_DATA_FPATH
    if training_data_fpath.is_file():
        labeled_lines = list(msvdd_bloc.fileio.load_json(
            training_data_fpath, lines=True))
        seen_tokenized_lines = {
            tuple(tok_text for tok_text, _ in line)
            for line in labeled_lines
        }
    else:
        labeled_lines = []
        seen_tokenized_lines = {}

    n_labeled_lines = len(labeled_lines)
    LOGGER.info("loaded %s labeled lines from %s", n_labeled_lines, training_data_fpath)

    labels = args.labels or parser_module.LABELS
    print_help(labels)

    unlabeled_lines = list(msvdd_bloc.fileio.load_text(
        args.unlabeled_data.resolve(), lines=True))
    n = len(unlabeled_lines)
    for i, line in enumerate(unlabeled_lines):
        tokens = tuple(
            tok if isinstance(tok, str) else tok.text
            for tok in utils.tokenize(line)
        )
        if not tokens:
            LOGGER.debug("line \"%s\" doesn't have any tokens; skipping...", line)
            continue
        elif tokens in seen_tokenized_lines:
            LOGGER.debug("line \"%s\" already labeled; skipping...", line)
            continue
        else:
            try:
                print("\n{}".format("-" * 64))
                print("{} / {}".format(i, n))
                labeled_line = label_line(line, tokens, labels)
            except StopIteration:
                break
        seen_tokenized_lines.add(tokens)
        labeled_lines.append(labeled_line)

    if len(labeled_lines) > n_labeled_lines:
        msvdd_bloc.fileio.save_json(training_data_fpath, labeled_lines, lines=True)
        LOGGER.info(
            "saved %s labeled lines to %s",
            len(labeled_lines), training_data_fpath,
        )
    else:
        LOGGER.info("no additional lines labeled")


def add_arguments(parser):
    """
    Add arguments to ``parser``, modifying it in-place.

    Args:
        parser (:class:`argparse.ArgumentParser`)
    """
    parser.add_argument(
        "--unlabeled_data", type=pathlib.Path, required=True,
        help="path to .txt file on disk in which unlabeled items are saved as text, "
        "where each line corresponds to a separate item",
    )
    parser.add_argument(
        "--module_filepath", type=pathlib.Path, required=True,
        help="path to .py file on disk with the set of valid labels in :obj:`LABELS` "
        "and the path to training data in :obj:`TRAINING_DATA_FPATH`",
    )
    parser.add_argument(
        "--labels", type=str, nargs="+", default=None,
        help="if desired, specify the set of valid labels to be assigned to tokens; "
        "otherwise, load labels from the module specified in `module_filepath`",
    )
    parser.add_argument(
        "--loglevel", type=int, default=logging.INFO,
        help="numeric value of logging level above which you want to see messages"
        "see: https://docs.python.org/3/library/logging.html#logging-levels",
    )


def print_help(labels):
    """
    Args:
        labels (List[str])
    """
    msg = (
    "\n"
    "================================================================\n"
    "Available labels (assign to tokens using the integer values):\n"
    "{}\n"
    "\n"
    "Type 'help' to see this message again.\n"
    "Type 'oops' if you make a mistake and want to re-label the line.\n"
    "================================================================\n"
    ).format(
        "\n".join("{} => {}".format(i, label) for i, label in enumerate(labels))
    )
    print(msg)


def label_line(line, tokens, valid_labels):
    """
    Args:
        line (str)
        tokens (List[str])
        valid_labels (List[str])

    Returns:
        List[Tuple[str, str]]
    """
    choice = _get_valid_label_line_choice(line, valid_labels)
    if choice in ("l", "label"):
        labels = _get_token_labels(tokens, valid_labels)
        labeled_line = [(token, label) for token, label in zip(tokens, labels)]
        LOGGER.debug("labeled line: %s", labeled_line)
        return labeled_line
    elif choice in ("s", "skip"):
        print("skipping...")
        return []
    elif choice in ("e", "end"):
        raise StopIteration
    else:
        # note: this shouldn't be possible :)
        raise ValueError("'{}' is an invalid choice; try again...".format(choice))


def _get_valid_label_line_choice(line, valid_labels):
    """
    Args:
        line (str)
        valid_labels (List[str])

    Returns:
        str
    """
    valid_choices = {"l", "label", "s", "skip", "e", "end", "h", "help"}
    while True:
        print("\nLINE: \"{}\"".format(line))
        choice = input("(l)abel / (s)kip / (e)nd / (h)elp: ")
        if choice not in valid_choices:
            print('"{}" is an invalid choice; try again...'.format(choice))
        elif choice in ("h", "help"):
            print_help(valid_labels)
        else:
            return choice


def _get_token_labels(tokens, valid_labels):
    """
    Args:
        tokens (List[str])
        valid_labels (List[str])

    Returns:
        List[str]
    """
    valid_label_ints = {i for i in range(len(valid_labels))}
    while True:
        print("\nTOKENS: {}".format(" | ".join(tokens)))
        label_ints = input("labels: ")
        label_ints = re.split(" +", label_ints.strip())
        if any(label_int == "oops" for label_int in label_ints):
            print("no worries; try again...")
            continue
        if label_ints[-1] == "*":
            if not 1 < len(label_ints) < len(tokens):
                print("invalid input; try again...")
                continue
            else:
                idx = label_ints.index("*")
                label_ints = (
                    label_ints[0 : idx] + [label_ints[idx - 1]] * (len(tokens) - idx)
                )
        if len(label_ints) != len(tokens):
            print("the number of labels must match the number of tokens; try again...")
            continue
        label_ints = [int(label) for label in label_ints]
        invalid_label_ints = set(label_ints).difference(valid_label_ints)
        if invalid_label_ints:
            print("invalid label(s): {}; try again...".format(invalid_label_ints))
            continue
        else:
            return [valid_labels[label_int] for label_int in label_ints]


if __name__ == "__main__":
    sys.exit(main())
