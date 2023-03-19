import pytest

from asdf_inspect.exceptions import UnsupportedImplementation
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
