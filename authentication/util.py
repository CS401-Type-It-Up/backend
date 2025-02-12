import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import firestore

def Fetch_from_Firebase(key):
    cred = credentials.Certificate("../config/firebase_key.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://typeitup-928b9-default-rtdb.firebaseio.com/'})
    irestore_db = firestore.client()

    db_ref = db.reference(key)

    return db_ref