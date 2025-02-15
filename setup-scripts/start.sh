#!/bin/bash

SCRIPT_DIR=$(dirname "$(realpath "$0")")
ROOT_DIR=$(dirname "$SCRIPT_DIR")
RUNNER_DIR=$ROOT_DIR/actions-runner

if [ ! -d "$LOGS_DIR" ]; then
    mkdir "$LOGS_DIR"
fi

screen -S auto_feedback_runner "$RUNNER_DIR/run.sh"
