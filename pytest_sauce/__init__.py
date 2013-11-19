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

import sys
import os
import logging

from pymlconf import ConfigManager

__version__ = '0.2.8'


logger = logging.getLogger(__name__)


def get_config(config=None):
    '''
        Reads yaml configuration (default and given)

        :param str config: url to config file

        returns config object
    '''
    package_dir = os.path.dirname(__file__)
    configs = [os.path.join(package_dir, 'default.yaml')]
    if config:
        configs.append(config)

    logger.debug('reading config')
    return ConfigManager(files=configs)
