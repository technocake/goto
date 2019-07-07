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

    Other editors supported:
    Visual Studio Code: goto vscode | IntelliJ: goto idea
    """, None # noqa
