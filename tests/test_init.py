import tomllib
from pathlib import Path

import asdf_inspect


PYPROJECT_PATH = Path(__file__).parent.parent / 'pyproject.toml'


def test_version_matches_pyproject():
    with open(PYPROJECT_PATH, 'rb') as fobj:
        pyproject = tomllib.load(fobj)

    assert asdf_inspect.__version__ == pyproject['project']['version']


def test_public_api():
    assert asdf_inspect.__all__ == [
        '__version__', 'find_asdf_python_executable']
