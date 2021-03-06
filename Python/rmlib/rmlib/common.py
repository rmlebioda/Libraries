import platform
import os
from configparser import ConfigParser


if platform.system() in ['Linux', 'Darwin']:
    log_path = os.path.join(os.path.expanduser('~'), '.rml')
    setting_path = os.path.join(
        os.path.expanduser('~'), 'Dropbox/settings.conf')
else:
    raise SystemError('rmlib.common settings for os ' +
                      platform.system() + ' is not supported, implement by yourself where you have your conf file')

def read_config_parser(path=setting_path):
    _parser = ConfigParser()
    _parser.read(path)
    return _parser