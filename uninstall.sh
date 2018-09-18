rm -rf /usr/local/opt/goto
rm /usr/local/bin/goto
rm /usr/local/bin/project
rm /usr/local/bin/start_goto
rm /usr/local/bin/_gotoutils

echo "remove the line: source start_goto from your bash config file"
echo "(most likely .bash_profile or .bashrc in your home folder)"
echo
echo " Also, your data in ~/.goto is not deleted" 
