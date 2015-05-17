#!/usr/bin/env python3

from setuptools import setup #, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='vaip',
    version='0.1.0.dev',
    description='Very Automated Input Parsing',
    long_description=long_description,
    url='https://github.com/dacav/vaip',
    author='Giovanni [dacav] Simoni',
    author_email='dacav@openmailbox.org',
    license='MIT',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Quality Assurance',
    ],

    keywords='input checking',
    packages=['vaip'],
    install_requires=['rply'],
)
