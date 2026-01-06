from typing import Tuple, List


def get_vocabs_simple(text: str) -> Tuple[Tuple[str], Tuple[int]]:
    """Get vocabulary and their counts from the text.

    Args:
        text (str): The input text.

    Returns:
        Tuple[Tuple[str], Tuple[int]]: A tuple containing:
            - A tuple of unique words sorted alphabetically.
            - A tuple of counts corresponding to each unique word.
    """
    #define common punctuation marks
    punctuation = ".,!?';:"
    #replace punctuation marks with spaces
    for p in punctuation:
        text = text.replace(p, ' ')
    #obtain the list by splitting the text by spaces
    words = text.split()
    #return empty tuple if no words
    if not words:
        return ()
    #otherwise， returns two tuples: one with unique words sorted alphabetically, the other with their counts
    return (tuple(sorted(set(words))), tuple(words.count(word) for word in sorted(set(words))))

    
    


def get_vocabs(text: str) -> Tuple[Tuple[str], Tuple[int]]:
    """
    Get vocabulary and their counts from the text.

    Args:
        text (str): The input text.

    Returns:
        Tuple[Tuple[str], Tuple[int]]: A tuple containing:
            - A tuple of unique words sorted alphabetically.
            - A tuple of counts corresponding to each unique word.
    """

    text = text.lower()
    
    punctuation = ".,!?';:" #define common punctuation marks
    for p in punctuation:
        text = text.replace(p, ' ')

    words = text.split()

    word_counts = {}
    # if the word is already in the dictionary, increment its count; otherwise, add it with a count of 1
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
 
    sorted_words = tuple(sorted(word_counts.keys()))
    #create a tuple of counts corresponding to each word in sorted order
    counts = tuple(word_counts[word] for word in sorted_words)
    if not words:
        return ()
    return (sorted_words, counts)
        

# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    the_example_str = "Hello, apple?! 'You you', yOU, heLLo, I've, At, apPle."
    the_word_list, the_count_list = get_vocabs(the_example_str)
    print(f"the_word_list = {the_word_list}")   
    print(f"the_count_list = {the_count_list}")