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
import urllib2
import platform
from subprocess import Popen
from StringIO import StringIO
from zipfile import ZipFile


from pytest_sauce import get_config, logger

try:
    import pytestipdb
    USE_IPDB = True
except ImportError:
    USE_IPDB = False


def run_tests(config_path):
    '''
        Runs test suite based on configuration passed

        :param str config_path: path to yaml config file
    '''
    config = get_config(config_path)

    if config.type == 'saucelabs':
        logger.info('testing on saucelabs')
        credentials_yaml = config.saucelabs.get('yaml', config_path)
        return test_saucelabs(config, credentials_yaml)

    if config.type == 'selenium':
        logger.info('testing on selenium')
        return test_selenium(config)

    return test_unit(config)


def run(command, config):
    '''joins list of run arguments and runs them'''
    arguments = read_run_arguments(config)
    arguments.append(os.path.abspath(config.testpath))
    command_to_run = ' '.join(command + arguments)
    logger.info(command_to_run)
    pytest_proc = Popen(command_to_run,
                        cwd=(os.path.abspath(config.testpath)),
                        shell=True)
    try:
        pytest_proc.communicate()
    except KeyboardInterrupt:
        pytest_proc.kill()
    return pytest_proc.returncode


def test_selenium(config):
    '''
        runs selenium test based on config
    '''
    if not config['browsers']:
        logger.info('No browsers defined!')
        return

    for browser in config['browsers']:
        logger.info('testing %s browser' % browser['browsername'])
        call_arguments = ['py.test'] +\
            map_presets_to_cmd(browser)

        if browser['browsername'] == 'chrome':
            call_arguments += map_presets_to_cmd({
                'chromepath': get_chromedriver(config)
            })
        if config.selenium.xvfb and config.selenium.xvfb.xvfb_on:
            xfvb_args = map_presets_to_cmd(config.selenium.xvfb.options)
            xfvb_args.insert(0, 'xvfb-run')
            call_arguments = xfvb_args + call_arguments
        code = run(call_arguments, config)
        if code != 0:
            break

    return code


def test_saucelabs(config, credentials_yaml):
    '''
        runs selenium test based on config
    '''
    if not config['browsers']:
        logger.warning('No browsers defined!')
        return

    for browser in config['browsers']:
        logger.info('testing %s browser' % browser['browsername'])
        call_arguments = ['py.test',
                          '--saucelabs=%s'
                          % (os.path.abspath(credentials_yaml))
                          ] + map_presets_to_cmd(browser)
        code = run(call_arguments, config)
        if code != 0:
            break

    return code


def test_unit(config):
    '''
        runs unit or integration tests based on config
    '''
    logger.info('Running pytest tests without selenium')
    call_arguments = ['py.test', '-p no:pytest_mozwebqa']
    return run(call_arguments, config)


def map_presets_to_cmd(args):
    ret_args = []
    for argname, argval in args.items():
        prefix = '--'
        if len(argname) == 1:
            prefix = '-'
        if (isinstance(argval, bool) and argval):
            ret_args.append('%s%s' % (prefix, argname))
        elif len(argname) == 1:
            ret_args.append('-%s' % (argname))
            ret_args.append(argval)
        elif argval:
            ret_args.append('%s%s="%s"' % (prefix, argname, argval))
    return ret_args


def read_run_arguments(config):
    '''Returns additional configuration option to run tests'''
    command_arguments = map_presets_to_cmd(config.run)
    if USE_IPDB and '--pdb' in command_arguments:
        command_arguments[command_arguments.index('--pdb')] = '--ipdb'

    return command_arguments


def download_and_unzip(url, filename, path):
    '''
    Downloads data from url and unpacks zip file

    Args:
        url - url from wchich file will be downloaded
        filename - filename of file in zip to extract
        path - path to file in which data of file from zip will be written
    Returns:
        None, result should be extracted file on disk
    '''

    tmp_file = os.path.join('/tmp', filename)

    data = urllib2.urlopen(url)
    zipdata = StringIO(data.read())
    output = open(tmp_file, 'w')
    archive = ZipFile(zipdata)
    csvfile = archive.open(filename)
    output.write(csvfile.read())
    output.close()

    path_parts = path.rsplit('/', 1)
    if len(path_parts) > 1 and not os.path.exists(path_parts[0]):
        os.makedirs(path_parts[0])

    os.rename(tmp_file, path)
    os.chmod(path, 0744)


def get_saucelabs_connect(config=None, config_path=None, update=False):
    '''
    Downloads saucelabs connect binary into **config.saucelabs.connect.file**

    :param pymlconf.ConfigManager config: configuration object
    :param str config_path: path to config
    :param bool update: - (optional) if True overwrites exisiting binary
    '''
    if not config:
        if config_path:
            config = get_config(config_path)
        else:
            logger.error('No config provided!')
            return

    sauce_config = config.saucelabs

    if not update and os.path.isfile(sauce_config.connect.file):
        logger.debug('%s already exists' % sauce_config.connect.file)
    else:
        logger.info('Downloading %s' % sauce_config.connect.url)
        download_and_unzip(sauce_config.connect.url,
                           'Sauce-Connect.jar',
                           sauce_config.connect.file)
        logger.info('Downloaded')

    return os.path.abspath(sauce_config.connect.file)


def run_saucelabs(config_path):
    '''
        Runs saucelabs
    '''
    config = get_config(config_path)
    sauce = get_saucelabs_connect(config)
    command = ['java',
               '-jar',
               sauce,
               config.get('username'),
               config.get('api-key')]
    pytest_proc = Popen(' '.join(command), shell=True)
    try:
        pytest_proc.communicate()
    except KeyboardInterrupt:
        pytest_proc.kill()
    if pytest_proc.returncode != 0:
        return pytest_proc.returncode
    return 0


def get_chromedriver(config=None, config_path=None, update=False):
    '''
    Downloads chromedriver binary into **config.selenium.chromedriver.file**
    path

    :param pymlconf.ConfigManager config: configuration object
    :param update: - (optional) if True overwrites existing binary
    '''
    if not config:
        if config_path:
            config = get_config(config_path)
        else:
            logger.error('No config provided!')
            return

    chromedriver_config = config.selenium.chromedriver
    if not update and os.path.isfile(chromedriver_config.file):
        logger.debug('%s already exists' % chromedriver_config.file)
    else:
        url = None
        if platform.system() in ('Windows', ):
            url = chromedriver_config.url + chromedriver_config.zips['win']
        elif platform.system() in ('Mac', 'Darwin'):
            url = chromedriver_config.url + chromedriver_config.zips['mac']
        elif platform.system() in ('Linux'):
            if platform.architecture()[0] == '32bit':
                url = chromedriver_config.url +\
                    chromedriver_config.zips['linux32']
            if platform.architecture()[0] == '64bit':
                url = chromedriver_config.url +\
                    chromedriver_config.zips['linux64']

        if not url:
            raise Exception('Architecture is not detected')

        logger.info('Downloading %s' % url)
        download_and_unzip(url,
                           'chromedriver',
                           chromedriver_config.file)
        logger.info('Downloaded')

    return os.path.abspath(chromedriver_config.file)
