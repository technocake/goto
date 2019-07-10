#!/bin/bash
# load common goto utils
source _gotoutils


TESTPROJECT=testproject
OUTPUTFILE=/tmp/.gototest-cmd-output
# PROJECTFILE

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color


function set_up {
    if [[ -z "$GOTOPATH" || "$GOTOPATH" == "${HOME}/.goto" ]]; then
        echo "GOTOPATH not set in environment."
        echo "Tests should not run on real goto state folder."
        echo "i.e use GOTOPATH=/tmp/.goto   instead"
        exit 1
    fi
    echo "setting up tests"
    create_goto_folders "$GOTOPATH"
    touch "$OUTPUTFILE"
    PROJECTFILE="$GOTOPATH/projects/$TESTPROJECT.json"
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
    elif [[ "$result" =~ "Traceback" ]]; then
        _fail_test "command: '$cmd' did contain not only human readable error message"
    else
        return 0
    fi
}


function _failing_cmd_should_not_print_ah_hoy_twice {
    cmd=$1
    $cmd &> "$OUTPUTFILE"
    result="$(cat "$OUTPUTFILE" | grep -c 'Ah hoy!')"
    if [  "$result" -ne 1 ]; then
        _fail_test "command: '$cmd' did return the wrong number of Ah hoys ($result)"
    else
        return 0
    fi
}


function _display_projectfile {
    echo "Contents of projectfile $PROJECTFILE:"
    if [ -f "$PROJECTFILE" ]; then
        cat "$PROJECTFILE"
    else
        echo "projectfile $PROJECTFILE is not existing"
    fi
}

function _projectfile_should_contain {
    local magicword="$1"
    if [[ $(cat $PROJECTFILE | grep $magicword | wc -l) -ne 1 ]]; then
        _fail_test "magicword '$magicword' missing in project file"
    else
        return 0
    fi
}

function _projectfile_should_not_contain {
    local magicword="$1"
    if [[ $(cat $PROJECTFILE | grep $magicword | wc -l) -ne 0 ]]; then
        _fail_test "magicword '$magicword' should not be in project file"
    else
        return 0
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

    _cmd_should_succeed "project testgotoinit"
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
    _projectfile_should_contain "$magicword"
    # Adding magicword that already exist
    _cmd_should_fail "goto add $magicword $uri"
    _projectfile_should_contain "$magicword"
    _failing_cmd_should_give_human_message "goto add $magicword $uri"

    # Invoking without any magic words
    _cmd_should_fail "goto add"
    _failing_cmd_should_give_human_message "goto add"
    _projectfile_should_contain "$magicword"

    # Invoking without any uri
    _cmd_should_fail "goto add test_add_no_uri"
    _failing_cmd_should_give_human_message "goto add test_add_no_uri"
    _projectfile_should_contain "$magicword"

    # Invoking with & in uri, unescaped
    # TODO: turns out to be hard to test actually, due to the fact that commands tested are always wrapped in quotes.
    # _cmd_should_fail "goto add test_unescaped_ampersand_in_url http://lol?haha=hehe&hihi=hoho"
    # _failing_cmd_should_give_human_message "goto add test_unescaped_ampersand_in_url http://lol?haha=hehe&hihi=hoho"
    # TODO: add _projectfile_should_not_contain test_unescaped_ampersand_in_url check here
    _cmd_should_succeed "goto add test_escaped_ampersand_in_url 'http://lol?haha=hehe&hihi=hoho'"
    _projectfile_should_contain "test_escaped_ampersand_in_url"
}

function test_07_goto {
    magicword="test_goto"
    testcdpath="/tmp"
    nonexisting_magicword="IDoNotExist"
    uri="http://example.com"

    _cmd_should_succeed "goto add $magicword $uri"
    _cmd_should_fail "goto $nonexisting_magicword"
    _failing_cmd_should_give_human_message "goto $nonexisting_magicword"
    _failing_cmd_should_not_print_ah_hoy_twice "goto $nonexisting_magicword"

    _cmd_should_succeed "goto add testcd2 $testcdpath"
    _cmd_should_succeed "goto testcd2"
    if [[ "$PWD" != "$testcdpath" ]]; then _fail_test "goto cd failed"; fi

    _cmd_should_succeed "goto cd testcd"
    if [[ "$PWD" != "$testcdpath" ]]; then _fail_test "goto cd failed"; fi


    _projectfile_should_contain "$magicword"
}

function TODO_test_08_goto_add_æøå {
    existing_magicword="test_æøå"
    nonexisting_magicword="IDoNotExist"
    uri="http://example.com/æøå"

    _cmd_should_succeed "goto add $existing_magicword $uri"
    _projectfile_should_contain "$existing_magicword"

}


function test_09_goto_show {
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

function test_10_goto_rm {
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

function test_11_goto_update {
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

function test_12_only_one_ah_hoy_at_the_time_please {
    nonexisting_magicword="IDoNotExist"

    for command in '' show add update rm rename mv; do
        _cmd_should_fail "goto $command $nonexisting_magicword"
        _failing_cmd_should_give_human_message "goto $command $nonexisting_magicword"
        _failing_cmd_should_not_print_ah_hoy_twice "goto $command $nonexisting_magicword"
    done
}


function test_13_goto_rename {
    existing_magicword1="test_1"
    existing_magicword2="test_2"
    new_magicword="test_3"
    nonexisting_magicword="IDoNotExist"
    uri="http://example.com"

    _cmd_should_succeed "goto add $existing_magicword1 $uri"
    _cmd_should_succeed "goto add $existing_magicword2 $uri"

    # Invoking rename without any magic words
    _cmd_should_fail "goto rename"
    _failing_cmd_should_give_human_message "goto rename"

    _projectfile_should_contain $existing_magicword1
    _projectfile_should_contain $existing_magicword2


    # Invoking rename with one magicword
    _cmd_should_fail "goto rename $existing_magicword1"
    _failing_cmd_should_give_human_message "goto rename $existing_magicword1"

    _projectfile_should_contain $existing_magicword1
    _projectfile_should_contain $existing_magicword2


    # Invoking rename with both magicwords
    _cmd_should_succeed "goto rename $existing_magicword1 $new_magicword"
    _cmd_should_fail "goto rename $existing_magicword1 $new_magicword"
    _failing_cmd_should_give_human_message "goto rename $existing_magicword1 $new_magicword"

    _projectfile_should_not_contain $existing_magicword1
    _projectfile_should_contain $existing_magicword2
    _projectfile_should_contain $new_magicword


    # re add existing_magicword1
    _cmd_should_succeed "goto add $existing_magicword1 $uri"


    # Invoking rename targeting existing magicword
    _cmd_should_fail "goto rename $existing_magicword1 $existing_magicword2"
    _failing_cmd_should_give_human_message "goto rename $existing_magicword1 $existing_magicword2"

    _projectfile_should_contain $existing_magicword1
    _projectfile_should_contain $existing_magicword2    
    _projectfile_should_contain $new_magicword


    # Invoking rename targeting existing magicword and setting force flag to true
    _cmd_should_succeed "goto rename $existing_magicword1 $existing_magicword2 --force"
    
    _projectfile_should_not_contain $existing_magicword1
    _projectfile_should_contain $existing_magicword2    
    _projectfile_should_contain $new_magicword
}


function TODO_test_14_goto_copy {
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
