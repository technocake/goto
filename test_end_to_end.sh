#!/bin/bash
# load common goto utils
source _gotoutils


TESTPROJECT=testproject
OUTPUTFILE=/tmp/.gototest-cmd-output
LATEST_RAN_COMMAND=""

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
    PROJECTFOLDER="$GOTOPATH/projects/$TESTPROJECT"
    PROJECTFILE="$PROJECTFOLDER/private/magicwords.json"
}


function _fail_test {
    message=$1
    echo -e "${RED}Test failed - $message${NC}"
    echo "LAST RUN CMD: $LATEST_RAN_COMMAND"
    echo
    echo "OUTPUT: $(cat "$OUTPUTFILE")"
    echo
    _display_projectfile
    echo "Test failed - $message"
    tear_down
    exit 1
}

function _cmd_should_fail {
    cmd=$1
    LATEST_RAN_COMMAND="$cmd"
    if eval "$cmd" &> "$OUTPUTFILE"; then
        _fail_test "command: '$cmd' should fail, but did not."
    else
        return 0
    fi
}
_cmd_should_fail "ls nosuchfile"


function _cmd_should_succeed {
    cmd=$1
    LATEST_RAN_COMMAND="$cmd"
    if eval "$cmd" &> "$OUTPUTFILE"; then
        return 0
    else
        _fail_test "command: '$cmd' should succeed, but did not."
    fi
}
_cmd_should_succeed "ls"


function _cmd_should_be_empty {
    cmd=$1
    LATEST_RAN_COMMAND="$cmd"
    eval "$cmd" &> "$OUTPUTFILE"
    result="$(cat "$OUTPUTFILE")"
    if [ -n "$result" ]; then
        _fail_test "command: '$cmd' did not return empty"
    else
        return 0
    fi
}


function _failing_cmd_should_give_human_message {
    cmd=$1
    LATEST_RAN_COMMAND="$cmd"
    eval "$cmd" &> "$OUTPUTFILE"
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
    LATEST_RAN_COMMAND="$cmd"
    eval "$cmd" &> "$OUTPUTFILE"
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
    if [[ $(cat $PROJECTFILE | grep "\"$magicword\"" | wc -l) -ne 1 ]]; then
        _fail_test "magicword '$magicword' missing in project file"
    else
        return 0
    fi
}

