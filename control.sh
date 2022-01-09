#!/usr/bin/env bash
###################################################################################################
# --------------------------------------- Common Command ---------------------------------------- #
###################################################################################################
REQUIRED_COMMANDS=()
# System Command
REQUIRED_COMMANDS+=("basename")
REQUIRED_COMMANDS+=("date")
REQUIRED_COMMANDS+=("dirname")
REQUIRED_COMMANDS+=("mkdir")
REQUIRED_COMMANDS+=("read")
REQUIRED_COMMANDS+=("rm")
REQUIRED_COMMANDS+=("tabs")
REQUIRED_COMMANDS+=("touch")
# Git Command
REQUIRED_COMMANDS+=("git")
# Python Command
REQUIRED_COMMANDS+=("python3")
REQUIRED_COMMANDS+=("pip3")

# Verify the required commands
function command_exist() {
    command -v "${cmd}" > "/dev/null" || { echo "Not found required command \"${cmd}\", Exit!"; exit; }
}

for cmd in "${REQUIRED_COMMANDS[@]}"; do command_exist "${cmd}"; done

###################################################################################################
# -------------------------------------- Global Variables --------------------------------------- #
###################################################################################################
if [[ "${0}" != "-bash" ]]; then
    # Put all global variables in this block in order to make "source ./control.sh" work
    PROJECT_NAME="eztree"
    BASE_DIRECTORY="$(dirname "${0}")"
else
    BASE_DIRECTORY="."
fi

###################################################################################################
# ------------------------------------- Mini EZ-Bash Library ------------------------------------ #
###################################################################################################
function ez_contain() {
    # ${1} = Item, ${2} ~ ${n} = List
    for data in "${@:2}"; do [[ "${1}" = "${data}" ]] && return 0; done; return 1
}

function ez_exclude() {
    ez_contain "${@}" && return 1 || return 0
}

function ez_join() {
    local delimiter="${1}"; local i=0; local out_put=""
    for data in "${@:2}"; do
        [[ "${i}" -eq 0 ]] && out_put="${data}" || out_put+="${delimiter}${data}"
        ((++i))
    done
    echo "${out_put}"
}

function ez_log_stack() {
    local ignore_top_x="${1}"; local stack=""; local i=$((${#FUNCNAME[@]} - 1))
    if [[ -n "${ignore_top_x}" ]]; then
        for ((; i > "${ignore_top_x}"; --i)); do stack+="[${FUNCNAME[${i}]}]"; done
    else
        # i > 0 to ignore self "ez_log_stack"
        for ((; i > 0; --i)); do stack+="[${FUNCNAME[${i}]}]"; done
    fi
    echo "${stack}"
}

function ez_print_usage() {
    tabs 30; (>&2 echo -e "${1}\n"); tabs
}

function ez_build_usage() {
    local operation argument description="No Description"
    while [[ -n "${1}" ]]; do
        case "${1}" in
            "-o" | "--operation") shift; operation=${1}; [[ -n "${1}" ]] && shift ;;
            "-a" | "--argument") shift; argument=${1}; [[ -n "${1}" ]] && shift ;;
            "-d" | "--description") shift; description=${1}; [[ -n "${1}" ]] && shift ;;
            *) echo "$(ez_log_stack) Unknown argument \"${1}\""; return 1 ;;
        esac
    done
    if [[ "${operation}" = "init" ]]; then
        [[ -z "${argument}" ]] && argument="${FUNCNAME[1]}"
        # shellcheck disable=SC2028
        echo "\n[Function Name]\t\"${argument}\"\n[Function Info]\t${description}\n"
    elif [[ "${operation}" = "add" ]]; then
        # shellcheck disable=SC2028
        echo "${argument}\t${description}\n"
    else
        echo "$(ez_log_stack) Invalid value \"${operation}\" for \"-o|--operation\""; return 1
    fi
}

function ez_print_log() {
    local usage time_stamp
    if [[ "${1}" = "-h" ]] || [[ "${1}" = "--help" ]]; then
        usage=$(ez_build_usage -o "init" -d "Print Log to Console")
        usage+=$(ez_build_usage -o "add" -a "-l|--logger" -d "Logger type such as INFO, WARN, ERROR, ...")
        usage+=$(ez_build_usage -o "add" -a "-m|--message" -d "Message to print")
        ez_print_usage "${usage}"; return
    fi
    time_stamp="$(date '+%Y-%m-%d %H:%M:%S')"; local logger="INFO"; local message=""
    while [[ -n "${1}" ]]; do
        case "${1}" in
            "-l" | "--logger") shift; logger=${1}; [[ -n "${1}" ]] && shift ;;
            "-m" | "--message") shift; message=${1}; [[ -n "${1}" ]] && shift ;;
            *) echo "[${time_stamp}]$(ez_log_stack)[ERROR] Unknown argument identifier \"${1}\""; return 1 ;;
        esac
    done
    echo "[${time_stamp}]$(ez_log_stack 1)[${logger}] ${message}"
}

###################################################################################################
# -------------------------------------- Control Function --------------------------------------- #
###################################################################################################
function control_clean() {
    local directories=(
        "${BASE_DIRECTORY}/build"
        "${BASE_DIRECTORY}/dist"
        "${BASE_DIRECTORY}/.pytest_cache"
        "${BASE_DIRECTORY}/src/${PROJECT_NAME}.egg-info"
    )
    directories+=($(find "${BASE_DIRECTORY}" -name "__pycache__" -type "d"))
    for directory in "${directories[@]}"; do
        if [[ -d "${directory}" ]]; then
            ez_print_log -m "Removing \"${directory}\" ..."
            rm -rf "${directory}"
        fi
    done
}

