import firebase_admin
from firebase_admin import credentials, db

def Fetch_from_Firebase(key):
    cred = credentials.Certificate("config/firebase_key.json")
    # firebase_admin.initialize_app(cred, {'databaseURL': 'https://typeitup-928b9-default-rtdb.firebaseio.com/'})
    db_ref = db.reference(key)

    return db_ref