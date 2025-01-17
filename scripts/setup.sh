#!/bin/bash

SCRIPT_DIR=$(dirname "$(realpath "$0")")
PARENT_DIR=$(dirname "$SCRIPT_DIR")
RUNNER_DIR=$PARENT_DIR/actions-runner

source "$PARENT_DIR/.env"

mkdir "$RUNNER_DIR"
cd "$RUNNER_DIR"

# Download the latest runner package
curl -o "actions-runner-linux-x64-$ACTIONS_RUNNER_RELEASE.tar.gz" -L "https://github.com/actions/runner/releases/download/v$ACTIONS_RUNNER_RELEASE/actions-runner-linux-x64-$ACTIONS_RUNNER_RELEASE.tar.gz"

# Optional: Validate the hash
echo "ba46ba7ce3a4d7236b16fbe44419fb453bc08f866b24f04d549ec89f1722a29e  actions-runner-linux-x64-$ACTIONS_RUNNER_RELEASE.tar.gz" | shasum -a 256 -c

# Extract the installer
tar xzf "./actions-runner-linux-x64-$ACTIONS_RUNNER_RELEASE.tar.gz"

./config.sh
