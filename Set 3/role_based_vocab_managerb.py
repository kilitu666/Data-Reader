from typing import Optional
import os
from task7 import TextProcessor


class Role:
    """
    Defines the role of a user, including their username, access level, and display name.

    Attributes:
        user_name (str): The login username of the user.
        access (str): The access level of the user, either "admin" or "reader".
        name (str): The display name of the user.
    """
    def __init__(self, user_name: str, access: str, name: str):
        self.user_name = user_name
        self.access = access  # 'admin' or 'reader'
        self.name = name
    
    def get_user_name(self):
        return self.user_name
    
    def get_access(self):
        return self.access

    def get_name(self):
        return self.name


class RoleBasedVocabSys:
    """
    A role-based vocabulary management system that allows users to log in, view vocabulary statistics, and
    for administrators to update the vocabulary by adding or deleting text files.
    """
    def __init__(
        self,
        users_info,
        stopwords_filepath = "data/stop_words_english.txt",
        corpus_filepath = "data/ag_news_test.csv",
        idx2label_filepath = "data/idx2label.json"
        ):
        
        # The provided users information    
        self.users_info = users_info

        self.text_processor = TextProcessor(
            stopwords_filepath = stopwords_filepath,
            corpus_filepath = corpus_filepath,
            idx2label_filepath = idx2label_filepath)
        
        # The current logged-in user information (None if no user is logged in)
        self.current_user : Optional[Role] = None


    def prompt_existing_path(self) -> str:
        """
        Prompt the user to input a valid file path until a correct one is provided.

        Returns:
            str: The valid file path entered by the user.
        """
        while True:
            path = input("Enter the file path: ").strip()
            if os.path.exists(path):
                return path
            continue

    def update_vocab_add(self):
        """
        Admin functionality: Add a new file to the corpus and update the vocabulary.
        """
        path = self.prompt_existing_path()
        self.text_processor.add_file(path)  
        print("done.")

    def update_vocab_delete(self):
        """
        Admin functionality: Delete a file from the corpus and update the vocabulary.
        """
        path = self.prompt_existing_path()
        self.text_processor.delete_file(path) 
        print("done.")

    def top_10_frequency(self):
        """
        Display the top 10 most frequent vocabulary words with their counts.
        """
        sorted_vocab = sorted(self.text_processor.word_freq.items(), 
                              key=lambda item: (-item[1], item[0]))
        top_10 = sorted_vocab[:10]
        print("========================================")
        for word, freq in top_10:
            print(f"{word} {freq}")
        print("========================================")
        print("[  Omit the menu... ]")

    def last_10_frequency(self):
        """
        Display the 10 least frequent vocabulary words with their counts.
        """
        bottom_vocab = sorted(self.text_processor.word_freq.items(), 
                              key=lambda item: (item[1], item[0]))
        last_10 = bottom_vocab[:10]
        print("========================================")
        for word, freq in last_10:
            print(f"{word} {freq}")
        print("========================================")
        print("[  Omit the menu... ]")

    def start(self):
        """
        Start the system, print the welcome message, and launch the user interaction loop.
        """
        print("Welcome to the Mark system v0.0!")
        menu = self.generate_menu()
        print(menu)
        self.get_user_choice()
          
    def generate_menu(self) -> str:
        """
        Generate the menu string based on the current login state.

        Returns:
            str: The menu options string to display.
        """
        # Non-logged-in user menu
        if self.current_user is None:
            return "Please Login:\n 1. Exit\n 2.Login\n"
        # Logged-in user menu
        else:
            header = f"Welcome {self.current_user.get_name()}\n Please choose one option below:\n"
            base_menu = [
                "1:Exit",
                "2:Logout/Re-Login",
                "3:Show top 10 frequency vocabularies",
                "4:Show last 10 frequency vocabularies"]
            if self.current_user.get_access() == "admin":
                base_menu.append("5:Updating Vocabulary for adding")
                base_menu.append("6:Updating Vocabulary for excluding")
            return f"========================================\n{header}\n" + "\n".join(base_menu) + "\n"
        
    
    def verify_user_choice(self, user_choice) -> bool:
        """
        Verify and process the user's menu choice.

        Args:
            user_choice (int): The menu option chosen by the user.

        Returns:
            bool: True if the system should exit, False otherwise.
        """
        if self.current_user is None:
            if user_choice == 1:
                print("Exiting the system. Goodbye!")
                return True
            elif user_choice == 2:
                self.login()
                return False
        else:
            if user_choice == 1:
                print("Exiting the system. Goodbye!")
                return True
            elif user_choice == 2:
                self.current_user = None
                self.login()
                return False
            elif user_choice == 3:
                self.top_10_frequency()
                return False
            elif user_choice == 4:
                self.last_10_frequency()
                return False    
            elif user_choice == 5 and self.current_user.get_access() == "admin":
                self.update_vocab_add()
                return False
            if user_choice == 6 and self.current_user.get_access() == "admin":
                self.update_vocab_delete()
                return False
            else:
                print("Invalid choice. Please try again.")
                return False

    
    def get_user_choice(self):
        """
        Continuously prompt the user for menu choices until the user decides to exit.
        """
        while True:
            menu = self.generate_menu()
            print(menu)
            try:
                user_choice = int(input("Enter your choice: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if self.verify_user_choice(user_choice):
                break
            
    
    def login(self):
        """
        Prompt the user to log in with username and password (case-insensitive username).

        Returns:
            bool: True if login is successful, False otherwise.
        """
        account_name = input("Please key your account name: ").strip()
        password = input("Please key your password: ").strip()
        if not account_name or not password:
            return False

    # Case-insensitive username match
        matched_key = None
        for k in self.users_info.keys():
            if k.lower() == account_name.lower():
                matched_key = k
                break

        if matched_key is None:
            print("Incorrect username or password!")
            return False

        user_data = self.users_info[matched_key]
        if password == user_data["password"]:
            self.current_user = Role(
                user_name=matched_key,
                access=user_data["role"],
                name=user_data["name"])
            return True
        else:
            print("Incorrect username or password!")
            return False

if __name__ == "__main__":
    users_info = {
        "Jueqing": {
            "role": "reader",
            "password": "jueqing123",
            "name": "Jueqing Lu"
        },
        "Trang": {
            "role": "admin",
            "password": "trang123",
            "name": "Trang Vu"
        },
        "land": {
            "role": "admin",
            "password": "landu123",
            "name": "Lan Du"
        }
        
    }
    a_sys = RoleBasedVocabSys(users_info)
    a_sys.start()