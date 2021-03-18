# coding: utf-8
from __future__ import unicode_literals
import os
import shutil

from ..gotomagic.text import GotoError, GotoWarning
from ..gotomagic.utils import detect_unmigrated_data, prompt_to_migrate_data, list_jfiles, create_project_folder
from .. import settings


def help():
    return "{0:40}{1}".format('--migrate', 'Migrate data to new format')


def names():
    return ['--migrate']


def run(magic, command, args, options):
    """
    migrate magicwords.
    """

    if not detect_unmigrated_data():
        return "Nothing to migrate", None

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
    projects = []
    unmigrated_projects = []

    output = ['Found {} projects to migrate'.format(len(jfiles))]
    warning = None

    for jfile in jfiles:
        project = jfile.split('.json')[0]
        from_file = os.path.join(projects_folder, jfile)
        destination = os.path.join(projects_folder, project, 'private', 'magicwords.json')  # noqa

        # project cmd used to leave empty files for each project
        stubfile = os.path.join(projects_folder, project)
        if os.path.isfile(stubfile):
            os.remove(stubfile)

        create_project_folder(project)

        if move_magicwords(from_file, destination):
            migrations += 1
            projects += [project]
        else:
            unmigrated_projects += [project]
            output.append('Skipping project {} (source file: {} destination file already exists: {}'.format(project, from_file, destination))  # noqa

    output.append('{} of {} projects were migrated'.format(migrations, len(jfiles)))  # noqa
    output.append('Migrated projects: {}'.format(" ".join(projects)))  # noqa

    if not migrations == len(jfiles):
        warning = GotoWarning('not_all_projects_migrated', projects=" ".join(unmigrated_projects))  # noqa

    output = '\n'.join(output)
    return output, warning


def move_magicwords(from_file, destination):
    try:
        if not os.path.exists(destination):
            shutil.move(from_file, destination)
            return True
        else:
            return False
    except shutil.Error:
        # todo: user-friendly warning here.
        raise
