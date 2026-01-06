from typing import Tuple


def save_word_freq(words: Tuple[str], freqs: Tuple[int], file_path: str = 'word_freq.txt'):
    """Save word frequencies to a text file.

    Args:
        words (Tuple[str]): A tuple of words.
        freqs (Tuple[int]): A tuple of corresponding word frequencies.
        file_path (str, optional): The file path to save the word frequencies. Defaults to 'word_freq.txt'.
    Returns: 
            None
    """

    pairs = sorted(zip(words, freqs), key=lambda x: (-x[1], x[0])) # Sort by frequency descending, then alphabetically

    with open(file_path, 'w', encoding='utf-8') as f:
        for word, freq in pairs:
            f.write(f"{word} {freq}\n")

def save_word2idx(word: Tuple[str], file_path: str="word2idx.txt"):
    """Save word to index mapping to a text file.

    Args:
        word (Tuple[str]): A tuple of words.
        file_path (str, optional): The file path to save the word to index mapping. Defaults to "word2idx.txt".
    Returns: 
            None
    """
    word = sorted(word) # Sort words alphabetically
    with open(file_path, 'w', encoding='utf-8') as f:
        for idx, w in enumerate(word):
            f.write(f"{w} {idx}\n")
            

def save_idx2word(word: Tuple[str], file_path: str="idx2word.txt"):
    """Save index to word mapping to a text file.
    Args:
        word (Tuple[str]): A tuple of words.
        file_path (str, optional): The file path to save the index to word mapping. Defaults to "idx2word.txt".
    Returns: 
            None
    """
    words = sorted(word) # Sort words alphabetically
    with open(file_path, 'w', encoding='utf-8') as f:
        for idx, w in enumerate(words):
            f.write(f"{idx} {w}\n")
            
            
def load_word_freq(file_path: str):
    """Load word frequencies from a text file.
    Args:
        file_path (str): The file path to load the word frequencies from.
    Returns:
        dict: A dictionary mapping words to their frequencies.
    """
    result = {}
    with open(file_path, 'r', encoding='utf-8') as f: # read file with utf-8 encoding
        for line in f:
            word, freq = line.strip().split()
            result[word] = int(freq)
    return result

def load_word2idx(file_path: str):
    """Load word to index mapping from a text file.
    Args:
        file_path (str): The file path to load the word to index mapping from.
    Returns:
        dict: A dictionary mapping words to their indices.
    """
    result = {}
    with open(file_path, 'r', encoding='utf-8') as f: # read file with utf-8 encoding
        for line in f:
            word, idx = line.strip().split()
            result[word] = int(idx)
    return result


def load_idx2word(file_path: str):
    """Load index to word mapping from a text file.
    Args:
        file_path (str): The file path to load the index to word mapping from.
    Returns:
        dict: A dictionary mapping indices to their corresponding words.
    """
    result = {}
    with open(file_path, 'r', encoding='utf-8') as f: # read file with utf-8 encoding
        for line in f:
            idx, word = line.strip().split()
            result[int(idx)] = word
    return result


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    sample_words = ("apple", "dog", "master")
    sample_freqs = (3, 10, 1)

    pairs = sorted(zip(sample_words, sample_freqs), key=lambda x: (-x[1], x[0]))
    sorted_words, sorted_freqs = zip(*pairs)

    save_word_freq(sorted_words, sorted_freqs, "word_freq.txt")
    save_word2idx(sample_words, "word2idx.txt")
    save_idx2word(sample_words, "idx2word.txt")

    wf = load_word_freq("word_freq.txt")
    w2i = load_word2idx("word2idx.txt")
    i2w = load_idx2word("idx2word.txt")

