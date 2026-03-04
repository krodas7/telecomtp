import firebase_admin
from firebase_admin import credentials, firestore
import os

def init_firestore():
    """Inicializar Firestore con credenciales de servicio"""
    # Solo inicializar si no está ya inicializado
    if not firebase_admin._apps:
        # Verificar que el archivo existe
        if not os.path.exists('firebase-credentials.json'):
            raise FileNotFoundError("No se encontró el archivo 'firebase-credentials.json'")
        
        # Crear credenciales
        cred = credentials.Certificate('firebase-credentials.json')
        
        # Inicializar con configuración
        # Nota: databaseURL no es necesaria para Firestore, solo para Realtime Database
        # Removida para evitar confusión con proyecto incorrecto
        firebase_admin.initialize_app(cred)
    
    # Retornar cliente de Firestore
    return firestore.client()

def init_firestore_with_auth(user_token):
    """Inicializar Firestore con autenticación de usuario"""
    # Esta función se puede implementar para usar tokens de usuario
    # Por ahora, usamos el método tradicional
    return init_firestore()

