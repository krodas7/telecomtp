import os
import firebase_admin
from firebase_admin import credentials, firestore

# Ruta absoluta a la clave para que funcione desde cualquier directorio de ejecución
_DIR = os.path.dirname(os.path.abspath(__file__))
_KEY_PATH = os.path.join(_DIR, "firebase-key.json")


def init_firestore():
    if not firebase_admin._apps:
        if not os.path.exists(_KEY_PATH):
            raise FileNotFoundError(
                f"No se encontró el archivo de credenciales: {_KEY_PATH}\n"
                "Descarga la clave de cuenta de servicio desde Firebase Console y guárdala como firebase-key.json"
            )
        cred = credentials.Certificate(_KEY_PATH)
        firebase_admin.initialize_app(cred)
    return firestore.client()
