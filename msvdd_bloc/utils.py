"""
utils
-----
"""


def to_collection(val, val_type, col_type):
    """
    Validate and cast a value or values to a collection.

    Args:
        val (object): Value or values to validate and cast.
        val_type (type): Type of each value in collection, e.g. ``int`` or ``str``.
        col_type (type): Type of collection to return, e.g. ``tuple`` or ``set``.

    Returns:
        object: Collection of type ``col_type`` with values all of type ``val_type``.

    Raises:
        TypeError
    """
    if val is None:
        return None
    if isinstance(val, val_type):
        return col_type([val])
    elif isinstance(val, (tuple, list, set, frozenset)):
        if not all(isinstance(v, val_type) for v in val):
            raise TypeError("not all values are of type {}".format(val_type))
        return col_type(val)
    else:
        raise TypeError(
            "values must be {} or a collection thereof, not {}".format(
                val_type, type(val),
            )
        )


def dedupe_results(results, dupe_key):
    """
    Filter out items in ``results`` with the same ``dupe_key`` value, keeping only
    the first instance.

    Args:
        results ((List[dict]))
        dupe_key (str)

    Returns:
        List[dict]
    """
    unique_results = []
    seen_keys = set()
    for result in results:
        if result[dupe_key] in seen_keys:
            continue
        else:
            seen_keys.add(result[dupe_key])
            unique_results.append(result)
    return unique_results


def chunk_items(items, chunk_size):
    """
    Yield successive chunks of items.

    Args:
        items (list or tuple)
        chunk_size (int)

    Yields:
        list or tuple
    """
    for i in range(0, len(items), chunk_size):
        yield items[i : min(i + chunk_size, len(items))]
