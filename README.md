# How to Set up the Auto Feedback Runner

## Prerequisites

Before starting, make sure you have the following:

- A Linux-based operating system
- x86_64 Architecture
- Python 3 Installed: ```sudo apt install python3```
- Pip Installed: ```sudo apt install python3-pip```

## Steps

### 0. Clone the Repository
```git@github.com:Auto-grading/AutoFeedbackRunner.git```

### 1. Change to the repository's directory
```cd AutoFeedbackRunner```

Here you will find the directory ```.github```, which a copy of this will need to be put in each student's repo

### 2. Set the OPENAI_API_KEY Environment Variable
```nano .env```

copy and paste your OpenAI API key after ```OPENAI_API_KEY=```

### 3. Configure the Runner

On your runner's machine:

```cd scripts```

```./setup.sh```

You will need to provide your organization's URL and runner register token.

To find these, inside your organization on GitHub go to:

Settings > Actions > Runners > New runner > New self-hosted runner

You will see a line that looks like this where you can find the url and runner register token:

```./config.sh --url <Organization URL> --token <Runner Register Token>```

Enter the URL and the Runner Register token when prompted by the setup script

### 4. Give the Runner Write Permissions

Inside your organization on GitHub, go to:

Settings > Actions > General

If you scroll down, you should see a section called Workflow Permissions.

In this section, select Read and write permissions and press Save.

### 5. Start the runner

This will create a screen session for the runner:

```start.sh```

### When you want to stop the runner

This will stop the runner's screen session:

```stop.sh```
