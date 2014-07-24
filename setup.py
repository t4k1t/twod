#!/usr/bin/python2

""" Setup script for twod. """

from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="twod",

    version='0.3.0',

    description="twod TwoDNS host IP updater",
    long_description=long_description,

    # The project URL.
    url='https://github.com/tablet-mode/twod',

    # Author details
    author='Tablet Mode',
    author_email='tablet-mode@monochromatic.cc',

    # Choose your license
    license='GPLv3',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'License :: OSI Approved :: GPLv3 License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='daemon dns',

    packages=find_packages(exclude=["docs", "tests*"]),

    install_requires=[],

    package_data={},

    data_files=[],
    entry_points={
        'console_scripts': ['twod = twod.twod:main', ]
    },
)
