#!/bin/bash
. bin/_gotoutils # load common utils 

INSTALL_DIR=/usr/local/opt/goto


echo Step 1: Installing goto into $INSTALL_DIR 
mkdir -p $INSTALL_DIR || check_status
cp -r . $INSTALL_DIR  || check_status



echo Step 2: Adding symlinks to /usr/local/bin
ln -s $INSTALL_DIR/bin/* /usr/local/bin/ || check_status noexit
if [[ "$?" -ne 0 ]]; then
    echo "Failed to symlink to /usr/local/bin"

    if prompt "want to try /usr/bin instead? [y|n]"; then

        echo "Adding symlinks to /usr/bin"
        ln -s $INSTALL_DIR/bin/* /usr/bin/ || check_status
    fi
fi

# Step 2.5 - if running sudo, get original users home
if [ -n "$SUDO_USER" ]; then
        HOME=$(getent passwd $SUDO_USER | cut -d: -f6)
fi

USER=$(logname)


echo Step 3: Setting up magic data folder in ${HOME}/.goto
MAGICPATH="${HOME}/.goto"
if [[ ! -d "$MAGICPATH" ]]; then
    mkdir ${HOME}/.goto || check_status
    mkdir ${HOME}/.goto/projects || check_status
    touch ${HOME}/.goto/active-project || check_status

    # If run by sudo, chown folders from root to user
    if [ -n "$SUDO_USER" ]; then
    	chown -R $USER:$USER "${HOME}/.goto" || check_status
    fi
fi

# add init_script to.bash_profile:


if [ -f "${HOME}/.bash_profile" ]; then
    echo 
    echo "Next step is required to make goto work:"
    echo

    if prompt "Add goto startup script to .bash_profile? [y|n]: "; then
        echo
        echo "source start_goto" >> ${HOME}/.bash_profile || check_status
    else
    echo   
    echo "If you want to do this manually add the line 'source start_goto' to your .bash_profile"
    fi
else
    echo "~/.bash_profile does not exist"
    echo 
    echo "To make goto function properly, add this line to your bash config file: "
    echo
    echo "         source start_goto"
    echo
    echo "into one of these (.bashrc | .profile | .bash_profile)"

    if prompt "Want to append to .bashrc? [y|n]: "; then
        echo "source start_goto" >> ${HOME}/.bashrc || check_status
    fi

fi


# make goto ready -- now.
source start_goto || check_status

# add your first project
project add goto || check_status

# set the context to this project
project goto

# add your first shortcuts
goto add code "$INSTALL_DIR" || check_status
goto add goto https://github.com/technocake/goto
goto add github https://github.com/technocake/goto

echo Installation Succesful!
