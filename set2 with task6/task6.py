from task4 import get_stopwords, get_vocabs
from task5 import (
    load_word_freq, load_word2idx, load_idx2word,
    save_word_freq, save_word2idx, save_idx2word   
)
import os

def extract_vocab(stopwords_path: str, files):
    """Read text from one or more files and extract vocabulary using stopwords.
    Args:
    - stopwords_path: path to a stopwords file (one word per line)
    - files: str or iterable of str (file paths to read)
    Returns: 
            (words_tuple, freqs_tuple) or tuple() if nothing extracted
    """
    # Normalise files to list[str]
    if isinstance(files, str):
        files = [files]
    else:
        files = list(files)

    # Load stopwords
    try:
        sw = get_stopwords(stopwords_path)
    except Exception:
        sw = []

    
    texts = []
    for fp in files:  # Iterate through each file path
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                texts.append(f.read())
        except Exception:
            # Skip unreadable/missing files
            continue

    if not texts:
        return tuple()

    all_text = "\n".join(texts)
    return get_vocabs(all_text, sw)

def updating_for_adding(
        stopwords_path: str,
        added_files: str | list,
        in_path: str,
        out_path: str
    ):
    """
    Update vocabulary by adding words from new files.

    Args:
        stopwords_path (str): Path to the stopwords file.
        added_files (str | list): A single file path or a list of file paths to
        in_path (str): Directory path containing existing vocabulary files.
        out_path (str): Directory path to save updated vocabulary files.
        
    Returns: None
    """
    # Load existing data
    wf_path_in = os.path.join(in_path, "word_freq.txt")
    w2i_path_in = os.path.join(in_path, "word2idx.txt")
    i2w_path_in = os.path.join(in_path, "idx2word.txt")

    try:
        curr_wf = load_word_freq(wf_path_in)
    except Exception:
        curr_wf = {}
    try:
        curr_w2i = load_word2idx(w2i_path_in)
    except Exception:
        curr_w2i = {}
    try:
        curr_i2w = load_idx2word(i2w_path_in)
    except Exception:
        curr_i2w = {}
    # manually parse existing word_freq.txt if available and dict is empty
    if not curr_wf and os.path.isfile(wf_path_in):
        try:
            with open(wf_path_in, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) != 2: 
                        continue
                    w, c = parts[0], parts[1] 
                    try:
                        curr_wf[w] = int(c)
                    except ValueError:
                        continue
        except Exception:
            pass

    # Normalise added_files to list if it's a single string, else return as list
    files = [added_files] if isinstance(added_files, str) else list(added_files)
    result = extract_vocab(stopwords_path, files)
    if not result:
        new_words, new_freqs = (), ()
    else:
        new_words, new_freqs = result

    # Merge new words and frequencies into current word frequency dictionary
    for w, c in zip(new_words, new_freqs):
        curr_wf[w] = int(curr_wf.get(w, 0)) + int(c)
        
    os.makedirs(out_path, exist_ok=True) # Ensure output directory exists
    wf_path_out = os.path.join(out_path, "word_freq.txt")
    
    pairs = list(curr_wf.items())
    pairs.sort(key=lambda kv: -int(kv[1])) # Sort the 2nd value from high to low
    
    with open(wf_path_out, 'w', encoding='utf-8') as f:
        for w, cnt in pairs:
            f.write(f"{w} {cnt}\n")

    words_sorted = sorted(curr_wf.keys()) 
    w2i_path_out = os.path.join(out_path, "word2idx.txt")
    i2w_path_out = os.path.join(out_path, "idx2word.txt")
    with open(w2i_path_out, 'w', encoding='utf-8') as f:
        for idx, w in enumerate(words_sorted):
            f.write(f"{w} {idx}\n")
    with open(i2w_path_out, 'w', encoding='utf-8') as f:
        for idx, w in enumerate(words_sorted):
            f.write(f"{idx} {w}\n")




def updating_for_deleting(
        stopwords_path: str,
        excluded_files: str | list,
        in_path: str,
        out_path: str
    ):
    """
    Update vocabulary by removing words from excluded files.

    Args:
        stopwords_path (str): Path to the stopwords file.
        excluded_files (str | list): A single file path or a list of file paths to
        in_path (str): Directory path containing existing vocabulary files.
        out_path (str): Directory path to save updated vocabulary files.

    Returns: None
    """
    # Load existing data
    wf_path_in = os.path.join(in_path, "word_freq.txt")
    w2i_path_in = os.path.join(in_path, "word2idx.txt")
    i2w_path_in = os.path.join(in_path, "idx2word.txt")
    
    try:
        curr_wf = load_word_freq(wf_path_in)
    except Exception:
        curr_wf = {}
    try:
        curr_w2i = load_word2idx(w2i_path_in)
    except Exception:
        curr_w2i = {}
    try:
        curr_i2w = load_idx2word(i2w_path_in)
    except Exception:
        curr_i2w = {}
   
    if (not curr_wf) and os.path.isfile(wf_path_in): 
        try:
            with open(wf_path_in, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) != 2:
                        continue
                    w, c = parts[0], parts[1]
                    try:
                        curr_wf[w] = int(c)
                    except ValueError:
                        continue
        except Exception:
            pass
    
    # Normalise excluded_files to list if it's a single string, else return as list
    files = [excluded_files] if isinstance(excluded_files, str) else list(excluded_files)

    # Extract vocabulary from excluded files
    del_words, del_freqs = extract_vocab(stopwords_path, files)

    # Merge deleted words and frequencies into current word frequency dictionary
    for w, c in zip(del_words, del_freqs):
        if w in curr_wf:
            curr_wf[w] = int(curr_wf[w]) - int(c)
            if curr_wf[w] <= 0:
                del curr_wf[w]
    
    os.makedirs(out_path, exist_ok=True)
    
    wf_path_out = os.path.join(out_path, "word_freq.txt")
    
    save_word_freq(tuple(curr_wf.keys()),
                    tuple(curr_wf[w] for w in curr_wf.keys()), 
                    wf_path_out)
    
    save_idx2word(tuple(curr_wf.keys()), os.path.join(out_path, "idx2word.txt"))
    save_word2idx(tuple(curr_wf.keys()), os.path.join(out_path, "word2idx.txt"))
    
    
    pairs = list(curr_wf.items())
    pairs.sort(key=lambda kv: -int(kv[1])) # Sort the 2nd value from high to low

    with open(wf_path_out, 'w', encoding='utf-8') as f:
        for w, cnt in pairs:
            f.write(f"{w} {cnt}\n")

