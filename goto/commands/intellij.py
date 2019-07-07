import subprocess
from ..gotomagic.utils import detect_platform
from ..gotomagic.text import Error


def intellij(magic, _):
    """
    Launch IntelliJ. Open it in the code folder.
    """

    platform = detect_platform()

    if platform in ['osx', 'linux']:
        cmd = "idea"
    elif platform == 'win':
        cmd = "idea.exe"

    try:
        code = magic['code']
    except KeyError:
        return None, Error("no_magicword_named_code")

    try:
        subprocess.check_call('%s "%s"' % (cmd, code), shell=True)
    except subprocess.CalledProcessError:
        return None, Error("intellij_launch_failed")

    return None, None
