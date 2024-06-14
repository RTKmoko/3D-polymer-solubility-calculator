import os.path
import importlib.util
import sys
from os import PathLike
from operator import add, sub
from enum import IntEnum, Enum


class VersionLevel(IntEnum):
    major = 0
    minor = 1
    patch = 2


class Direction(Enum):
    forward = add
    backward = sub


class VersionInfo:
    def __init__(self, file: PathLike):
        self._version_file = file
        self._current_version = self.load()

    def load(self):
        """
        Import version file from path: self._version_file using importlib.util
        :return: version string in format int,int,int
        """
        if not os.path.isfile(self._version_file):
            raise FileNotFoundError(f"Version file not found: {self._version_file}")

        f_path, f_name = os.path.split(self._version_file)
        module_name, _ = os.path.splitext(f_name)

        spec = importlib.util.spec_from_file_location(module_name, self._version_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, 'version'):
            version = module.version
            if isinstance(version, tuple) and all(isinstance(i, int) for i in version):
                return f'{version}'
            else:
                raise ValueError("Version information is not in the correct format (int, int, int)")
        else:
            raise AttributeError("Module does not contain 'version' attribute")

    def set(self, version_lvl: VersionLevel, direct_ion: Direction, step1: int):
        """
        Modify current version
        :param version_lvl: major, minor, patch
        :param direct_ion: use operator
        :param step1: count of version point
        :return:
        """
        version_list = list(self._current_version)
        level_index = version_lvl.value
        operator_func = direct_ion.value

        # Update the version number at the specified level
        version_list[level_index] = operator_func(version_list[level_index], int(step1))

        # Ensure no negative version numbers
        if version_list[level_index] < 0:
            raise ValueError("Version level cannot be negative")

        # Return the updated version string
        self._current_version = tuple(version_list)
        return ','.join(map(str, self._current_version))


if __name__ == '__main__':
    version_file, version_level, operation, direction, step = sys.argv[1:]

    version_str = VersionInfo(version_file).set(VersionLevel[version_level], Direction[direction], step)
    os.environ['VERSION'] = version_str
    sys.exit(version_str)
