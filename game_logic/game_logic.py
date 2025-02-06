import random
import json


class TypeGame:
    def __init__(self, db_ref):
        self.db_ref = db_ref
        self.current_level = 1
        self.max_level = 4
        self.words_per_level = 5
        self.current_word_index = 0
        self.input_progress = ''  # Stores user's current input progress
        self.word_list = []

    def load_words_for_current_level(self):
        """
        Fetch a random set of words for the current level from Firebase.
        """
        try:
            path = f"levels/level{self.current_level}/words"
            words = self.db_ref.child(path).get()

            if not words:
                raise ValueError(f"No words available for Level {self.current_level}.")

            self.word_list = random.sample(words, min(self.words_per_level, len(words)))
            self.current_word_index = 0
            self.input_progress = ''
            print(f"Words loaded for Level {self.current_level}: {self.word_list}")

        except (ValueError, Exception) as e:
            print(f"Error loading words: {e}")
            raise

    def process_user_input(self, user_input):
        """
        Process the user's input for the current word.
        """
        print(f"User Input: {user_input}")
        print(f"Current Word: {self.word_list[self.current_word_index]}")
        print(f"Current Progress: {self.input_progress}")

        current_word = self.word_list[self.current_word_index]

        if current_word.startswith(self.input_progress + user_input):
            self.input_progress += user_input

            if self.input_progress == current_word:
                self.current_word_index += 1
                self.input_progress = ''

                if self.current_word_index >= self.words_per_level:
                    return self.advance_level()

            return {"next_level": False, "next_char": True, "victory": False}

        return {"next_level": False, "next_char": False, "victory": False}

    def advance_level(self):
        """
        Move to the next level or declare victory if the game is complete.
        """
        self.current_level += 1
        self.current_word_index = 0

        if self.current_level > self.max_level:
            print("Game Completed!")
            return {"victory": True}

        print(f"Welcome to Level {self.current_level}!")
        self.load_words_for_current_level()
        return {"word_list": self.word_list, "next_level": True, "victory": False}

    def start_game(self):
        """
        Initialize the game by loading the first level.
        """
        self.load_words_for_current_level()
