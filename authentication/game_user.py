import random

from authentication.models import ProgressModel
from authentication.util import generate_uuid
from config.db import db_ref


class GameUser:
    """
    Game User Object
    """

    def __init__(
            self,
            id="",
            username="",
            password="",
            level=1,
            wordlist=None,
            life=10,
    ):
        # uuid will be created in create()
        self.id = id
        self.username = username
        self.password = password
        self.progress = ProgressModel(level, wordlist, life)

    def _to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
        }

    ## ---------------- GET Methods ---------------- ##
    def get_id(self):
        return self.id

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password  # ⚠️ 实际使用时密码不应直接暴露

    def get_level(self):
        return self.progress.level

    def get_wordlist(self):
        return self.progress.wordlist

    def get_life(self):
        return self.progress.life

    ## ---------------- SET Methods ---------------- ##
    def set_id(self, id):
        self.id = id

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password  # ⚠️ 密码最好哈希存储

    def set_level(self, level):
        if level < 1:
            raise ValueError("Level cannot be less than 1")
        self.progress.level = level

    def set_wordlist(self, wordlist):
        if not isinstance(wordlist, list):
            raise TypeError("Wordlist must be a list")
        self.progress.wordlist = wordlist

    def set_life(self, life):
        if life < 0:
            raise ValueError("Life cannot be negative")
        self.progress.life = life

    def create(self, num):
        """
        Create a "new user to the firebase" based on the information provided
        Username, password and ID is required
        Email is not required but will be checked if provided
        created_at is auto filled

        Raises:
            ValueError: Username or Password cannot be empty
            KeyError: Current Username is already existed
            KeyError: Current Email is already existed
        """
        if db_ref.child('users').child(self.username).get():
            raise KeyError("Current Username is already existed")

        self.id = generate_uuid()
        db_ref.child('users').child(self.username).set(self._to_dict())

        # Store user's game progress using ProgressModel
        words = db_ref.child(f"wordlists/level{self.progress.level}").get()

        if not words:
            raise KeyError(f"No words found for level {self.progress.level}.")

        # Randomly sample words from the wordlist
        selected_words = random.sample(words, min(num, len(words)))
        self.progress.wordlist = selected_words
        print(f"Initialize user with wordlist: {self.progress.wordlist}")

        # Store the progress in Firebase, saving the word indexes
        progress_data = self.progress.to_dict()
        db_ref.child('game_progress').child(self.username).set(progress_data)

    def login(self):
        user_data = db_ref.child('users').child(self.username).get()

        if not user_data:
            raise KeyError('Username does not exist')

        if user_data.get("password") != self.password:
            raise KeyError("Incorrect password")

        self.id = user_data.get("id")

        progress_data = db_ref.child('game_progress').child(self.username).get()
        if progress_data:
            self.progress = ProgressModel.from_dict(progress_data)

    def save_progress(self, data):
        life = data.get('life')
        word_index = data.get('word_index')
        char_index = data.get('char_index')

        # Check if 'life' is provided
        if life is None or word_index is None or char_index is None:
            raise ValueError("Missing required progress data: 'life', 'word_index', and 'char_index' must all be "
                             "provided.")

        # Validate data types
        if not isinstance(life, int) or life < 0:
            raise ValueError("Life must be a non-negative integer.")
        if not isinstance(word_index, int) or word_index < 0:
            raise ValueError("word_index must be a positive integer.")
        if not isinstance(char_index, int) or char_index < 0:
            raise ValueError("char_index must be a positive integer.")

        # Retrieve user data
        user_data = db_ref.child('users').child(self.username).get()

        if not user_data:
            raise KeyError("User does not exist.")

        # Prepare progress data for updating
        progress = {
            "life": life,
            "word_index": word_index,
            "char_index": char_index
        }

        # Update only the 'life' attribute in the game progress in Firebase
        db_ref.child('game_progress').child(self.username).update(progress)

        return {"success": True, "message": "Progress updated successfully."}