import pytest

from asdf_inspect.exceptions import VersionParseError
from asdf_inspect.version import Version

from tests.testlib import spec_fixture


@pytest.mark.parametrize('string_version', [
    spec_dict['version']
    for spec_dict in spec_fixture['specs']
    if spec_dict['implementation'] == 'cpython'
])
def test_parse_fixture_cpython_specs(string_version):
    Version.from_string_version(string_version)


def test_parse_error():
    with pytest.raises(VersionParseError):
        Version.from_string_version('1.a.0')


@pytest.mark.parametrize('str_v1,str_v2,expected', [
    ('2.0', '2.0.0', True),
    ('2.0-dev', '2.0.0-dev', True),
    ('2.0a1', '2.0.0a1', True),
    ('2.0.1', '2.0', False),
    ('2.0', '2.0.0-dev', False),
    ('2.0a1', '2.0', False),
    ('2.0a1', '2.0a2', False),
    ('2.0a1', '2.0b1', False),
])
def test_eq_ne(str_v1, str_v2, expected):
    v1 = Version.from_string_version(str_v1)
    v2 = Version.from_string_version(str_v2)

    eq_result = v1 == v2
    ne_result = v1 != v2

    assert eq_result is expected
    assert ne_result is not expected


@pytest.mark.parametrize('str_v1,str_v2,expected', [
    ('2.0', '2.0.0', False),
    ('2.0.0', '2.0.1', True),
    ('2.0', '2.0.1', True),
    ('2.0.1', '2.0.0', False),
    ('2.0-dev', '2.0', True),
    ('2.1-dev', '2.0', False),
    ('2.0a3', '2.0', True),
    ('2.0a4', '2.0a5', True),
    ('2.0a10', '2.0a2', False),
    ('2.0.1b3', '2.0.0', False),
    ('2.0b3', '2.0a7', False),
    ('2.0a7', '2.0b3', True),
])
def test_lt_ge(str_v1, str_v2, expected):
    v1 = Version.from_string_version(str_v1)
    v2 = Version.from_string_version(str_v2)

    lt_result = v1 < v2
    ge_result = v1 >= v2

    assert lt_result is expected
    assert ge_result is not expected


@pytest.mark.parametrize('str_v1,str_v2,expected', [
    ('2.0', '2.0.0', False),
    ('2.0.0', '2.0.1', False),
    ('2.0', '2.0.1', False),
    ('2.0.1', '2.0.0', True),
    ('2.0-dev', '2.0', False),
    ('2.1-dev', '2.0', True),
    ('2.0a3', '2.0', False),
    ('2.0a4', '2.0a5', False),
    ('2.0a10', '2.0a2', True),
    ('2.0.1b3', '2.0.0', True),
    ('2.0b3', '2.0a7', True),
    ('2.0a7', '2.0b3', False),
])
def test_gt_le(str_v1, str_v2, expected):
    v1 = Version.from_string_version(str_v1)
    v2 = Version.from_string_version(str_v2)

    gt_result = v1 > v2
    le_result = v1 <= v2

    assert gt_result is expected
    assert le_result is not expected


@pytest.mark.parametrize('str_v1,str_v2,expected', [
    ('2.6.7', '2.6', True),
    ('2.6.7', '2.6.7', True),
    ('2.6', '2.6.7', False),
    ('2.6.7', '2.7', False),
    ('2.6.7-dev', '2.6', False),
    ('2.6.7', '2.6-dev', False),
    ('2.6.7-dev', '2.6-dev', False),
    ('2.6.7-dev', '2.6.7-dev', True),
    ('2.6.8-dev', '2.6.7-dev', False),
    ('2.6.7a3', '2.6', False),
    ('2.6.7a3', '2.6.7b3', False),
    ('2.6.7a3', '2.6.8a3', False),
    ('2.6.7a3', '2.6.7a3', True),
])
def test_contains(str_v1, str_v2, expected):
    v1 = Version.from_string_version(str_v1)
    v2 = Version.from_string_version(str_v2)

    result = v1 in v2

    assert result is expected


@pytest.mark.parametrize('string_version', [
    '',
    '3',
    '3.',
    'abc',
    '3.12.1.4',
    '3.12a',
    '3.12c1',
    '3.12-rc1',
    ' 3.12',
])
def test_parse_error_invalid(string_version):
    with pytest.raises(VersionParseError):
        Version.from_string_version(string_version)


