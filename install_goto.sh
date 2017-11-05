#!/bin/bash

mkdir /usr/local/opt/goto/.state

# add commands
ln -s /usr/local/opt/goto/bin/* /usr/local/bin/

# add init_script to.bash_profile:
echo "source start_goto" >> ${HOME}/.bash_profile

# make goto ready -- now.
source start_goto