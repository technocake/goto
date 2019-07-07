import subprocess


def vscode(magic, _):
    """
    Launch Visual Studio Code in the code folder
    """

    try:
        code = magic['code']
    except KeyError:
        return None, "no_magicword_named_code"

    try:
        subprocess.check_call('code "%s"' % code, shell=True)
    except subprocess.CalledProcessError:
        return None, "vscode_launch_failed"

    return None, None
