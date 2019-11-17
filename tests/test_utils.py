import pytest

from msvdd_bloc import utils


def test_to_collection():
    inputs_outputs = [
        [(1, int, list), [1]],
        [([1, 2], int, tuple), (1, 2)],
        [((1, 1.0), (int, float), set), {1, 1.0}],
    ]
    assert utils.to_collection(None, int, list) is None
    for input_, output in inputs_outputs:
        assert utils.to_collection(*input_) == output


def test_dedupe_results():
    results = [
        {"id": 1, "key1": "a", "key2": "b"},
        {"id": 2, "key1": "c", "key2": "b"},
        {"id": 3, "key1": "a", "key2": "d"},
    ]
    for dupe_key in ["key1", "key2"]:
        deduped_results = utils.dedupe_results(results, dupe_key)
        assert deduped_results
        assert len(deduped_results) <= len(results)
        assert len(set(result[dupe_key] for result in results)) == len(deduped_results)
