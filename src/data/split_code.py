import os
import json
import random
from src.constants import RAW_DATA_DIR, MIN_PREFIX_LENGTH, MIN_SUFFIX_LENGTH, PROCESSED_DATA_DIR

def read_code_files(directory):
    """
    Reads all code files from a specified directory and its subdirectories.

    Parameters:
        directory (str): The root directory to search for code files.

    Returns:
        list: A list of tuples containing file paths and their corresponding programming language.
    """
    code_files = []
    # Walk through the directory tree
    for root, _, files in os.walk(directory):
        for file in files:
            # Check if the file has a code file extension
            if file.endswith((".py", ".java", ".c")):
                # Determine the programming language based on the file extension
                if file.endswith(".py"):
                    language = "python"
                elif file.endswith(".java"):
                    language = "java"
                elif file.endswith(".c"):
                    language = "c"
                else:
                    language = "unknown"
                # Add the full path of the code file and its language to the list
                code_files.append((os.path.join(root, file), language))
    return code_files

def pick_line_position(code_lines):
    """
    Picks a valid line and a cursor position within that line, ensuring the line is not a comment or empty.

    Parameters:
        code_lines (list): A list of code lines from the file.

    Returns:
        tuple: A tuple containing the chosen line index and the cursor position within that line.
               Returns (None, None) if no valid lines are found.
    """
    # Find indexes of lines that are not empty and do not start with comment characters
    valid_lines_indexes = [
        i for i, line in enumerate(code_lines)
        if line.strip() and not line.strip().startswith(("\n", "#", "//"))
    ]

    # If there are no valid lines, return None
    if not valid_lines_indexes:
        return None, None  # No valid lines found

    # Randomly choose a line index from the valid lines
    chosen_line = random.choice(valid_lines_indexes)

    # Choose a random cursor position within the chosen line (up to half its length)
    position_in_line = random.randint(0, len(code_lines[chosen_line].strip()) // 2)
    # Adjust the position to maintain indentation by adding leading whitespace length
    position_in_line += len(code_lines[chosen_line]) - len(code_lines[chosen_line].lstrip())

    return chosen_line, position_in_line

def construct_prefix_middle_suffix(code_lines, chosen_line, position_in_line):
    """
    Constructs the prefix, middle, and suffix sections of the code based on the chosen line and cursor position.

    Parameters:
        code_lines (list): A list of code lines from the file.
        chosen_line (int): The index of the chosen line in the code_lines list.
        position_in_line (int): The cursor position within the chosen line.

    Returns:
        tuple: A tuple containing the prefix, middle, and suffix strings.
    """
    # Construct the prefix by joining all lines up to the chosen line and adding the part of the chosen line before the cursor
    prefix = '\n'.join(code_lines[:chosen_line]) + '\n' + code_lines[chosen_line][:position_in_line]

    # Start constructing the middle section from the cursor position in the chosen line
    middle = code_lines[chosen_line][position_in_line:] + '\n'

    # Determine how many additional lines to add to the middle section (1 to 5, but not exceeding the file length)
    additional_lines = min(len(code_lines) - chosen_line - 1, random.randint(1, 5))
    for i in range(1, additional_lines + 1):
        # Skip lines that are comments
        if not code_lines[chosen_line + i].strip().startswith(("#", "//")):
            # Add the line to the middle section
            middle += code_lines[chosen_line + i] + '\n'

    # Construct the suffix by joining all lines after the middle section
    suffix_start = chosen_line + additional_lines + 1
    suffix = '\n'.join(code_lines[suffix_start:])

    return prefix, middle, suffix

def split_code_example(code_text):
    """
    Splits code text into prefix, middle, and suffix sections at a random point, ensuring minimum length requirements.

    Parameters:
        code_text (str): The full text of the code file.

    Returns:
        dict or None: A dictionary with 'prefix', 'middle', 'suffix', and 'language' keys if successful; otherwise, None.
    """
    # Check if the code text meets the minimum prefix length requirement
    if len(code_text) < MIN_PREFIX_LENGTH:
        return None

    # Split the code text into lines
    code_lines = code_text.splitlines()
    if len(code_lines) < 1:
        return None

    # Pick a valid line and cursor position
    chosen_line, position_in_line = pick_line_position(code_lines)
    if chosen_line is None:
        return None

    # Construct the prefix, middle, and suffix sections
    prefix, middle, suffix = construct_prefix_middle_suffix(code_lines, chosen_line, position_in_line)

    # Ensure the prefix and suffix meet the minimum length requirements
    if len(prefix) >= MIN_PREFIX_LENGTH and len(suffix) >= MIN_SUFFIX_LENGTH:
        return {"prefix": prefix, "middle": middle, "suffix": suffix}
    return None

def generate_code_completion_examples(directory, num_examples=4):
    """
    Generates code completion examples from code files in the specified directory.

    Parameters:
        directory (str): The directory containing code files.
        num_examples (int): The number of examples to generate per file.

    Returns:
        list: A list of dictionaries containing 'prefix', 'middle', 'suffix', and 'language' for each example.
    """
    # Read all code files from the directory
    code_files = read_code_files(directory)
    examples = []
    # Iterate to generate the specified number of examples
    for _ in range(num_examples):
        for file_path, language in code_files:
            with open(file_path, 'r', encoding='utf-8') as file:
                code_text = file.read()

            # Attempt to split the code into an example
            example = split_code_example(code_text)
            if example:
                # Include the programming language in the example
                example['language'] = language
                examples.append(example)

    return examples

def generate_split():
    """
    Generates code completion examples and saves them to a JSON file.
    """
    # Generate the dataset
    dataset = generate_code_completion_examples(RAW_DATA_DIR, num_examples=4)
    # Define the output file path
    output_file = os.path.join(PROCESSED_DATA_DIR, 'code_completion_dataset.json')

    # Save the dataset to a JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=4)

    print(f"Generated {len(dataset)} code completion examples and saved to {output_file}")
