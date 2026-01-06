# copy your codes from task 1 to here if necessary
from typing import Dict

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

def process_multiple_students_marks(mark_dict: Dict[str, str]) -> Dict[str, Dict[str, int | float]]:
    """Process marks for multiple students.

    Args:
        mark_dict (Dict[str, str]): A dictionary where keys are student names and values are their marks as strings.

    Returns:
        Dict[str, Dict[str, int | float]]: A dictionary mapping student names to their processed marks dictionaries.
    """
    result = {}
    for student, marks in mark_dict.items(): # e.g., "Jueqing": "A1: 99, A2: 200, A3: -100" 
        result[student] = mark_str_to_dict_revised(marks)
    return result

def mark_str_to_dict_revised(mark_str: str) -> Dict[str, int | float]:
    """Convert a string representation of marks into a dictionary with validity checks.

    Args:
        mark_str (str): A string containing comma-separated key:value pairs.

    Returns:
        Dict[str, int | float]: A dictionary representation of the marks with invalid values fixed.
    """
    result = {}
    items = mark_str.split(',')
    for grade in items: # define each grade, e.g., "A1: 99"
        key, value = grade.split(':')
        key = key.strip()
        num = float(value.strip())
        fixed = fix_invalid_value(num)
        is_finite = fixed != float('inf') and fixed != float('-inf')
        if is_finite and fixed == int(fixed): # integer value
            result[key] = int(fixed)
        else:
            result[key] = fixed
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

    if not marks: # empty input case
        return {"average_mark": float('-inf'), "invalid_count": 0, "valid_count": 0}

    for record in marks.values():  # iterate through each student's marks
        if not isinstance(record, dict):
            invalid_count += 1
            continue

        if split not in record:
            invalid_count += 1
            continue

        value = record[split]
        is_finite = value != float('inf') and value != float('-inf')
        if isinstance(value, (int, float)) and is_finite:   # valid mark
            total += float(value)
            valid_count += 1
        else:
            invalid_count += 1

    if valid_count == 0: # no valid marks case
        average = float('-inf')
    else: # compute average
        avg = total / valid_count
        average = int(avg) if avg == int(avg) else avg

    return {"average_mark": average, "invalid_count": invalid_count, "valid_count": valid_count}

#Task 2    
def after_login(user_info, mark_unprocessed, user_name):
    """ This is menu after login (correct user_name and password).
    args:
        user_info: a dictionary containing user names and passwords
        mark_unprocessed: a dictionary containing user names and their unprocessed marks
    
    returns:
        None
    """
    while True:
        print("==================================")
        keys = list(user_info.keys())
        username = keys[0]
        print(f"Welcome {username}")
        print("Please choose one option below:")
        print("1.Exit")
        print("2.Re-Login")
        print("3.Show mark records")
        print("4.Show summarization")
        logged_choice=input("Your choice (number only): ")
        # choose exit, stop loop
        if logged_choice == "1":
            print("==================================")
            print("See u!")
            return
        # Re-login means go back main menu again and stop loop
        elif logged_choice == "2":
            print("You have logged off successfully!")
            main(user_info, mark_unprocessed)(user_info, mark_unprocessed)
            return
        # Show mark records and continue the loop
        elif logged_choice == "3":
            print("==================================")
            print("Results:")
            #use function process_multiple_students_marks(mark_dict)to produce the marks of each student in each assignment
            for student, marks in process_multiple_students_marks(mark_unprocessed).items():
                print(f"{student}:")
                for assignment, mark in marks.items():
                    print(f"  {assignment}: {mark}")
        # Show summarisation and continue the loop
        elif logged_choice == "4":
            print("==================================")
            print("Available Assignments: {'A3', 'A2', 'A1'}")
            assignment_choice = input("The Assignment you want to check (e.g., A1): ")
            if assignment_choice == "A1":
                summary = summarize_marks(process_multiple_students_marks(mark_unprocessed), assignment_choice)
                print(f"Summary for {assignment_choice}:")
                print(f"  Average Mark: {summary['average_mark']}")
                print(f"  Valid Count: {summary['valid_count']}")
                print(f"  Invalid Count: {summary['invalid_count']}")
            if assignment_choice == "A2":
                summary = summarize_marks(process_multiple_students_marks(mark_unprocessed), assignment_choice)
                print(f"Summary for {assignment_choice}:")
                print(f"  Average Mark: {summary['average_mark']}")
                print(f"  Valid Count: {summary['valid_count']}")
                print(f"  Invalid Count: {summary['invalid_count']}")
            if assignment_choice == "A3":
                summary = summarize_marks(process_multiple_students_marks(mark_unprocessed), assignment_choice)
                print(f"Summary for {assignment_choice}:")
                print(f"  Average Mark: {summary['average_mark']}")
                print(f"  Valid Count: {summary['valid_count']}")
                print(f"  Invalid Count: {summary['invalid_count']}")



def main(user_info, mark_unprocessed):
    """ Show the main menu at the first.
    args:       
        user_info: a dictionary containing user names and passwords
        mark_unprocessed: a dictionary containing user names and their unprocessed marks
    returns:
        None
    """
    # start the main menu loop:
    while True:
        print("==================================")
        print("Welcome to the Mark system v0.0!")
        print("Please Login:")
        print("1.Exit")
        print("2.Login")
        login_choice=input("Your choice (number only): ")
        # choose exit, stop loop
        if login_choice == "1":
            print("==================================")
            print("See u!")
            return
        # choose login, input name and password.
        elif login_choice == "2":
            print("==================================")
            user_name=input("Please key your account name: ").strip()
            password=input("Please key your password: ").strip()
            # if name and passsword all are correct, prepare to get in to another page and stop loop. 
            for real_name, real_pass in user_info.items():
                if real_name.lower() == user_name.lower() and real_pass == password:
                    print("Login successful!")
                    after_login(user_info, mark_unprocessed, user_name)
                    return
            # if name or password isn't correct, continue loop.
            else:
                print("==================================")
                print("Incorrect username or password!")

    


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if __name__ == "__main__":
    user_info = {
        "Jueqing": "Jueqing123"
    }
    mark_unprocessed = {
        "Jueqing": "A1: 99, A2: 200, A3: -100",
        "Trang"  : "A1: 300, A2: 100, A3: 100"
    }
    main(user_info, mark_unprocessed)