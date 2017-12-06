#!/usr/bin/python2

"""Setup script for twod."""

from setuptools import setup, find_packages
import codecs
import os
import sys

import setuptools

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def get_version(fname='twod/_version.py'):
    """Fetch version from file."""
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return (line.split('=')[-1].strip().strip('"'))

INSTALL_REQUIRES = [
    'requests>=2.8.1',
    'lockfile>=0.9.1',
]

EXTRAS_REQUIRE = {}

# Different versions of dependencies depending on python version
if sys.version_info[0:2] < (3, 0):
    INSTALL_REQUIRES.append("python-daemon<2.0")
else:
    INSTALL_REQUIRES.append("python-daemon>2.1.1")

# Additional requirements for python 2
if int(setuptools.__version__.split(".", 1)[0]) < 18:
    assert "bdist_wheel" not in sys.argv, "setuptools 18 required for wheels."
    if sys.version_info[0:2] < (3, 0):
        INSTALL_REQUIRES.append("configparser>=3.5.0")
else:
    EXTRAS_REQUIRE[":python_version<'3.0'"] = ["configparser>=3.5.0"]

setup(
    name="twod",

    version=get_version(),

    description="twod TwoDNS host IP updater",
    long_description=long_description,

    # The project URL.
    url='https://github.com/tablet-mode/twod',

    # Author details
    author='Thomas Kager',
    author_email='tablet-mode@monochromatic.cc',

    # Choose your license
    license='GPLv3',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'License :: OSI Approved :: GPLv3 License',

        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

    keywords='daemon dns',

    packages=find_packages(exclude=["docs", "tests*"]),

    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,

    package_data={},

    data_files=[],
    entry_points={
        'console_scripts': ['twod = twod.twod:main', ]
    },
)
