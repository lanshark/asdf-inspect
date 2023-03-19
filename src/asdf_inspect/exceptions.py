from __future__ import annotations


class ASDFInspectError(Exception):
    message = 'generic error'

    def __init__(self, message: str | None = None) -> None:
        if message:
            self.message = message

    def __str__(self) -> str:
        return self.message


class PathError(ASDFInspectError):
    message = 'path error'


class ParseError(ASDFInspectError):
    message = 'generic parse error'


class SpecParseError(ParseError):
    message = 'spec parse error'


class VersionParseError(ParseError):
    message = 'version parse error'


class UnsupportedImplementation(ASDFInspectError):
    message = 'only CPython is currently supported'
