
# errors
messages = dict(
    open_failed="""
Oh noes...
    - Something clogged up the magic, and the magicword could not be opened.

    Computer says: {message}
    """,

    magic_could_not_be_saved="""
Oh noes...!

    - Something clogged up the magic, and the magicwords could not be saved.

    Computer says: {message}

    If you want us to fix it - please tell us about this on github here:

        https://github.com/technocake/goto/issues

    Feel free to create a new issue if one does not already exist.

    """,

    subl_launch_failed="""
Error: could not launch Sublime Text

    This is most likely due to not having the subl command in path.

    For more info see:
        http://docs.sublimetext.info/en/latest/command_line/command_line.html
""",

    intellij_launch_failed="""
Error:  could not launch IntelliJ.

    This is most likely due to not having set up the IntelliJ
    Command Launching yet.

    To be able to launch IntelliJ from the command line,
    this feature must be activated from the IntelliJ menu on your system.

    For more info, see:

        https://www.jetbrains.com/help/idea/working-with-the-ide-features-from-command-line.html
    """,

    vscode_launch_failed="""
Error: could not launch vscode

    This is most likely due to not having set up the vscode
    Command Launching yet.

    For more info, see:

        https://code.visualstudio.com/docs/editor/command-line
    """,
)