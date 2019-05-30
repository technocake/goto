# code: utf-8
"""
project: goto

handlers to open different kinds of magic words.
Examples could be files, urls, visualstudio-solutions.
"""
import subprocess
import webbrowser
import os
import sys

from .utils import detect_platform


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


def copy_to_clipboard(url):
    import pyperclip
    pyperclip.copy(url)


def open_sublime(code):
    """
        Launches Sublime Text in the code folder via the subl cli-command.

        throws
            subprocess.CalledProcessError if not able to run the subl command.
    """
    subprocess.check_call('subl "%s"' % code, shell=True)


def open_vscode(code):
    """
        Launches Visual Studio Code in the code folder via cli.

        throws
            subprocess.CalledProcessError if not able to run the code command.
    """
    subprocess.check_call('code "%s"' % code, shell=True)


def open_intellij(code):
    """
        Launches IntelliJ from command line and opens it in the code folder.

        throws
            subprocess.CalledProcessError if not able to run the idea command.
    """
    platform = detect_platform()

    if platform in ['osx', 'linux']:
        cmd = "idea"
    elif platform == 'win':
        cmd = "idea.exe"
    subprocess.check_call('%s "%s"' % (cmd, code), shell=True)


def open_folder(folder):
    "opens folders"
    folder = os.path.expanduser(folder)
    platform = detect_platform()
    if platform == 'linux':
        subprocess.call('xdg-open "%s"' % folder, shell=True)
    elif platform == 'osx':
        subprocess.call('open "%s"' % folder, shell=True)
    elif platform == 'win':
        subprocess.call('start "%s"' % folder, shell=True)


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