function control_build() {
    # https://packaging.python.org/en/latest/tutorials/packaging-projects/
    ez_print_log -m "Upgrading build ..."
    python3 -m "pip" "install" --upgrade "build"
    ez_print_log -m "Building ..."
    python3 -m "build"
    # python3 setup.py sdist bdist_wheel
}

function control_test() {
    # https://docs.pytest.org/en/latest/
    ez_print_log -m "Installing pytest ..."
    pip3 "install" "pytest" --upgrade
    ez_print_log -m "Running tests ..."
    pytest -vv
}

function control_uninstall() {
    ez_print_log -m "Uninstalling ${PROJECT_NAME} ..."
    pip3 "uninstall" "${PROJECT_NAME}" -y
}

function control_install_local() {
    ez_print_log -m "Installing local build ..."
    pip3 "install" --editable "${BASE_DIRECTORY}"
}

function control_install_test() {
    # https://test.pypi.org/project/eztree
    ez_print_log -m "Installing test repo ..."
    pip3 "install" -i "https://test.pypi.org/simple/" "${PROJECT_NAME}" --upgrade
}

function control_install() {
    # https://pypi.org/project/eztree
    ez_print_log -m "Installing ${PROJECT_NAME} ..."
    pip3 "install" "${PROJECT_NAME}" --upgrade
}

function control_publish_test() {
    ez_print_log -m "Upgrading twine ..."
    python3 -m "pip" "install" --upgrade "twine"
    ez_print_log -m "Publishing test repo ..."
    python3 -m "twine" "upload" --repository "testpypi" "dist/"*
}

function control_publish() {
    ez_print_log -m "Upgrading twine ..."
    python3 -m "pip" "install" --upgrade "twine"
    ez_print_log -m "Publishing pypi repo ..."
    python3 -m "twine" "upload" "dist/"*
}

###################################################################################################
# ---------------------------------------- Main Function ---------------------------------------- #
###################################################################################################
function control() {
    local VALID_SKIPS=("clean" "build" "test" "uninstall" "install_local" "install_test" "install" "publish_test" "publish" )
    local VALID_OPERATIONS=("ALL" "${VALID_SKIPS[@]}") usage=""
    if [[ -z "${1}" ]] || [[ "${1}" = "-h" ]] || [[ "${1}" = "--help" ]]; then
        usage=$(ez_build_usage -o "init" -d "Control Project Pipeline")
        usage+=$(ez_build_usage -o "add" -a "-o|--operations" -d "Choose from: [$(ez_join ', ' "${VALID_OPERATIONS[@]}")]")
        usage+=$(ez_build_usage -o "add" -a "-s|--skips" -d "Choose from: [$(ez_join ', ' "${VALID_SKIPS[@]}")]")
        usage+=$(ez_build_usage -o "add" -a "-f|--flags" -d "[Optional] The arguments of control_* function")
        ez_print_usage "${usage}"; return
    fi
    local args=("-o" "--operations" "-s" "--skips") operations=() skips=() flags=()
    while [[ -n "${1}" ]]; do
        case "${1}" in
            "-o" | "--operations") shift
                while [[ -n "${1}" ]]; do
                    if ez_contain "${1}" "${args[@]}"; then break; else operations+=("${1}") && shift; fi
                done ;;
            "-s" | "--skips") shift
                while [[ -n "${1}" ]]; do
                    if ez_contain "${1}" "${args[@]}"; then break; else skips+=("${1}") && shift; fi
                done ;;
            "-f" | "--flags") shift
                while [[ -n "${1}" ]]; do
                    if ez_contain "${1}" "${args[@]}"; then break; else flags+=("${1}") && shift; fi
                done ;;
            *) ez_print_log -l "ERROR" -m "Unknown argument identifier \"${1}\", please choose from [${args[*]}]"; return 1 ;;
        esac
    done
    [[ -z "${operations[*]}" ]] && ez_print_log -l "ERROR" -m "No operation found!" && return 1
    if [[ "${#operations[@]}" -gt 1 ]] && ez_contain "ALL" "${operations[@]}"; then
        ez_print_log -l "ERROR" -m "Cannot mix \"ALL\" with other operations" && return 1
    fi
    for opt in "${operations[@]}"; do
        ez_exclude "${opt}" "${VALID_OPERATIONS[@]}" && ez_print_log -l "ERROR" -m "Invalid operation \"${opt}\"" && return 1
    done
    for skp in "${skips[@]}"; do
        ez_exclude "${skp}" "${VALID_SKIPS[@]}" && ez_print_log -l "ERROR" -m "Invalid skip \"${skp}\"" && return 1
    done
    if [[ "${operations[0]}" = "ALL" ]]; then
        operations=("clean" "uninstall" "build" "install_local" "test")
    fi
    for opt in "${operations[@]}"; do
        ez_contain "${opt}" "${skips[@]}" && ez_print_log -m "Operation \"${opt}\" is skipped!" && continue
        ez_print_log -m "Operation \"${opt}\" is running ..."
        if "control_${opt}" "${flags[@]}"; then ez_print_log -m "Operation \"${opt}\" complete!"
        else ez_print_log -l "ERROR" -m "Operation \"${opt}\" failed!"; return 2; fi
    done
    ez_print_log -m "Workflow Complete!!!"
}

# Entry Point
[[ "${0}" != "-bash" ]] && [[ "${0}" != "-sh" ]] && [[ $(basename "${0}") = "control.sh" ]] && control "${@}"

