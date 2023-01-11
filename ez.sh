#!/usr/bin/env bash
###################################################################################################
# --------------------------------------- Common Command ---------------------------------------- #
###################################################################################################
REQUIRED_COMMANDS=()
# System Command
REQUIRED_COMMANDS+=("basename")
REQUIRED_COMMANDS+=("cut")
REQUIRED_COMMANDS+=("column")
REQUIRED_COMMANDS+=("date")
REQUIRED_COMMANDS+=("dirname")
REQUIRED_COMMANDS+=("printf")
REQUIRED_COMMANDS+=("grep")
# REQUIRED_COMMANDS+=("mkdir")
REQUIRED_COMMANDS+=("rm")
REQUIRED_COMMANDS+=("sed")
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
    BASE_DIRECTORY="$(dirname "${0}")"
else
    BASE_DIRECTORY="."
fi

# Put all global variables in this block in order to make "source ./control.sh" work
PROJECT_NAME="ezcode"
CODE_DIRECTORY="${BASE_DIRECTORY}/src"
TEST_DIRECTORY="${BASE_DIRECTORY}/tests"

###################################################################################################
# ------------------------------------- Mini EZ-Bash Library ------------------------------------ #
###################################################################################################
function ezb_now { date "+%F %T"; }
function ezb_contains { local i; for i in "${@:2}"; do [[ "${1}" = "${i}" ]] && return 0; done; return 1; }
function ezb_excludes { local i; for i in "${@:2}"; do [[ "${1}" = "${i}" ]] && return 1; done; return 0; }
function ezb_join() {
    local delimiter="${1}" i=0 out_put=""
    for data in "${@:2}"; do [[ "${i}" -eq 0 ]] && out_put="${data}" || out_put+="${delimiter}${data}"; ((++i)); done
    echo "${out_put}"
}
function ezb_log_stack {
    local ignore_top_x="${1}" i=$((${#FUNCNAME[@]} - 1)) stack
    if [[ -n "${ignore_top_x}" ]]; then
        for ((; i > ignore_top_x; i--)); do stack+="[${FUNCNAME[${i}]}]"; done
    else
        # i > 0 to ignore self "ezb_log_stack"
        for ((; i > 0; i--)); do stack+="[${FUNCNAME[$i]}]"; done
    fi
    [[ "${stack}" != "[]" ]] && echo "${stack}"
}
function ezb_log_info { echo -e "[$(ezb_now)][${EZB_LOGO}]$(ezb_log_stack 1)[INFO] ${@}"; }
function ezb_log_error {
    (>&2 echo -e "[$(ezb_now)][${EZB_LOGO}]$(ezb_log_stack 1)[$(ezb_string_format "ForegroundRed" "ERROR")] ${@}")
}
function ezb_print_usage { echo; printf "${1}\n" | column -s "#" -t; echo; }
function ezb_build_usage {
    if [[ -z "${1}" ]] || [[ "${1}" = "-h" ]] || [[ "${1}" = "--help" ]]; then
        # column delimiter = "#"
        local usage="[Function Name]#ezb_build_usage#\n[Function Info]#EZ-BASH usage builder\n"
        usage+="-o|--operation#Choose from: [\"add\", \"init\"]\n"
        usage+="-a|--argument#Argument Name\n"
        usage+="-d|--description#Argument Description\n"
        ezb_print_usage "${usage}" && return 0
    fi
    local operation="" argument="" description="No Description"
    while [[ -n "${1}" ]]; do
        case "${1}" in
            "-o" | "--operation") shift; operation=${1}; shift ;;
            "-a" | "--argument") shift; argument=${1}; shift ;;
            "-d" | "--description") shift; description=${1}; shift ;;
            *) ezb_log_error "Unknown argument identifier \"${1}\". Run \"${FUNCNAME[0]} --help\" for more info"; return 1 ;;
        esac
    done
    # column delimiter = "#"
    case "${operation}" in
        "init")
            [[ -z "${argument}" ]] && argument="${FUNCNAME[1]}"
            echo "[Function Name]#\"${argument}\""
            echo "[Function Info]#${description}\n" ;;
        "add")
            echo "${argument}#${description}\n" ;;
        *) ezb_log_error "Unknown argument identifier \"${1}\". Run \"${FUNCNAME[0]} --help\" for more info"; return 1 ;;
    esac
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
            ezb_log_info "Removing \"${directory}\" ..."
            rm -rf "${directory}"
        fi
    done
}

function control_build() {
    # https://packaging.python.org/en/latest/tutorials/packaging-projects/
    ezb_log_info "Upgrading pip ..."
    python3 -m "pip" "install" --user --upgrade "pip"
    # ezb_log_info "Upgrading build ..."
    # python3 -m "pip" "install" --user --upgrade "build"
    # ezb_log_info "Building ..."
    # python3 -m "build"
    ezb_log_info "Building dist ..."
    python3 "setup.py" "sdist" "bdist_wheel"
}

