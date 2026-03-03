import json
from google.cloud.firestore_v1 import DocumentSnapshot
from google.cloud.firestore_v1 import DocumentReference
from google.cloud.firestore_v1 import GeoPoint
from google.protobuf.timestamp_pb2 import Timestamp as ProtoTimestamp
from datetime import datetime
from firebase_config import init_firestore

# Conversor para tipos especiales
def firestore_to_json_compatible(obj):
    if isinstance(obj, GeoPoint):
        return {"_type": "GeoPoint", "lat": obj.latitude, "lng": obj.longitude}
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, DocumentReference):
        return {"_type": "DocumentReference", "path": obj.path}
    elif isinstance(obj, DocumentSnapshot):
        return obj.to_dict()
    elif isinstance(obj, ProtoTimestamp):
        return obj.ToDatetime().isoformat()
    elif isinstance(obj, bytes):
        return obj.decode("utf-8", errors="ignore")
    raise TypeError(f"Tipo no serializable: {type(obj)}")

def export_document_to_json(collection_name, document_id, output_file):
    db = init_firestore()
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()

    if doc.exists:
        data = doc.to_dict()
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False, default=firestore_to_json_compatible)
        print(f"✅ Documento exportado correctamente a {output_file}")
    else:
        print(f"❌ El documento '{document_id}' no existe en la colección '{collection_name}'.")

# Ejecutar
if __name__ == "__main__":
    export_document_to_json(
        collection_name="mantenimientos/2025AbrilChepi/Preventive",
        document_id="8hzKbsJD6mHtHVYYtoat",
        output_file="Corrective_exportado.json"
    )
