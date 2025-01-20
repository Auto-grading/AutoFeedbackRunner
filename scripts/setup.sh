#!/bin/bash

SCRIPT_DIR=$(dirname "$(realpath "$0")")
PARENT_DIR=$(dirname "$SCRIPT_DIR")
RUNNER_DIR=$PARENT_DIR/actions-runner

if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed."
    exit 1
fi

# create the oython virtual environment for running the auto feedback script
python3 -m venv "$PARENT_DIR/feedback_venv"

# activate the venv
source "$PARENT_DIR/feedback_venv/bin/activate"

# install the required packages
pip install -r "$PARENT_DIR/requirements.txt"

# set up the Github Actions Runner
mkdir "$RUNNER_DIR"
cd "$RUNNER_DIR"

# Load environment variables to get the release version
source "$PARENT_DIR/.env"

# Download the latest runner package
curl -o "actions-runner-linux-x64-$ACTIONS_RUNNER_RELEASE.tar.gz" -L "https://github.com/actions/runner/releases/download/v$ACTIONS_RUNNER_RELEASE/actions-runner-linux-x64-$ACTIONS_RUNNER_RELEASE.tar.gz"

# Optional: Validate the hash
echo "ba46ba7ce3a4d7236b16fbe44419fb453bc08f866b24f04d549ec89f1722a29e  actions-runner-linux-x64-$ACTIONS_RUNNER_RELEASE.tar.gz" | shasum -a 256 -c

# Extract the installer
tar xzf "./actions-runner-linux-x64-$ACTIONS_RUNNER_RELEASE.tar.gz"

# Configure the runner
./config.sh
