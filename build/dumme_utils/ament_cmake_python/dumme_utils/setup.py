from setuptools import find_packages
from setuptools import setup

setup(
    name='dumme_utils',
    version='0.0.1',
    packages=find_packages(
        include=('dumme_utils', 'dumme_utils.*')),
)
