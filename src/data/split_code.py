import os
import json
import random
from src.constants import RAW_DATA_DIR, MIN_PREFIX_LENGTH, MIN_SUFFIX_LENGTH, PROCESSED_DATA_DIR

def read_code_files(directory):
    """Reads all code files from a specified directory."""
    code_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".py", ".java", ".c")):
                code_files.append(os.path.join(root, file))
    return code_files

def pick_line_position(code_lines):
    """Picks a valid line and position for the cursor, ensuring the middle does not start with a comment."""
    valid_lines_indexes = [i for i, line in enumerate(code_lines) if line.strip() and not line.strip().startswith(("\n", "#", "//"))]

    if not valid_lines_indexes:
        return None, None  # No valid lines found

    chosen_line = random.choice(valid_lines_indexes)

    # Choose a random position within the chosen line for the cursor
    position_in_line = random.randint(0, len(code_lines[chosen_line].strip()) // 2)
    position_in_line += len(code_lines[chosen_line]) - len(code_lines[chosen_line].lstrip())  # Maintain indentation

    return chosen_line, position_in_line

def construct_prefix_middle_suffix(code_lines, chosen_line, position_in_line):
    """Constructs prefix, middle, and suffix sections based on the chosen line and position."""
    prefix = '\n'.join(code_lines[:chosen_line]) + '\n' + code_lines[chosen_line][:position_in_line]

    # Construct the middle starting from the cursor position in the chosen line
    middle = code_lines[chosen_line][position_in_line:] + '\n'

    # Add more lines to the middle if needed and possible
    additional_lines = min(len(code_lines) - chosen_line - 1, random.randint(1, 5))
    for i in range(1, additional_lines + 1):
        # Ensure the middle lines are not comments
        if not code_lines[chosen_line + i].strip().startswith(("#", "//")):
            middle += code_lines[chosen_line + i] + '\n'

    # Construct the suffix starting from the line after the middle section
    suffix_start = chosen_line + additional_lines + 1
    suffix = '\n'.join(code_lines[suffix_start:])

    return prefix, middle, suffix

def split_code_example(code_text):
    """Splits code into prefix, middle, and suffix sections at a random point."""
    if len(code_text) < MIN_PREFIX_LENGTH:
        return None

    code_lines = code_text.splitlines()
    if len(code_lines) < 1:
        return None

    chosen_line, position_in_line = pick_line_position(code_lines)
    if chosen_line is None:
        return None

    prefix, middle, suffix = construct_prefix_middle_suffix(code_lines, chosen_line, position_in_line)

    # Ensure each section meets the minimum length requirements
    if len(prefix) >= MIN_PREFIX_LENGTH and len(suffix) >= MIN_SUFFIX_LENGTH:
        return {"prefix": prefix, "middle": middle, "suffix": suffix}
    return None

def generate_code_completion_examples(directory, num_examples=4):
    """Generates code completion examples from code files in the specified directory."""
    code_files = read_code_files(directory)
    examples = []
    for iter in range(num_examples):
        for file_path in code_files:
            with open(file_path, 'r', encoding='utf-8') as file:
                code_text = file.read()

            example = split_code_example(code_text)
            if example:
                examples.append(example)



    return examples


def generate_split():
    dataset = generate_code_completion_examples(RAW_DATA_DIR, num_examples=4)
    output_file = os.path.join(PROCESSED_DATA_DIR, 'code_completion_dataset.json')

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=4)

    print(f"Generated {len(dataset)} code completion examples and saved to {output_file}")
