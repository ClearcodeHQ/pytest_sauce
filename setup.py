# -*- coding: utf-8 -*-

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
    'pymlconf'
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
    author='The A Team',
    author_email='thearoom@clearcode.cc',
    url='https://example.com',
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
