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
            difficulty="easy",
    ):
        # uuid will be created in create()
        self._id = id
        self._username = username
        self._password = password
        self.progress = ProgressModel(level, wordlist, life, difficulty)

    def _to_dict(self):
        return {
            "id": self._id,
            "username": self._username,
            "password": self._password,
            "level": self.progress.level,
            "wordlist": self.progress.wordlist,
            "life": self.progress.life,
            "difficulty": self.progress.difficulty,
        }

    ## ---------------- GET Methods ---------------- ##
    def get_id(self):
        return self._id

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password  # ⚠️ 实际使用时密码不应直接暴露

    def get_level(self):
        return self.progress.level

    def get_wordlist(self):
        return self.progress.wordlist

    def get_life(self):
        return self.progress.life

    def get_difficulty(self):
        return self.progress.difficulty

    ## ---------------- SET Methods ---------------- ##
    def set_id(self, id):
        self._id = id

    def set_username(self, username):
        self._username = username

    def set_password(self, password):
        self._password = password  # ⚠️ 密码最好哈希存储

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

    def set_difficulty(self, difficulty):
        if difficulty not in ["easy", "medium", "hard"]:
            raise ValueError("Invalid difficulty level")
        self.progress.difficulty = difficulty

    def create(self):
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
        if db_ref.child('users').child(self._username).get():
            raise KeyError("Current Username is already existed")

        self._id = generate_uuid()

        db_ref.child('users').child(self._username).set(self._to_dict())

        # Store user's game progress using ProgressModel
        db_ref.child('game_progress').child(self._username).set(self.progress.to_dict())

    def save(self):
        """
        Update the user information and save it to firebase
        """
        updated_data = self._to_dict()
        db_ref.update(updated_data)

    def login(self):
        user_data = db_ref.child('users').child(self._username).get()

        if not user_data:
            raise KeyError('Username does not exist')

        if user_data.get("password") != self._password:
            raise KeyError("Incorrect password")

        self._id = user_data.get("id")

        progress_data = db_ref.child('game_progress').child(self._username).get()
        if progress_data:
            self.progress = ProgressModel.from_dict(progress_data)

    def save_progress(self, data):
        try:
            if not isinstance(data, dict):
                raise TypeError("Progress data must be a dictionary.")

            level = data.get('level')
            wordlist = data.get('wordlist')
            life = data.get('life')
            difficulty = data.get('difficulty')

            # Check if any required fields are missing
            if level is None or wordlist is None or life is None or difficulty is None:
                raise ValueError(
                    "Missing required progress data: level, wordlist, life, and difficulty must all be provided.")

            # Validate data types
            if not isinstance(level, int) or level < 1:
                raise ValueError("Level must be a positive integer.")
            if not isinstance(wordlist, list):
                raise TypeError("Wordlist must be a list.")
            if not isinstance(life, int) or life < 0:
                raise ValueError("Life must be a non-negative integer.")
            if difficulty not in ["easy", "medium", "hard"]:
                raise ValueError("Invalid difficulty level. Choose from 'easy', 'medium', or 'hard'.")

            # Retrieve user data
            user_data = db_ref.child('users').child(self._username).get()

            if not user_data:
                raise KeyError("User does not exist.")

            # Prepare progress data
            progress = {
                "level": level,
                "wordlist": wordlist,
                "life": life,
                "difficulty": difficulty,
            }

            # Save progress data to Firebase
            db_ref.child('game_progress').child(self._username).set(progress)
            return {"success": True, "message": "Progress saved successfully."}

        except (TypeError, ValueError, KeyError) as e:
            return {"success": False, "error": str(e)}

        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}