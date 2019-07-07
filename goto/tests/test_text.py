from unittest import TestCase
import os

from ..gotomagic.text import GotoWarning, GotoError, error, warning


class TestMagicText(TestCase):

    def test_getting_warning_message(self):
        """ Should get some text"""
        warn = GotoWarning('show_missing_magicword')

        self.assertEqual(warn.message,
                         warning.messages['show_missing_magicword'],
                         "Message differs")

