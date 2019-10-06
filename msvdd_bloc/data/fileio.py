import io
import json
import zipfile


def get_filepaths(dirpath, suffix):
    """
    Get full paths to all files under ``dirpath`` with a file type like ``suffix``.

    Args:
        dirpath (:class:`pathlib.Path`)
        suffix (str or Set[str])

    Returns:
        List[str]
    """
    if isinstance(suffix, str):
        suffix = {suffix}
    return sorted(
        str(path) for path in dirpath.resolve().iterdir()
        if path.is_file() and path.suffix in suffix
    )


def save_json(filepath, data):
    """
    Save ``data`` to disk at ``filepath`` as a JSON file.

    Args:
        filepath (str)
        data (List[dict])
    """
    with io.open(filepath, mode="wt", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_text_files_to_zip(filepath, text_files):
    """
    Args:
        filepath (str)
        text_files (Sequence[Tuple[str, str]])
    """
    with zipfile.ZipFile(filepath, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for fname, text in text_files:
            zf.writestr(fname, text)


def load_text_files_from_zip(filepath):
    """
    Args:
        filepath (str)

    Yields:
        Tuple[str, str]
    """
    with zipfile.ZipFile(filepath, mode="r") as zf:
        for member in zf.infolist():
            with zf.open(member, mode="r") as f:
                text = f.read().decode("utf-8")
                yield (member.filename, text)
