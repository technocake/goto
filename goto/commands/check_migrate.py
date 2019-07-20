# coding: utf-8
from __future__ import unicode_literals

from ..gotomagic.text import GotoError, GotoWarning
from ..gotomagic.utils import detect_unmigrated_data


def check_migrate(magic, command, args, options):
    ''' checks if we need to migrate underlaying data structure in goto'''

    if detect_unmigrated_data():
            return None, GotoWarning('data_not_migrated')
    else:
        return "Nothing to migrate", None
