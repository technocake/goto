import subprocess


def subl(magic, _):
    """
    Launch Sublime Text in the code folder
    """

    try:
        code = magic['code']
    except KeyError:
        return None, "no_magicword_named_code"

    try:
        subprocess.check_call('subl "%s"' % code, shell=True)
    except subprocess.CalledProcessError:
        return None, "subl_launch_failed"

    return None, None
