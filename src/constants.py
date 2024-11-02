import os 

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DATA_DIR = os.path.join(PROJECT_ROOT, "data")

RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
TOKENIZED_DATA_DIR = os.path.join(DATA_DIR, "tokenized")

PROCESSED_DATA_JSON = os.path.join(PROCESSED_DATA_DIR, "code_completion_dataset.json")
TOKENIZED_DATA_JSON = os.path.join(TOKENIZED_DATA_DIR, "tokenized_dataset.json")

MAX_TOKENS = 1024
NUM_EXAMPLES = 50

MIN_PREFIX_LENGTH = 50
MIN_SUFFIX_LENGTH = 0