function control_test() {
    # https://docs.pytest.org/en/latest/
    ezb_log_info "Installing flake8 ..."
    python3 -m "pip" "install" --user --upgrade "flake8"
    ezb_log_info "Running flake8 checks ..."
    if ! python3 -m "flake8" --ignore "E124,E128,E501,W391" "${CODE_DIRECTORY}"; then
        ezb_log_error "Failed flake8 checks!"; return 1
    fi
    ezb_log_info "Installing pytest ..."
    python3 -m "pip" "install" --user --upgrade "pytest"
    ezb_log_info "Installing pytest-srcpaths ..."
    python3 -m "pip" "install" --user --upgrade "pytest-srcpaths"
    ezb_log_info "Running tests ..."
    [[ -z "${1}" ]] && pytest -vv "${TEST_DIRECTORY}" || pytest -vv "${TEST_DIRECTORY}/${1}"
}

function control_uninstall() {
    ezb_log_info "Uninstalling ${PROJECT_NAME} ..."
    python3 -m "pip" "uninstall" "${PROJECT_NAME}" -y
}

function control_install_local() {
    ezb_log_info "Installing local build ..."
    python3 -m "pip" "install" --upgrade "setuptools" --user
    python3 -m "pip" "install" --editable "${BASE_DIRECTORY}" --user
    # python3 -m "pip" "install" --editable "${BASE_DIRECTORY}"
    # python3 "${BASE_DIRECTORY}/setup.py" "install" --user
    # python3 "${BASE_DIRECTORY}/setup.py" "install"
}

function control_install_test() {
    # https://test.pypi.org/project/ezcode
    ezb_log_info "Installing test repo ..."
    python3 -m "pip" "install" --user --upgrade --index-url "https://test.pypi.org/simple/" "${PROJECT_NAME}"
}

function control_install() {
    # https://pypi.org/project/ezcode
    ezb_log_info "Installing ${PROJECT_NAME} ..."
    python3 -m "pip" "install" --upgrade "${PROJECT_NAME}" --user
    # python3 -m "pip" "install" --upgrade "${PROJECT_NAME}"
}

function control_publish_test() {
    ezb_log_info "Upgrading twine ..."
    python3 -m "pip" "install" --user --upgrade "twine"
    ezb_log_info "Publishing test repo ..."
    python3 -m "twine" "upload" --verbose --repository "testpypi" "dist/"*
}

function control_publish() {
    ezb_log_info "Upgrading twine ..."
    python3 -m "pip" "install" --upgrade "twine" --user
    ezb_log_info "Publishing pypi repo ..."
    python3 -m "twine" "upload" --verbose "dist/"*
}

function control_bump() {
    if git "diff" "${BASE_DIRECTORY}/setup.py" | grep "version=" | grep "^+\|^-"; then
        ezb_log_info "Found unstaged version change, skip version bump!" && return 0
    fi
    if git "diff" --staged "${BASE_DIRECTORY}/setup.py" | grep "version=" | grep "^+\|^-"; then
        ezb_log_info "Found uncommitted version change, skip version bump!" && return 0
    fi
    local version=$(cat "${BASE_DIRECTORY}/setup.py" | grep "version=" | sed "s/[^0-9.]*\([0-9.]*\).*/\1/") new_version
    local major=$(echo "${version}" | cut -d "." -f 1)
    local minor=$(echo "${version}" | cut -d "." -f 2)
    local patch=$(echo "${version}" | cut -d "." -f 3)
    ezb_log_info "Current Version: ${version}"
    if [[ -z "${1}" ]] || [[ "${1}" = "patch" ]]; then
        ((++patch)); new_version="${major}.${minor}.${patch}"
        ezb_log_info "Bumped Patch Version: ${new_version}"
    elif [[ "${1}" = "minor" ]]; then
        ((++minor)); new_version="${major}.${minor}.${patch}"
        ezb_log_info "Bumped Minor Version: ${new_version}"
    elif [[ "${1}" = "major" ]]; then
        ((++major)); new_version="${major}.${minor}.${patch}"
        ezb_log_info "Bumped Major Version: ${new_version}"
    else
        ezb_log_error "Wrong argument \"${1}\"" && return 1
    fi
    sed -i ".bak" "s/${version}/${new_version}/" "${BASE_DIRECTORY}/setup.py"
    rm "${BASE_DIRECTORY}/setup.py.bak"
    git diff "${BASE_DIRECTORY}/setup.py"
}

