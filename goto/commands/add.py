import sys
from ..gotomagic.text import print_text
from ..gotomagic import text

def run(magic):
    try:
        magic.add_shortcut(sys.argv[3], sys.argv[4])
        magic.save()
        print('Added magic word %s' % sys.argv[3])
        return 0
    except IndexError:
        if len(sys.argv) > 3:
            print_text(
                text.warning["missing_uri"],
                magicword=sys.argv[3]
            )
            return 1
        else:
            print_text(
                text.warning["missing_magicword_and_uri"]
            )
        return 1
