from __future__ import annotations

import logging
from pathlib import Path

from .exceptions import ParseError, UnsupportedImplementation
from .path import get_asdf_python_executable_path, get_asdf_versions_directory
from .spec import ASDFPythonSpec
from .version import Version


log = logging.getLogger(__name__)


def find_asdf_python_executable(spec: ASDFPythonSpec | str) -> Path | None:
    if not isinstance(spec, ASDFPythonSpec):
        if not isinstance(spec, str):
            raise TypeError(f'unexpected spec type: {type(spec)}')
        spec = ASDFPythonSpec.from_string_spec(spec)
    spec.is_supported(raise_exception=True)
    requested_version = Version.from_string_version(spec.version)
    log.debug('requested %s', requested_version)
    best_match_version: Version | None = None
    best_match_dir: Path | None = None
    for version_dir in get_asdf_versions_directory().iterdir():
        try:
            _spec = ASDFPythonSpec.from_string_spec(version_dir.name)
            _spec.is_supported(raise_exception=True)
            version = Version.from_string_version(_spec.version)
        except (ParseError, UnsupportedImplementation) as exc:
            log.warning('%s: %s', type(exc), exc)
            continue
        if version not in requested_version:
            continue
        log.debug('proposed %s', version)
        if not best_match_version or version > best_match_version:
            best_match_version = version
            best_match_dir = version_dir
    if not best_match_version:
        return None
    log.debug('accepted %s', best_match_version)
    return get_asdf_python_executable_path(best_match_dir)
