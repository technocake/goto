import os
import sys


def detect_platform():
    """
        Detects if we are on osx, linux or win
    """

    if sys.platform in ['linux', 'linux2']:
        return 'linux'
    elif sys.platform in ['darwin']:
        return 'osx'
    elif sys.platform in ['win32']:
        return 'win'
    raise Exception("Error: Unknown platform. Could not determine if running linux, osx or windows")  # noqa


def is_file(raw_uri):
    ''' checks if the file or folder exist and returns True if so '''
    candidate = os.path.abspath(raw_uri)
    return os.path.exists(candidate)
