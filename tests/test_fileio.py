import inspect
import pathlib

import pytest

from msvdd_bloc import fileio


@pytest.fixture(scope="module")
def pkg_dirpath():
    return pathlib.Path(inspect.getfile(fileio)).resolve().parent


@pytest.fixture(scope="module")
def json_data():
    return [
        {"text": "This is an example sentence."},
        {"text": "This is another example sentence."},
    ]


@pytest.fixture(scope="module")
def text_data():
    return """
    This is an example sentence.
    This is another example sentence.
    """


@pytest.fixture(scope="module")
def text_files():
    return [
        ("text1.txt", "This is an example sentence."),
        ("text2.txt", "This is another example sentence."),
    ]



class TestGetFilepaths:

    def test(self, pkg_dirpath):
        filepaths = fileio.get_filepaths(pkg_dirpath)
        assert filepaths
        assert isinstance(filepaths, list)
        assert all(isinstance(filepath, str) for filepath in filepaths)
        assert all(pathlib.Path(filepath).is_file() for filepath in filepaths)
        assert all(str(pkg_dirpath) in filepath for filepath in filepaths)

    def test_suffix(self, pkg_dirpath):
        suffixes = (
            ".py",
            (".py", ".md"),
            {".py", ".md"},
        )
        for suffix in suffixes:
            filepaths = fileio.get_filepaths(pkg_dirpath, suffix=suffix)
            assert filepaths
            if not isinstance(suffix, (str, tuple)):
                suffix = tuple(suffix)
            assert all(filepath.endswith(suffix) for filepath in filepaths)


class TestSaveLoadJson:

    def test(self, tmp_path, json_data):
        filepath = tmp_path.joinpath("test.json")
        fileio.save_json(filepath, json_data, lines=False)
        json_data_loaded = next(fileio.load_json(filepath, lines=False))
        assert json_data == json_data_loaded

    def test_lines(self, tmp_path, json_data):
        filepath = tmp_path.joinpath("test.json")
        fileio.save_json(filepath, json_data, lines=True)
        json_data_loaded = list(fileio.load_json(filepath, lines=True))
        assert json_data == json_data_loaded


class TestSaveLoadText:

    def test(self, tmp_path, text_data):
        filepath = tmp_path.joinpath("test.txt")
        fileio.save_text(filepath, text_data, lines=False)
        text_data_loaded = next(fileio.load_text(filepath, lines=False))
        assert text_data == text_data_loaded

    def test_lines(self, tmp_path, text_data):
        text_lines = text_data.split()
        filepath = tmp_path.joinpath("test.txt")
        fileio.save_text(filepath, text_lines, lines=True)
        text_lines_loaded = list(fileio.load_text(filepath, lines=True))
        assert text_lines == text_lines_loaded


class TestSaveLoadTextFilesToZip:

    def test(self, tmp_path, text_files):
        filepath = tmp_path.joinpath("test.zip")
        fileio.save_text_files_to_zip(filepath, text_files)
        text_files_loaded = list(fileio.load_text_files_from_zip(filepath))
        assert text_files == text_files_loaded
