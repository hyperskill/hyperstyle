#!/bin/bash
#
# Sets the environment needed for Hyperstyle to work.

# ----------------------------------------------------------------------------------------------------------------------

#######################################
# Checks whether the linter needs to be installed.
#
# If the linter folder is empty, the linter must be installed,
# otherwise, the linter must be reinstalled at the user's request.
#
# If the folder does not exist, it will be created.
# If it is necessary to reinstall the linter, all files in the passed folder will be deleted.
#
# Arguments:
#   Folder with the linter files, a path.
# Returns:
#   0 if the linter needs to be installed, 1 otherwise.
#######################################
function need_to_install_linter() {
  if [[ -d $1 ]] && [[ -n $(ls -A "$1") ]]; then
    read -p "The folder is not empty. Do you want to reinstall the linter? (Y/n): " -r
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      return 1 # 1=false
    fi
    rm -rf "$1"
  fi

  mkdir -p "$1"
  return 0 # 0=true
}

#######################################
# Checks the return code.
#
# If the return code is non-zero, the error message is shown and the script
# exits with exit status 1, otherwise the success message is shown.
#
# Arguments:
#   Return code, an integer.
#   Success message, a string.
#   Error message, a string.
# Outputs:
#   Writes messages to stdout.
#######################################
function check_return_code() {
  if [[ $1 -ne 0 ]]; then
    echo "ERROR: $3"
    exit 1
  fi
  echo "$2"
}

# ----------------------------------------------------------------------------------------------------------------------

echo "Checking variables..."

: "${CHECKSTYLE_VERSION:?Variable is not defined}"
: "${CHECKSTYLE_DIRECTORY:?Variable is not defined}"

: "${DETEKT_VERSION:?Variable is not defined}"
: "${DETEKT_DIRECTORY:?Variable is not defined}"

: "${PMD_VERSION:?Variable is not defined}"
: "${PMD_DIRECTORY:?Variable is not defined}"

echo "The variables are defined."

echo

read -p "Do you want to install ESLint? (Y/n): " -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo "Installing ESLint..."
  npm install eslint@7.5.0 -g && eslint --init
  check_return_code $? "ESLint installed." "ESLint installation failed."
else
  echo "ESLint installation skipped."
fi

echo

read -p "Do you want to install Python requirements? (Y/n): " -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo "Installing Python requirements..."
  pip install --no-cache-dir -r requirements-test.txt -r requirements.txt .
  check_return_code $? "Python requirements installed." "Python requirements installation failed."
else
  echo "Python requirements installation skipped."
fi

echo

echo "Installing Checkstyle ${CHECKSTYLE_VERSION} ..."
if need_to_install_linter "${CHECKSTYLE_DIRECTORY}"; then
  curl -SLO "https://github.com/checkstyle/checkstyle/releases/download/checkstyle-${CHECKSTYLE_VERSION}/checkstyle-${CHECKSTYLE_VERSION}-all.jar" --output-dir "${CHECKSTYLE_DIRECTORY}"
  check_return_code $? "Checkstyle ${CHECKSTYLE_VERSION} installed." "Checkstyle ${CHECKSTYLE_VERSION} installation failed."
else
  echo "Checkstyle ${CHECKSTYLE_VERSION} installation skipped."
fi

echo

echo "Installing detekt ${DETEKT_VERSION} ..."
if need_to_install_linter "${DETEKT_DIRECTORY}"; then
  curl -SLO "https://github.com/detekt/detekt/releases/download/v${DETEKT_VERSION}/detekt-cli-${DETEKT_VERSION}.zip" --output-dir "${DETEKT_DIRECTORY}" &&
    unzip "${DETEKT_DIRECTORY}/detekt-cli-${DETEKT_VERSION}.zip" -d "${DETEKT_DIRECTORY}" &&
    curl -H "Accept: application/zip" -SLO "https://repo.maven.apache.org/maven2/io/gitlab/arturbosch/detekt/detekt-formatting/${DETEKT_VERSION}/detekt-formatting-${DETEKT_VERSION}.jar" --output-dir "${DETEKT_DIRECTORY}"
  check_return_code $? "Detekt ${DETEKT_VERSION} installed." "Detekt ${DETEKT_VERSION} installation failed."
else
  echo "Detekt ${DETEKT_VERSION} installation skipped."
fi

echo

echo "Installing PMD ${PMD_VERSION} ..."
if need_to_install_linter "${PMD_DIRECTORY}"; then
  curl -SLO "https://github.com/pmd/pmd/releases/download/pmd_releases/${PMD_VERSION}/pmd-bin-${PMD_VERSION}.zip" --output-dir "${PMD_DIRECTORY}" &&
    unzip "${PMD_DIRECTORY}/pmd-bin-${PMD_VERSION}.zip" -d "${PMD_DIRECTORY}"
  check_return_code $? "PMD ${PMD_VERSION} installed." "PMD ${PMD_VERSION} installation failed."
else
  echo "PMD ${PMD_VERSION} installation skipped."
fi
