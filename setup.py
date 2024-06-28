from setuptools import setup, find_packages
from polimer_solibity_calculator.version import VERSION

with open('README.md', 'r') as readme:
    README = ''.join(readme.readlines())

print(f"Build version: {VERSION}")


setup(
    name='pcs_3d',
    version=VERSION,
    packages=find_packages(exclude=['.venv']),
    url='',
    license='',
    author='ronald',
    author_email='',
    description=README,
    package_data={
        'polimer_solibity_calculator': [
            "scripts/*.sh",
            "scripts/*.bat",
            "data.json"
        ]
    },
)
