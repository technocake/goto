# code: utf-8
"""
Magic is stored here.
"""
import json
import codecs
import os

from . import text
from .text import print_text


class GotoMagic():
    """ Goto's Black box.

        Nah, not really, it is just the place where
        magic shortcuts are created, updated, removed and
        used.

        tl-dr: saving magic as json.
    """

    def __init__(self, jfile):
        """ Loads json from jfile """
        self.jfile = jfile
        self.magic = load_magic(jfile)

    def reload(self):
        """ reload the magic """
        self.__init__(self.jfile)

    def save(self):
        """ Saves the magic to jsonfile jfile """
        save_magic(self.jfile, self.magic)

    def add_shortcut(self, magicword, uri):
        """ Adds a magic shortcut if it does not exist yet.
            If it exists, it warns the user.
        """
        uri = parse_uri(uri)
        if magicword in self.magic.keys():
            print_text(
                text.warning.messages["adding_existing_magicword"],
                magicword=magicword,
                uri=self.magic[magicword],
                newuri=uri
            )
            exit(1)
        else:
            self.magic[magicword] = uri

    def update_shortcut(self, magicword, uri):
        """ Simply overwrites the content of the magicword """
        uri = parse_uri(uri)
        if magicword in self.magic.keys():
            self.magic[magicword] = uri
        else:
            print_text(
                text.warning.messages["updating_nonexisting_magicword"],
                magicword=magicword
            )
            exit(1)

    def remove_shortcut(self, magicword):
        """ Simply removes a shortcut """
        try:
            self.magic.pop(magicword)
        except KeyError:
            print_text(
                text.warning.messages["removing_nonexisting_magicword"],
                magicword=magicword
            )
            exit(1)

    def show_shortcut(self, magicword):
        """ shows a shortcut """
        try:
            print(self.magic[magicword])
        except KeyError:
            print_text(
                text.warning.messages["magicword_does_not_exist"],
                magicword=magicword
            )
            exit(1)

    def get_uri(self, magicword):
        """ returns the uri from the shortcut of name <magicword> """
        try:
            return self.magic[magicword]
        except KeyError:
            print_text(
                text.warning.messages["magicword_does_not_exist"],
                magicword=magicword
            )
            return None

    def list_shortcuts(self, verbose=False):
        """ Lists all magicwords.
            Optionally may list verbosedly all uris too
            if verbose = True.
        """
        if verbose:
            for key in sorted(self.magic.keys()):
                value = self.magic[key]
                print("%16s --> %s" % (key, value))
        else:
            for key in sorted(self.magic.keys()):
                print(key)

    def __getitem__(self, key):
        """
            Makes it possible to do print(magic[magiword])
        """
        return self.magic[key]

    def __missing__(self, key):
        """
            ux when magicword is missing
        """
        print_text(
            text.warning.messages["magicword_does_not_exist"],
            magicword=key
        )

    def __setitem__(self, key, value):
        """ sets a magicword. Brutal style """
        self.magic[key] = value

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
            magic = json.loads(f.read())
    else:
        magic = {}
    return magic


def save_magic(jfile, magic):
    "saves the magic shortcuts as json into a file"
    with codecs.open(jfile, 'w+', encoding='utf-8') as f:
        try:
            data = json.dumps(magic, sort_keys=True, indent=4, ensure_ascii=False)
            f.write(data)
        except Exception as e:
            print_text(
                text.error.messages["magic_could_not_be_saved"],
                message=e.message
            )