@pytest.mark.parametrize('string_version,base,pre,dev', [
    ('3.12', (3, 12), None, False),
    ('3.12.1', (3, 12, 1), None, False),
    ('3.13.0a4', (3, 13, 0), ('a', 4), False),
    ('3.13.0b1', (3, 13, 0), ('b', 1), False),
    ('3.13.0rc2', (3, 13, 0), ('rc', 2), False),
    ('3.14-dev', (3, 14), None, True),
])
def test_parse_fields(string_version, base, pre, dev):
    version = Version.from_string_version(string_version)

    assert version.base == base
    assert version.pre == pre
    assert version.dev is dev


@pytest.mark.parametrize('string_version', [
    '3.12', '3.12.0', '3.12.1', '3.13.0a4', '3.13.0rc2', '3.14-dev',
])
def test_str_round_trip(string_version):
    version = Version.from_string_version(string_version)

    assert str(version) == string_version
    assert repr(version) == f'Version {string_version}'


@pytest.mark.parametrize('str_v1,str_v2', [
    ('2.0', '2.0.0'),
    ('0.0', '0.0.0'),
])
def test_hash_ignores_trailing_zeros(str_v1, str_v2):
    v1 = Version.from_string_version(str_v1)
    v2 = Version.from_string_version(str_v2)

    assert hash(v1) == hash(v2)
    assert len({v1, v2}) == 1


@pytest.mark.parametrize('str_v1,str_v2', [
    ('2.0', '2.0a1'),
    ('2.0', '2.0-dev'),
    ('2.0a1', '2.0b1'),
])
def test_hash_differs(str_v1, str_v2):
    v1 = Version.from_string_version(str_v1)
    v2 = Version.from_string_version(str_v2)

    assert len({v1, v2}) == 2


@pytest.mark.parametrize('other', ['3.12', (3, 12), 3.12, None])
def test_eq_ne_non_version(other):
    version = Version.from_string_version('3.12')

    assert (version == other) is False
    assert (version != other) is True


@pytest.mark.parametrize('op', [
    lambda a, b: a < b,
    lambda a, b: a <= b,
    lambda a, b: a > b,
    lambda a, b: a >= b,
])
def test_ordering_non_version_raises(op):
    version = Version.from_string_version('3.12')

    with pytest.raises(TypeError):
        op(version, '3.12')


@pytest.mark.parametrize('item', ['3.12.1', (3, 12, 1), None])
def test_contains_non_version(item):
    version = Version.from_string_version('3.12')

    assert (item in version) is False


def test_sorting():
    string_versions = [
        '3.12.1', '3.12-dev', '3.12.0rc1', '3.12.0a2', '3.11.9',
        '3.12.0b1', '3.12.0a10', '3.12.0',
    ]
    versions = sorted(map(Version.from_string_version, string_versions))

    assert list(map(str, versions)) == [
        '3.11.9', '3.12-dev', '3.12.0a2', '3.12.0a10', '3.12.0b1',
        '3.12.0rc1', '3.12.0', '3.12.1',
    ]


def test_descriptors_on_class():
    assert Version.base is Version.__dict__['base']
    assert Version._hash is Version.__dict__['_hash']
    assert Version.__eq__ is Version.__dict__['__eq__']


def test_parse_error_message_includes_version():
    with pytest.raises(VersionParseError, match=r"^invalid version: '3\.x'$"):
        Version.from_string_version('3.x')


@pytest.mark.parametrize('string_version,base', [
    ('10.0', (10, 0)),
    ('10.1.2', (10, 1, 2)),
    ('12.0a1', (12, 0)),
    ('3.100.1000', (3, 100, 1000)),
])
def test_multi_digit_components(string_version, base):
    version = Version.from_string_version(string_version)

    assert version.base == base
    assert str(version) == string_version


def test_multi_digit_major_ordering():
    v9 = Version.from_string_version('9.9.9')
    v10 = Version.from_string_version('10.0')

    assert v9 < v10
    assert v9 not in Version.from_string_version('1.0')


@pytest.mark.parametrize('attr', ['base', 'pre', 'dev'])
def test_attributes_are_read_only(attr):
    version = Version.from_string_version('3.13.0rc1')
    original = getattr(version, attr)

    with pytest.raises(AttributeError, match=f"^'{attr}' is read-only$"):
        setattr(version, attr, 'changed')
    with pytest.raises(AttributeError, match=f"^'{attr}' is read-only$"):
        delattr(version, attr)

    assert getattr(version, attr) == original
