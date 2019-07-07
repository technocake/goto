import subprocess
from ..gotomagic.handlers import open_intellij

def intellij(magic, _):
    try:
        open_intellij(magic['code'])
    except KeyError:
        return None, "no_magicword_named_code"
    except subprocess.CalledProcessError:
        return None, "intellij_launch_failed"
