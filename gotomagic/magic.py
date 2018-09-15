# code: utf-8
"""
Magic is stored here.
"""
import json
import os
import gotomagic.text as text
from gotomagic.text import print_text


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

    def save(self):
        """ Saves the magic to jsonfile jfile """
        save_magic(self.jfile, self.magic)

    def add_shortcut(self, magicword, uri):
        """ Adds a magic shortcut if it does not exist yet.
            If it exists, it warns the user.
        """
        if magicword in self.magic.keys():
            print_text(
                text.warning["adding_existing_magicword"],
                magicword=magicword,
                uri=uri
            )
        else:
            self.magic[magicword] = uri

    def update_shortcut(self, magicword, uri):
        """ Simply overwrites the content of the magicword """
        self.magic[magicword] = uri

    def remove_shortcut(self, magicword):
        """ Simply removes a shortcut """
        try:
            self.magic.pop(magicword)
        except KeyError:
            print_text(
                text.warning["removing_nonexisting_magicword"],
                magicword=magicword
            )

    def show_shortcut(self, magicword):
        """ shows a shortcut """
        try:
            print(self.magic[magicword])
        except KeyError:
            print_text(
                text.warning["magicword_does_not_exist"],
                magicword=magicword
            )

    def get_uri(self, magicword):
        """ returns the uri from the shortcut of name <magicword> """
        try:
            return self.magic[magicword]
        except KeyError:
            print_text(
                text.warning["magicword_does_not_exist"],
                magicword=magicword
            )

    def list_shortcuts(self, verbose=False):
        """ Lists all magicwords.
            Optionally may list verbosedly all uris too
            if verbose = True.
        """
        if verbose:
            for k, v in self.magic.items():
                print("%16s --> %s" % (k, v))
        else:
            for k in self.magic.keys():
                print(k)

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
            text.warning["magicword_does_not_exist"],
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


def load_magic(jfile):
    "Loads the magic shortcuts from a json file object"
    if os.path.isfile(jfile) and os.path.getsize(jfile) > 0:
        with open(jfile, 'r') as f:
            magic = json.load(f)
    else:
        magic = {}
    return magic


def save_magic(jfile, magic):
    "saves the magic shortcuts as json into a file"
    with open(jfile, 'w+') as f:
        json.dump(magic, f, sort_keys=True, indent=4)
