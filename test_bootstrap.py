import bootstrap


def test_render_path(tmpdir):
    path = tmpdir / "___test___"
    path.mkdir()
    path = path / "___dir___"
    path.mkdir()

    values = {"test": "subdir1", "dir": "subdir2"}
    bootstrap.render_paths({str(path)}, values)

    subdir = tmpdir.listdir()[0]
    print(subdir)
    assert str(subdir) == str(tmpdir / "subdir1")

    subdir = subdir.listdir()[0]
    assert str(subdir) == str(tmpdir / "subdir1" / "subdir2")


def test_main():
    assert bootstrap.main() == 0
