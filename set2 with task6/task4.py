# copy your task4 code here
from typing import Tuple, List, Optional
import os


def get_stopwords(stopwords_file: str) -> List[str]:
    """
    Read stop words from a file and return them as a list.

    Args:
        stopwords_file (str): The path to the stop words file.

    Returns:
        List[str]: A list of stop words.
    """
    words = []
    with open(stopwords_file, 'r', encoding='utf-8') as f:
        for line in f:
            w = line.strip().lower() # Convert to lowercase for case insensitivity
            if w: # Avoid adding empty lines
                words.append(w) 
    return words
   



def get_vocabs(text: str, stopwords: List) -> Tuple[Tuple[str], Tuple[int]] | Tuple[()]:
    """
    Get vocabulary and their counts from the text, excluding stop words.
    
    Args:
        text (str): The input text.
        stopwords (List): A list of stop words to exclude.
        
    Returns:
        Tuple[Tuple[str], Tuple[int]] | Tuple[()]: A tuple containing:
            - A tuple of unique words sorted alphabetically.
            - A tuple of counts corresponding to each unique word.
        Returns an empty tuple if no valid words are found.
    
    """
    tokens = []
    current = "" 
    for ch in text: # Iterate through each character in the text
        if ch.isdigit() or ch.isalpha(): # Check if the character is alphanumeric
            current += ch.lower() 
        else:
            if current: # If we have a current token, add it to the list
                tokens.append(current.lower())
                current = ""
    if current: # Add the last token if exists
        tokens.append(current.lower())

    sw = set(stopwords) # Convert stopwords list to a set(non-repetition) for faster lookup
    filtered = []
    for t in tokens:
        if not t.isalpha(): # Filter out non-alphabetic tokens
            continue
        if len(t) < 2: # Filter out tokens shorter than 2 characters
            continue
        if t in sw: # Filter out stop words
            continue
        filtered.append(t)
        
    if not filtered: # If no valid words remain after filtering, return empty tuple
        return tuple() 
    
    counts = {}
    for w in filtered: # Count occurrences of each word
        counts[w] = counts.get(w, 0) + 1
    
    vocab_sorted = tuple(sorted(counts.keys()))
    freqs = tuple(counts[w] for w in vocab_sorted)
    
    return vocab_sorted, freqs


def process_mini_dataset(
        stop_words: List[str],
        data_path: str = 'data',
        category: Optional[str] = None,
    ):
    """Process a mini dataset of text files.

    Args:
        stop_words (List[str]): A list of stop words to exclude.
        data_path (str, optional): The path to the data directory. Defaults to 'data'.
        category (Optional[str], optional): The specific category to process. Defaults to None.

    Returns:
        None
    """
    texts = []
    if category: #process a specific category
        root_path = os.path.join(data_path, category)  # construct the path to the category directory
        if not os.path.exists(root_path): # check if the directory exists, if not, return empty tuple
            return tuple()
        search_dirs = [root_path] 
    elif not os.path.isdir(data_path):
        return tuple()
    search_dirs = [os.path.join(data_path, d) for d in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, d))] 

    for folder in search_dirs:  # Iterate through each folder in the search directories
        for fname in os.listdir(folder):
            fpath = os.path.join(folder, fname)
            if os.path.isfile(fpath) and fname.endswith('.txt'):
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    texts.append(content)
    if not texts:  # If no valid texts were found, return empty tuple
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
