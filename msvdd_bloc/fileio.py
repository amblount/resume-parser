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


def save_json(filepath, data, *, lines=False):
    """
    Save ``data`` to disk at ``filepath`` as a JSON file.

    Args:
        filepath (str)
        data (List[dict])
        lines (bool)
    """
    with io.open(filepath, mode="wt", encoding="utf-8") as f:
        if lines is False:
            json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            for item in data:
                f.write(json.dumps(item) + "\n")


def load_json(filepath, *, lines=False):
    """
    Load JSON data stored to disk at ``filepath`.

    Args:
        filepath (str)
        lines (bool)

    Yields:
        object: Next JSON item
    """
    with io.open(filepath, mode="rt", encoding="utf-8") as f:
        if lines is False:
            yield json.load(f)
        else:
            for line in f:
                yield json.loads(line)


def save_text(filepath, data, *, lines=False):
    """
    Save ``data`` to disk at ``filepath`` as a JSON file.

    Args:
        filepath (str)
        data (List[dict])
        lines (bool)
    """
    with io.open(filepath, mode="wt", encoding="utf-8") as f:
        if lines is False:
            f.write(data)
        else:
            for item in data:
                f.write(item + "\n")


def load_text(filepath, *, lines=False):
    """
    Load text data stored to disk at ``filepath`.

    Args:
        filepath (str)
        lines (bool)

    Yields:
        str: Next (line of) text to read in.
    """
    with io.open(filepath, mode="rt", encoding="utf-8") as f:
        if lines is False:
            yield f.read()
        else:
            for line in f:
                yield line.strip()


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
