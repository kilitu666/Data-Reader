from typing import Tuple, List, Optional
import os


def get_stopwords(stopwords_file: str) -> List[str]:
    """Read stop words from a file and return their lowercase as a list.
    Args:
        stopwords_file (str): Path to the stop words file.
    Returns:
        List[str]: A list of stop words.
    """
    words = []
    with open(stopwords_file, 'r', encoding='utf-8') as f:
        for line in f:
            w = line.strip().lower() 
            if w:
                words.append(w)
    return words
   



def get_vocabs(text: str, stopwords: List) -> Tuple[Tuple[str], Tuple[int]] | Tuple[()]:
    """ Abstract words from the given text, filter them based on the criteria, return them as a sorted tuple along with their frequencies.
    Args:
        text (str): The input text to process.
        stopwords (List): A list of stop words to filter out.
    Returns:
        Tuple[Tuple[str], Tuple[int]] | Tuple[()]: A tuple containing :
             - A tuple of sorted words and a tuple of their corresponding frequencies.
             - Or an empty tuple if no valid words are"""
    tokens = []
    current = ""
    # Tokenisation: split by non-alphanumeric characters
    for ch in text:
        if ch.isdigit() or ch.isalpha():
            current += ch.lower()
        elif current:
                tokens.append(current.lower())
                current = ""
    # Finalize the last token if exists
    if current:
        tokens.append(current.lower())
        
    # Convert stopwords to a set for faster lookup (remove duplicates too if exists)
    sw = set(stopwords)
    filtered = []
    # Filtering tokens with the given criteria
    for t in tokens:
        if not t.isalpha():
            continue
        if len(t) < 2:
            continue
        if t in sw:
            continue
        filtered.append(t)

    # If no valid words remain after filtering, return an empty tuple    
    if not filtered:
        return tuple()
 
    counts = {}
    # Count frequencies of each word
    for w in filtered: 
        counts[w] = counts.get(w, 0) + 1
    
    vocab_sorted = tuple(sorted(counts.keys()))
    freqs = tuple(counts[w] for w in vocab_sorted)

    return vocab_sorted, freqs


def process_mini_dataset(
        stop_words: List[str],
        data_path: str = 'data',
        category: Optional[str] = None,
    ):
    """Process a mini dataset to extract vocabulary and their frequencies, and write them to 'word_freq.txt'.
    Args:
        stop_words (List[str]): A list of stop words to filter out.
        data_path (str, optional): Path to the dataset directory. Defaults to 'data'.
        category (Optional[str], optional): Specific category subdirectory to process. Defaults to None.
    Returns:
        Tuple[Tuple[str], Tuple[int]] | Tuple[()]: A tuple containing:
            - A tuple of sorted words and a tuple of their corresponding frequencies.
            - Or an empty tuple if no valid words are found or if the directory doesn't exist.
    """
    
    texts = []
    if category: # process a specific category
        root_path = os.path.join(data_path, category)
        if not os.path.exists(root_path): # directory doesn't exist return empty tuple
            return tuple()
        search_dirs = [root_path] # only search this directory
    else:
        if not os.path.isdir(data_path): 
            return tuple()
        search_dirs = [os.path.join(data_path, d) for d in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, d))] 
    
    for folder in search_dirs: # iterate through each directory
        for fname in os.listdir(folder): 
            fpath = os.path.join(folder, fname) 
            if os.path.isfile(fpath) and fname.endswith('.txt'): 
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    texts.append(content)
    if not texts:
        return tuple()

    all_text = '\n'.join(texts)
    result = get_vocabs(all_text, stop_words)
    # If no vocabulary was found, return empty and do not write a file
    if not result:
        return tuple()

    vocab_sorted, freqs = result
    # Pair and sort by frequency descending
    pairs = sorted(zip(vocab_sorted, freqs), key=lambda x: x[1], reverse=True)

    # Write to word_freq.txt in the current working directory
    out_path = os.path.join(os.getcwd(), 'word_freq.txt')
    with open(out_path, 'w', encoding='utf-8') as wf:
        for word, count in pairs:
            wf.write(f"{word}\t{count}\n")

    # Preserve original return value
    return vocab_sorted, freqs

# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    # your testing code goes here
    stopwords = get_stopwords("data/stop_words_english.txt")