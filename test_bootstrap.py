import io

import pytest

import bootstrap


@pytest.fixture
def path(tmpdir):
    path = tmpdir / "___test___"
    path.mkdir()
    path = path / "___dir___"
    path.mkdir()
    return path


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


def test_traverse_repo(path, file):
    root = file.parent
    (root / ".git").mkdir()
    subdir = root / "___subdir___"
    subdir.mkdir()
    (root / "no_match.txt").write_text("No match here")

    bootstrap.traverse_repo(str(root))

    assert {"dir", "test", "subdir", "var1", "var2"} == bootstrap.variables
    assert {str(path), str(subdir)} == bootstrap.file_paths
    assert {str(file): {"var1", "var2"}} == bootstrap.file_contents


def test_traverse_repo_binary_file():
    pass


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


def test_render_paths(path, tmpdir):
    values = {"test": "subdir1", "dir": "subdir2"}

    bootstrap.render_paths({str(path)}, values)

    subdir = tmpdir.listdir()[0]
    assert str(subdir) == str(tmpdir / "subdir1")

    subdir = subdir.listdir()[0]
    assert str(subdir) == str(tmpdir / "subdir1" / "subdir2")


def test_create_github_repo():
    pass


def test_push_to_github():
    pass
