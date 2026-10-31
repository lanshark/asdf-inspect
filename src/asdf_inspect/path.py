from __future__ import annotations

import logging
import os
from pathlib import Path

from .exceptions import PathError


log = logging.getLogger(__name__)

# ASDF_DATA_DIR is the variable asdf itself uses for its data directory.
# ASDF_ROOT is accepted as a fallback for backward compatibility with
# earlier releases of this library.
ASDF_DATA_DIR_ENV_VARS = ('ASDF_DATA_DIR', 'ASDF_ROOT')


def get_asdf_root() -> Path:
    for env_var in ASDF_DATA_DIR_ENV_VARS:
        # asdf treats an empty value the same as an unset one
        if value := os.environ.get(env_var):
            asdf_root = Path(value).expanduser().resolve()
            log.debug('asdf data dir from %s: %s', env_var, asdf_root)
            break
    else:
        asdf_root = Path.home() / '.asdf'
        log.debug('asdf data dir (default): %s', asdf_root)
    if not asdf_root.exists():
        raise PathError(f'asdf root does not exist: {asdf_root}')
    if not asdf_root.is_dir():
        raise PathError(f'asdf root is not a directory: {asdf_root}')
    return asdf_root


def get_asdf_versions_directory() -> Path:
    versions_dir = (get_asdf_root() / 'installs/python').resolve()
    log.debug('asdf python versions dir: %s', versions_dir)
    if not versions_dir.exists():
        raise PathError(f'asdf versions path does not exist: {versions_dir}')
    if not versions_dir.is_dir():
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
