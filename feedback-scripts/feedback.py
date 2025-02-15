import os
import sys
from pathlib import Path

import openai
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

FILE_EXT = ".java"
FEEDBACK_INSTRUCTIONS = """
You are a helpful code reviewing assistant.
Act as a professional software engineer reviewing code written by an undergraduate computer science student.
0. Review the code and the associated README file.
1. Do not Generate or suggest new code.
2. Do not Write explanations or examples of how to fix issues.
3. Do not Provide updates or revised versions of the code.
4. Focus on these aspects:
- Code clarity (naming conventions, readability).
- Use of comments (includes function and file header comments, does not comment the obvious)
- Code structure and modularity.
- Adherence to best practices (error handling, validation).
5. Be verbose in your observations.
Format your response in Markdown for easy readability.
"""


def load_environment_variables():
    """
    Load environment variables used throughout this script
    """
    if not find_dotenv():
        raise FileNotFoundError(".env file not found")
    load_dotenv()


def get_readme(assignment_directory):
    """
    Read the content from the repo's readme

    Args:
        assignment_directory (str): directory of the student's assignment repo

    Returns:
        str: Content of the README.md file in the student's repo
    """
    with open(f"{assignment_directory}/README.md") as readme:
        return readme.read()


def get_student_code(assignment_directory):
    """
    Read the student's code files in the repo

    Args:
        assignment_directory (str): directory of the student's assignment repo

    Returns:
        str: All the student's code concatenated as a string. Each file is labeled by name in the string
    """
    code_files = []

    assignment_directory = Path(assignment_directory)
    for file in assignment_directory.iterdir():
        if file.is_file() and file.suffix == FILE_EXT:
            with file.open("r") as code_file:
                code_files.append(f"File {os.path.basename(file)}:\n{code_file.read()}")

    return "\n".join(code_files)


def get_gpt_feedback(problem_description, code):
    """
    Get feedback on the student's code via the OpenAI API

    Args:
        problem_description (str): description of the problem
        code (str): the student's solution

    Returns:
        str: the feedback returned by the OpenAI API
    """
    problem = f"Here is the problem description:\n{problem_description}"
    solution = f"Here is the student's code:\n{code}"

    gpt_model = os.getenv("GPT_MODEL")
    if gpt_model is None:
        raise RuntimeError("No GPT_MODEL set in .env file")

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # send the message to the OpenAI API
        response = client.chat.completions.create(
            model=gpt_model,
            messages=[
                {"role": "system", "content": FEEDBACK_INSTRUCTIONS},
                {"role": "user", "content": problem},
                {"role": "user", "content": solution}
            ],
        )
        if response.choices is None or response.choices[0].message is None:
            raise RuntimeError("Unexpected response format from OpenAI")

        return response.choices[0].message.content

    except openai.APIError as e:
        raise RuntimeError(f"OpenAI API error: {e}")


def get_feedback_run_number(assignment_directory):
    """
    Count the number of feedback files in the repo so far

    Args:
        assignment_directory (str): directory of the student's assignment repo

    Returns:
        int: the number of feedback files in the repo
    """
    feedback_dir = Path(f"{assignment_directory}/feedback")
    return sum(entry.is_file() for entry in os.scandir(feedback_dir))


def create_feedback_file(assignment_directory, feedback_content):
    """
    Create a new feedback file in the student's repo with the given content

    Args:
        assignment_directory (str): directory of the student's assignment repo
        feedback_content (str): the content to store in the feedback file
    """
    # create feedback directory if it does not already exist
    feedback_dir = Path(f"{assignment_directory}/feedback")
    os.makedirs(feedback_dir, exist_ok=True)

    # Save the feedback to a markdown file
    feedback_file_path = os.path.join(feedback_dir, f"feedback-{get_feedback_run_number(assignment_directory)}.md")
    with open(feedback_file_path, "w") as feedback:
        feedback.write(feedback_content)


def main():
    """
    Main function
    """
    # Get the path of the repository passed in as a command line argument
    print("Resolving the student's repository's path...")
    repo_path = sys.argv[1]

    print("Load environment variables for the feedback script...")
    load_environment_variables()

    print("Reading the problem description from the README...")
    readme = get_readme(repo_path)

    print("Getting the student's code...")
    student_code = get_student_code(repo_path)

    print("Requesting GPT Feedback...")
    feedback = get_gpt_feedback(readme, student_code)
    print("Successfully retrieved GPT Feedback!")

    print("Creating feedback file...")
    create_feedback_file(repo_path, feedback)
    print("Pushing feedback file...")


if __name__ == "__main__":
    main()
