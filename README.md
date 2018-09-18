

# Goto is a magic tool that takes you were you want to be, now. 

Projects have their own folders, important files, links to good articles or key websites. 
The problem is that all these are spread out on different locations.
By adding shortcuts to goto, so called magic words, you can jump to them.
The shortcuts are assciated with a project name. And you can switch the project
any time.

In example:

```
    goto visualstudio  -->  Opens the solutionfile for the vs solutions file of the current project
    goto jira          -->  Opens a jira board for the current project
    goto bitbucket     -->  bitbucket repo for the current project
```
 
## Setup 

### Mac OS-X

Please note no sudo

```
git clone https://github.com/technocake/goto
cd goto 
./install.sh
```

### Linux
Please note the added sudo

```
git clone https://github.com/technocake/goto
cd goto 
sudo ./install.sh
```

### Windows (using gitbash)
```
# open git bash as Administrator
git clone https://github.com/technocake/goto
cd goto 
./install.sh
# If asked anything, say yes
```
Now you can test it. No need to close the terminal.

```
goto goto
```


## Usage

```
The basics
        - Adding a shortcut:        goto add <magicword> <url or path>
        - Updating a shortcut:      goto update <magicword> <url or path>
        - Removing a shortcut:      goto rm <magicword>

        - Show url of shortcut:     goto show <magicword>

        - Listing all shortcuts:    goto list
        - With the urls printed:    goto list -v

    Working with folders and files:
        - cd in terminal:           goto cd <magicword>
        - open folder in Finder:    goto -f <magicword>

    code - A specially magic magic word:
        If you add a shortcut
        to a folder,and name the
        shortcut "code";            goto add code <path to folder with code>
        - you may then do this:     goto subl
        and it opens
        Sublime Text in your folder.

```




#### How does Goto know which project is the active one?

You tell goto with this command:  `project <project-name>`

Examples: project django-blog  | project website  |  project goto


#### How does Goto know which projects exists?

You tell Goto with the command:

     `project add <project-name>`

 
#### How does Goto know which shortcuts there are in the project?

Define them once, and use them a thousand times. By this command:

     `goto add <magic-word> <URI>`

A magic-word is the name of your shortcut. 

Examples:

`goto add github https://github.com/technocake/goto`
`goto add music ~/the/sound/of/music`  
`goto add jira http://jira.com/project/X`

First one adds a url to a repo on github relevant to the project.
The second one adds a folder path.

When you activate a project, Goto remembers which project you are thinking about right now. 

Then it makes sense to call the shortcut visualstudio, because it implicit means the visual studio project associated with this project.

Examples:

    goto add jira http://jira.com/project/X



## Uninstall (OS-X)

```
rm -rf /usr/local/opt/goto

# remove symbolic links
rm /usr/local/bin/goto
rm /usr/local/bin/project
rm /usr/local/bin/start_goto
rm /usr/local/bin/_gotoutils

#lastly, remove the line `source start_goto` from .bash_profile

```

