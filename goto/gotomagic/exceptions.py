''' Goto exceptions

Somehow related to GotoWarnings and GotoErrors
'''
from .text import GotoWarning, GotoError


class GotoException(Exception):
    '''
        Usage:
            >>> raise GotoException(
            >>>         'adding_existing_magicword_short',
            >>>          magicword=magicword)

    '''

    def __init__(self, msg=None, **kwargs):
        if msg is None:
            raise Exception("Programming error - msg not specified")
        self.message = GotoWarning(msg, **kwargs).message

# Hack
warnings = type('warnings', (object,), {'GotoException': GotoException})  # noqa