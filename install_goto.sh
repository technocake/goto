#!/bin/bash

mkdir ${HOME}/.goto
mkdir ${HOME}/.goto/projects
touch ${HOME}/.goto/active-project

# add commands
ln -s /usr/local/opt/goto/bin/* /usr/local/bin/

# add init_script to.bash_profile:

echo "Goto needs to run a startup script for it to work. "
echo "This can be automatically added now to your .bash_profile file"
echo "If you want to do this manually add the line 'source start_goto'"

if [ -f "${HOME}/.bash_profile" ]; then
    read -p "Want to automatically add the goto startup script to your .bash_profile? " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "source start_goto" >> ${HOME}/.bash_profile
    fi
else
    echo "~/.bash_profile does not exist"
    echo 
    echo "To make goto function properly, add this line to your bash config file: "
    echo
    echo "         source start_goto"
    echo
    echo "into one of these (.bashrc | .profile | .bash_profile)"

fi


# make goto ready -- now.
source start_goto

# add your first project
project add goto

# set the context to this project
project goto

# add your first shortcuts
goto add code /usr/local/opt/goto
goto add goto https://github.com/technocake/goto
goto add github https://github.com/technocake/goto