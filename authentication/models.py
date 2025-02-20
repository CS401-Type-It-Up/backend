from datetime import datetime

from authentication.util import generate_uuid
from config.db import db_ref

class GameUser:
    """
    Game User Object
    """
    def __init__(
        self,
        id         = "",
        username   = "",
        password   = "",
        email      = "",
        created_at = ""
    ):
        self._id         = id
        self._username   = username
        self._password   = password
        self._email      = email
        self._created_at = created_at
        
        if not self._id:
            self._id = generate_uuid()
            
        if not self._created_at:
            current_time = datetime.now()
            self._created_at = current_time.strftime("%H:%M:%S")
    
    def _to_dict(self):
        return {
            "id"        : self._id,
            "username"  : self._username,
            "password"  : self._password,
            "email"     : self._email,
            "created_at": self._created_at
        }

    def set_email(self, email):
        self._email = email
    
    def get_email(self):
        return self._email
    
    def get_username(self):
        return self._username
    
    def get_password(self):
        return self._password
    
    def get_id(self):
        return self._id
    
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
        if self._email and db_ref.child('users').order_by_child("email").equal_to(self._email).get():
            raise KeyError("Current Email is already existed")
        
        new_user = self._to_dict()
        db_ref.child('users').child(self._username).set(new_user)
    
    def save(self):
        """
        Update the user information and save it to firebase
        """
        updated_data = self._to_dict()
        db_ref.update(updated_data)