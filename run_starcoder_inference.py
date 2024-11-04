import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from src.constants import TOKENIZED_DATA_JSON
from src.utils import get_device
from sacrebleu import sentence_chrf

from Levenshtein import distance as levenshtein_distance
from sentence_transformers import SentenceTransformer, util
import warnings
from collections import Counter
import torch.nn.functional as F
warnings.filterwarnings("ignore")

# Load the tokenizer and model for StarCoder
tokenizer = AutoTokenizer.from_pretrained("bigcode/starcoder", use_auth_token=True)
model = AutoModelForCausalLM.from_pretrained("bigcode/starcoder", use_auth_token=True)
model.eval()

# Load tokenized data from a JSON file
def load_tokenized_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_starcoder_embedding(code_text):
    # When computing the cosine similarity between two pieces of code,
    #we want to measure how similar their meanings are in the model's learned representation space,
    #to do this, we need to obtain the embeddings of the code snippets, not just their token ids.
    inputs = tokenizer.encode(code_text, return_tensors='pt', truncation=True).to(get_device())
    with torch.no_grad():
        outputs = model(inputs, output_hidden_states=True)
    last_hidden_state = outputs.hidden_states[-1]  
    embedding = torch.mean(last_hidden_state, dim=1)  
    return embedding

def compute_codebleu(preds, refs, lang="python"):
    #Simplified version of codebleu, I had some error with the codexglue repo
    #Here, I'll compute n gram matching score as a placeholder

    def ngram_match_score(candidate, reference, n):
        def ngram_counter(text, n):
            tokens = text.split()
            return Counter([tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)])
        candidate_ngrams = ngram_counter(candidate, n)
        reference_ngrams = ngram_counter(reference, n)
        overlap = sum((candidate_ngrams & reference_ngrams).values())
        total = sum(candidate_ngrams.values())
        return overlap / total if total > 0 else 0

    # Compute n gram scores
    ngram_scores = []
    for n in range(1, 5):
        score = ngram_match_score(preds, refs, n)
        ngram_scores.append(score)
    # Average n gram scores as a placeholder for Codebleu
    codebleu_score = sum(ngram_scores) / len(ngram_scores) * 100
    return codebleu_score

def run_inference_on_data(tokenized_data):
    inference_results = []

    for idx, entry in enumerate(tokenized_data):
        input_ids = torch.tensor(entry['prefix'][0]).unsqueeze(0).to(get_device())
        attention_mask = torch.ones_like(input_ids).to(get_device())
        with torch.no_grad():
            outputs = model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_new_tokens=200,
                num_return_sequences=1,
                do_sample=False  # Disable sampling for deterministic results
            )
            generated_ids = outputs[0]
            #Exclude the input_ids from the generated_ids to get the new tokens
            generated_tokens = generated_ids[input_ids.shape[1]:]
            generated_text = tokenizer.decode(generated_tokens, skip_special_tokens=True)

        # Decode the true middle text
        true_middle_text = tokenizer.decode(entry['middle'][0], skip_special_tokens=True)
        input_text = tokenizer.decode(entry['prefix'][0], skip_special_tokens=True)


        # Get the programming language from the entry
        lang = entry['language']  

        # Compute Exact Match
        exact_match = int(generated_text.strip() == true_middle_text.strip())

        # Compute chrF
        chrf_score = sentence_chrf(generated_text, [true_middle_text]).score

        # Compute Levenshtein distance
        lev_distance = levenshtein_distance(generated_text, true_middle_text)

        # Compute Cosine similarity of embeddings
        embedding1 = get_starcoder_embedding(generated_text)
        embedding2 = get_starcoder_embedding(true_middle_text)
        cosine_sim = F.cosine_similarity(embedding1, embedding2).item()

        # Compute Codebleu
        codebleu_score = compute_codebleu(generated_text, true_middle_text, lang)

        # Print the results for each metric
        print(f"Example {idx + 1}:")
        print("Input text:")
        print(input_text)
        print("\nGenerated text:")
        print(generated_text)
        print("\nTrue middle text:")
        print(true_middle_text)
        print("\nMetrics:")
        print(f"Language: {lang}")
        print(f"Exact match: {exact_match}")
        print(f"Chrf score: {chrf_score:.4f}")
        print(f"Levenshtein distance: {lev_distance}")
        print(f"Cosine similarity: {cosine_sim:.4f}")
        print(f"Codebleu score: {codebleu_score:.2f}")


        inference_results.append({
            "input": input_text,
            "generated": generated_text,
            "true_middle": true_middle_text,
            "language": lang,
            "metrics": {
                "exact_match": exact_match,
                "chrf": chrf_score,
                "levenshtein_distance": lev_distance,
                "cosine_similarity": cosine_sim,
                "codebleu": codebleu_score
            }
        })

    return inference_results

if __name__ == "__main__":
    # Load the tokenized data
    tokenized_data = load_tokenized_data(TOKENIZED_DATA_JSON)

    # Run inference
    results = run_inference_on_data(tokenized_data)
