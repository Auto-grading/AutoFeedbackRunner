#!/bin/bash

echo "Testing..."

SCRIPT_DIR=$(dirname "$(realpath "$0")")
PARENT_DIR=$(dirname "$SCRIPT_DIR")

source "$PARENT_DIR/feedback_venv/bin/activate"
python3 "$SCRIPT_DIR/feedback.py" "$1"
