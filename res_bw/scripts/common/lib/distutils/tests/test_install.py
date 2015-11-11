# 2015.11.10 21:35:25 St�edn� Evropa (b�n� �as)
# Embedded file name: scripts/common/Lib/distutils/tests/test_install.py
"""Tests for distutils.command.install."""
import os
import sys
import unittest
import site
from test.test_support import captured_stdout, run_unittest
from distutils import sysconfig
from distutils.command.install import install
from distutils.command import install as install_module
from distutils.command.build_ext import build_ext
from distutils.command.install import INSTALL_SCHEMES
from distutils.core import Distribution
from distutils.errors import DistutilsOptionError
from distutils.extension import Extension
from distutils.tests import support

def _make_ext_name(modname):
    if os.name == 'nt' and sys.executable.endswith('_d.exe'):
        modname += '_d'
    return modname + sysconfig.get_config_var('SO')


class InstallTestCase(support.TempdirManager, support.LoggingSilencer, unittest.TestCase):

    def test_home_installation_scheme(self):
        builddir = self.mkdtemp()
        destination = os.path.join(builddir, 'installation')
        dist = Distribution({'name': 'foopkg'})
        dist.script_name = os.path.join(builddir, 'setup.py')
        dist.command_obj['build'] = support.DummyCommand(build_base=builddir, build_lib=os.path.join(builddir, 'lib'))
        cmd = install(dist)
        cmd.home = destination
        cmd.ensure_finalized()
        self.assertEqual(cmd.install_base, destination)
        self.assertEqual(cmd.install_platbase, destination)

        def check_path(got, expected):
            got = os.path.normpath(got)
            expected = os.path.normpath(expected)
            self.assertEqual(got, expected)

        libdir = os.path.join(destination, 'lib', 'python')
        check_path(cmd.install_lib, libdir)
        check_path(cmd.install_platlib, libdir)
        check_path(cmd.install_purelib, libdir)
        check_path(cmd.install_headers, os.path.join(destination, 'include', 'python', 'foopkg'))
        check_path(cmd.install_scripts, os.path.join(destination, 'bin'))
        check_path(cmd.install_data, destination)

    @unittest.skipIf(sys.version < '2.6', 'site.USER_SITE was introduced in 2.6')
    def test_user_site(self):
        self.old_user_base = site.USER_BASE
        self.old_user_site = site.USER_SITE
        self.tmpdir = self.mkdtemp()
        self.user_base = os.path.join(self.tmpdir, 'B')
        self.user_site = os.path.join(self.tmpdir, 'S')
        site.USER_BASE = self.user_base
        site.USER_SITE = self.user_site
        install_module.USER_BASE = self.user_base
        install_module.USER_SITE = self.user_site

        def _expanduser(path):
            return self.tmpdir

        self.old_expand = os.path.expanduser
        os.path.expanduser = _expanduser

        def cleanup():
            site.USER_BASE = self.old_user_base
            site.USER_SITE = self.old_user_site
            install_module.USER_BASE = self.old_user_base
            install_module.USER_SITE = self.old_user_site
            os.path.expanduser = self.old_expand

        self.addCleanup(cleanup)
        for key in ('nt_user', 'unix_user', 'os2_home'):
            self.assertIn(key, INSTALL_SCHEMES)

        dist = Distribution({'name': 'xx'})
        cmd = install(dist)
        options = [ name for name, short, lable in cmd.user_options ]
        self.assertIn('user', options)
        cmd.user = 1
        self.assertFalse(os.path.exists(self.user_base))
        self.assertFalse(os.path.exists(self.user_site))
        cmd.ensure_finalized()
        self.assertTrue(os.path.exists(self.user_base))
        self.assertTrue(os.path.exists(self.user_site))
        self.assertIn('userbase', cmd.config_vars)
        self.assertIn('usersite', cmd.config_vars)

    def test_handle_extra_path(self):
        dist = Distribution({'name': 'xx',
         'extra_path': 'path,dirs'})
        cmd = install(dist)
        cmd.handle_extra_path()
        self.assertEqual(cmd.extra_path, ['path', 'dirs'])
        self.assertEqual(cmd.extra_dirs, 'dirs')
        self.assertEqual(cmd.path_file, 'path')
        cmd.extra_path = ['path']
        cmd.handle_extra_path()
        self.assertEqual(cmd.extra_path, ['path'])
        self.assertEqual(cmd.extra_dirs, 'path')
        self.assertEqual(cmd.path_file, 'path')
        dist.extra_path = cmd.extra_path = None
        cmd.handle_extra_path()
        self.assertEqual(cmd.extra_path, None)
        self.assertEqual(cmd.extra_dirs, '')
        self.assertEqual(cmd.path_file, None)
        cmd.extra_path = 'path,dirs,again'
        self.assertRaises(DistutilsOptionError, cmd.handle_extra_path)
        return

    def test_finalize_options(self):
        dist = Distribution({'name': 'xx'})
        cmd = install(dist)
        cmd.prefix = 'prefix'
        cmd.install_base = 'base'
        self.assertRaises(DistutilsOptionError, cmd.finalize_options)
        cmd.install_base = None
        cmd.home = 'home'
        self.assertRaises(DistutilsOptionError, cmd.finalize_options)
        cmd.prefix = None
        cmd.user = 'user'
        self.assertRaises(DistutilsOptionError, cmd.finalize_options)
        return

    def test_record(self):
        install_dir = self.mkdtemp()
        project_dir, dist = self.create_dist(py_modules=['hello'], scripts=['sayhi'])
        os.chdir(project_dir)
        self.write_file('hello.py', "def main(): print 'o hai'")
        self.write_file('sayhi', 'from hello import main; main()')
        cmd = install(dist)
        dist.command_obj['install'] = cmd
        cmd.root = install_dir
        cmd.record = os.path.join(project_dir, 'filelist')
        cmd.ensure_finalized()
        cmd.run()
        f = open(cmd.record)
        try:
            content = f.read()
        finally:
            f.close()

        found = [ os.path.basename(line) for line in content.splitlines() ]
        expected = ['hello.py',
         'hello.pyc',
         'sayhi',
         'UNKNOWN-0.0.0-py%s.%s.egg-info' % sys.version_info[:2]]
        self.assertEqual(found, expected)

    def test_record_extensions(self):
        install_dir = self.mkdtemp()
        project_dir, dist = self.create_dist(ext_modules=[Extension('xx', ['xxmodule.c'])])
        os.chdir(project_dir)
        support.copy_xxmodule_c(project_dir)
        buildextcmd = build_ext(dist)
        support.fixup_build_ext(buildextcmd)
        buildextcmd.ensure_finalized()
        cmd = install(dist)
        dist.command_obj['install'] = cmd
        dist.command_obj['build_ext'] = buildextcmd
        cmd.root = install_dir
        cmd.record = os.path.join(project_dir, 'filelist')
        cmd.ensure_finalized()
        cmd.run()
        f = open(cmd.record)
        try:
            content = f.read()
        finally:
            f.close()

        found = [ os.path.basename(line) for line in content.splitlines() ]
        expected = [_make_ext_name('xx'), 'UNKNOWN-0.0.0-py%s.%s.egg-info' % sys.version_info[:2]]
        self.assertEqual(found, expected)

    def test_debug_mode(self):
        old_logs_len = len(self.logs)
        install_module.DEBUG = True
        try:
            with captured_stdout():
                self.test_record()
        finally:
            install_module.DEBUG = False

        self.assertGreater(len(self.logs), old_logs_len)


def test_suite():
    return unittest.makeSuite(InstallTestCase)


if __name__ == '__main__':
    run_unittest(test_suite())
# okay decompyling c:\Users\PC\wotsources\files\originals\res_bw\scripts\common\lib\distutils\tests\test_install.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.11.10 21:35:25 St�edn� Evropa (b�n� �as)
