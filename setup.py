from setuptools import setup, find_packages

setup(
    name='checkmob_copiloto',
    version='0.1',
    packages=find_packages(where="backend"),
    package_dir={"": "backend"},
)
