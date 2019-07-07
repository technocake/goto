#!/bin/bash
# load common goto utils
source _gotoutils


TESTPROJECT=testproject
OUTPUTFILE=/tmp/.gototest-cmd-output

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color


function set_up {
    if [[ -z "$GOTOPATH" ]]; then
        echo "GOTOPATH not set in environment."
        echo "Tests should not run on real goto state folder."
        echo "i.e use GOTOPATH=/tmp/.goto   instead"
        exit 1
    fi
    echo "setting up tests"
    create_goto_folders "$GOTOPATH"
    touch "$OUTPUTFILE"
}


function _fail_test {
    message=$1
    echo -e "${RED}Test failed - $message${NC}"
    echo "OUTPUT: $(cat "$OUTPUTFILE")"
    _display_projectfile
    echo "Test failed - $message"
    tear_down
    exit 1
}

function _cmd_should_fail {
    cmd=$1
    if $cmd &> "$OUTPUTFILE"; then
        _fail_test "command: '$cmd' should fail, but did not."
    else
        return 0
    fi
}
_cmd_should_fail "ls nosuchfile"


function _cmd_should_succeed {
    cmd=$1
    if $cmd &> "$OUTPUTFILE"; then
        return 0
    else 
        _fail_test "command: '$cmd' should succeed, but did not."
    fi
}
_cmd_should_succeed "ls"


function _cmd_should_be_empty {
    cmd=$1
    $cmd &> "$OUTPUTFILE"
    result="$(cat "$OUTPUTFILE")"
    if [ -n "$result" ]; then
        _fail_test "command: '$cmd' did not return empty"
    else
        return 0
    fi
}

function _failing_cmd_should_give_human_message {
    cmd=$1
    $cmd &> "$OUTPUTFILE"
    result="$(cat "$OUTPUTFILE")"
    if [[ ! "$result" =~ "Ah hoy" ]]; then
        _fail_test "command: '$cmd' did not give human readable error message"
    else
        return 0
    fi
}

function _display_projectfile {
    projectfile="$GOTOPATH/projects/$TESTPROJECT.json"
    echo "Contents of projectfile $projectfile:"
    if [ -f "$projectfile" ]; then
        cat "$projectfile"
    else
        echo "projectfile $projectfile is not existing"
    fi
}


function test_01_not_initialized_should_fail {
    echo "... not initialized and deactived"
    _cmd_should_fail "goto"

    echo "... activating a project"
    _cmd_should_succeed "project add testgotoinit"
    _cmd_should_succeed "project testgotoinit"
    _cmd_should_fail "goto list"
    _cmd_should_fail "goto help"

    # source detection should kick in here
    _failing_cmd_should_give_human_message "goto"
    _failing_cmd_should_give_human_message "goto list"
    _failing_cmd_should_give_human_message "goto add test test"
    _failing_cmd_should_give_human_message "goto show test"
    _failing_cmd_should_give_human_message "goto rm test"
    _failing_cmd_should_give_human_message "goto copy test"
    _failing_cmd_should_give_human_message "goto help"

}

function test_02_initialization_should_work {
    local testcdpath=/tmp
    _cmd_should_succeed "source start_goto"
    

    source start_goto
    echo "... start_goto is now sourced for the rest of the remaining tests"
    
    _cmd_should_succeed "goto"

    # When goto is inititalized, cd should work
    _cmd_should_succeed "goto add testcd ${testcdpath}"
    _cmd_should_succeed "goto testcd"
    if [[ "$PWD" != "$testcdpath" ]]; then _fail_test "goto cd failed"; fi

    _cmd_should_succeed "goto cd testcd"
    if [[ "$PWD" != "$testcdpath" ]]; then _fail_test "goto cd failed"; fi
}


function test_03_deactivate_project {
    _cmd_should_succeed "project deactivate"
}


function test_04_switch_to_nonexistent_project {
    _cmd_should_fail "project $TESTPROJECT"
    _cmd_should_fail "goto list"
}


