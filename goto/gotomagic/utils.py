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