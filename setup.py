from setuptools import setup, find_packages

setup(
    name='pcs_3d',
    version='1.0.0',
    packages=find_packages(exclude=['.venv']),
    url='',
    license='',
    author='ronald',
    author_email='',
    description='',
    package_data={
        'polimer_solibity_calculator': [
            "scripts/*.sh",
            "scripts/*.bat",
            "data.json"
        ]
    },
)
