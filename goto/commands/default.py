import webbrowser
from ..gotomagic.utils import is_file
from ..gotomagic.text import GotoWarning, GotoError
from ..plugins import open


def help():
    return "<magicword>"


def names():
    return [None, '--default']


def run(magic, command, args, options):
    """
    Default behaviour when no commands are found in the first argument
    """
    verbose = '--verbose' in options or '-v' in options

    output = ""
    for magicword in args:
        uri = magic.get_uri(magicword)

        if uri is None:
            return None, GotoWarning('magicword_does_not_exist', magicword=magicword)  # noqa

        if is_file(uri):
            _output, err = open.run(magic, None, [magicword], verbose)
            if err:
                return None, err
            output += "%s\n" % _output
        else:
            try:
                webbrowser.open_new_tab(uri)
                output += "%s\n" % uri
            except webbrowser.Error:
                return None, GotoError('open_browser_tab_error')

    return output if verbose else None, None
