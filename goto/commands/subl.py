import subprocess
from ..gotomagic.text import Error


def subl(magic, _):
    """
    Launch Sublime Text in the code folder
    """

    try:
        code = magic['code']
    except KeyError:
        return None, Error("no_magicword_named_code")

    try:
        subprocess.check_call('subl "%s"' % code, shell=True)
    except subprocess.CalledProcessError:
        return None, Error("subl_launch_failed")

    return None, None
