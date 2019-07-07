from ..gotomagic.handlers import open_vscode

def vscode(magic, args):
    try:
        open_vscode(magic['code'])
    except KeyError:
        return None, "no_magicword_named_code"
    except subprocess.CalledProcessError:
        return "vscode_launch_failed"
