import os
import sys
from pathlib import Path

from textwrap import dedent
from openai import OpenAI

FILE_EXT = ".java"

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


# Function to get feedback from GPT on the student's code
def get_gpt_feedback(problem_description, code):
    # Format the problem and solution content to provide to GPT
    problem = f"Here is the problem description:\n{problem_description}"
    solution = f"Here is the student's code:\n{code}"

    gpt_model = "gpt-4o-mini"  # Specify the GPT model to use
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Initialize OpenAI client with API key
    res = client.chat.completions.create(
        model=gpt_model,
        messages=[{"role": "user", "content": problem},
                  {"role": "user", "content": solution}],
    )

    # Return the content of GPT's feedback
    return res.choices[0].message.content


# Function to create the feedback file and save the generated feedback
def create_feedback_file(content, feedback_run_number):
    # Save the feedback to a markdown file
    feedback_file_path = f"feedback/feedback-{feedback_run_number}.md"
    with open(feedback_file_path, "w") as feedback:
        feedback.write(content)


def main():
    repo_path = sys.argv[1]
    readme = get_readme(repo_path)
    student_code = get_student_code(repo_path)
    print(get_student_code(repo_path))


if __name__ == "__main__":
    main()
