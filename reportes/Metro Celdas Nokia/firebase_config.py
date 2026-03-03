import firebase_admin
from firebase_admin import credentials, firestore

def init_firestore():
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase-key.json")  # ← Ajusta esta ruta
        firebase_admin.initialize_app(cred)
    return firestore.client()

