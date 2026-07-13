from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'dumme_controller'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        (
            os.path.join('share', package_name),
            ['package.xml'],
        ),
        (
            os.path.join('share', package_name, 'launch'),
            glob('launch/*.py'),
        ),
        (
            os.path.join('share', package_name, 'config'),
            glob('config/*.yaml'),
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='asambhav',
    maintainer_email='sambhava06@gmail.com',
    description='Controller package for the Dumm-E robotic arm.',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            # Add controller nodes here later
            # 'controller_node = dumme_controller.controller_node:main',
            'slider_control = dumme_controller.slider_control:main',
        ],
    },
)