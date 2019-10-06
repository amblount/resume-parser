import io
import json


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


def save_data_to_disk(data, filepath):
    """
    Save ``data`` to disk at ``filepath`` as a JSON file.

    Args:
        data (List[dict])
        filepath (str)
    """
    with io.open(filepath, mode="wt", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
