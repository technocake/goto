# git.py
import os
import sys
import git
from .magic import GotoMagic


# HACK HACK
GOTOPATH = os.environ.get('GOTOPATH', os.path.expanduser('~/.goto'))



class GitMagic():
    """ Goto's Black Git box.

        Nah, not really, it is just the place where
        magic shortcuts are created, updated, removed and
        used.

        .. except also commited, and pushed.

        tl-dr: saving magic as json - then gitify the experience.
        https://gitpython.readthedocs.io/en/stable/tutorial.html
    """

    def __init__(self, project):
        """ Loads json from jfile """
        shared_file = os.path.join(
            GOTOPATH, 'projects', 'shared', project, '{}.json'.format(project)
        )

        shared_folder = os.path.dirname(shared_file)
        if not os.path.exists(shared_folder):
            os.makedirs(shared_folder)

        if not is_git_repo(shared_folder):
            self.repo = git.Repo.init(shared_folder)
        else:
            self.repo = git.Repo(shared_folder)

        shared_magic = GotoMagic(shared_file)
        self.magic = shared_magic

    def reload(self):
        """ reload the underlaying magic """
        self.magic.reload()

    def share(self):
        """
        Interpreting a share as to push to a remote.
        For now.
        """
        gotohub = self.repo.remotes.gotohub
        # may raise git.exc.GitCommandError
        gotohub.pull('master')
        gotohub.push('master')


    def save(self):
        """ Saves the magic to jsonfile jfile """
        self.magic.save()
        self.repo.git.add(self.magic.jfile)
        self.repo.index.commit(self.message)

    def add_shortcut(self, magicword, uri):
        """ Adds a magic shortcut if it does not exist yet.
            If it exists, it warns the user.
        """
        self.magic.add_shortcut(magicword, uri)
        self.message = "add magicword {}".format(magicword)

    def update_shortcut(self, magicword, uri):
        """ Simply overwrites the content of the magicword """
        self.magic.update_shortcut(magicword, uri)
        self.message = "update magicword {}".format(magicword)

    def remove_shortcut(self, magicword):
        """ Simply removes a shortcut """
        self.magic.remove_shortcut(magicword)
        self.message = "rm magicword {}".format(magicword)

    def show_shortcut(self, magicword):
        """ shows a shortcut """
        self.magic.show_shortcut(magicword)

    def get_uri(self, magicword):
        return self.magic.get_uri(magicword)

    def list_shortcuts(self, verbose=False):
        """ Lists all magicwords.
            Optionally may list verbosedly all uris too
            if verbose = True.
        """
        self.magic.list_shortcuts(verbose)

    def __getitem__(self, key):
        """
            Makes it possible to do print(magic[magiword])
        """
        return self.magic[key]

    def __missing__(self, key):
        """
            ux when magicword is missing
        """
        self.magic.__missing__(key)

    def __setitem__(self, key, value):
        """ sets a magicword. Brutal style """
        self.message = "set magicword {}".format(key)
        self.magic[key] = value

    def __delitem__(self, key):
        """ removes a magicword. Brutal style """
        self.message = "rm magicword {}".format(key)
        self.magic.__delitem__(key)

    def __len__(self):
        """ returns number of magicwords. """
        return len(self.magic)

    def keys(self):
        return self.magic.keys()



def is_git_repo(path):
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False
