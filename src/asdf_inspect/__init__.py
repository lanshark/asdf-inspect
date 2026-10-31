from importlib import metadata as _metadata

from .inspect import find_asdf_python_executable


__version__ = _metadata.version('asdf-inspect')


__all__ = ['__version__', 'find_asdf_python_executable']
