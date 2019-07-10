import codecs
import os
from ..gotomagic.text import GotoError, GotoWarning

GOTOPATH = os.environ.get('GOTOPATH', os.path.expanduser('~/.goto'))

def use(magic, command, args):

    if len(args) == 0:
        return None, GotoWarning('missing_project_name', command=command)

    project_name = args[0]
    project_file = GOTOPATH+'/projects/'+project_name
    active_project_file = GOTOPATH+'/active-project'

    if os.path.isfile(project_file):
        try:
            with codecs.open(active_project_file, 'w+', encoding='utf-8') as f:
                try:
                    f.write(project_name)
                    return u"Using existing project %s" % project_name, None
                except Exception as e:
                    return None, GotoError("project_not_changed", project=project_name, file=active_project_file)
        except Exception as e:
            return None, GotoError('no_such_file', file=active_project_file)
    else:
        try:
            with codecs.open(project_file, 'w+', encoding='utf-8') as f:
                pass
        except Exception as e:
            return None, GotoError('no_such_file', file=project_file)

        try:
            with codecs.open(active_project_file, 'w+', encoding='utf-8') as f:
                try:
                    f.write(project_name)
                    return u"Using new project %s" % project_name, None
                except Exception as e:
                    return None, GotoError("project_not_changed", project=project_name, file=active_project_file)
        except Exception as e:
            return None, GotoError('no_such_file', file=active_project_file)

