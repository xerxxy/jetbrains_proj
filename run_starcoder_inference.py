import json
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from src.constants import TOKENIZED_DATA_JSON

# Load the tokenizer and model for StarCoder
tokenizer = AutoTokenizer.from_pretrained("bigcode/starcoder", use_auth_token=True)
model = AutoModelForCausalLM.from_pretrained("bigcode/starcoder", use_auth_token=True)

# Set the model to evaluation mode
model.eval()

# Load tokenized data from a JSON file
def load_tokenized_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Run inference on each tokenized entry
def run_inference_on_data(tokenized_data):
    inference_results = []

    for entry in tokenized_data:
        # Convert prefix tokens to a tensor for the model
        input_ids = torch.tensor(entry['prefix']).to(model.device)

        with torch.no_grad():
            # Generate output from the model
            outputs = model.generate(input_ids, max_length=200, num_return_sequences=1)
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        inference_results.append({
            "input": tokenizer.decode(entry['prefix'][0], skip_special_tokens=True),
            "generated": generated_text
        })

    return inference_results


if __name__ == "__main__":
    # Load the tokenized data
    tokenized_data = load_tokenized_data(TOKENIZED_DATA_JSON)
    
    # Run inference
    results = run_inference_on_data(tokenized_data)
    print(results)
