import os
import sys
from pathlib import Path

from dotenv import load_dotenv, find_dotenv
from textwrap import dedent
from openai import OpenAI

FILE_EXT = ".java"

def load_environment_variables():
    if not find_dotenv():
        raise FileNotFoundError(".env file not found!")
    load_dotenv()

def get_readme(assignment_directory):
    with open(f"{assignment_directory}/README.md") as readme:
        return readme.read()


def get_student_code(assignment_directory):
    code_files = []

    assignment_directory = Path(assignment_directory)
    for file in assignment_directory.iterdir():
        if file.is_file() and file.suffix == FILE_EXT:
            with file.open("r") as code_file:
                code_files.append(f"File {os.path.basename(file)}:\n{code_file.read()}")

    return "\n".join(code_files)


def get_prompt_description(feedback_categories):
    return dedent(f"""
    You are a helpful code reviewing assistant.
    Act as a professional software engineer reviewing code written by an undergraduate computer science student.
    0. Review the code and the associated README file.
    1. Focus on these aspects:
        - Code clarity (naming conventions, readability).
        - Use of comments (includes function and file header comments, does not comment the obvious)
        - Code structure and modularity.
        - Adherence to best practices (error handling, validation).
    2. Be verbose in your observations.
    3. Do not:
        - Generate or suggest new code.
        - Write explanations or examples of how to fix issues.
        - Provide updates or revised versions of the code.
    Format your response in Markdown for easy readability.
    """)


# Function to get feedback from GPT on the student's code
def get_gpt_feedback(problem_description, code):
    # Format the problem and solution content to provide to GPT
    problem = f"Here is the problem description:\n{problem_description}"
    solution = f"Here is the student's code:\n{code}"

    gpt_model = os.getenv("GPT_MODEL")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # send the message to ChatGPT
    res = client.chat.completions.create(
        model=gpt_model,
        messages=[{"role": "user", "content": problem},
                  {"role": "user", "content": solution}],
    )

    # Return the content of GPT's feedback
    return res.choices[0].message.content


def get_feedback_run_number(assignment_directory):
    runs_path = Path(f"{assignment_directory}/feedback_runs")
    runs = 1
    if os.path.exists(runs_path):
        with open(runs_path, "r") as runs_file:
            runs = int(runs_file.read())

    with open(runs_path, "w") as runs_file:
        runs_file.write(str(runs + 1))

    return runs


# Function to create the feedback file and save the generated feedback
def create_feedback_file(assignment_directory, content):
    # Save the feedback to a markdown file
    feedback_file_path = f"feedback/feedback-{get_feedback_run_number(assignment_directory)}.md"
    with open(feedback_file_path, "w") as feedback:
        feedback.write(content)


def main():
    repo_path = sys.argv[1]

    load_environment_variables()

    readme = get_readme(repo_path)
    student_code = get_student_code(repo_path)
    feedback = get_gpt_feedback(readme, student_code)
    create_feedback_file(repo_path, feedback)


if __name__ == "__main__":
    main()
