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
#   Linter name, a string.
#   Folder with the linter files, a path.
# Returns:
#   0 if the linter needs to be installed, 1 otherwise.
#######################################
function need_to_install_linter() {
  if [[ -d $2 ]] && [[ -n $(ls -A "$2") ]]; then
    read -p "The folder with the $1 sources is not empty. Do you want to reinstall $1? (Y/n): " -r
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      return 1 # 1=false
    fi
    rm -rf "$2"
  fi

  mkdir -p "$2"
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

: "${GOLANG_LINT_VERSION:?Variable is not defined}"
: "${GOLANG_LINT_DIRECTORY:?Variable is not defined}"

: "${CODE_SERVER_HOST:?Variable is not defined}"
: "${CODE_SERVER_PORT:?Variable is not defined}"

echo "The variables are defined."

echo

read -p "Do you want to install Python requirements for the Hyperstyle project? (Y/n): " -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo "Installing Python requirements..."
  pip install --no-cache-dir -r requirements.txt
  check_return_code $? "Python requirements installed." "Python requirements installation failed."
else
  echo "Python requirements installation skipped."
fi

echo

read -p "Do you want to install Python test requirements for the Hyperstyle project? (Y/n): " -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo "Installing Python test requirements..."
  pip install --no-cache-dir -r requirements-test.txt
  check_return_code $? "Python test requirements installed." "Python test requirements installation failed."
else
  echo "Python test requirements installation skipped."
fi

echo

read -p "Do you want to install ESLint? This is the linter for JavaScript. ESLint will be installed globally. (Y/n): " -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo "Installing ESLint..."
  npm install eslint@7.5.0 -g && eslint --init
  check_return_code $? "ESLint installed." "ESLint installation failed."
else
  echo "ESLint installation skipped."
fi

echo

echo "Installing Checkstyle ${CHECKSTYLE_VERSION} ..."
if need_to_install_linter "Checkstyle" "${CHECKSTYLE_DIRECTORY}"; then
  curl -SL "https://github.com/checkstyle/checkstyle/releases/download/checkstyle-${CHECKSTYLE_VERSION}/checkstyle-${CHECKSTYLE_VERSION}-all.jar" --output "${CHECKSTYLE_DIRECTORY}/checkstyle-${CHECKSTYLE_VERSION}-all.jar" --create-dirs
  check_return_code $? "Checkstyle ${CHECKSTYLE_VERSION} installed." "Checkstyle ${CHECKSTYLE_VERSION} installation failed."
else
  echo "Checkstyle ${CHECKSTYLE_VERSION} installation skipped."
fi

echo

echo "Installing detekt ${DETEKT_VERSION} ..."
if need_to_install_linter "detekt" "${DETEKT_DIRECTORY}"; then
  curl -SL "https://github.com/detekt/detekt/releases/download/v${DETEKT_VERSION}/detekt-cli-${DETEKT_VERSION}.zip" --output "${DETEKT_DIRECTORY}/detekt-cli-${DETEKT_VERSION}.zip" --create-dirs &&
    unzip "${DETEKT_DIRECTORY}/detekt-cli-${DETEKT_VERSION}.zip" -d "${DETEKT_DIRECTORY}" &&
    curl -H "Accept: application/zip" -SL "https://repo.maven.apache.org/maven2/io/gitlab/arturbosch/detekt/detekt-formatting/${DETEKT_VERSION}/detekt-formatting-${DETEKT_VERSION}.jar" --output "${DETEKT_DIRECTORY}/detekt-formatting-${DETEKT_VERSION}.jar" --create-dirs
  check_return_code $? "Detekt ${DETEKT_VERSION} installed." "Detekt ${DETEKT_VERSION} installation failed."
else
  echo "Detekt ${DETEKT_VERSION} installation skipped."
fi

echo

echo "Installing PMD ${PMD_VERSION} ..."
if need_to_install_linter "PMD" "${PMD_DIRECTORY}"; then
  curl -SL "https://github.com/pmd/pmd/releases/download/pmd_releases/${PMD_VERSION}/pmd-bin-${PMD_VERSION}.zip" --output "${PMD_DIRECTORY}/pmd-bin-${PMD_VERSION}.zip" --create-dirs &&
    unzip "${PMD_DIRECTORY}/pmd-bin-${PMD_VERSION}.zip" -d "${PMD_DIRECTORY}"
  check_return_code $? "PMD ${PMD_VERSION} installed." "PMD ${PMD_VERSION} installation failed."
else
  echo "PMD ${PMD_VERSION} installation skipped."
fi

echo

echo "Installing golangci-lint ${GOLANG_LINT_VERSION} ..."
if need_to_install_linter "golangci-lint" "${GOLANG_LINT_DIRECTORY}"; then
  curl -SL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh |
    sh -s -- -b "${GOLANG_LINT_DIRECTORY}" "v${GOLANG_LINT_VERSION}"
  check_return_code $? "Golangci-lint ${GOLANG_LINT_VERSION} installed." "Golangci-lint ${GOLANG_LINT_VERSION} installation failed."
else
  echo "Golangci-lint ${GOLANG_LINT_VERSION} installation skipped."
fi

echo "Generating proto files  ..."
   export PROTO_PATH="hyperstyle/src/python/review/inspectors/ij_python/proto"
   python3 -m grpc_tools.protoc --proto_path=. --python_out=. --pyi_out=. --grpc_python_out=. ${PROTO_PATH}/model.proto
