# code: utf-8
"""
project: goto

handlers to open different kinds of magic words.
Examples could be files, urls, visualstudio-solutions.
"""
import subprocess
import webbrowser
import os


def parse_magic_word(current_project, word):
    """ parses words in format of either:
            word
        or
            project.word

        reduces to a pair of project and word.

        TODO: not beeing used currently.
    """
    project, word = word.split('.') if "." in word else current_project, word
    return (project, word)


def parse_uri(raw_uri):
    ''' Main goal right now: distinguish filesystem paths
        and urls/uris.

        If no scheme is present, assume it is
        a filesystem path. And test for path existence.

        This embeds a rule that all web-urls must start with
        either http:// or https:// for goto to handle them
        properly. One might ponder if goto should magically
        understand that www.gotomagic.com (without scheme)
        is a http-uri.

        TODO: here one could test if the raw_uri
              could work as a valid http(s):// uri,
              in the case where a uri is entered
              with no scheme.

        To handle cases such as: `goto add .`
        if the raw_uri is a path, get the absolute
        path and store that.
    '''
    candidate = os.path.abspath(raw_uri)
    if os.path.exists(candidate):
        return candidate
    else:
        return raw_uri


def copy_to_clipboard(url):
    import pyperclip
    pyperclip.copy(url)


def open_sublime(code):
    "hack"
    subprocess.call('subl "%s"' % code, shell=True)


def open_folder(folder):
    "opens folders"
    folder = os.path.expanduser(folder)
    subprocess.call('open "%s"' % folder, shell=True)


def open_link(url):
    "Opens a link. Might do more stuff later."
    webbrowser.open(url)


def open_terminal(path):
    " Opens a new terminal window and cd-s to the given path "
    path = os.path.expanduser(path)
    subprocess.call(""" osascript <<END
                        tell app "Terminal" to do script "cd %s"
                        END
                    """ % path, shell=True)
