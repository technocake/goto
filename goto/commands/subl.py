import subprocess
from ..gotomagic.text import GotoError, GotoWarning


def subl(magic, _):
    """
    Launch Sublime Text in the code folder
    """

    try:
        code = magic['code']
    except KeyError:
        return None, GotoWarning("no_magicword_named_code")

    try:
        subprocess.check_call('subl "%s"' % code, shell=True)
    except subprocess.CalledProcessGotoError:
        return None, GotoError("subl_launch_failed")

    return None, None
