from ..gotomagic.handlers import open_sublime

def subl(magic, args):
    try:
        open_sublime(magic['code'])
    except KeyError:
        return None, "no_magicword_named_code"
    except subprocess.CalledProcessError:
        return None, "subl_launch_failed"
