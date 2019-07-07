from unittest import TestCase
from string import Formatter

from ..gotomagic.text import GotoWarning, GotoError, error, warning


def get_dict_with_format_args(message):
    """
        Returns a dict of all expected keyword arguments
        in a formated string. Where the value for each key is the key.

        'Hello {name}' would return: {'name': 'name'}
    """
    args = [arg[1] for arg in Formatter().parse(message) if arg[1] is not None]
    return {key: key for key in args}


class TestMagicText(TestCase):

    def test_getting_warning_message(self):
        """
        Testing GotoWarning to return properly formated
        text for all warning messages.
        """

        for message_name in warning.messages.keys():
            raw_message = warning.messages[message_name]
            kwargs = get_dict_with_format_args(raw_message)

            warn = GotoWarning(message_name, **kwargs)
            expected_message = raw_message.format(**kwargs)

            self.assertEqual(warn.message,
                             expected_message,
                             "Message differs for {}".format(message_name))

    def test_getting_error_message(self):
        """
        Testing GotoError to return properly formated
        text for all error messages.
        """

        for message_name in error.messages.keys():
            raw_message = error.messages[message_name]
            kwargs = get_dict_with_format_args(raw_message)

            err = GotoError(message_name, **kwargs)
            expected_message = raw_message.format(**kwargs)

            self.assertEqual(err.message,
                             expected_message,
                             "Message differs for {}".format(message_name))