function _projectfile_should_not_contain {
    local magicword="$1"
    if [[ $(cat $PROJECTFILE | grep "\"$magicword\"" | wc -l) -ne 0 ]]; then
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
    if [ ! -d "$PROJECTFOLDER" ]; then
        _fail_test "project folder not created"
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

function TODOtest_07_goto_many {
    declare -a magicwords
    declare -a uris
    magicwords=(
        "red"
        "blue"
        #"green"
        #"yellow"
        #"orange"
    )
    uris=(
        "http://red.com"
        "http://blue.com"
        #"goto+subl://orange.com"
        #"mailto:jon@gmail.com"
        #"spotify:green.com"
        #"sftp:hallo@yellow.com"
    )

    for i in "${!magicwords[@]}"; do
        _cmd_should_succeed "goto add ${magicwords[$i]} ${uris[$i]}";
    done

    for i in "${!magicwords[@]}"; do
        _projectfile_should_contain "${magicwords[$i]}";
    done

    for i in "${!magicwords[@]}"; do
        _cmd_should_succeed "goto ${magicwords[$i]}";
    done

    # goto all at the same time
    _cmd_should_succeed "goto ${magicwords[*]}"
}


function test_07_goto_nonexisting_magicword {
    nonexisting_magicword="IDoNotExist"

    _cmd_should_fail "goto $nonexisting_magicword"
    _failing_cmd_should_give_human_message "goto $nonexisting_magicword"
    _failing_cmd_should_not_print_ah_hoy_twice "goto $nonexisting_magicword"
}

function test_08_goto_add_æøå {
    existing_magicword="test_æøå"
    nonexisting_magicword="IDoNotExist"
    uri="http://example.com/æøå"

    _cmd_should_succeed "goto add $existing_magicword $uri"
    _projectfile_should_contain "$existing_magicword"

}

function test_09_goto_show_æøå {
    existing_magicword="test_shæw"
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

function test_10_goto_rm_æøå {
    existing_magicword="test_ræmøve"
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

function test_11_goto_list {
    _cmd_should_succeed "goto list"

    # TODO: make the for loops work

    # for line in "$(goto list)"; do
    #     if [ $(echo $line | wc -w) -gt 1 ]; then
    #         _fail_test "magicwords should (atleast in this test) contain only one word"
    #     fi
    # done

    echo ... "goto list --verbose"
    _cmd_should_succeed 'goto list -v'
    _cmd_should_succeed 'goto list --verbose'

    # for line in "$(goto list --verbose)"; do
    #     if [ $(echo $line | wc -w) -eq 1 ]; then
    #         _fail_test "verbose goto list should show uris."
    #     fi
    # done
}

function test_12_goto_update {
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

function test_13_only_one_ah_hoy_at_the_time_please {
    nonexisting_magicword="IDoNotExist"

    for command in '' show add update rm rename mv; do
        _cmd_should_fail "goto $command $nonexisting_magicword"
        _failing_cmd_should_give_human_message "goto $command $nonexisting_magicword"
        _failing_cmd_should_not_print_ah_hoy_twice "goto $command $nonexisting_magicword"
    done
}


function test_14_goto_rename_æøå {
    existing_magicword1="test_æ"
    existing_magicword2="test_ø"
    new_magicword="test_ålræit"
    nonexisting_magicword="IDoNotExist"
    uri="http://example.com"

    _cmd_should_succeed "goto add $existing_magicword1 $uri"
    _cmd_should_succeed "goto add $existing_magicword2 $uri"

    echo ... Invoking rename without any magic words
    _cmd_should_fail "goto rename"
    _failing_cmd_should_give_human_message "goto rename"

    _projectfile_should_contain $existing_magicword1
    _projectfile_should_contain $existing_magicword2


    echo ... Invoking rename with one magicword
    _cmd_should_fail "goto rename $existing_magicword1"
    _failing_cmd_should_give_human_message "goto rename $existing_magicword1"

    _projectfile_should_contain $existing_magicword1
    _projectfile_should_contain $existing_magicword2


    echo ... Invoking rename with both magicwords
    _cmd_should_succeed "goto rename $existing_magicword1 $new_magicword"
    _cmd_should_fail "goto rename $existing_magicword1 $new_magicword"
    _failing_cmd_should_give_human_message "goto rename $existing_magicword1 $new_magicword"

    _projectfile_should_not_contain $existing_magicword1
    _projectfile_should_contain $existing_magicword2
    _projectfile_should_contain $new_magicword


    echo ... re-add existing_magicword1
    _cmd_should_succeed "goto add $existing_magicword1 $uri"


    echo ... Invoking rename targeting existing magicword
    _cmd_should_fail "goto rename $existing_magicword1 $existing_magicword2"
    _failing_cmd_should_give_human_message "goto rename $existing_magicword1 $existing_magicword2"

    _projectfile_should_contain $existing_magicword1
    _projectfile_should_contain $existing_magicword2
    _projectfile_should_contain $new_magicword


    echo ... Invoking rename targeting existing magicword and setting force flag to true
    _cmd_should_succeed "goto rename $existing_magicword1 $existing_magicword2 --force"
    _cmd_should_succeed "goto rename $existing_magicword2 $existing_magicword1 -f"
    _cmd_should_succeed "goto rename $existing_magicword1 $existing_magicword2 --force"

    _projectfile_should_not_contain $existing_magicword1
    _projectfile_should_contain $existing_magicword2
    _projectfile_should_contain $new_magicword
}

function TODOtest_15_goto_copy {
    # By using the python pyperclip module,
    # It would be possible to inspect the content of the clipboard:

    # >>> import pyperclip
    # >>> pyperclip.copy('The text to be copied to the clipboard.')
    # >>> pyperclip.paste()
    # 'The text to be copied to the clipboard.'


    # TODO: save clipboard, and put it back after running test.
    _cmd_should_succeed "goto copy testcd"
    # TODO: handle utf-8 issues in python2
    # CLIPBOARD_DATA=$(python -c 'import pyperclip; print(pyperclip.paste())')
}


function test_16_unmigrated_data_detection {
    project="unmigrated_project"
    magicword="test_migration"
    json='{"'$magicword'": "https://github.com/technocake/goto/issues/108"}'

    echo "$json" > "$GOTOPATH/projects/$project.json"
    touch "$GOTOPATH/projects/$project" # project cmd used to do this

    # when json files are present in the root of .goto/projects,
    # goto should detect it and prompt the user to migrate data.
    # But running a prompting command would hault the test run forever,
    # so we give it some input.

    # Simulating Ctrl+D by closing stdin: 0<&-
    _cmd_should_fail 'goto'
    _failing_cmd_should_give_human_message 'goto'

    _cmd_should_fail 'goto --check-migrate'
    _failing_cmd_should_give_human_message 'goto --check-migrate'

    _cmd_should_fail 'echo n | goto --migrate'
    _failing_cmd_should_give_human_message 'echo n | goto --migrate'

    _cmd_should_fail 'project'
    _failing_cmd_should_give_human_message 'project'

    _cmd_should_fail 'goto testcd 0<&-'
}


function test_17_migrate_data {
    project="unmigrated_project"
    magicword="test_migration"

    _cmd_should_fail 'project $project'
    _cmd_should_fail 'goto --migrate 0<&-'
    _cmd_should_succeed 'echo y | goto --migrate'
    _cmd_should_succeed 'project $project'

    if [ -f "$GOTOPATH/projects/$project.json" ]; then
        _fail_test 'Old project jfile still present in .goto/projects'
    fi

    if [ ! -d "$GOTOPATH/projects/$project/private" ]; then
        _fail_test "New folder structure not created for migrated project"
    fi

    jfiles=(`find "$GOTOPATH/projects" -maxdepth 1 -type f -name "*.json"`)
    if [ ${#jfiles[@]} -ne 0 ]; then
        _fail_test "jfiles still present in project folder"
    fi

    _cmd_should_succeed "goto list"
    _cmd_should_succeed "goto show $magicword"
    _cmd_should_succeed "goto add test_migration_æøå lol"


    # reseting to default test project
    _cmd_should_succeed "project $TESTPROJECT"
}




function tear_down {
    if [[ -n "$GOTOPATH" && -d "$GOTOPATH" ]]; then
        rm -rf "$GOTOPATH"
    fi

    if [[ -f "$OUTPUTFILE" ]]; then
        rm "$OUTPUTFILE"
    fi
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


# If previous test runs are aborted, new runs should start clean.
tear_down

set_up
discover_and_run_tests
tear_down
