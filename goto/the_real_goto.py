#!/usr/bin/env python
# code: utf-8
'Goto - the magic project that takes you where you need to be, now.'
import sys
import codecs

from .gotomagic.handlers import *
from .gotomagic.magic import GotoMagic, is_file
from .gotomagic import text
from .gotomagic.text import print_text


# make sure we print in utf-8
try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
except:
    pass # TODO: implement utf-8 encoding of py2.7


def usage():
    return """
    Goto - the magic traveler, how may I help you?

    Wondering how to change project?
        project help                  Consult my brother in command

    The basics
        goto <magicword>                        Go to shortcut
        goto add    <magicword> <url or path>   Add shortcut      
        goto update <magicword> <url or path>   Update shortcut
        goto rm     <magicword>                 Remove shortcut
        goto show   <magicword>                 Show url of shortcut
        goto list                               List all shortcuts  
        goto list -v                            With the urls printed

    Working with folders and files
        goto <magicword>              Goto will cd to a folder shortcut by default. 
        goto cd   <magicword>         cd in terminal
        goto open <magicword>         Open in finder/file explorer
        goto -o   <magicword>                                    

    If you add a shortcut to a folder, and name it "code"...
        goto add code <path to folder with code>
        
    ...this command will open folder with Sublime Text
        goto subl                                

    """

def main():
    jfile = sys.argv[1]
    magic = GotoMagic(jfile)

    if len(sys.argv) == 2:
        print(usage())
        exit(0)

    if len(sys.argv) > 2:
        if sys.argv[2] in ['help', '-h', '/?', '--help']:
            print(usage())
            exit(0)

        if sys.argv[2] == 'add':
            try:
                magic.add_shortcut(sys.argv[3], sys.argv[4])
                magic.save()
                print('Added magic word %s' % sys.argv[3])
                exit(0)
            except IndexError:
                if len(sys.argv) > 3:
                    print_text(
                        text.warning["missing_uri"],
                        magicword=sys.argv[3]
                    )
                else:
                    print_text(
                        text.warning["missing_magicword_and_uri"]
                    )
                exit(1)

        if sys.argv[2] == 'update':
            magic.update_shortcut(sys.argv[3], sys.argv[4])
            magic.save()
            print('Updated magic word %s' % sys.argv[3])
            exit(0)

        if sys.argv[2] == 'rm':
            try:
                magic.remove_shortcut(sys.argv[3])
                magic.save()
                print('Removed magic word %s' % sys.argv[3])
                exit(0)
            except Exception:
                print('Failed to remove magic word %s' % sys.argv[3])
                exit(1)

        if sys.argv[2] == 'show':
            magic.show_shortcut(sys.argv[3])
            exit(0)

        if sys.argv[2] == 'copy':
            copy_to_clipboard(str(magic.get_uri(sys.argv[3])))
            exit(0)

        if sys.argv[2] == 'list':
            magic.list_shortcuts(verbose=('-v' in sys.argv))
            exit(0)

        if sys.argv[2] == 'subl':
            try:
                open_sublime(magic['code'])
            except KeyError:
                print(text.warning["no_magicword_named_code"])
            exit(0)

        if '-o' in sys.argv or '--open' in sys.argv or 'open' in sys.argv:
            open_folder(magic.get_uri(sys.argv[3]))
            exit(0)

        if sys.argv[2] == 'cd':
            open_terminal(magic.get_uri(sys.argv[3]))
            exit(0)
        # default
        url = magic.get_uri(sys.argv[2])
        if url is not None:
            if is_file(url):
                open_folder(url)
            else:
                open_link(magic[sys.argv[2]])

if __name__ == '__main__':
    main()
