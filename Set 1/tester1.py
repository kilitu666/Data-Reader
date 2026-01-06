from typing import Dict

def mark_str_to_dict(mark_str: str) -> Dict[str, int | float]:
    """
    Comment:
        Convert a string representation of marks into a dictionary.

    Args:
        mark_str (str): A string containing comma-separated key:value pairs.

    Returns:
        Dict[str, int | float]: A dictionary representation of the marks.
    """
    result = {}
    items = mark_str.split(',')

    for grade in items:  # e.g., "A1: 99"
        key, value = grade.split(':')   # split into key and value
        key = key.strip() # remove leading/trailing whitespace
    
        num = float(value.strip()) # parse value to float
        result[key] = int(num) if num.is_integer() else num # store as int if whole number, else float
    return result


def fix_invalid_value(mark: int | float) -> int | float:
    """Fix invalid mark values.

    Args:
        mark (int | float): The original mark value.

    Returns:
        The fixed mark value:
        - If the mark is between 0 and 100 (inclusive), return it unchanged.
        - If the mark is less than 0 or greater than 100, return negative infinity.
    """
    if 0 <= mark <= 100: # valid range
        return mark 
    else:
        return float('-inf') 


def mark_str_to_dict_revised(mark_str: str) -> Dict[str, int | float]:
    """Convert a string representation of marks into a dictionary with validity checks.

    Args:
        mark_str (str): A string containing comma-separated key:value pairs.

    Returns:
        Dict[str, int | float]: A dictionary representation of the marks with invalid values fixed.
    """
    result = {}
    items = mark_str.split(',')
    for grade in items:
        key, value = grade.split(':')
        key = key.strip()
        num = float(value.strip())
        fixed = fix_invalid_value(num)
        is_finite = fixed != float('inf') and fixed != float('-inf')
        if is_finite and fixed == int(fixed):
            result[key] = int(fixed)
        else:
            result[key] = fixed
    return result


def process_multiple_students_marks(mark_dict: Dict[str, str]) -> Dict[str, Dict[str, int | float]]:
    """Process marks for multiple students.

    Args:
        mark_dict (Dict[str, str]): A dictionary where keys are student names and values are their marks as strings.

    Returns:
        Dict[str, Dict[str, int | float]]: A dictionary mapping student names to their processed marks dictionaries.
    """
    result = {}
    for student, marks in mark_dict.items(): # e.g., "Jueqing": "A1: 99, A2: 200, A3: -100" 
        result[student] = mark_str_to_dict_revised(marks) # process each student's marks
    return result


def summarize_marks(marks: Dict[str, Dict], split: str) -> dict:
    """Summarize the marks for a specific subject.

    Args:
        marks (Dict[str, Dict]): A dictionary mapping student names to their marks.
        split (str): The subject to summarize (e.g., "A1").

    Returns:
        dict: A summary of the marks for the specified subject.
    """

    total = 0.0
    valid_count = 0
    invalid_count = 0

    if not marks:
        return {"average_mark": float('-inf'), "invalid_count": 0, "valid_count": 0}

    for record in marks.values():
        if not isinstance(record, dict):
            invalid_count += 1
            continue

        if split not in record:
            invalid_count += 1
            continue

        value = record[split]
        is_finite = value != float('inf') and value != float('-inf')
        if isinstance(value, (int, float)) and is_finite:
            total += float(value)
            valid_count += 1
        else:
            invalid_count += 1

    if valid_count == 0:
        average = float('-inf')
    else:
        avg = total / valid_count
        average = int(avg) if avg == int(avg) else avg

    return {"average_mark": average, "invalid_count": invalid_count, "valid_count": valid_count}


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    # Your testing code goes here
    m = {
        "Jueqing": "A1: 99, A2: 200, A3: -100",
        "Trang"  : "A1: 300, A2: 100, A3: 100"
    }
    res = process_multiple_students_marks(m)
    print(res)