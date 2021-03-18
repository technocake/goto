#  coding: utf-8
"""
Magic is stored here.
"""
from __future__ import absolute_import, unicode_literals
from builtins import dict, str  # redefine dict and str to be py3-like in py2.
# http://johnbachman.net/building-a-python-23-compatible-unicode-sandwich.html

import json
import codecs
import os
import sys

from .text import GotoWarning
from .. import settings
from . import utils


class GotoMagic():
    """ Goto's Black box.

        Nah, not really, it is just the place where
        magic shortcuts are created, updated, removed and
        used.

        tl-dr: saving magic as json.
    """

    def __init__(self, project, scope='private', GOTOPATH=None):
        """ Loads json from jfile """
        if GOTOPATH is None:
            GOTOPATH = settings.GOTOPATH
        self.project = project

        # Creates folder only if not exisiting
        utils.create_project_folder(project, scope, GOTOPATH)

        self.jfile = os.path.join(
            GOTOPATH, 'projects', project, scope, "magicwords.json")
        self.magic = load_magic(self.jfile)

    def reload(self):
        """ reload the magic """
        self.__init__(self.jfile)   

    def _magic_set(self, key, value):
        '''
            Single point of entry for writing magicwords and uris
            to the internal dict.

            This method makes sure that it is encoded
            as utf-8 unicode strings on python2.
        '''
        if sys.version_info[0] == 2:
            if not isinstance(key, unicode):
                key = unicode(key, encoding='utf-8')

            if not isinstance(value, unicode):
                value = unicode(value, encoding='utf-8')

        self.magic[key] = value
        return None

    def save(self):
        """ Saves the magic to jsonfile jfile """
        err = save_magic(self.jfile, self.magic)
        return err

    def add_shortcut(self, magicword, uri):
        """ Adds a magic shortcut if it does not exist yet.
            If it exists, it warns the user.
        """
        if magicword in self.magic.keys():
            return GotoWarning("adding_existing_magicword", 
                magicword=magicword,
                uri=self.magic[magicword],
                newuri=uri
            )

        # setting the magic
        uri = parse_uri(uri)
        err = self._magic_set(magicword, uri)
        if err:
            return err
        return None

    def update_shortcut(self, magicword, uri):
        """ Simply overwrites the content of the magicword """
        uri = parse_uri(uri)
        if magicword in self.magic.keys():
            err = self._magic_set(magicword, uri)
            if err:
                return err
            return None
        else:
            return GotoWarning("updating_nonexisting_magicword", magicword=magicword)


    def rename_shortcut(self, from_magicword, to_magicword, overwrite=False):
        """ Renaming a shortcut 
            Possible errors:

            from_magicword not existing -- checked first
            to_magicword existing -- checked second

            But it is allowed to overwrite to_magicword
            if overwrite == True.
        """
        if from_magicword not in self.magic:
            return GotoWarning('magicword_does_not_exist', magicword=from_magicword)  # noqa

        if not overwrite and to_magicword in self.magic:
            uri = self.magic[to_magicword]
            return GotoWarning('adding_existing_magicword_short', magicword=to_magicword, uri=uri)  # noqa


        from_uri = self.magic[from_magicword]
        del self.magic[from_magicword]
        err = self._magic_set(to_magicword, from_uri)
        
        if err:
            return err
        return None

    def remove_shortcut(self, magicword):
        """ Simply removes a shortcut """
        try:
            self.magic.pop(magicword)
            return None
        except KeyError:
            return GotoWarning("removing_nonexisting_magicword", magicword=magicword)

    def get_uri(self, magicword):
        """ returns the uri from the shortcut of name <magicword> """
        if magicword in self.magic.keys():
            return self.magic[magicword]
        else:
            return None
            

    def list_shortcuts(self, verbose=False):
        """ Lists all magicwords.
            Optionally may list verbosedly all uris too
            if verbose = True.
        """
        return sorted(self.magic.keys())
        

    def __getitem__(self, key):
        """
            Makes it possible to do print(magic[magiword])
        """
        return self.magic[key]

    def __missing__(self, key):
        """
            ux when magicword is missing
        """
        pass

    def __setitem__(self, key, value):
        """ sets a magicword. Brutal style """
        self._magic_set(key, value)

    def __delitem__(self, key):
        """ removes a magicword. Brutal style """
        self.magic.pop(key)

    def __len__(self):
        """ returns number of magicwords. """
        return len(self.magic.keys())

    def keys(self):
        return self.magic.keys()


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
        # it is not a file or directory
        # So it must be an uri.
        # But which kind?
        return raw_uri



def load_magic(jfile):
    "Loads the magic shortcuts from a json file object"
    if os.path.isfile(jfile) and os.path.getsize(jfile) > 0:
        with codecs.open(jfile, 'r', encoding="utf-8") as f:
            if sys.version_info[0] == 2:
                magic = json.loads(f.read(), encoding='utf-8')
            else:
                magic = json.loads( f.read())
    else:
        magic = {}
    return magic


def save_magic(jfile, magic):
    "saves the magic shortcuts as json into a file"
    with codecs.open(jfile, 'w+', encoding='utf-8') as f:
        try:
            if sys.version_info[0] == 2:
                data = json.dumps(magic, sort_keys=True, indent=4, ensure_ascii=False, encoding='utf-8')
                f.write(unicode(data))
            else:
                data = json.dumps(magic, sort_keys=True, indent=4, ensure_ascii=False)
                f.write(data)
            return None
        except Exception as e:
            return GotoWarning("magic_could_not_be_saved", message=str(e))
