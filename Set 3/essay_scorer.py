from task7 import TextProcessor
import math

class EssayScorer:
    def __init__(self, text_processor):
        """Initialize the EssayScorer with a TextProcessor instance.

        Args:
            text_processor (TextProcessor): An instance of the TextProcessor class.
            self: The instance of the EssayScorer class.
        Returns:
            None
        """
        self.tp = text_processor

    def _clean_keep_stopwords(self, text: str) -> list:
        """Clean the input text while retaining stopwords.
        Args:
            text (str): The input text to be cleaned.
        Returns:
            list: A list of cleaned tokens.
        """
        # Lowercase the text
        text = text.lower()
        punctuation = ".,!?';:\"()[]{}#%&*/\\-=_+<>$"
        for p in punctuation:
            text = text.replace(p, " ")
        words = text.split()
        filtered = []
        # Filtering tokens with the given criteria
        for w in words:
            if len(w) < 2:
                continue
            if w.isdigit():
                continue
            if not w.isalpha():
                continue
            filtered.append(w)
        return filtered

    def _length_score(self, L:int) -> float:
        """Calculate the length score of the essay.

        Args:
            L (int): The length of the essay in words.

        Returns:
            float: The length score of the essay.
        
        """
        if 300 <= L <= 500:
            return 10.0
        diff = 300 - L if L < 300 else L - 500
        score = 10.0 - (diff / 20.0)  # diff=276 -> -13.8
        return max(0.0, score)
    
    def _topic_words(self, problem_statement: str) -> list[str]:
        """Extract topic words from the problem statement by removing stopwords.
        Args:
            problem_statement (str): The problem statement or essay prompt.
        Returns:
            list: A list of topic words extracted from the problem statement.
        """
        toks = self._clean_keep_stopwords(problem_statement)
        stop = set(self.tp.stopwords)
        return [t for t in toks if t not in stop]  

    def _relevance_score(self, topic_words: list[str], essay_tokens: list[str]) -> float:
        """Calculate the relevance score of the essay based on topic words.

        Args:
            topic_words (list[str]): A list of topic words extracted from the problem statement.
            essay_tokens (list[str]): A list of tokens from the essay.

        Returns:
            float: The relevance score of the essay.
        """
        if not topic_words: 
            return 0.0
        denom = 3 * len(topic_words)
        if denom == 0:
            return 0.0
        freq = {}
        for t in essay_tokens:
            freq[t] = freq.get(t, 0) + 1
        capped_sum = 0
        for tw in topic_words:
            capped_sum += min(3, freq.get(tw, 0))
        return 40.0 * capped_sum / denom 
    
    def _rarity_points(self, word: str) -> int:
        """"Assign rarity points to a word based on its frequency in the corpus.
        Args:
            word (str): The word for which to assign rarity points.
            Returns:
            int: The rarity points assigned to the word.
        Returns: -1 if the word is not found in the corpus.
        5 points for frequency 1
        """
        f = self.tp.word_freq.get(word, 0)
        if f == 0:
            return -1
        if 1 <= f <= 3:
            return 5
        if 4 <= f <= 20:
            return 4
        if 21 <= f <= 50:
            return 3
        if 51 <= f <= 100:
            return 2
        return 1

    def _rarity_score(self, essay_tokens_no_stop: list[str]) -> float:
        """Calculate the rarity score of the essay based on unique words.

        Args:
            essay_tokens_no_stop (list[str]): A list of tokens from the essay without stopwords.

        Returns:
            float: The rarity score of the essay.

        """
        if not essay_tokens_no_stop:
            return 0.0
        uniq = set(essay_tokens_no_stop)
        U = len(uniq)
        if U == 0:
            return 0.0
        total_pts = sum(self._rarity_points(w) for w in uniq)
        score = 30.0 * total_pts / (3.0 * U)
        return min(30.0, max(0.0, score))

    def _variety_score(self, essay_tokens_no_stop: list[str]) -> float:
        """Calculate the variety score of the essay based on unique words.
        Args:
            essay_tokens_no_stop (list[str]): A list of tokens from the essay without stopwords
        Returns:
            float: The variety score of the essay.
        """
        L = len(essay_tokens_no_stop)
        if L == 0:
            return 0.0
        U = len(set(essay_tokens_no_stop))
        return 20.0 * math.sqrt(U / L)

    def _filler_penalty(self, essay_tokens: list[str]) -> float:
        """Calculate the filler penalty of the essay based on filler words.

        Args:
            essay_tokens (list[str]): A list of tokens from the essay.

        Returns:
            float: The filler penalty of the essay.
        """
        if not essay_tokens:
            return 0.0
        stop = set(self.tp.stopwords)
        stops = sum(1 for t in essay_tokens if t in stop)
        return -10.0 if stops / len(essay_tokens) >= 0.5 else 0

    def score_essay(self, prob_statement, file_path):
        """
        Score the essay based on the given problem statement and essay file path.
        Args:
            prob_statement (str): The problem statement or essay prompt.
            file_path (str): The path to the essay text file.
        Returns:
            dict: A dictionary containing individual scores and the total score.    
        """
        # Read and process the essay
        with open(file_path, "r", encoding="utf-8") as f:
            essay_raw = f.read()
        essay_tokens = self._clean_keep_stopwords(essay_raw)

        # Remove stopwords for certain calculations
        stop = set(self.tp.stopwords)
        essay_no_stop = [t for t in essay_tokens if t not in stop]

        # The topic words from the problem statement
        topics = self._topic_words(prob_statement)

        # Four scoring components and one penalty
        length_mark = self._length_score(len(essay_tokens))
        relevance   = self._relevance_score(topics, essay_tokens)
        rarity      = self._rarity_score(essay_no_stop)
        variety     = self._variety_score(essay_no_stop)
        penalty     = self._filler_penalty(essay_tokens)

        # Return the scores in a dictionary two decimal places
        result = {
            'length':    round(max(0.0, length_mark), 2),
            'relevance': round(max(0.0, relevance),   2),
            'rarity':    round(max(0.0, rarity),      2),
            'variety':   round(max(0.0, variety),     2),
            'penalty':   round(penalty,               2),
        }
        total = result['length'] + result['relevance'] + result['rarity'] + result['variety'] + result['penalty']
        result['total_score'] = round(max(0.0, total), 2)
        return result
        

if __name__ == "__main__":
    tp = TextProcessor(
        stopwords_filepath="data/stop_words_english.txt",
        corpus_filepath="data/ag_news_test.csv",
        idx2label_filepath="data/idx2label.json",
    )
    scorer = EssayScorer(tp)
    prob_statement = "The impact of technology on education."
    score = scorer.score_essay(prob_statement, "/home/sample_essay.txt")
    print(score)
