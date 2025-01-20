# How to Set up the Auto Feedback Runner


### 0. Clone the Repository
```git@github.com:Auto-grading/AutoFeedbackRunner.git```

### 1. Change to the repository's directory
```cd AutoFeedbackRunner```

Here you will find the directory ```.github```, which a copy of this will need to be put in each student's repo

### 2. Set the OPENAI_API_KEY Environment Variable
```nano .env```

copy and paste your OpenAI API key after ```OPENAI_API_KEY=```

### 3. Configure the Runner

Inside your organization on GitHub go to:

Settings > Actions > Runners > New runner > New self-hosted runner

You will see a line that looks like this where you can find the url and runner register token:

```./config.sh --url <Organization URL> --token <Runner Register Token>```

Back on your runner's machine:

```cd scripts```

```./setup.sh```

When prompted for the URL and runner register token, enter the url and token found from performing the steps above on GitHub

### 4. Start the runner

This will create a screen session for the runner:

```start.sh```

### When you want to stop the runner

This will stop the runner's screen session:

```stop.sh```
