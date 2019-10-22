import importlib
import sys


def load_module_from_path(*, name, fpath):
    """
    Args:
        name (str)
        fpath (str of :class:`pathlib.Path`)
    """
    if name in sys.modules:
        return sys.modules[name]
    else:
        spec = importlib.util.spec_from_file_location(name, fpath)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module
