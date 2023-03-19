import pytest

from asdf_inspect import find_asdf_python_executable
from asdf_inspect.exceptions import UnsupportedImplementation
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
