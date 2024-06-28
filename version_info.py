import os.path
import re
import sys
from enum import IntEnum, Enum
from operator import add, sub
from os import PathLike
from typing import Tuple, Optional


class VersionLevel(IntEnum):
    major = 0
    minor = 1
    patch = 2


class Direction(Enum):
    forward = add
    backward = sub


class VersionInfo:
    def __init__(self, file: PathLike, backup: bool = False):
        self._version_file = file
        self._backup_flag = backup
        self._current_version: Optional[Tuple[int, int, int], None] = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            raise exc_type(exc_val, exc_tb)
        self.store()

    def load(self):
        if not os.path.isfile(self._version_file):
            raise FileNotFoundError(f"Version file not found: {self._version_file}")

        with open(self._version_file, 'r') as v_file:
            v_file_str = ''.join(v_file.readlines()).strip()
            print(f"File: {v_file_str}")
            # ver_name, ver_str = re.split(r"\s*=\s*", v_file_str, 2)
            # major, minor, patch = [int(i) for i in ver_str[1:-1].split('.')]

        # self._current_version = major, minor, patch
        self._current_version = 1, 1, 1


    @property
    def version(self):
        return '.'.join(map(str, self._current_version))

    def set(self, version_lvl: VersionLevel, direct_ion: Direction, step: int):
        version_list = list(self._current_version)
        level_index = version_lvl.value
        operator_func = direct_ion.value

        # Update the version number at the specified level
        version_list[level_index] = operator_func(version_list[level_index], int(step))

        # Ensure no negative version numbers
        if version_list[level_index] < 0:
            raise ValueError("Version level cannot be negative")

        # Return the updated version string
        self._current_version = tuple(version_list)

    def store(self):
        with open(self._version_file, 'w+') as version:
            version.write(f"VERSION = '{self.version}'\n")

    def update_readme(self, template, target='README.md', pattern='<version>'):
        with open(template, 'r') as readme:
            readme_str = ''.join(readme.readlines())
            readme_str = readme_str.replace(pattern, self.version)
        with open(target, 'w+') as writ_me:
            writ_me.write(readme_str)


if __name__ == '__main__':
    version_file, readme_template, version_level, direction, step_ = sys.argv[1:]

    with VersionInfo(version_file) as ver:
        ver.load()
        ver.set(VersionLevel[version_level], Direction[direction], step_)
        version_str = ver.version
        ver.update_readme(readme_template)
    print(version_str)