# function control_view_md() {
#     local file_path="${1}" file_name="$(basename ${1} | cut -d '.' -f 1)"
#     mkdir -p "${BASE_DIRECTORY}/html"
#     python3 -m "pip" "install" "requests" --user
#     python -c "\
# import json, pathlib, requests;\
# base_dir = pathlib.Path('${BASE_DIRECTORY}');\
# payload = {'text': (base_dir/'${file_path}').read_text(encoding='utf-8'), 'mode': 'markdown'};\
# html_str = requests.post('https://api.github.com/markdown', data=json.dumps(payload), headers={'Accept':'application/vnd.github+jso'}).text;\
# open((base_dir/'html/${file_name}.html'), 'w').write(html_str);\
# "
#     python -m "http.server" --directory "${BASE_DIRECTORY}/html" "9999" &
#     open "http://localhost:9999/${file_name}.html"
# }

###################################################################################################
# ---------------------------------------- Main Function ---------------------------------------- #
###################################################################################################
function ez() {
    local VALID_OPERATIONS=("clean" "build" "test" "uninstall" "install_local" "install_test" "install" "publish_test" "publish" "bump")
    if [[ -z "${1}" ]] || [[ "${1}" = "-h" ]] || [[ "${1}" = "--help" ]]; then
        local usage=$(ezb_build_usage -o "init" -d "Control Project Pipeline")
        usage+=$(ezb_build_usage -o "add" -a "-o|--operations" -d "Choose from: [$(ezb_join ', ' "${VALID_OPERATIONS[@]}")]")
        usage+=$(ezb_build_usage -o "add" -a "-a|--arguments" -d "The arguments of control_* function, e.g. test_array.py::test_binary_search")
        usage+=$(ezb_build_usage -o "add" -a "-s|--skip" -d "Skip operations, e.g. test")
        usage+=$(ezb_build_usage -o "add" -a "-d|--development" -d "[Flag] Development Workflow: [clean, uninstall, build, test, install_local, clean]")
        usage+=$(ezb_build_usage -o "add" -a "-r|--release" -d "[Flag] Release Workflow: [clean, build, test, publish, clean]")
        ezb_print_usage "${usage}"; return
    fi
    local main_args=("-o" "--operations" "-s" "--skip" "-d" "--development" "-r" "--release" "-a" "--arguments")
    local operations=() arguments=() skip=() development release complete_operations=()
    while [[ -n "${1}" ]]; do
        case "${1}" in
            "-o" | "--operations") shift
                while [[ -n "${1}" ]]; do
                    if ezb_contains "${1}" "${main_args[@]}"; then break; else operations+=("${1}") && shift; fi
                done ;;
            "-a" | "--arguments") shift
                while [[ -n "${1}" ]]; do
                    if ezb_contains "${1}" "${main_args[@]}"; then break; else arguments+=("${1}") && shift; fi
                done ;;
            "-s" | "--skip") shift
                while [[ -n "${1}" ]]; do
                    if ezb_contains "${1}" "${main_args[@]}"; then break; else skip+=("${1}") && shift; fi
                done ;;
            "-d" | "--development") shift; development="True" ;;
            "-r" | "--release") shift; release="True" ;;
            *) ezb_log_error "Unknown argument identifier \"${1}\", please choose from [${main_args[*]}]"; return 1 ;;
        esac
    done
    if [[ "${development}" = "True" ]] && [[ "${release}" = "True" ]]; then
        ezb_log_error "Cannot choose more than one workflow!" && return 1
    elif [[ "${development}" = "True" ]] || [[ "${release}" = "True" ]]; then
        [[ -n "${operations[*]}" ]] && ezb_log_error "The operations and workflow are mutually exclusive" && return 1
    else
        [[ -z "${operations[*]}" ]] && ezb_log_error "Must select at least one operation if no workflow is selected!" && return 1
    fi
    [[ "${development}" = "True" ]] && operations=("clean" "uninstall" "build" "test" "install_local" "clean")
    [[ "${release}" = "True" ]] && operations=("clean" "uninstall" "bump" "build" "test" "publish" "clean" "install")
    for opt in "${operations[@]}"; do
        ezb_excludes "${opt}" "${VALID_OPERATIONS[@]}" && ezb_log_error "Invalid operation \"${opt}\"" && return 1
    done
    for opt in "${operations[@]}"; do
        ezb_contains "${opt}" "${skip[@]}" && ezb_log_info "Operation \"${opt}\" is skipped!" && continue
        ezb_log_info "Operation \"${opt}\" is running ..."
        if "control_${opt}" "${arguments[@]}"; then
            ezb_log_info "Operation \"${opt}\" complete!"
            complete_operations+=("${opt}")
        else
            ezb_log_error "Operation \"${opt}\" failed!"
            return 2
        fi
    done
    ezb_log_info "Complete operations: [$(ezb_join ', ' ${complete_operations[@]})]"
    ezb_log_info "Skipped operations: [$(ezb_join ', ' ${skip[@]})]"
    ezb_log_info "Workflow Complete!!!"
}

# Entry Point
[[ "${0}" != "-bash" ]] && [[ "${0}" != "-sh" ]] && [[ $(basename "${0}") = "ez.sh" ]] && ez "${@}"

