import sys, io

from {{ cookiecutter.tool_name_slug }}.__main__ import main


def test_{{ cookiecutter.tool_name_slug }}___main__good():
    with io.StringIO() as fake_stderr:
        sys.argv = [sys.argv[0], "-h"]
        orig_stderr = sys.stderr
        sys.stderr = fake_stderr

        with pytest.raises(SystemExit) as e:
            main()
            assert str(e.value) == '0'
            assert 'Usage: info [OPTIONS] ' in sys.stderr.getvalue()
        sys.stderr = orig_stderr
