import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import firestore

cred = credentials.Certificate("../config/firebase_key.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://typeitup-928b9-default-rtdb.firebaseio.com/'})
firestore_db = firestore.client()

ref = db.reference( f"levels/level1/words")
data = ref.get()
