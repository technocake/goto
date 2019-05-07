from unittest import TestCase
import os

from .magic import GotoMagic

tmpgotofile = 'testgotofile.json'


class TestMagic(TestCase):
    def setUp(self):
        """ Sets up goto magic to use tmp file """
        self.magic = GotoMagic(tmpgotofile)

    def test_adding_shortcut(self):
        """ Adding shortcuts through the gotomagic module"""
        self.magic.add_shortcut('test', 'http://example.com')
        self.magic.save()

        self.assertTrue(os.path.exists(tmpgotofile),
                        'Adding shortcut on empty project'
                        ' did not create magic file')

    def tearDown(self):
        """ Empty testgotofile after each test """
        if os.path.exists(tmpgotofile):
            # Displaying contents of testfile
            with open(tmpgotofile) as f:
                print(f.read())
            os.remove(tmpgotofile)
