# code: utf-8
"""
Magic is stored here.
"""
import json
import os


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
