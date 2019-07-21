# coding: utf-8
from __future__ import unicode_literals


import os
import sys
from ..gotomagic.text import GotoWarning
from .. import settings

# py2-3 cheat sheet: http://python-future.org/compatible_idioms.html
# make Python 2 and 3 use input (instead of raw_input | input)
from builtins import input


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


def create_project_folder(project, scope='private', GOTOPATH=None):
    '''
        Creates project folder in goto state folders,
        if not already existing.

        scope can be either private or shared
    '''
    if GOTOPATH is None:
        GOTOPATH = settings.GOTOPATH

    project_folder = os.path.join(GOTOPATH, 'projects', project)
    scope_folder = os.path.join(GOTOPATH, 'projects', project, scope)

    # Both folders already exist
    if os.path.exists(project_folder)\
    and os.path.exists(scope_folder):
        return

    # project folder exist, BUT it is a file..
    if os.path.isfile(project_folder):
        return

    os.makedirs(scope_folder)


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


def list_jfiles():
    GOTOPATH = settings.GOTOPATH
    files = os.listdir(os.path.join(GOTOPATH, 'projects'))
    jfiles = filter(lambda f: '.json' in f, files)

    return list(jfiles)


def detect_unmigrated_data():
    '''
    Detects if the data in the gotopath folder is
    not migrated to the current latest version.

    The check is to see fi there is any json files
    in the root of ~/.goto/projects
    '''
    return len(list_jfiles()) != 0


def prompt_to_migrate_data():
    ''' Ask the user to migrate their project data '''
    try:
        return 'y' in input('Shall goto migrate your data now? [y|n]: ').lower()  # noqa
    except (IOError, EOFError, RuntimeError, KeyboardInterrupt):
        # In case of Ctrl+D or Ctrl+C
        return False


def handle_unescaped_ampersand_url():
    command = sys.argv[2]
    magicword = sys.argv[3]
    return GotoWarning('unescaped_ampersand_url_detected', command=command, magicword=magicword)  # noqa


def healthcheck():
    '''
    Runs all healthchecks.
        - detect_unescaped_ampersand_url
        - detect_unmigrated_data
    returns GotoWarning if any issues detected.
    '''
    if len(sys.argv) >= 3:
        if detect_unescaped_ampersand_url():
            return handle_unescaped_ampersand_url()

    if detect_unmigrated_data():
        # ugly hack to make it work
        if '--migrate' not in sys.argv and '--check-migrate' not in sys.argv:
            return GotoWarning('data_not_migrated')

    # No issues detected
    return None


# *----------  Python 2 fixes below ---------------------------------* #


def print_utf8(message):
    ''' fixes utf-8 unicode printing bugs in python 2.
        Making sure all printed strings are of the unicode type,
        and that they are encoded to bytes using the utf-8 encoding.

        All internal strings in goto should be utf-8 encoded.

        In python3 this is the default behaviour.
    '''
    if sys.version_info[0] == 2:
        if not isinstance(message, unicode):  # noqa
            message = unicode(message, 'utf-8')  # noqa
        message = message.encode('utf-8')

    print(message)


def fix_python2():
    '''
        Assume all input is utf-8.
        I am sure this will cause issues
    '''
    if sys.version_info[0] == 2:
        sys.argv = map(lambda arg: unicode(arg, 'utf8'), sys.argv)  # noqa


def make_sure_we_print_in_utf8():
    try:
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    except:
        pass  # TODO: implement utf-8 encoding of py2.7

