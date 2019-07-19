# coding: utf-8
from __future__ import unicode_literals
import os
import shutil

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
        return migrate_data()
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
    jfiles = list_jfiles()
    migrations = 0

    output = ['Found {} projects to migrate'.format(len(jfiles))]
    warning = None

    for jfile in jfiles:
        project = jfile.split('.json')[0]
        fpath = os.path.join(projects_folder, jfile)
        target = os.path.join(projects_folder, project, 'private', 'magicwords.json')  # noqa

        # project cmd used to leave empty files for each project
        stubfile = os.path.join(projects_folder, project)
        if os.path.isfile(stubfile):
            os.remove(stubfile)

        create_project_folder(project)

        if not os.path.exists(target):
            shutil.move(
                fpath,
                target
            )
            migrations += 1
            output.append('moved {} to {}'.format(fpath, target))
        else:
            output.append('Skipping project {} (source file: {} destination file already exists: {}'.format(project, fpath, target))  # noqa

    output.append('{} of {} projects were migrated'.format(migrations, len(jfiles)))  # noqa

    if not migrations == len(jfiles):
        warning = GotoWarning('not_all_projects_migrated')  # noqa

    output = '\n'.join(output)
    return output, warning