function test_05_add_project {
    _cmd_should_succeed "project add $TESTPROJECT"
    if [ ! -f "${GOTOPATH}/projects/${TESTPROJECT}" ]; then
        _fail_test "project file not created"
    fi
    _cmd_should_succeed "goto list"
}


function test_06_goto_add {
    magicword="test_add"
    nonexisting_magicword="IDoNotExist"
    uri="http://example.com"

    _cmd_should_succeed "goto add $magicword $uri"
    # Adding magicword that already exist
    _cmd_should_fail "goto add $magicword $uri"
    _failing_cmd_should_give_human_message "goto add $magicword $uri"

    # Invoking without any magic words
    _cmd_should_fail "goto add"
    _failing_cmd_should_give_human_message "goto add"

    # Invoking without any uri
    _cmd_should_fail "goto add test_add_no_uri"
    _failing_cmd_should_give_human_message "goto add test_add_no_uri"
}


function test_07_goto_show {
    existing_magicword="test_show"
    nonexisting_magicword="IDoNotExist"
    uri="http://example.com"

    _cmd_should_succeed "goto add $existing_magicword $uri"

    # Invoking show without any magic words
    _cmd_should_fail "goto show"
    _failing_cmd_should_give_human_message "goto show"
    
    _cmd_should_succeed "goto show $existing_magicword"

    _cmd_should_fail "goto show $nonexisting_magicword"
    _failing_cmd_should_give_human_message "goto show $nonexisting_magicword"
}

function test_08_goto_rm {
    existing_magicword="test_rm"
    nonexisting_magicword="IDoNotExist"
    uri="http://example.com"
    _cmd_should_succeed "goto add $existing_magicword $uri"
    _cmd_should_succeed "goto rm $existing_magicword"

    # Invoking rm without any magic words
    _cmd_should_fail "goto rm"
    _failing_cmd_should_give_human_message "goto rm"

    _cmd_should_fail "goto rm $nonexisting_magicword"
    _failing_cmd_should_give_human_message "goto rm $nonexisting_magicword"

    # adding it again should also work,
    # and is necessary for the rest of the tests.
    _cmd_should_succeed "goto add $existing_magicword $uri"
}

function test_09_goto_update {
    existing_magicword="test_update"
    nonexisting_magicword="IDoNotExist"
    uri="http://example.com"
    new_uri="https://example.com/secure"

    _cmd_should_succeed "goto add $existing_magicword $uri"
    _cmd_should_succeed "goto update $existing_magicword $new_uri"

    # Invoking rm without any magic words
    _cmd_should_fail "goto update"
    _failing_cmd_should_give_human_message "goto update"

    _cmd_should_fail "goto update $existing_magicword"
    _failing_cmd_should_give_human_message "goto update $existing_magicword"

    _cmd_should_fail "goto update $nonexisting_magicword $new_uri"
    _failing_cmd_should_give_human_message "goto update $nonexisting_magicword"
}

function TODO_test_10_goto_copy {
    # By using the python pyperclip module,
    # It would be possible to inspect the content of the clipboard:
    
    # >>> import pyperclip
    # >>> pyperclip.copy('The text to be copied to the clipboard.')
    # >>> pyperclip.paste()
    # 'The text to be copied to the clipboard.'
    # 
    # To get this content from a shell script it could be done 
    # like so:
    # 
    CLIPBOARD_DATA=$(python -c 'import pyperclip; print(pyperclip.paste())')
}

function tear_down {
    if [[ -n "$GOTOPATH" && -d "$GOTOPATH" ]]; then
        rm -rf "$GOTOPATH"
    fi

    rm "$OUTPUTFILE"
}

function discover_and_run_tests {
    functions=$(declare -F | cut -d ' ' -f3)
    DISCOVERED_TESTS=0
    for f in $functions; do
        
        if [[ "$f" == test_* ]]; then
            let DISCOVERED_TESTS=DISCOVERED_TESTS+1
            echo "$f"
            $f
        fi
    done

    echo -e "${GREEN}All tests passed!${NC}"
    echo "ran $DISCOVERED_TESTS tests successfully!"

}


set_up
discover_and_run_tests
tear_down
