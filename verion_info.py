import os.path
import importlib.util


class VersionInfo:
    def __init__(self, version_file):
        self._version_file = version_file
        self._current_version = self.load()

    @classmethod
    def from_file(cls, version_file):
        return cls(version_file)

    def load(self):
        f_path, f_name = os.path.split(self._version_file)
        module_name, _ = os.path.splitext(f_name)

