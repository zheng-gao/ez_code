#!/usr/bin/env bash
###################################################################################################
# --------------------------------------- Common Command ---------------------------------------- #
###################################################################################################
REQUIRED_COMMANDS=()
# System Command
REQUIRED_COMMANDS+=("basename")
REQUIRED_COMMANDS+=("cut")
REQUIRED_COMMANDS+=("date")
REQUIRED_COMMANDS+=("dirname")
REQUIRED_COMMANDS+=("grep")
REQUIRED_COMMANDS+=("mkdir")
REQUIRED_COMMANDS+=("rm")
REQUIRED_COMMANDS+=("sed")
REQUIRED_COMMANDS+=("tabs")
# Git Command
REQUIRED_COMMANDS+=("git")
# Python Command
REQUIRED_COMMANDS+=("python3")

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
    PROJECT_NAME="ezcode"
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
    )
    directories+=($(find "${BASE_DIRECTORY}" -name "__pycache__" -type "d"))
    directories+=($(find "${BASE_DIRECTORY}" -name "*.egg-info" -type "d"))
    directories+=($(find "${BASE_DIRECTORY}" -name "ezcode-*" -type "d"))
    for directory in "${directories[@]}"; do
        if [[ -d "${directory}" ]]; then
            ez_print_log -m "Removing \"${directory}\" ..."
            rm -rf "${directory}"
        fi
    done
}

function control_build() {
    # https://packaging.python.org/en/latest/tutorials/packaging-projects/
    ez_print_log -m "Upgrading pip ..."
    python3 -m "pip" "install" --upgrade "pip" --user
    ez_print_log -m "Upgrading build ..."
    python3 -m "pip" "install" --upgrade "build" --user
    ez_print_log -m "Building ..."
    python3 -m "build"
    # python3 setup.py sdist bdist_wheel
}

function control_test() {
    # https://docs.pytest.org/en/latest/
    ez_print_log -m "Installing flake8 ..."
    python3 -m "pip" "install" --upgrade "flake8" --user
    ez_print_log -m "Running flake8 checks ..."
    if ! python3 -m "flake8" --ignore "E124,E128,E501,W391" "${BASE_DIRECTORY}/src"; then
        ez_print_log -l "ERROR" -m "Failed flake8 checks!"; return 1
    fi
    ez_print_log -m "Installing pytest ..."
    python3 -m "pip" "install" --upgrade "pytest" --user
    ez_print_log -m "Installing pytest-srcpaths ..."
    python3 -m "pip" "install" --upgrade "pytest-srcpaths" --user
    ez_print_log -m "Running tests ..."
    pytest -vv "${BASE_DIRECTORY}/tests/${1}"
}

function control_uninstall() {
    ez_print_log -m "Uninstalling ${PROJECT_NAME} ..."
    python3 -m "pip" "uninstall" "${PROJECT_NAME}" -y
}

function control_install_local() {
    ez_print_log -m "Installing local build ..."
    python3 -m "pip" "install" --editable "${BASE_DIRECTORY}" --user
}

function control_install_test() {
    # https://test.pypi.org/project/ezcode
    ez_print_log -m "Installing test repo ..."
    python3 -m "pip" "install" -i "https://test.pypi.org/simple/" "${PROJECT_NAME}" --upgrade --user
}

function control_install() {
    # https://pypi.org/project/ezcode
    ez_print_log -m "Installing ${PROJECT_NAME} ..."
    python3 -m "pip" "install" "${PROJECT_NAME}" --upgrade --user
}

function control_publish_test() {
    ez_print_log -m "Upgrading twine ..."
    python3 -m "pip" "install" --upgrade "twine" --user
    ez_print_log -m "Publishing test repo ..."
    python3 -m "twine" "upload" --verbose --repository "testpypi" "dist/"*
}

function control_publish() {
    ez_print_log -m "Upgrading twine ..."
    python3 -m "pip" "install" --upgrade "twine" --user
    ez_print_log -m "Publishing pypi repo ..."
    python3 -m "twine" "upload" --verbose "dist/"*
}

