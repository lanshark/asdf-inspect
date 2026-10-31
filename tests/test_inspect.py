import logging

import pytest

from asdf_inspect import find_asdf_python_executable
from asdf_inspect.exceptions import SpecParseError, UnsupportedImplementation
from asdf_inspect.spec import ASDFPythonSpec


class TestFindASDFPythonExecutable:

    @pytest.fixture(autouse=True)
    def setup(self, monkeypatch, tmp_path):
        self.asdf_root = tmp_path / 'asdf_root'
        monkeypatch.setenv('ASDF_ROOT', str(self.asdf_root))
        self.versions_dir = self.asdf_root / 'installs/python'
        self.versions_dir.mkdir(parents=True)

    def prepare_version(self, version):
        bin_path = self.versions_dir / version / 'bin'
        bin_path.mkdir(parents=True)
        exec_path = bin_path / 'python'
        exec_path.touch(mode=0o777)
        return exec_path

    def prepare_versions(self, *versions):
        return [self.prepare_version(version) for version in versions]

    @pytest.mark.parametrize('version', [
        '3.7', ASDFPythonSpec.from_string_spec('3.7'),
        '3.7.16', ASDFPythonSpec.from_string_spec('3.7.16'),
    ])
    def test_found(self, version):
        self.prepare_versions('3.7.2', '3.7.1', '3.7.16', '3.8.16')
        assert find_asdf_python_executable(version) == (
            self.versions_dir / '3.7.16' / 'bin' / 'python')

    @pytest.mark.parametrize('version', ['3.9', '3.7.3'])
    def test_not_found(self, version):
        self.prepare_versions('3.7.2', '3.8.3')
        assert find_asdf_python_executable(version) is None

    def test_unsupported(self):
        with pytest.raises(UnsupportedImplementation):
            find_asdf_python_executable('fakepython-3.7')

    @pytest.mark.parametrize('spec', [None, 3.12, b'3.12'])
    def test_invalid_spec_type(self, spec):
        with pytest.raises(TypeError, match='unexpected spec type'):
            find_asdf_python_executable(spec)

    def test_invalid_spec(self):
        with pytest.raises(SpecParseError):
            find_asdf_python_executable('3.x')

    def test_no_versions_installed(self):
        assert find_asdf_python_executable('3.12') is None

    def test_skips_unparsable_and_unsupported(self, caplog):
        self.prepare_versions('3.12.1', 'pypy3.10-7.3.17', '3.x-broken')

        with caplog.at_level(logging.WARNING, logger='asdf_inspect.inspect'):
            result = find_asdf_python_executable('3.12')

        assert result == self.versions_dir / '3.12.1' / 'bin' / 'python'
        assert len(caplog.records) == 2

    def test_prerelease_not_matched_by_final_spec(self):
        self.prepare_versions('3.13.0rc2')

        assert find_asdf_python_executable('3.13') is None

    def test_prerelease_matched_exactly(self):
        self.prepare_versions('3.13.0rc1', '3.13.0rc2', '3.13.0')

        assert find_asdf_python_executable('3.13.0rc2') == (
            self.versions_dir / '3.13.0rc2' / 'bin' / 'python')

    def test_final_preferred_over_prerelease(self):
        self.prepare_versions('3.13.0rc2', '3.13.0', '3.13.1')

        assert find_asdf_python_executable('3.13') == (
            self.versions_dir / '3.13.1' / 'bin' / 'python')

    def test_dev(self):
        self.prepare_versions('3.14-dev', '3.14.0')

        assert find_asdf_python_executable('3.14-dev') == (
            self.versions_dir / '3.14-dev' / 'bin' / 'python')
