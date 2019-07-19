# coding: utf-8
from __future__ import unicode_literals
import os

from ..gotomagic.text import GotoError, GotoWarning
from ..gotomagic.utils import detect_unmigrated_data, prompt_to_migrate_data, list_jfiles, create_project_folder
from .. import settings


def migrate(magic, command, args):
    """
    migrate magicwords.
    """

    if not detect_unmigrated_data():
        return "Nothing to migrate", None
    elif '--check-migrate' in command:
        return None, GotoWarning('data_not_migrated')

    if prompt_to_migrate_data():
        migrate_data()
        return 'All projects are now migrated', None
    else:
        return None, GotoWarning('goto_wont_work_without_migrating_data')


def migrate_data():
    ''' Migrating data

        goto format:
        from v0 - 1.5.x
        to  v1.6.0 and above
    '''
    GOTOPATH = settings.GOTOPATH
    projects_folder = os.path.join(GOTOPATH, 'projects')

    for jfile in list_jfiles():
        project = jfile.split('.json')[0]
        target = os.path.join(projects_folder, project, 'private', 'magicwords.json')  # noqa

        # project cmd used to leave empty files for each project
        stubfile = os.path.join(projects_folder, project)
        if os.path.isfile(stubfile):
            os.remove(stubfile)

        create_project_folder(project)

        if not os.path.exists(target):
            os.rename(
                os.path.join(projects_folder, jfile),
                target
            )
