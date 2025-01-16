SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Define the consistent directory path (e.g., create 'some_directory' one level up)
RUNNER_DIR=$(dirname "$SCRIPT_DIR")/actions-runner

mkdir "$RUNNER_DIR" && cd $RUNNER_DIR

# Download the latest runner package
curl -o actions-runner-linux-x64-2.321.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.321.0/actions-runner-linux-x64-2.321.0.tar.gz

# Optional: Validate the hash
echo "ba46ba7ce3a4d7236b16fbe44419fb453bc08f866b24f04d549ec89f1722a29e  actions-runner-linux-x64-2.321.0.tar.gz" | shasum -a 256 -c

# Extract the installer
tar xzf ./actions-runner-linux-x64-2.321.0.tar.gz
