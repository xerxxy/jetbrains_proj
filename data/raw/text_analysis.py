
def count_words(file_path):
    """Counts the words in a given text file."""
    try:
        with open(file_path, 'r') as file:
            text = file.read()
        words = text.split()
        return len(words)
    except FileNotFoundError:
        print("File not found!")
        return None

def most_common_word(file_path):
    """Finds the most common word in a given text file."""
    from collections import Counter
    try:
        with open(file_path, 'r') as file:
            text = file.read().lower()
        words = text.split()
        word_counts = Counter(words)
        return word_counts.most_common(1)[0]
    except FileNotFoundError:
        print("File not found!")
        return None

def main():
    file_path = 'sample.txt'
    print(f"Total word count: {count_words(file_path)}")
    common_word, frequency = most_common_word(file_path)
    print(f"The most common word is '{common_word}' with a frequency of {frequency}.")

if __name__ == "__main__":
    main()
