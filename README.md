# jetbrains_proj

## Code Completion and Evaluation with StarCoder

### Overview
This project implements a code completion and evaluation pipeline using the StarCoder language model. It performs code completion on a dataset of code snippets and evaluates the generated code using various metrics to assess the model's performance across different programming languages.

### Features
- **Code Completion with StarCoder**: Generates code completions based on provided code prefixes using the StarCoder model.
- **Multi-Language Support**: Processes code snippets in various programming languages as specified in the dataset.
- **Comprehensive Evaluation Metrics**:
  - **Exact Match**: Checks if the generated code exactly matches the reference code.
  - **chrF Score**: Calculates the character n-gram F-score to measure similarity.
  - **Levenshtein Distance**: Computes the minimum number of single-character edits required to change the generated code into the reference code.
  - **Cosine Similarity**: Uses the StarCoder model's embeddings to measure semantic similarity between code snippets.
  - **CodeBLEU Score**: Provides a fallback to a simplified CodeBLEU computation.
- **Embeddings with StarCoder**: Utilizes StarCoder's encoder to generate embeddings for code snippets, ensuring consistency in representation.

### Project Organization
- Inside `jetbrains_proj`, all the files from the JetBrains project are organized as follows:
  - **`data` folder**:
    - `raw` directory: Contains raw code files in different programming languages.
    - `processed` directory: Contains the data split into the format needed.
    - `tokenized` directory: Contains the tokenized data used for running the code completion model.
- **Root folder**:
  - `run_dataset_split`: Calls modules inside `src/data` to split the raw data.
  - `run_dataset_tokenizer`: Calls modules inside `src/data` to tokenize the data.
  - `run_starcoder_inference`: Runs the code completion model and evaluation metrics.
- **`src` directory**:
  - Contains the main modules for data splitting and tokenization.
  - **`src/constants`**: Stores constants used throughout the project to avoid hardcoding values.

### Details on Splitting and Tokenization
- **Data Splitting**:
  - The splitting process avoids cases where the middle section is invalid (e.g., comments or empty lines).
  - Examples are picked where the prefix is empty to create more generalized cases.
- **Tokenization**:
  - The tokenization process passes the split data through a tokenizer specifically chosen to match the StarCoder model.

### Metrics and Evaluation
- Besides **exact match** and **chrF**, I've considered the following metrics:
  - **Levenshtein distance** which like **exact match** and **chrF**, are used for blind comparison (no semantic information).
  - **CodeBLEU**, and **cosine similarity** of embeddings are used to capture code semantics better.
- The approach aims to evaluate semantic similarity, same as similar sentences have similar embeddings in LLMs or autoencoders creating similar embeddings for similar images (another example is -> word2vec).

### Model Selection Rationale
- The **big version of StarCoder** was chosen due to the dataset's complexity, which reflects entry-level programmers' coding styles and often includes messy code. The smaller versions of StarCoder were expected to underperform for this task.
