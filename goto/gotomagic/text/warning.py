
# warnings

messages = dict(
    adding_existing_magicword="""

Ah hoy!

    - You already have a magic word named {magicword},
    it points to: {uri}

    If you want to override it use:
        goto update {magicword} {newuri}
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

    missing_magicword_and_uri="""
Ah hoy!
    - Remember, a shortcut has a name and a target uri (or path).

    Try again by adding both a name and a uri/path to where the shortcut
    should go to:

                goto {command} <magicword> <uri>

    example:
        goto {command} website http://example.org
    """
)