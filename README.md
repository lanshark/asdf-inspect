# asdf-inspect

An auxiliary library for the [virtualenv-asdf][virtualenv-asdf] and [tox-asdf-redux][tox-asdf-redux] plugins.

## Configuration

Python installs are looked up in `<asdf data dir>/installs/python`. The asdf
data directory is taken from the first non-empty value of:

1. `ASDF_DATA_DIR` (the variable asdf itself uses)
2. `ASDF_ROOT` (deprecated; kept for backward compatibility)
3. `~/.asdf` (asdf's default)

## Limitations

Only CPython is supported at the moment.


NOTE: this is modified from [pyenv-inspect][pyenv-inspect] by un-def.

[pyenv-inspect]: https://github.com/un-def/pyenv-inspect
[virtualenv-asdf]: https://github.com/lanshark/virtualenv-asdf
[tox-asdf-redux]: https://github.com/lanshark/tox-asdf-redux
