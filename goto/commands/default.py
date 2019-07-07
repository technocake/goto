from ..gotomagic.handlers import open_folder, open_link

def default(magic, command):
    # default
    url = magic.get_uri(command)
    if url is None:
        return

    if is_file(url):
        open_folder(url)
    else:
        open_link(magic[command])
