from __future__ import annotations

import os
from pathlib import Path

from .exceptions import PathError


def get_asdf_root() -> Path:
    try:
        asdf_root = Path(os.environ['ASDF_ROOT']).resolve()
    except KeyError:
        asdf_root = Path.home() / '.asdf'
    if not asdf_root.exists():
        raise PathError(f'asdf root does not exist: {asdf_root}')
    if not asdf_root.is_dir():
        raise PathError(f'asdf root is not a directory: {asdf_root}')
    return asdf_root


def get_asdf_versions_directory() -> Path:
    asdf_root = get_asdf_root()
    print(f'asdf_root={asdf_root}')
    versions_dir = (asdf_root / 'installs/python').resolve()
    print(f'versions_dir = {versions_dir}')
    if not versions_dir.exists():
        print('get_asdf_versions_directory does not exist')
        raise PathError(f'asdf versions path does not exist: {versions_dir}')
    if not versions_dir.is_dir():
        print('get_asdf_versions_directory is not a directory')
        raise PathError(
            f'asdf versions path is not a directory: {versions_dir}')
    return versions_dir


def get_asdf_python_executable_path(version_dir: Path) -> Path:
    exec_path = (version_dir / 'bin' / 'python').resolve()
    if not exec_path.exists():
        raise PathError(f'asdf python binary does not exist: {exec_path}')
    if not exec_path.is_file():
        raise PathError(f'asdf python binary is not a file: {exec_path}')
    if not os.access(exec_path, os.X_OK):
        raise PathError(f'asdf python binary is not executable: {exec_path}')
    return exec_path
