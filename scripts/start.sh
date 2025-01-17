#!/bin/bash

SCRIPT_DIR=$(dirname "$(realpath "$0")")
ROOT_DIR=$(dirname "$SCRIPT_DIR")
RUNNER_DIR=$ROOT_DIR/actions-runner
LOGS_DIR=$ROOT_DIR/logs

if [ ! -d "$LOGS_DIR" ]; then
    mkdir "$LOGS_DIR"
fi

screen -S auto_feedback_runner -L -Logfile "$LOGS_DIR" "$RUNNER_DIR/run.sh"
