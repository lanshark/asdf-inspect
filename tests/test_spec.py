import pytest

from asdf_inspect.exceptions import SpecParseError, UnsupportedImplementation
from asdf_inspect.spec import ASDFPythonSpec, Implementation

from tests.testlib import spec_fixture


@pytest.mark.parametrize('actual,expected', [(
    ASDFPythonSpec.from_string_spec(spec_dict['string_spec']),
    ASDFPythonSpec(
        spec_dict['string_spec'],
        Implementation(spec_dict['implementation']),
        spec_dict['version'],
    ),
) for spec_dict in spec_fixture['specs']])
def test_python_spec(actual, expected):
    assert actual == expected


@pytest.mark.parametrize('raise_exception', [False, True])
def test_is_supported(raise_exception):
    spec = ASDFPythonSpec.from_string_spec('3.10.3')

    result = spec.is_supported(raise_exception=raise_exception)

    assert result is True


def test_is_not_supported():
    spec = ASDFPythonSpec.from_string_spec('unsupported-3.10.3')

    result = spec.is_supported()

    assert result is False


def test_is_not_supported_raise_exception():
    spec = ASDFPythonSpec.from_string_spec('unsupported-3.10.3')

    with pytest.raises(UnsupportedImplementation):
        spec.is_supported(raise_exception=True)


@pytest.mark.parametrize('string_spec', ['3.x', '3.12.1.4', '3.12foo'])
def test_parse_error(string_spec):
    with pytest.raises(SpecParseError):
        ASDFPythonSpec.from_string_spec(string_spec)


@pytest.mark.parametrize('string_spec,expected', [
    ('3.12.1', {
        'string_spec': '3.12.1',
        'implementation': 'cpython',
        'version': '3.12.1',
    }),
    ('pypy3.10-7.3.17', {
        'string_spec': 'pypy3.10-7.3.17',
        'implementation': 'unsupported',
        'version': None,
    }),
])
def test_to_dict(string_spec, expected):
    assert ASDFPythonSpec.from_string_spec(string_spec).to_dict() == expected


def test_parse_error_empty():
    with pytest.raises(SpecParseError, match='^invalid spec: empty string$'):
        ASDFPythonSpec.from_string_spec('')


def test_parse_error_message_includes_spec():
    with pytest.raises(SpecParseError, match=r"^invalid spec: '3\.x'$"):
        ASDFPythonSpec.from_string_spec('3.x')


def test_unsupported_message_includes_spec():
    spec = ASDFPythonSpec.from_string_spec('pypy3.10-7.3.17')
    message = (
        r"^unsupported implementation: 'pypy3\.10-7\.3\.17' "
        r"\(only CPython is currently supported\)$")

    with pytest.raises(UnsupportedImplementation, match=message):
        spec.is_supported(raise_exception=True)


@pytest.mark.parametrize('string_spec', [
    '10.0', '10.1.2', '12.0a1', '10.0-dev',
])
def test_multi_digit_major(string_spec):
    spec = ASDFPythonSpec.from_string_spec(string_spec)

    assert spec.implementation == Implementation.CPYTHON
    assert spec.version == string_spec
