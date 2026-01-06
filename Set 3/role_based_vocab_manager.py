import pandas as pd
import json
from typing import Dict


class TextProcessor:
    """ 
    A class to process text data, build vocabulary, and manage word-frequency mappings. 
    """
    def __init__(
        self,
        stopwords_filepath: str,
        corpus_filepath: str,
        idx2label_filepath: str
        ) -> None:
        """Initialize the TextProcessor with file paths for stopwords, corpus, and label mapping.

        Args:
            stopwords_filepath (str): Path to the stopwords file.
            corpus_filepath (str): Path to the corpus file.
            idx2label_filepath (str): Path to the index-to-label mapping file.
        Returns:
            None
        """
        # Initialize attributes
        self.word_freq: Dict[str, int] = {}
        self.word2idx: Dict[str, int] = {}
        self.idx2word: Dict[int, str] = {}
        
        # Load stopwords
        self.stopwords = []
        with open(stopwords_filepath, 'r') as f:
            for line in f.readlines():
                w = line.strip().lower()
                if w:
                    self.stopwords.append(w)
        # Load idx2label mapping
        with open(idx2label_filepath, 'r') as f:
            self.idx2label = json.load(f)
        # Load corpus and add label names using idx2label
        df = pd.read_csv(corpus_filepath)
        df["label_name"] = df["label"].map(self.idx2label)
        self.corpus = df

        # Build vocabulary from the corpus
        all_text = " ".join(self.corpus["text"].astype(str))
        self.build_vocab(all_text)

    def clean_text(self, text: str) -> list[str]:
        """" 
        Clean the input string by applying preprocessing rules.
        
        Rules: 
            1. Convert to lowercase.
            2. Remove punctuation.
            3. Remove stopwords.
            4. Discard words with length < 2 or containing non-alphabetic characters.
            
        Args:
            text (str): The input text to be cleaned.
        Returns:
            list[str]: A list of cleaned words."""
        text = text.lower()
        #define common punctuation marks
        punctuation = ".,!?';:\"()[]{}#%&*/\\-=_+<>$"
        #replace punctuation marks with spaces
        for p in punctuation:
            text = text.replace(p, ' ')
        #obtain the list by splitting the text by spaces
        words = text.split()
        cleaned_words = []
        for word in words:
            #remove stopwords from the list
            if word in self.stopwords:
                continue
            #discard words with length less than 2
            if len(word) < 2:
                continue
            #discard words with non-alphabetic characters
            if not word.isalpha():
               continue
            cleaned_words.append(word)
        return cleaned_words
                
    def build_vocab(self, text: str) -> None:
        """ 
        Build vocabulary(self.word_freq, self.word2idx, self.idx2word) from the given text.
        Args:   
            text (str): The input text to build vocabulary from.
        Returns:
            None
        """
        # Initialize word frequency dictionary avoid counting from previous data(add_file)
        self.word_freq = {}
        words = self.clean_text(text)
        # Count word frequencies
        for word in words:
            if word in self.word_freq:
                self.word_freq[word] += 1
            else:
                self.word_freq[word] = 1
        # Create word2idx and idx2word mappings
        sorted_words = sorted(self.word_freq.keys())
        self.word2idx = {word: idx for idx, word in enumerate(sorted_words)}
        self.idx2word = {idx: word for word, idx in self.word2idx.items()}



    def add_file(self, add_file_path: str) -> None:
        """ Add a new text file to the corpus, update the vocabulary and mappings accordingly.
        Args:
            add_file_path (str): The path to the text file to be added.
        Returns:
            None
        """
        df = pd.read_csv(add_file_path)
        df["label_name"] = df["label"].map(self.idx2label)
        # Concat the new data to the existing corpus
        self.corpus = pd.concat([self.corpus, df], ignore_index=True)
        # Rebuild vocabulary with the updated corpus
        all_text = " ".join(self.corpus["text"].astype(str))
        self.build_vocab(all_text)
        self.save()

    def delete_file(self, delete_file_path) -> None:
        """
        Delete a file to the corpus, update the vocabulary and mappings accordingly.
        Args:
            delete_file_path (str): The path to the text file to be deleted.
        Returns:
            None
        """
        df_to_delete = pd.read_csv(delete_file_path)
        df_to_delete["label_name"] = df_to_delete["label"].map(self.idx2label)

        # Left join corpus with df_to_delete to find rows to remove;
        # indicator=True adds a special column "_merge" to show the source of each row
        merged = self.corpus.merge(
            df_to_delete[['label', 'text']],
            on=['label', 'text'],
            how='left',
            indicator=True)
        # Keep only rows that are in corpus but not in df_to_delete
        self.corpus = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])
        # Rebuild vocabulary with the updated corpus
        all_text = " ".join(self.corpus["text"].astype(str))
        self.build_vocab(all_text)
        self.save()

    def load(self) -> None:
        """ 
        Load vocabulary from the saved files (word_freq.txt, word2idx.txt, idx2word.txt).
        Returns:
            None"""
        self.word_freq = {}
        with open("word_freq.txt", 'r', encoding='utf-8') as f:
            for line in f.readlines():
                word, freq = line.strip().split(",")
                self.word_freq[word] = int(freq)
        # Load word2idx file
        self.word2idx = {}
        with open("word2idx.txt", 'r', encoding='utf-8') as f:
            for line in f.readlines():
                word, idx = line.strip().split(",")
                self.word2idx[word] = int(idx)
        # Load idx2word file
        self.idx2word = {}
        with open("idx2word.txt", 'r', encoding='utf-8') as f:
            for line in f.readlines():
                idx, word = line.strip().split(",")
                self.idx2word[int(idx)] = word
        

    def save(self) -> None:
        """ 
        Save the current vocabulary to files (word_freq.txt, word2idx.txt, idx2word.txt).
        Returns:
            None"""
        # Save word-frequency file
        with open("word_freq.txt", 'w', encoding='utf-8') as f:
            sorted_freq = sorted(self.word_freq.items(), key=lambda item: (-item[1], item[0]))
            for word, freq in sorted_freq:
                f.write(f"{word},{freq}\n")
        # Save word to index file
        with open("word2idx.txt", 'w', encoding='utf-8') as f:
            for word, idx in sorted(self.word2idx.items()):
                f.write(f"{word},{idx}\n")
        # Save index to word file
        with open("idx2word.txt", 'w', encoding='utf-8') as f:
            for idx, word in sorted(self.idx2word.items()):
                f.write(f"{idx},{word}\n")


if __name__ == "__main__":
    
    tp = TextProcessor(
        stopwords_filepath="data/stop_words_english.txt",
        corpus_filepath="data/ag_news_test.csv",
        idx2label_filepath="data/idx2label.json",
    )