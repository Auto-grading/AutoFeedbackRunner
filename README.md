# How to Set up the Auto Feedback Runner

## Prerequisites

### 0. System Requirements

Before starting, make sure you have the following:

- A Linux-based operating system
- x86_64 Architecture
- Python 3 Installed: ```sudo apt install python3```
- Pip Installed: ```sudo apt install python3-pip```

### 1. Give Runners Write Permissions

Inside your organization on GitHub, go to:

Settings > Actions > General

If you scroll down, you should see a section called Workflow Permissions.

In this section, select Read and write permissions and press Save.

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

### 4. Start/Stop the Runner

#### Start

This will create a screen session for the runner:

```./start.sh```

#### Stop

This will stop the runner's screen session:

```./stop.sh```

### 5. Running the Workflow in the Student's Repository

In the root directory of this cloned repository:

Copy the file ```.github/workflows/auto_feedback.yml``` into the student's repository

Inside the student's repository:

Click on the issues tab

Create a new issue. This will run the workflow. 

The runner will get the feedback via the OpenAI API and push it to the student's repository in the ```feedback``` folder
