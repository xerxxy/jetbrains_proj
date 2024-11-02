from transformers import AutoTokenizer 
from src.constants import PROCESSED_DATA_DIR, PROCESSED_DATA_JSON, TOKENIZED_DATA_JSON
import os
import json

# Initialize the tokenizer for StarCoder
tokenizer = AutoTokenizer.from_pretrained("bigcode/starcoder")

def tokenize_entry(entry):
    """
    Takes a code completion example and returns the tokenized version.
    
    Args:
        example (dict): A dictionary with keys 'prefix', 'middle', and 'suffix' containing code segments.
    
    Returns:
        dict: A dictionary containing the tokenized 'prefix', 'middle', and 'suffix'.
    """
    tokenized = {
        "prefix": tokenizer.encode(entry["prefix"], return_tensors="pt", truncation=True).tolist(),
        "middle": tokenizer.encode(entry["middle"], return_tensors="pt", truncation=True).tolist(),
        "suffix": tokenizer.encode(entry["suffix"], return_tensors="pt", truncation=True).tolist()
    }
    return tokenized  

def load_processed_examples():
    """Loads processed examples from JSON files in the specified directory."""
    processed_data = []

    with open(PROCESSED_DATA_JSON, 'r', encoding='utf-8') as file:
       processed_data = json.load(file)

    return processed_data

def tokenize_dataset():
    """Tokenizes the processed dataset and saves it as a single JSON file."""
    # Load processed examples from the specified directory
    processed_data = load_processed_examples()
    print(processed_data)
    # Tokenize each example
    tokenized_examples = [tokenize_entry(entry) for entry in processed_data]

    # Save the tokenized examples to the specified JSON file
    with open(TOKENIZED_DATA_JSON, 'w', encoding='utf-8') as f:
        json.dump(tokenized_examples, f, indent=4)
    
    print(f"Tokenized dataset saved to {TOKENIZED_DATA_JSON}")

