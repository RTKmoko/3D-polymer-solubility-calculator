import os
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
        self._version_file = os.path.abspath(file)  # Ensure absolute path
        print(f"Resolved version file path: {self._version_file}")  # Debug print
        self._current_version = self.load()

    def load(self):
        """
        Import version file from path: self._version_file using importlib.util
        :return: version tuple in format (int, int, int)
        """
        if not os.path.isfile(self._version_file):
            raise FileNotFoundError(f"Version file not found: {self._version_file}")

        f_path, f_name = os.path.split(self._version_file)
        module_name, _ = os.path.splitext(f_name)
        print(f"Module name: {module_name}, File path: {f_path}")  # Debug print

        try:
            spec = importlib.util.spec_from_file_location(module_name, self._version_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception as e:
            raise ImportError(f"Error importing module: {e}")

        if hasattr(module, 'VERSION'):
            version = module.VERSION
            print(f"Loaded version: {version}")  # Debug print
            if isinstance(version, str):
                try:
                    version_tuple = tuple(map(int, version.split('.')))
                    if len(version_tuple) == 3:
                        return version_tuple
                    else:
                        raise ValueError("Version string is not in the correct format 'int.int.int'")
                except ValueError as e:
                    raise ValueError(f"Error parsing version string: {e}")
            else:
                raise ValueError("VERSION attribute is not a string")
        else:
            raise AttributeError("Module does not contain 'VERSION' attribute")

    def set(self, version_lvl: VersionLevel, direct_ion: Direction, step: int):
        """
        Modify current version
        :param version_lvl: major, minor, patch
        :param direct_ion: use operator
        :param step: count of version point
        :return: updated version string in format int,int,int
        """
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
        return ','.join(map(str, self._current_version))


if __name__ == '__main__':
    version_file, version_level, direction, step = sys.argv[1:]

    print(f"Version file path: {version_file}")  # Debug print
    try:
        version_info = VersionInfo(version_file)
        updated_version_str = version_info.set(VersionLevel[version_level], Direction[direction], int(step))
        print(updated_version_str)
        sys.exit(updated_version_str)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
