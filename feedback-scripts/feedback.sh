#!/bin/bash

SCRIPT_DIR=$(dirname "$(realpath "$0")")
PARENT_DIR=$(dirname "$SCRIPT_DIR")

source "$PARENT_DIR/feedback_venv/bin/activate"
screen -S auto_feedback_runner -X stuff "$(python3 "$SCRIPT_DIR/feedback.py" "$1")\n"
