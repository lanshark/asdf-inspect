import pytest

from asdf_inspect.exceptions import (
    ASDFInspectError, ParseError, PathError, SpecParseError,
    UnsupportedImplementation, VersionParseError,
)


@pytest.mark.parametrize('exc_class,message', [
    (ASDFInspectError, 'generic error'),
    (PathError, 'path error'),
    (ParseError, 'generic parse error'),
    (SpecParseError, 'spec parse error'),
    (VersionParseError, 'version parse error'),
    (UnsupportedImplementation, 'only CPython is currently supported'),
])
def test_default_message(exc_class, message):
    assert str(exc_class()) == message


def test_custom_message():
    exc = PathError('custom')

    assert str(exc) == 'custom'
    assert PathError.message == 'path error'


@pytest.mark.parametrize('exc_class', [
    PathError, ParseError, SpecParseError, VersionParseError,
    UnsupportedImplementation,
])
def test_hierarchy(exc_class):
    assert issubclass(exc_class, ASDFInspectError)
