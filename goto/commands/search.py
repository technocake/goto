# coding: utf-8
from __future__ import unicode_literals
from ..gotomagic.magic import GotoMagic


def help():
    return "{0:10}{1:30}{2}".format('list', '[-v]', 'List all shortcuts')


def names():
    return ['--search', '-s']


def run(magic, command, args, options):
    """
    Search magicwords!
    """
    verbose = '-v' in options or '--verbose' in options
    global_search = '-g' in options or '--global' in options

    if (len(args) == 0):
        return None, GotoWarning("missing_magicword", command='search')

    query = args[0]
    index = all_project_magic(magic, global_search)

    # TODO update api in all_project_magic
    if not index:
        return None, None

    # Search
    magicwords = filter(search(query), index)

    output = "\n".join(magicwords)

    return output, None


def search(query):
    # search magicword
    return lambda shortcut: query in shortcut


def all_project_magic(magic, global_search=False):
    """Loads all projects GotoMagic for searching."""

    if global_search:
        projects = magic.list_projects()
    else:
        projects = [magic.project]

    #TODO handle None

    magic = {}
    index = []

    for project in projects:
        m = GotoMagic(project)
        magic[project] = m
        magicwords = m.list_shortcuts()

        for magicword in magicwords:
            shortformat = "{}.{}".format(project, magicword)
            index.append(shortformat)
            #index.append((project, magicword, shortformat))

    return index