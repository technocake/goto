"""Flask Application."""

import os, subprocess, sys

# load libaries
from flask import Flask, render_template

from goto import GotoMagic
from goto.the_real_goto import run_command, parse_args

# init Flask app
app = Flask(__name__)

project = None


# view functions
@app.route('/', defaults={'project': project})
@app.route('/map', defaults={'project': project})
@app.route('/map/<project>')
def map(project):
    """Show magic."""
    project = detect(project)
    magic = GotoMagic(project)
    shortcuts = magic.magic.items()
    return render_template('map.html', project=project, shortcuts=shortcuts)


@app.route('/projects')
def projects():
    """Show the magic projects!"""
    project = detect(None)
    projects = list_projects()
    return render_template('projects.html', projects=projects, project=project)


@app.route('/<magicword>', defaults={'project': project})
@app.route('/<magicword>/<project>')
def goto(magicword, project):
    return run_goto(magicword, project)


@app.route('/project/<project>')
def project(project):
    return subprocess.check_output(
        f"project {project}",
        shell=True
        ).decode(sys.stdout.encoding)

def detect(project):
    if project is None:
        return subprocess.check_output('project').rstrip().decode(sys.stdout.encoding)
    else:
        return project

def list_projects():
    projects = subprocess.check_output('project list', shell=True).decode(sys.stdout.encoding).split('\n')
    return projects

def run_goto(magicword, project=None):

    project = detect(project)

    magic = GotoMagic(project)
    argv = [magicword]
    command, args, options = parse_args(argv)

    if command is None:
        options = ["--open"]

    output, err = run_command(magic, command, args, options)

    if err:
        return err.message
    if output is not None:
        return output

    try:
        uri = magic.get_uri(magicword)
        return uri
    except:
        return "something is off."
    return "something is off."


if __name__ == "__main__":
    ####################
    # FOR DEVELOPMENT
    ####################
    app.run(host='0.0.0.0', port=80, debug=True)