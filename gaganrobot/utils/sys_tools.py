# pylint: disable=missing-module-docstring

from glob import glob
from os.path import isfile, relpath
from typing import Dict, List, Union


class SafeDict(Dict[str, str]):
    """ modded dict """

    def __missing__(self, key: str) -> str:
        return '{' + key + '}'


def get_import_path(root: str, path: str) -> Union[str, List[str]]:
    """ return import path """
    seperator = '\\' if '\\' in root else '/'
    if isfile(path):
        return '.'.join(relpath(path, root).split(seperator))[:-3]
    all_paths = glob(root + path.rstrip(seperator) +
                     f"{seperator}*.py", recursive=True)
    return sorted(
        [
            '.'.join(relpath(f, root).split(seperator))[:-3] for f in all_paths
            if not f.endswith("__init__.py")
        ]
    )
