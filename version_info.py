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
        f_path, f_name = os.path.split(self._version_file)
        module_name, _ = os.path.splitext(f_name)
        return ''

    def set(self, version_level: VersionLevel, direction: Direction, step: int):
        """
        Modify current version
        :param version_level: major, minor, patch
        :param direction: use operator
        :param step: count of version point
        :return:
        """
        return ''


if __name__ == '__main__':
    version_file, version_level, operation, direction, step = sys.argv[1:]

    version_str = VersionInfo(version_file).set(VersionLevel[version_level], Direction[direction], step)
    os.environ['VERSION'] = version_str
    sys.exit(version_str)