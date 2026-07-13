from setuptools import find_packages
from setuptools import setup

setup(
    name='dumme_msgs',
    version='0.0.1',
    packages=find_packages(
        include=('dumme_msgs', 'dumme_msgs.*')),
)
