import pytest

from asdf_inspect.exceptions import PathError
from asdf_inspect.path import (
    get_asdf_python_executable_path, get_asdf_root,
    get_asdf_versions_directory,
)

from tests.testlib import BaseTestClass


@pytest.fixture
def asdf_root(tmp_path):
    path = tmp_path / '.asdf'
    path.mkdir()
    return path


class BaseTestGetASDFRoot(BaseTestClass):

    def test_ok(asdf_root):
        asdf_root.mkdir()

        assert get_asdf_root() == asdf_root

    def test_error_does_not_exist(asdf_root):
        message = f'asdf root does not exist: {asdf_root}'

        with pytest.raises(PathError, match=message):
            get_asdf_root()

    def test_error_not_a_directory(asdf_root):
        asdf_root.touch()
        message = f'asdf root is not a directory: {asdf_root}'

        with pytest.raises(PathError, match=message):
            get_asdf_root()


class TestGetASDFRootFromEnvironment(BaseTestGetASDFRoot):

    @pytest.fixture
    def asdf_root(tmp_path):
        return tmp_path / '.asdf'

    @pytest.fixture(autouse=True)
    def setup(monkeypatch, asdf_root):
        monkeypatch.setenv('ASDF_ROOT', str(asdf_root))


class TestGetASDFRootFallback(BaseTestGetASDFRoot):

    @pytest.fixture
    def asdf_root(fake_home):
        return fake_home / '.asdf'

    @pytest.fixture
    def fake_home(tmp_path):
        return tmp_path / 'home' / 'user'

    @pytest.fixture(autouse=True)
    def setup(monkeypatch, fake_home):
        fake_home.mkdir(parents=True)
        monkeypatch.setattr('pathlib.Path.home', lambda: fake_home)
        monkeypatch.delenv('ASDF_ROOT', raising=False)


class TestGetASDFVersionsDirectory(BaseTestClass):

    @pytest.fixture
    def versions_dir(asdf_root):
        return asdf_root / 'installs/python'

    @pytest.fixture(autouse=True)
    def setup(monkeypatch, asdf_root):
        monkeypatch.setattr(
            'asdf_inspect.path.get_asdf_root', lambda: asdf_root)

    def test_ok(versions_dir):
        versions_dir.mkdir(parents=True)

        assert get_asdf_versions_directory() == versions_dir

    def test_error_does_not_exist(versions_dir):
        message = f'asdf versions path does not exist: {versions_dir}'

        with pytest.raises(PathError, match=message):
            get_asdf_versions_directory()

    def test_error_not_a_directory(versions_dir):
        versions_dir.parent.mkdir(parents=True)
        versions_dir.touch()
        message = f'asdf versions path is not a directory: {versions_dir}'

        with pytest.raises(PathError, match=message):
            get_asdf_versions_directory()


class TestGetASDFPythonExecutablePath(BaseTestClass):

    @pytest.fixture
    def version_dir(asdf_root):
        # SAS - use get_versions_dir - make that a common lib fn?
        return asdf_root / 'installs/python' / '3.10.7'

    @pytest.fixture
    def exec_path(version_dir):
        return version_dir / 'bin' / 'python'

    @pytest.fixture(autouse=True)
    def setup(exec_path):
        exec_path.parent.mkdir(parents=True)

    def test_ok(version_dir, exec_path):
        exec_path.touch(mode=0o777)

        assert get_asdf_python_executable_path(version_dir) == exec_path

    def test_error_does_not_exist(version_dir):
        message = f'asdf python binary does not exist: {version_dir}'

        with pytest.raises(PathError, match=message):
            get_asdf_python_executable_path(version_dir)

    def test_error_not_a_file(version_dir, exec_path):
        exec_path.mkdir(parents=True)
        message = f'asdf python binary is not a file: {version_dir}'

        with pytest.raises(PathError, match=message):
            get_asdf_python_executable_path(version_dir)

    def test_error_not_executable(version_dir, exec_path):
        exec_path.touch(mode=0o666)
        message = f'asdf python binary is not executable: {version_dir}'

        with pytest.raises(PathError, match=message):
            get_asdf_python_executable_path(version_dir)
