from unittest import TestCase
import os
import shutil

from ..gotomagic.magic import GotoMagic


# Setting up a temporary gotopath.
TMPGOTOPATH = '/tmp/.goto-unit-tests'
project = '__testgoto__'
tmpgotofile = os.path.join(TMPGOTOPATH, 'projects', project, 'private', 'magicwords.json')  # noqa


class TestMagic(TestCase):
    def setUp(self):
        """ Sets up goto magic to use tmp file """
        self.magic = GotoMagic(project, scope='private', GOTOPATH=TMPGOTOPATH)

    def test_adding_shortcut(self):
        """ Adding shortcuts through the gotomagic module"""
        self.magic.add_shortcut('test', 'http://example.com')
        self.magic.save()

        self.assertTrue(os.path.exists(tmpgotofile),
                        'Adding shortcut on empty project'
                        ' did not create magic file')

    def tearDown(self):
        """ Empty testgotofile after each test """
        if os.path.exists(TMPGOTOPATH):
            # Displaying contents of testfile
            with open(tmpgotofile) as f:
                print(f.read())
            shutil.rmtree(TMPGOTOPATH)
