from setuptools import setup, find_packages
from psc_3d.version import VERSION

with open('README.md', 'r') as readme:
    README = ''.join(readme.readlines())

print(f"Build version: {VERSION}")

with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='psc_3d',
    version=VERSION,
    packages=find_packages(exclude=['.venv']),
    url='',
    license='',
    author='Ronald Oguz',
    author_email='',
    description=README,
    long_description_content_type="text/markdown",
    install_requires=required_packages,
    package_data={
        'psc_3d': [
            "scripts/*.sh",
            "scripts/*.bat",
            "data.json"
        ]
    },
)
