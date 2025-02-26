class ProgressModel:
    """
    Progress model for storing user game progress.
    """
    def __init__(self, level=1, wordlist=None, life=10, difficulty="easy"):
        self.level = level
        self.wordlist = wordlist if wordlist is not None else []
        self.life = life
        self.difficulty = difficulty

    def to_dict(self):
        """
        Convert the progress model to a dictionary that can be saved to the database.
        """
        return {
            "level": self.level,
            "wordlist": self.wordlist,
            "life": self.life,
            "difficulty": self.difficulty,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a ProgressModel instance from a dictionary.
        """
        return cls(
            level=data.get("level", 1),
            wordlist=data.get("wordlist", []),
            life=data.get("life", 10),
            difficulty=data.get("difficulty", "easy")
        )
