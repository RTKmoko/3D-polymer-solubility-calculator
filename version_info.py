import os.path
import importlib.util
import sys
from os import PathLike
from operator import add, sub
from enum import IntEnum, Enum
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

        f_path, f_name = os.path.split(self._version_file)
        # module_name, _ = os.path.splitext(f_name)
        # print(f"Load: {f_path}, {f_name}, {module_name}")
        # spec = importlib.util.spec_from_file_location(module_name, self._version_file)
        # print(f"Spec: {spec}")
        # module = importlib.util.module_from_spec(spec)
        # spec.loader.exec_module(module)

        # assert hasattr(module, 'VERSION'), "Module does not contain 'VERSION' attribute"
        # major, minor, patch = [int(i) for i in module.VERSION.split('.', 3)]

        with open(self._version_file, 'r') as v_file:
            v_file_str = ''.join(v_file.readlines())
            ver_name, ver_str = v_file_str.split('=', 2)
            major, minor, patch = [int(i) for i in ver_str.strip()[1:-1].split('.')]

        self._current_version = major, minor, patch

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
