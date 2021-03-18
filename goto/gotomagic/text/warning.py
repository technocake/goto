# coding: utf-8
from __future__ import absolute_import, unicode_literals
from builtins import dict, str  # redefine dict and str to be py3-like in py2.


# warnings

messages = dict(
    adding_existing_magicword="""
Ah hoy!

    - You already have a magic word named {magicword},
    it points to: {uri}

    If you want to override it use:
        goto update {magicword} {newuri}
    """,

    adding_existing_magicword_short="""
Ah hoy!

    - You already have a magic word named {magicword},
    it points to: {uri}
    """,

    removing_nonexisting_magicword="""
Ah hoy!

    - Attempt to remove non-existing shortcut with name {magicword}

    Are you sure it exists in the project you are in now?
    Type:

        goto list

    to see all shortcuts in this project.
    """,

    updating_nonexisting_magicword="""
Ah hoy!

    - Attempt to update non-existing shortcut with name {magicword}

    Are you sure it exists in the project you are in now?
    Type:

        goto list

    to see all shortcuts in this project.
    """,

    magicword_does_not_exist="""
Ah hoy!

    - The Magic word {magicword} does not exist.

    Are you sure it exists in the project you are in now?
    Type:

        goto list

    to see all shortcuts in this project.
    """,

    no_magicword_named_code="""
Ah hoy!
    - No magicword named code.
    Create it with
        goto add code <path to folder>
    in order to be able to run goto subl.
    """,

    missing_uri="""
Ah hoy!
    - Remember, a shortcut has a name and a target uri (or path).

    Try again by adding another argument with where the shortcut
    should go to:

                goto {command} {magicword} <uri>
    """,

    missing_magicword="""
Ah hoy!
    Error: missing magic word.

    Try again by adding the magicword you want to {command}:

                goto {command} <magicword>
    """,

    missing_both_magicwords="""
Ah hoy!
    Error: missing both magicwords

    Try again by adding the magicword you want to {command}
    and the magicword you want to {command} to:

                goto {command} <from> <to>
    """,

    missing_to_magicword="""
Ah hoy!
    Error: missing second magic word.

    Try again by adding the magicword you want to {command} to:

                goto {command} {magicword} <to>
    """,

    missing_magicword_and_uri="""
Ah hoy!
    - Remember, a shortcut has a name and a target uri (or path).

    Try again by adding both a name and a uri/path to where the shortcut
    should go to:

                goto {command} <magicword> <uri>

    example:
        goto {command} website http://example.org
    """,

    unescaped_ampersand_url_detected="""
Ah hoy!
    - Detected an ampersand (&) in the uri.

    Since goto is ran in a shell, unescaped &'s will make
    goto run in the background, with only half of the uri
    you intended to give it.
    This is expected behaviour in bash/zsh.

    Effectively, chopping your url in half.

    Example: http://example.com?query=param&query2=param
    would loose everything after the & character.

    Try again, but this time wrap the url with "":

        goto {command} {magicword} "http://your-url?a=1&b=2"
    """,

    data_not_migrated="""
Ah hoy!
    - Goto detects that your magicwords needs to be migrated.


    This is because earlier versions of goto stored the
    project data in a different way.
    details: https://github.com/technocake/goto/issues/108
    But no worries, it can be done automagically:

    run the command:
        goto --migrate
    """,

    goto_wont_work_without_migrating_data="""
Ah hoy!

    Goto will not work before data is migrated.
    (the next time you run goto you will be prompted again)
    """,

    not_all_projects_migrated="""
Ah hoy!

    Not all projects could be migrated.
    Please check the output above and move files manually.

    Unmigrated projects: {projects}
""",

    rider_launch_failed="""
Error:  could not launch Rider.

    This is most likely due to not having set up the Rider
    Command Line Launching yet.

    To be able to launch Rider from the command line, see:

        https://www.jetbrains.com/help/rider/Opening_Files_from_Command_Line.html
    """,
)
