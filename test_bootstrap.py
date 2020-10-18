import io
import os

import pytest

import bootstrap


@pytest.fixture
def directory(tmpdir):
    root = tmpdir

    subdir_1 = root / "___subdir1___"
    subdir_1.mkdir()

    test_file = subdir_1 / "___test___.txt"
    test_file.write_text(" ", "utf-8")

    subdir_2 = subdir_1 / "___subdir2___"
    subdir_2.mkdir()

    return test_file, subdir_2


@pytest.fixture
def file(tmp_path):
    path = tmp_path / "test_file.txt"
    file_contents = (
        "Lorem ipsum ___var1___ sit amet, consectetur adipiscing elit, sed do eiusmod "
        "tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, "
        "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo "
        "consequat. Duis aute irure ___var1___ in reprehenderit in voluptate velit "
        "esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat "
        "cupidatat non proident, sunt in ___var2___ qui officia deserunt mollit anim "
        "id est laborum."
    )
    path.write_text(file_contents)
    return path


def test_traverse_repo(directory, file):
    root = file.parent
    (root / ".git").mkdir()
    (root / "no_match.txt").write_text("No match here")
    (root / "test_file").write_bytes(os.urandom(100))

    test_file, subdir = directory

    bootstrap.traverse_repo(str(root))

    assert {"subdir1", "test", "subdir2", "var1", "var2"} == bootstrap.variables
    assert {str(test_file), str(subdir)} == bootstrap.file_paths
    assert {str(file): {"var1", "var2"}} == bootstrap.file_contents


def test_inquire(capsys, monkeypatch):
    variables = {"var1", "var2"}
    values = io.StringIO("val1\nval2\n")
    monkeypatch.setattr("sys.stdin", values)

    res = bootstrap.inquire(variables)

    out, _ = capsys.readouterr()
    if "var1: var2: " in out:
        expected = {
            "var1": "val1",
            "var2": "val2",
        }
    else:
        expected = {
            "var2": "val1",
            "var1": "val2",
        }

    assert res == expected


def test_render_files(file):
    values = {"var1": "dolor", "var2": "culpa"}

    bootstrap.render_files({str(file): set(values)}, values)

    assert file.read_text() == (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
        "tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, "
        "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo "
        "consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse "
        "cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non "
        "proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    )


def test_render_paths(directory, tmpdir):
    values = {"subdir1": "subdir", "test": "file", "subdir2": "subdir_2"}

    file, dir_ = directory

    bootstrap.render_paths({str(file), str(dir_)}, values)

    assert [str(tmpdir / "subdir")] == tmpdir.listdir()
    assert sorted(
        [str(tmpdir / "subdir" / "file.txt"), str(tmpdir / "subdir" / "subdir_2")]
    ) == sorted((tmpdir / "subdir").listdir())
