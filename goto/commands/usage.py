def usage():
    """
    Get information about usage
    """

    return """
    Goto - the magic traveler, how may I help you?

    Wondering how to change project?
        project help                  Consult my brother in command

    The basics
        goto <magicword>                        Go to shortcut
        goto add    <magicword> <url or path>   Add shortcut
        goto update <magicword> <new url/path>  Update shortcut
        goto rename <magicword> <new name>      Rename shortcut
        goto rm     <magicword>                 Remove shortcut
        goto show   <magicword>                 Show url of shortcut
        goto list                               List all shortcuts
        goto list -v                            With the urls printed

    Working with folders and files
        goto <magicword>              Goto will cd to a folder shortcut by default.
        goto cd   <magicword>         cd in terminal
        goto open <magicword>         Open in finder/file explorer

    Launching Code editors
        goto subl                     Opens Sublime Text in code folder* 
        goto idea                     Opens IntelliJ in code folder*
        goto vscode                   Opens Visual Studio Code in code folder*

    * requires a magicword named code pointing to a folder.
        goto add code <path to folder with code>

    """, None # noqa
