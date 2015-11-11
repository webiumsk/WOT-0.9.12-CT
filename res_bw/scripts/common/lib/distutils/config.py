# 2015.11.10 21:35:03 St�edn� Evropa (b�n� �as)
# Embedded file name: scripts/common/Lib/distutils/config.py
"""distutils.pypirc

Provides the PyPIRCCommand class, the base class for the command classes
that uses .pypirc in the distutils.command package.
"""
import os
from ConfigParser import ConfigParser
from distutils.cmd import Command
DEFAULT_PYPIRC = '[distutils]\nindex-servers =\n    pypi\n\n[pypi]\nusername:%s\npassword:%s\n'

class PyPIRCCommand(Command):
    """Base command that knows how to handle the .pypirc file
    """
    DEFAULT_REPOSITORY = 'https://pypi.python.org/pypi'
    DEFAULT_REALM = 'pypi'
    repository = None
    realm = None
    user_options = [('repository=', 'r', 'url of repository [default: %s]' % DEFAULT_REPOSITORY), ('show-response', None, 'display full response text from server')]
    boolean_options = ['show-response']

    def _get_rc_file(self):
        """Returns rc file path."""
        return os.path.join(os.path.expanduser('~'), '.pypirc')

    def _store_pypirc(self, username, password):
        """Creates a default .pypirc file."""
        rc = self._get_rc_file()
        f = os.fdopen(os.open(rc, os.O_CREAT | os.O_WRONLY, 384), 'w')
        try:
            f.write(DEFAULT_PYPIRC % (username, password))
        finally:
            f.close()

    def _read_pypirc(self):
        """Reads the .pypirc file."""
        rc = self._get_rc_file()
        if os.path.exists(rc):
            self.announce('Using PyPI login from %s' % rc)
            repository = self.repository or self.DEFAULT_REPOSITORY
            config = ConfigParser()
            config.read(rc)
            sections = config.sections()
            if 'distutils' in sections:
                index_servers = config.get('distutils', 'index-servers')
                _servers = [ server.strip() for server in index_servers.split('\n') if server.strip() != '' ]
                if _servers == []:
                    if 'pypi' in sections:
                        _servers = ['pypi']
                    else:
                        return {}
                for server in _servers:
                    current = {'server': server}
                    current['username'] = config.get(server, 'username')
                    for key, default in (('repository', self.DEFAULT_REPOSITORY), ('realm', self.DEFAULT_REALM), ('password', None)):
                        if config.has_option(server, key):
                            current[key] = config.get(server, key)
                        else:
                            current[key] = default

                    if current['server'] == repository or current['repository'] == repository:
                        return current

            elif 'server-login' in sections:
                server = 'server-login'
                if config.has_option(server, 'repository'):
                    repository = config.get(server, 'repository')
                else:
                    repository = self.DEFAULT_REPOSITORY
                return {'username': config.get(server, 'username'),
                 'password': config.get(server, 'password'),
                 'repository': repository,
                 'server': server,
                 'realm': self.DEFAULT_REALM}
        return {}

    def initialize_options(self):
        """Initialize options."""
        self.repository = None
        self.realm = None
        self.show_response = 0
        return

    def finalize_options(self):
        """Finalizes options."""
        if self.repository is None:
            self.repository = self.DEFAULT_REPOSITORY
        if self.realm is None:
            self.realm = self.DEFAULT_REALM
        return
# okay decompyling c:\Users\PC\wotsources\files\originals\res_bw\scripts\common\lib\distutils\config.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:35:03 St�edn� Evropa (b�n� �as)
