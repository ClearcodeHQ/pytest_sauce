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

from setuptools import Command


class PytestSauce(Command):

    """setuptools Command"""
    description = "Runs pytest sauce tests"
    user_options = [('config=', 'c', 'pytest_sauce configuration file')]

    def initialize_options(self):
        """init options"""
        self.config = None

    def finalize_options(self):
        """finalize options"""
        pass

    def run(self):
        """runner"""
        self.run_command('egg_info')

        # make sure install requries are installed
        if self.distribution.install_requires:
            self.distribution.fetch_build_eggs(
                self.distribution.install_requires)

        # makes sure all tests requires are here
        if self.distribution.tests_require:
            self.distribution.fetch_build_eggs(
                self.distribution.tests_require)

        # checks possible 'test' in extras_require
        if 'test' in self.distribution.extras_require:
            self.distribution.fetch_build_eggs(
                self.distribution.extras_require['test'])

        if not self.config:
            raise AttributeError('Please, provide test config')

        from pytest_sauce.utils import run_tests

        errno = run_tests(self.config)
        sys.exit(errno)