function control_bump() {
    if git "diff" "${BASE_DIRECTORY}/setup.py" | grep "version=" | grep "^+\|^-"; then
        ez_print_log -m "Found unstaged version change, skip version bump!" && return 0
    fi
    if git "diff" --staged "${BASE_DIRECTORY}/setup.py" | grep "version=" | grep "^+\|^-"; then
        ez_print_log -m "Found uncommitted version change, skip version bump!" && return 0
    fi
    local version=$(cat "${BASE_DIRECTORY}/setup.py" | grep "version=" | sed "s/[^0-9.]*\([0-9.]*\).*/\1/") new_version
    local major=$(echo "${version}" | cut -d "." -f 1)
    local minor=$(echo "${version}" | cut -d "." -f 2)
    local patch=$(echo "${version}" | cut -d "." -f 3)
    ez_print_log -m "Current Version: ${version}"
    if [[ -z "${1}" ]] || [[ "${1}" = "patch" ]]; then
        ((++patch)); new_version="${major}.${minor}.${patch}"
        ez_print_log -m "Bumped Patch Version: ${new_version}"
    elif [[ "${1}" = "minor" ]]; then
        ((++minor)); new_version="${major}.${minor}.${patch}"
        ez_print_log -m "Bumped Minor Version: ${new_version}"
    elif [[ "${1}" = "major" ]]; then
        ((++major)); new_version="${major}.${minor}.${patch}"
        ez_print_log -m "Bumped Major Version: ${new_version}"
    else
        ez_print_log -l "ERROR" -m "Wrong argument \"${1}\"" && return 1
    fi
    sed -i ".bak" "s/${version}/${new_version}/" "${BASE_DIRECTORY}/setup.py"
    rm "${BASE_DIRECTORY}/setup.py.bak"
    git diff "${BASE_DIRECTORY}/setup.py"
}

###################################################################################################
# ---------------------------------------- Main Function ---------------------------------------- #
###################################################################################################
function ez() {
    local VALID_OPERATIONS=(
        "clean" "build" "test" "uninstall" "install_local" "install_test" "install" "publish_test" "publish" "bump")
    if [[ -z "${1}" ]] || [[ "${1}" = "-h" ]] || [[ "${1}" = "--help" ]]; then
        local usage=$(ez_build_usage -o "init" -d "Control Project Pipeline")
        usage+=$(ez_build_usage -o "add" -a "-o|--operations" -d "Choose from: [$(ez_join ', ' "${VALID_OPERATIONS[@]}")]")
        usage+=$(ez_build_usage -o "add" -a "-a|--arguments" -d "The arguments of control_* function")
        usage+=$(ez_build_usage -o "add" -a "-d|--development" -d "[Flag] Development Workflow: [clean, uninstall, build, test, install_local, clean]")
        usage+=$(ez_build_usage -o "add" -a "-r|--release" -d "[Flag] Release Workflow: [clean, build, test, publish, clean]")
        ez_print_usage "${usage}"; return
    fi
    local main_args=("-o" "--operations" "-d" "--development" "-r" "--release" "-a" "--arguments") operations=() arguments=() development release
    while [[ -n "${1}" ]]; do
        case "${1}" in
            "-o" | "--operations") shift
                while [[ -n "${1}" ]]; do
                    if ez_contain "${1}" "${main_args[@]}"; then break; else operations+=("${1}") && shift; fi
                done ;;
            "-a" | "--arguments") shift
                while [[ -n "${1}" ]]; do
                    if ez_contain "${1}" "${main_args[@]}"; then break; else arguments+=("${1}") && shift; fi
                done ;;
            "-d" | "--development") shift; development="True" ;;
            "-r" | "--release") shift; release="True" ;;
            *) ez_print_log -l "ERROR" -m "Unknown argument identifier \"${1}\", please choose from [${main_args[*]}]"; return 1 ;;
        esac
    done
    if [[ "${development}" = "True" ]] && [[ "${release}" = "True" ]]; then
        ez_print_log -l "ERROR" -m "Cannot choose more than one workflow!" && return 1
    elif [[ "${development}" = "True" ]] || [[ "${release}" = "True" ]]; then
        [[ -n "${operations[*]}" ]] && ez_print_log -l "ERROR" -m "The operations and workflow are mutually exclusive" && return 1
    else
        [[ -z "${operations[*]}" ]] && ez_print_log -l "ERROR" -m "Must select at least one operation if no workflow is selected!" && return 1
    fi
    [[ "${development}" = "True" ]] && operations=("clean" "uninstall" "build" "test" "install_local" "clean")
    [[ "${release}" = "True" ]] && operations=("clean" "bump" "build" "test" "publish" "clean")
    for opt in "${operations[@]}"; do
        ez_exclude "${opt}" "${VALID_OPERATIONS[@]}" && ez_print_log -l "ERROR" -m "Invalid operation \"${opt}\"" && return 1
    done
    for opt in "${operations[@]}"; do
        ez_contain "${opt}" "${skips[@]}" && ez_print_log -m "Operation \"${opt}\" is skipped!" && continue
        ez_print_log -m "Operation \"${opt}\" is running ..."
        if "control_${opt}" "${arguments[@]}"; then ez_print_log -m "Operation \"${opt}\" complete!"
        else ez_print_log -l "ERROR" -m "Operation \"${opt}\" failed!"; return 2; fi
    done
    ez_print_log -m "Workflow Complete!!!"
}

# Entry Point
[[ "${0}" != "-bash" ]] && [[ "${0}" != "-sh" ]] && [[ $(basename "${0}") = "ez.sh" ]] && ez "${@}"

