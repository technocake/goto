## Goto
v1.5.3

*Goto is a magic tool that takes you were you want to be, now.*

When you are involved in different projects,  they all  have their own folders, important files, links to good articles or key websites. The problem is that all these are spread out on different locations.

By adding shortcuts to goto, so called magic words, you can jump to them.
The shortcuts are associated with a project name. And you can switch the project context
any time.

### Usage

```bash
$ project your-project
active project is now: your-project

$ goto add github https://github.com/user/your-project
Added magic word github

$ goto github
# opens https://github.com/user/your-project in your browser
```

### Setup

#### Mac OS-X / Linux / Win (git bash)
```
pip install magicgoto
```
After install, close and reopen your terminal.

#### Windows (using gitbash)
Open git bash and do the same as above.


git bash is included when you install git on windows usually.

Some git bash installs comes without any rcfile. 
If you get this error: `Ah hoy! Failed to determine rcfile...` 
you can fix it by running`touch ~/.bash_profile` and then `install_goto`




#### Linux - User Site install
On linux, the recommended way to install goto is by `pip install --user magicgoto`


> This requires that you have your User site bin  in your path.
> Usually this is `~/.local/bin`. So adding `PATH="${HOME}/.local/bin:$PATH"` to
> your rcfile should do the trick in most cases.


### Commands

##### goto

*Used to add and jump to shortcuts.*

```
    The basics
        goto <magicword>                        Go to shortcut
        goto [<magicword>...]                   Go to many shortcuts
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
```



**project**

*Used to add and switch project contexts.*

```
Usage: project [add <projectname>] | [list]
   other commands:
     add <projectname> - adds a new project and makes it the active project.
     rm  <projectname> - removes the project
     list              - lists all projects
     deactivate        - deactivates goto project
     help              - if you want to read this one more time.
```




#### How does Goto know which project is the active one?

You tell goto with this command:  `project <project-name>`

Examples: `project django-blog`  | `project website`  |  `project goto`

``````bash
$ project goto
active project is now: goto
``````



Running `project` with no arguments, will show you the current active project.

```bash
$ project
goto
```




#### How does Goto know which projects exists?

You tell Goto with the command:

     project add <project-name>





#### How does Goto know which shortcuts there are in the project?

Define them once, and use them a thousand times. By this command:

     goto add <magic-word> <URI>

A **magic-word** is the name of your shortcut.
The **URI** is the target of your shortcut. It could be a file, a directory, a web-url.

##### Examples:

* `goto add github https://github.com/technocake/goto`
* `goto add music ~/the/sound/of/music`
* `goto add jira http://jira.com/project/X`

First one adds a url to a repo on github relevant to the project.
The second one adds a folder path.

When you activate a project, Goto remembers which project you are thinking about right now.

Then it makes sense to call the shortcut visualstudio, because it implicit means the visual studio project associated with this project.

Examples:

    goto add jira http://jira.com/project/X



## Uninstall

```bash
pip uninstall magicgoto
# remove source start_goto from your ~/.bash_profile | ~/.bashrc | ~/.zshrc
# project data is kept intact in ~/.goto
```


## Features

### Goto many things with one command

![goto-many](./images/goto-many.gif)


