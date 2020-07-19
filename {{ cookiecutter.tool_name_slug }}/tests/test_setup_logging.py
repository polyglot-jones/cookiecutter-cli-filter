from {{ cookiecutter.tool_name_slug }}.core.logger import setup_logging


def test_setup_logging_good_name():
    assert setup_logging("blah") is None


def test_setup_logging_null_name():
    
    with pytest.raises(AssertionError):
        setup_logging(None)


def test_setup_logging_invalid_name():
    with pytest.raises(AssertionError):
        setup_logging(dict())
