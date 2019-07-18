import os
import sys
from ..gotomagic.text import GotoWarning


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


def detect_unescaped_ampersand_url():
    '''
        Detects if user has entered a url with ampersand,
        and accidentaly launched goto in the background,
        cutting the url in half

        based on
        https://stackoverflow.com/questions/24861351/how-to-detect-if-python-script-is-being-run-as-a-background-process
    '''
    if len(sys.argv) < 3:
        return False
    command = sys.argv[2]
    if command in ['add', 'update']:
        try:
            if os.getpgrp() == os.tcgetpgrp(sys.stdout.fileno()):
                # Interactive mode
                return False
            else:
                # Background mode
                return True
        # exception triggered if piping output to a file:
        # i.e  goto list > /tmp/lol
        except Exception:
            pass
    return False


def healthcheck():
    '''
        Runs all healthchecks.
        Currently there is only one:
            - detect_unescaped_ampersand_url

        returns GotoWarning if any issues detected.
    '''
    if detect_unescaped_ampersand_url():
        if len(sys.argv) >= 3:
            command = sys.argv[2]
            magicword = sys.argv[3]
            return GotoWarning(
                'unescaped_ampersand_url_detected',
                command=command,
                magicword=magicword
            )
    # No issues detected
    return None
