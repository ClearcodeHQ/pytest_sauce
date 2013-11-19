# -*- coding: utf-8 -*-

# Copyright (C) 2013 by Clearcode <http://clearcode.cc>
# and associates (see AUTHORS).
#
# This file is part of pytest_sauce.
#
# Pytest_sauce is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pytest_sauce is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pytest_sauce. If not, see <http://www.gnu.org/licenses/>.

import os
import re
from setuptools import setup, find_packages

here = os.path.dirname(__file__)
with open(os.path.join(here, 'pytest_sauce', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)


def read(fname):
    return open(os.path.join(here, fname)).read()

requirements = [
    'pytest',
    'pytest_mozwebqa',
    'pymlconf <0.3.1,>0.3.1',  # this is due to error on this Pymlconf version
]

test_requires = []

extras_require = {
    'docs': ['sphinx'],
    'tests': test_requires,
    'ipdb': [
        'pytest-ipdb',
        'ipdb'
    ]   # This can be installed only through easy_install,
        # as pip doesn't read .egg files (pytest-ipdb is served through .egg files only)
}

setup(
    name='pytest_sauce',
    version=package_version,
    description='''pytest_sauce provides sane and helpful methods worked
    out in clearcode to run py.test tests with selenium/saucelabs''',
    long_description=(
        read('README.rst')
        + '\n\n' +
        read('CHANGES.rst')
    ),
    keywords='pytest mozwebqa selenium saucelabs',
    author='Clearcode - The A Room',
    author_email='thearoom@clearcode.cc',
    url='https://github.com/clearcode/pytest_sauce',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Testing',
    ],
    packages=find_packages(),
    install_requires=requirements,
    tests_require=test_requires,
    test_suite='tests',
    include_package_data=True,
    zip_safe=False,
    extras_require=extras_require,
)
