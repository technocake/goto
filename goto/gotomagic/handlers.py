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
    "hack"
    subprocess.call('subl "%s"' % code, shell=True)


def open_folder(folder):
    "opens folders"
    folder = os.path.expanduser(folder)
    if sys.platform in ['linux', 'linux2']:
        subprocess.call('xdg-open "%s"' % folder, shell=True)
    elif sys.platform in ['darwin']:
        subprocess.call('open "%s"' % folder, shell=True)
    elif sys.platform in ['win32']:
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
