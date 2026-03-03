import logging
import os
import uuid
import urllib.parse
from dataclasses import dataclass
from datetime import datetime, time

from django.conf import settings
from django.utils import timezone

try:
    import firebase_admin
    from firebase_admin import auth, credentials, firestore, storage
except ImportError:  # pragma: no cover - optional dependency
    firebase_admin = None
    credentials = None
    auth = None
    firestore = None
    storage = None


logger = logging.getLogger(__name__)


@dataclass
class FirebaseSyncResult:
    ok: bool
    transaction_id: str = ""
    document_id: str = ""
    message: str = ""


def _get_firestore_client():
    if not getattr(settings, "FIREBASE_ENABLED", False):
        return None, "Firebase deshabilitado"
    if firebase_admin is None:
        return None, "Dependencia firebase-admin no instalada"

    credentials_file = getattr(settings, "FIREBASE_CREDENTIALS_FILE", "")
    if not credentials_file:
        return None, "FIREBASE_CREDENTIALS_FILE no configurado"
    if not os.path.isabs(credentials_file):
        credentials_file = os.path.join(settings.BASE_DIR, credentials_file)
    if not os.path.exists(credentials_file):
        return None, f"Credenciales Firebase no encontradas: {credentials_file}"

    if not firebase_admin._apps:
        cred = credentials.Certificate(credentials_file)
        options = {}
        project_id = getattr(settings, "FIREBASE_PROJECT_ID", "")
        if project_id:
            options["projectId"] = project_id
        storage_bucket = getattr(settings, "FIREBASE_STORAGE_BUCKET", "")
        if not storage_bucket and project_id:
            storage_bucket = f"{project_id}.appspot.com"
        if storage_bucket:
            options["storageBucket"] = storage_bucket
        firebase_admin.initialize_app(cred, options or None)

    return firestore.client(), ""


def _get_storage_bucket():
    client, error = _get_firestore_client()
    if client is None:
        return None, error
    if storage is None:
        return None, "Dependencia firebase-admin no instalada"
    bucket_name = getattr(settings, "FIREBASE_STORAGE_BUCKET", "")
    if not bucket_name:
        project_id = getattr(settings, "FIREBASE_PROJECT_ID", "")
        if project_id:
            bucket_name = f"{project_id}.appspot.com"
    try:
        return storage.bucket(bucket_name) if bucket_name else storage.bucket(), ""
    except Exception as exc:
        logger.error("Error obteniendo bucket Firebase: %s", exc)
        return None, str(exc)


def _movimiento_timestamp_ms(fecha):
    tz = timezone.get_current_timezone()
    fecha_dt = datetime.combine(fecha, time.min)
    fecha_dt = timezone.make_aware(fecha_dt, tz)
    return int(fecha_dt.timestamp() * 1000)


def _datetime_to_ms(value):
    if value is None:
        return 0
    if isinstance(value, datetime):
        if timezone.is_naive(value):
            value = timezone.make_aware(value, timezone.get_current_timezone())
        return int(value.timestamp() * 1000)
    return 0


def _date_to_ms(value):
    if value is None:
        return 0
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return 0
    tz = timezone.get_current_timezone()
    value_dt = datetime.combine(value, time.min)
    value_dt = timezone.make_aware(value_dt, tz)
    return int(value_dt.timestamp() * 1000)


def _parse_firestore_timestamp(value):
    if not value:
        return None
    tz = timezone.get_current_timezone()
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value) / 1000.0, tz=tz)
    if isinstance(value, datetime):
        return value if timezone.is_aware(value) else timezone.make_aware(value, tz)
    if hasattr(value, "timestamp"):
        try:
            timestamp_value = value.timestamp()
            return datetime.fromtimestamp(float(timestamp_value), tz=tz)
        except Exception:
            return None
    return None


def _estado_por_porcentaje(porcentaje):
    try:
        porcentaje = int(porcentaje)
    except (TypeError, ValueError):
        porcentaje = 0
    if porcentaje >= 100:
        return "completada"
    if porcentaje > 0:
        return "en_progreso"
    return "pendiente"


def _build_transaction_payload(movimiento, actor=None):
    tipo_movimiento = getattr(movimiento, "tipo_movimiento", "gasto")
    transaction_type = "DEPOSIT" if tipo_movimiento == "deposito" else "EXPENSE"
    period = movimiento.fecha.strftime("%Y-%m")

    user_id = getattr(settings, "FIREBASE_CAJA_MENUDA_USER_ID", "")

    user_name = getattr(settings, "FIREBASE_CAJA_MENUDA_USER_NAME", "")
    if not user_name and actor is not None:
        user_name = actor.get_full_name() or actor.username

    coordinator_id = getattr(settings, "FIREBASE_COORDINATOR_ID", "")

    payload = {
        "id": movimiento.firebase_transaction_id or "",
        "type": transaction_type,
        "userId": user_id,
        "userName": user_name,
        "amount": float(movimiento.monto or 0),
        "timestamp": _movimiento_timestamp_ms(movimiento.fecha),
        "receiptUrl": "",
        "invoiceNumber": movimiento.folio or "",
        "expenseType": "OTHER" if transaction_type == "EXPENSE" else None,
        "odometerUrl": "",
        "description": movimiento.descripcion or "Movimiento caja menuda",
        "coordinatorId": coordinator_id,
        "period": period,
        "vehicleId": "",
        "vehicleLabel": "",
        "odometerReadingKm": 0.0,
        "fuelLiters": 0.0,
        "source": "web",
        "sourceId": str(movimiento.id),
    }
    return payload


def _balance_effect(tipo_movimiento, monto):
    if tipo_movimiento == "deposito":
        return float(monto)
    return -float(monto)


def _update_user_balance(client, user_id, delta):
    if not user_id:
        return
    if abs(delta) < 0.0001:
        return

    user_ref = client.collection("users").document(user_id)
    user_doc = user_ref.get()
    if not user_doc.exists:
        return
    current_balance = user_doc.get("balance") or 0.0
    new_balance = float(current_balance) + float(delta)
    user_ref.update({"balance": new_balance})


def sync_caja_menuda_to_firebase(
    movimiento,
    actor=None,
    previous_monto=None,
    previous_tipo=None,
):
    client, error = _get_firestore_client()
    if client is None:
        return FirebaseSyncResult(ok=False, message=error)

    try:
        payload = _build_transaction_payload(movimiento, actor=actor)
        transaction_id = movimiento.firebase_transaction_id or uuid.uuid4().hex
        payload["id"] = transaction_id

        client.collection("transactions").document(transaction_id).set(payload, merge=True)

        user_id = payload.get("userId", "")
        if previous_monto is None or previous_tipo is None:
            delta = _balance_effect(movimiento.tipo_movimiento, movimiento.monto)
        else:
            previous_effect = _balance_effect(previous_tipo, previous_monto)
            new_effect = _balance_effect(movimiento.tipo_movimiento, movimiento.monto)
            delta = new_effect - previous_effect
        _update_user_balance(client, user_id, delta)

        return FirebaseSyncResult(ok=True, transaction_id=transaction_id)
    except Exception as exc:
        logger.error("Error sincronizando caja menuda con Firebase: %s", exc)
        return FirebaseSyncResult(ok=False, message=str(exc))


def fetch_expenses_for_caja_menuda(sort_key="timestamp", sort_order="desc"):
    client, error = _get_firestore_client()
    if client is None:
        return [], error

    try:
        query = (
            client.collection("transactions")
        )
        docs = query.stream()
        expenses = []
        tz = timezone.get_current_timezone()
        for doc in docs:
            data = doc.to_dict() or {}
            transaction_type = data.get("type")
            if transaction_type not in ("EXPENSE", "DEPOSIT"):
                continue
            if data.get("source") == "web":
                continue
            data["id"] = data.get("id") or doc.id
            timestamp_ms = data.get("timestamp")
            if timestamp_ms:
                try:
                    data["timestamp_dt"] = datetime.fromtimestamp(
                        float(timestamp_ms) / 1000.0, tz=tz
                    )
                except Exception:
                    data["timestamp_dt"] = None
            expenses.append(data)
        reverse = str(sort_order).lower() != "asc"
        if sort_key == "userName":
            expenses.sort(key=lambda item: (item.get("userName") or "").lower(), reverse=reverse)
        elif sort_key == "amount":
            expenses.sort(key=lambda item: float(item.get("amount") or 0), reverse=reverse)
        else:
            expenses.sort(key=lambda item: item.get("timestamp", 0), reverse=reverse)
        return expenses, ""
    except Exception as exc:
        logger.error("Error obteniendo gastos desde Firebase: %s", exc)
        return [], str(exc)


def fetch_expense_detail(transaction_id):
    client, error = _get_firestore_client()
    if client is None:
        return None, error

    try:
        doc = client.collection("transactions").document(transaction_id).get()
        if not doc.exists:
            return None, "Gasto no encontrado"
        data = doc.to_dict() or {}
        data["id"] = data.get("id") or doc.id
        tz = timezone.get_current_timezone()
        timestamp_ms = data.get("timestamp")
        if timestamp_ms:
            try:
                data["timestamp_dt"] = datetime.fromtimestamp(
                    float(timestamp_ms) / 1000.0, tz=tz
                )
            except Exception:
                data["timestamp_dt"] = None
        return data, ""
    except Exception as exc:
        logger.error("Error obteniendo gasto desde Firebase: %s", exc)
        return None, str(exc)


def create_firebase_deposit(
    user_id,
    user_name,
    amount,
    transfer_number,
    description,
    receipt_file,
    actor=None,
):
    client, error = _get_firestore_client()
    if client is None:
        return FirebaseSyncResult(ok=False, message=error)
    bucket, bucket_error = _get_storage_bucket()
    if bucket is None:
        return FirebaseSyncResult(ok=False, message=bucket_error)

    try:
        transaction_id = uuid.uuid4().hex
        period = timezone.localtime(timezone.now()).strftime("%Y-%m")
        ext = os.path.splitext(getattr(receipt_file, "name", "") or "")[1].lower()
        if ext not in (".jpg", ".jpeg", ".png", ".pdf"):
            ext = ".jpg"
        storage_path = f"{period}/{user_id}/deposits/{transaction_id}/receipt{ext}"
        blob = bucket.blob(storage_path)
        token = uuid.uuid4().hex
        blob.metadata = {"firebaseStorageDownloadTokens": token}
        receipt_file.seek(0)
        blob.upload_from_file(
            receipt_file,
            content_type=getattr(receipt_file, "content_type", "image/jpeg"),
        )
        encoded_path = urllib.parse.quote(storage_path, safe="")
        receipt_url = (
            f"https://firebasestorage.googleapis.com/v0/b/{bucket.name}/o/{encoded_path}"
            f"?alt=media&token={token}"
        )

        coordinator_id = getattr(settings, "FIREBASE_COORDINATOR_ID", "")
        payload = {
            "id": transaction_id,
            "type": "DEPOSIT",
            "userId": user_id,
            "userName": user_name,
            "amount": float(amount),
            "timestamp": int(timezone.now().timestamp() * 1000),
            "receiptUrl": receipt_url,
            "invoiceNumber": transfer_number,
            "coordinatorId": coordinator_id,
            "description": description,
            "period": period,
            "source": "web_deposit",
        }
        client.collection("transactions").document(transaction_id).set(payload, merge=True)
        _update_user_balance(client, user_id, float(amount))
        return FirebaseSyncResult(ok=True, transaction_id=transaction_id)
    except Exception as exc:
        logger.error("Error creando depósito en Firebase: %s", exc)
        return FirebaseSyncResult(ok=False, message=str(exc))


def _build_bitacora_planificacion_payload(planificacion):
    colaboradores = list(planificacion.colaboradores.all())
    trabajadores_diarios = list(planificacion.trabajadores_diarios.all())
    assigned_emails = [c.email for c in colaboradores if c.email]
    assigned_names = [c.nombre for c in colaboradores] + [t.nombre for t in trabajadores_diarios]
    created_by = planificacion.creado_por.get_full_name() or planificacion.creado_por.username
    proyecto_nombre = planificacion.firebase_project_name or planificacion.proyecto.nombre
    proyecto_id = planificacion.firebase_project_id or str(planificacion.proyecto_id)
    tareas_payload = []
    for tarea in planificacion.tareas.select_related('asignado_a').prefetch_related('subtareas'):
        subtareas_payload = []
        for subtarea in tarea.subtareas.all():
            subtareas_payload.append(
                {
                    "id": subtarea.firebase_id or subtarea.firebase_source_id or str(subtarea.id),
                    "sourceId": subtarea.firebase_source_id or str(subtarea.id),
                    "titulo": subtarea.titulo,
                    "descripcion": subtarea.descripcion or "",
                    "estado": subtarea.estado,
                    "comentario": subtarea.comentario or "",
                    "orden": subtarea.orden,
                    "updatedAtMs": _datetime_to_ms(subtarea.actualizado_en),
                }
            )
        asignado_email = tarea.asignado_a.email if tarea.asignado_a else ""
        asignado_nombre = tarea.asignado_a.nombre if tarea.asignado_a else ""
        tareas_payload.append(
            {
                "id": tarea.firebase_id or tarea.firebase_source_id or str(tarea.id),
                "sourceId": tarea.firebase_source_id or str(tarea.id),
                "titulo": tarea.titulo,
                "descripcion": tarea.descripcion or "",
                "estado": tarea.estado,
                "comentario": tarea.comentario or "",
                "orden": tarea.orden,
                "assignedUserEmail": asignado_email,
                "assignedUserName": asignado_nombre,
                "updatedAtMs": _datetime_to_ms(tarea.actualizado_en),
                "subtareas": subtareas_payload,
            }
        )

    payload = {
        "id": planificacion.firebase_document_id or "",
        "source": "web",
        "sourceId": str(planificacion.id),
        "titulo": planificacion.titulo,
        "descripcion": planificacion.descripcion or "",
        "proyectoId": proyecto_id,
        "proyectoNombre": proyecto_nombre,
        "fechaInicioMs": _date_to_ms(planificacion.fecha_inicio),
        "fechaFinMs": _date_to_ms(planificacion.fecha_fin) if planificacion.fecha_fin else 0,
        "horaInicio": planificacion.hora_inicio.isoformat() if planificacion.hora_inicio else "",
        "horaFin": planificacion.hora_fin.isoformat() if planificacion.hora_fin else "",
        "estado": planificacion.estado,
        "prioridad": planificacion.prioridad,
        "ubicacion": planificacion.ubicacion or "",
        "assignedUserEmails": assigned_emails,
        "assignedUserNames": assigned_names,
        "createdBy": created_by,
        "createdAtMs": _datetime_to_ms(planificacion.creado_en),
        "updatedAtMs": _datetime_to_ms(timezone.now()),
        "tareas": tareas_payload,
    }
    return payload


def fetch_bitacora_proyectos():
    client, error = _get_firestore_client()
    if client is None:
        return [], error

    collection_name = getattr(
        settings, "FIREBASE_BITACORA_PROYECTOS_COLLECTION", "bitacora_proyectos"
    )
    try:
        docs = client.collection(collection_name).stream()
        proyectos = []
        for doc in docs:
            data = doc.to_dict() or {}
            data["id"] = data.get("id") or doc.id
            proyectos.append(data)
        proyectos.sort(key=lambda item: item.get("nombre", "").lower())
        return proyectos, ""
    except Exception as exc:
        logger.error("Error obteniendo proyectos de bitácora desde Firebase: %s", exc)
        return [], str(exc)


def create_bitacora_proyecto(nombre, descripcion, actor=None):
    client, error = _get_firestore_client()
    if client is None:
        return FirebaseSyncResult(ok=False, message=error)

    collection_name = getattr(
        settings, "FIREBASE_BITACORA_PROYECTOS_COLLECTION", "bitacora_proyectos"
    )
    try:
        normalized = nombre.strip()
        if not normalized:
            return FirebaseSyncResult(ok=False, message="Nombre de proyecto requerido")

        existing = (
            client.collection(collection_name)
            .where("nombre_normalizado", "==", normalized.lower())
            .limit(1)
            .stream()
        )
        existing_doc = next(existing, None)
        if existing_doc and existing_doc.exists:
            return FirebaseSyncResult(ok=True, document_id=existing_doc.id)

        document_id = uuid.uuid4().hex
        created_by = ""
        if actor is not None:
            created_by = actor.get_full_name() or actor.username

        payload = {
            "id": document_id,
            "nombre": normalized,
            "descripcion": descripcion or "",
            "nombre_normalizado": normalized.lower(),
            "createdBy": created_by,
            "createdAtMs": _datetime_to_ms(timezone.now()),
            "updatedAtMs": _datetime_to_ms(timezone.now()),
            "source": "web",
        }
        client.collection(collection_name).document(document_id).set(payload, merge=True)
        return FirebaseSyncResult(ok=True, document_id=document_id)
    except Exception as exc:
        logger.error("Error creando proyecto de bitácora en Firebase: %s", exc)
        return FirebaseSyncResult(ok=False, message=str(exc))


def ensure_bitacora_proyecto(nombre, descripcion="", actor=None):
    if not nombre:
        return FirebaseSyncResult(ok=False, message="Nombre de proyecto requerido")
    return create_bitacora_proyecto(nombre, descripcion, actor=actor)


def sync_bitacora_planificacion_to_firebase(planificacion):
    client, error = _get_firestore_client()
    if client is None:
        return FirebaseSyncResult(ok=False, message=error)

    try:
        payload = _build_bitacora_planificacion_payload(planificacion)
        document_id = planificacion.firebase_document_id or uuid.uuid4().hex
        payload["id"] = document_id
        collection_name = getattr(
            settings, "FIREBASE_BITACORA_PLANIFICACIONES_COLLECTION", "bitacora_planificaciones"
        )
        client.collection(collection_name).document(document_id).set(payload, merge=True)
        return FirebaseSyncResult(ok=True, document_id=document_id)
    except Exception as exc:
        logger.error("Error sincronizando bitácora con Firebase: %s", exc)
        return FirebaseSyncResult(ok=False, message=str(exc))


def _build_bitacora_avance_payload(avance):
    planificacion = avance.planificacion
    registered_by = avance.registrado_por.get_full_name() or avance.registrado_por.username
    payload = {
        "id": avance.firebase_document_id or "",
        "planificacionId": planificacion.firebase_document_id or "",
        "planificacionSourceId": str(planificacion.id),
        "descripcion": avance.descripcion,
        "userId": avance.registrado_por_id or "",
        "userName": registered_by,
        "userEmail": avance.registrado_por.email or "",
        "createdAtMs": _datetime_to_ms(avance.fecha_avance),
        "source": "web",
        "updatedAtMs": _datetime_to_ms(timezone.now()),
    }
    return payload


def sync_bitacora_avance_to_firebase(avance):
    client, error = _get_firestore_client()
    if client is None:
        return FirebaseSyncResult(ok=False, message=error)

    try:
        payload = _build_bitacora_avance_payload(avance)
        document_id = avance.firebase_document_id or uuid.uuid4().hex
        payload["id"] = document_id
        collection_name = getattr(
            settings, "FIREBASE_BITACORA_AVANCES_COLLECTION", "bitacora_avances"
        )
        client.collection(collection_name).document(document_id).set(payload, merge=True)
        return FirebaseSyncResult(ok=True, document_id=document_id)
    except Exception as exc:
        logger.error("Error sincronizando avance de bitácora con Firebase: %s", exc)
        return FirebaseSyncResult(ok=False, message=str(exc))


def _build_bitacora_asignacion_payload(asignacion):
    tarea = asignacion.tarea
    subtarea = asignacion.subtarea
    planificacion = asignacion.planificacion
    payload = {
        "id": asignacion.firebase_document_id or "",
        "planificacionId": planificacion.firebase_document_id or "",
        "planificacionSourceId": str(planificacion.id),
        "tareaId": str(tarea.id) if tarea else "",
        "subtareaId": str(subtarea.id) if subtarea else "",
        "tareaTitulo": tarea.titulo if tarea else "",
        "subtareaTitulo": subtarea.titulo if subtarea else "",
        "tecnicoEmail": asignacion.tecnico_email or "",
        "tecnicoNombre": asignacion.tecnico_nombre or "",
        "fecha": asignacion.fecha.isoformat() if asignacion.fecha else "",
        "porcentaje": int(asignacion.porcentaje or 0),
        "estado": asignacion.estado,
        "comentario": asignacion.comentario or "",
        "source": "web",
        "updatedAtMs": _datetime_to_ms(timezone.now()),
    }
    return payload


def sync_bitacora_asignacion_to_firebase(asignacion):
    client, error = _get_firestore_client()
    if client is None:
        return FirebaseSyncResult(ok=False, message=error)

    try:
        payload = _build_bitacora_asignacion_payload(asignacion)
        document_id = asignacion.firebase_document_id or uuid.uuid4().hex
        payload["id"] = document_id
        collection_name = getattr(
            settings, "FIREBASE_BITACORA_ASIGNACIONES_COLLECTION", "bitacora_asignaciones"
        )
        client.collection(collection_name).document(document_id).set(payload, merge=True)
        return FirebaseSyncResult(ok=True, document_id=document_id)
    except Exception as exc:
        logger.error("Error sincronizando asignación de bitácora con Firebase: %s", exc)
        return FirebaseSyncResult(ok=False, message=str(exc))


def _build_bitacora_avance_diario_payload(avance):
    asignacion = avance.asignacion
    planificacion = asignacion.planificacion
    tarea = asignacion.tarea
    subtarea = asignacion.subtarea
    payload = {
        "id": avance.firebase_document_id or "",
        "asignacionId": asignacion.firebase_document_id or "",
        "planificacionId": planificacion.firebase_document_id or "",
        "planificacionSourceId": str(planificacion.id),
        "tareaId": str(tarea.id) if tarea else "",
        "subtareaId": str(subtarea.id) if subtarea else "",
        "fecha": avance.fecha.isoformat() if avance.fecha else "",
        "porcentaje": int(avance.porcentaje or 0),
        "comentario": avance.comentario or "",
        "estado": _estado_por_porcentaje(avance.porcentaje),
        "source": avance.firebase_source or "web",
        "createdAtMs": _datetime_to_ms(avance.creado_en),
        "updatedAtMs": _datetime_to_ms(timezone.now()),
    }
    return payload


def sync_bitacora_avance_diario_to_firebase(avance):
    client, error = _get_firestore_client()
    if client is None:
        return FirebaseSyncResult(ok=False, message=error)

    try:
        payload = _build_bitacora_avance_diario_payload(avance)
        document_id = avance.firebase_document_id or uuid.uuid4().hex
        payload["id"] = document_id
        collection_name = getattr(
            settings, "FIREBASE_BITACORA_AVANCES_DIARIOS_COLLECTION", "bitacora_avances_diarios"
        )
        client.collection(collection_name).document(document_id).set(payload, merge=True)
        return FirebaseSyncResult(ok=True, document_id=document_id)
    except Exception as exc:
        logger.error("Error sincronizando avance diario con Firebase: %s", exc)
        return FirebaseSyncResult(ok=False, message=str(exc))


def sync_bitacora_updates(
    planificacion,
    actor=None,
    sync_avances=True,
    sync_asignaciones=True,
    sync_avances_diarios=True,
):
    from .models import (
        AvancePlanificacion,
        BitacoraAsignacion,
        BitacoraAvanceDiario,
        BitacoraSubtarea,
        BitacoraTarea,
        Colaborador,
    )

    client, error = _get_firestore_client()
    if client is None:
        return FirebaseSyncResult(ok=False, message=error)

    collection_name = getattr(
        settings, "FIREBASE_BITACORA_PLANIFICACIONES_COLLECTION", "bitacora_planificaciones"
    )
    avances_collection = getattr(
        settings, "FIREBASE_BITACORA_AVANCES_COLLECTION", "bitacora_avances"
    )
    asignaciones_collection = getattr(
        settings, "FIREBASE_BITACORA_ASIGNACIONES_COLLECTION", "bitacora_asignaciones"
    )
    avances_diarios_collection = getattr(
        settings, "FIREBASE_BITACORA_AVANCES_DIARIOS_COLLECTION", "bitacora_avances_diarios"
    )
    updated_fields = []

    try:
        doc_snapshot = None
        if planificacion.firebase_document_id:
            doc_snapshot = (
                client.collection(collection_name)
                .document(planificacion.firebase_document_id)
                .get()
            )
        if doc_snapshot is None or not doc_snapshot.exists:
            docs = (
                client.collection(collection_name)
                .where("sourceId", "==", str(planificacion.id))
                .limit(1)
                .stream()
            )
            doc_snapshot = next(docs, None)

        if doc_snapshot and doc_snapshot.exists:
            data = doc_snapshot.to_dict() or {}
            if not planificacion.firebase_document_id:
                planificacion.firebase_document_id = doc_snapshot.id
                updated_fields.append("firebase_document_id")

            firebase_updated_at = _parse_firestore_timestamp(
                data.get("updatedAtMs") or data.get("updatedAt")
            )
            if firebase_updated_at and (
                planificacion.firebase_updated_at is None
                or firebase_updated_at > planificacion.firebase_updated_at
            ):
                nuevo_estado = data.get("estado") or ""
                if nuevo_estado and nuevo_estado != planificacion.estado:
                    planificacion.estado = nuevo_estado
                    updated_fields.append("estado")
                planificacion.firebase_updated_at = firebase_updated_at
                updated_fields.append("firebase_updated_at")

            planificacion.firebase_synced_at = timezone.now()
            updated_fields.append("firebase_synced_at")

        if updated_fields:
            planificacion.save(update_fields=list(set(updated_fields)))

            tareas_data = data.get("tareas") or []
            for tarea_data in tareas_data:
                firebase_id = str(tarea_data.get("id") or "").strip()
                source_id = str(tarea_data.get("sourceId") or "").strip()
                titulo = (tarea_data.get("titulo") or "").strip()
                if not titulo:
                    continue

                tarea = None
                if firebase_id:
                    tarea = BitacoraTarea.objects.filter(
                        planificacion=planificacion, firebase_id=firebase_id
                    ).first()
                if tarea is None and source_id.isdigit():
                    tarea = BitacoraTarea.objects.filter(
                        planificacion=planificacion, id=int(source_id)
                    ).first()
                if tarea is None and source_id:
                    tarea = BitacoraTarea.objects.filter(
                        planificacion=planificacion, firebase_source_id=source_id
                    ).first()

                assigned_email = (tarea_data.get("assignedUserEmail") or "").strip().lower()
                assigned_colab = None
                if assigned_email:
                    assigned_colab = Colaborador.objects.filter(email__iexact=assigned_email).first()

                tarea_values = {
                    "titulo": titulo,
                    "descripcion": tarea_data.get("descripcion") or "",
                    "estado": tarea_data.get("estado") or "pendiente",
                    "comentario": tarea_data.get("comentario") or "",
                    "orden": int(tarea_data.get("orden") or 0),
                    "asignado_a": assigned_colab,
                    "firebase_id": firebase_id,
                    "firebase_source_id": source_id,
                }

                if tarea is None:
                    tarea = BitacoraTarea.objects.create(
                        planificacion=planificacion,
                        creado_por=actor or planificacion.creado_por,
                        **tarea_values,
                    )
                else:
                    for key, value in tarea_values.items():
                        setattr(tarea, key, value)
                    tarea.save()

                subtareas_data = tarea_data.get("subtareas") or []
                for subtarea_data in subtareas_data:
                    sub_firebase_id = str(subtarea_data.get("id") or "").strip()
                    sub_source_id = str(subtarea_data.get("sourceId") or "").strip()
                    sub_titulo = (subtarea_data.get("titulo") or "").strip()
                    if not sub_titulo:
                        continue
                    subtarea = None
                    if sub_firebase_id:
                        subtarea = BitacoraSubtarea.objects.filter(
                            tarea=tarea, firebase_id=sub_firebase_id
                        ).first()
                    if subtarea is None and sub_source_id.isdigit():
                        subtarea = BitacoraSubtarea.objects.filter(
                            tarea=tarea, id=int(sub_source_id)
                        ).first()
                    if subtarea is None and sub_source_id:
                        subtarea = BitacoraSubtarea.objects.filter(
                            tarea=tarea, firebase_source_id=sub_source_id
                        ).first()

                    subtarea_values = {
                        "titulo": sub_titulo,
                        "descripcion": subtarea_data.get("descripcion") or "",
                        "estado": subtarea_data.get("estado") or "pendiente",
                        "comentario": subtarea_data.get("comentario") or "",
                        "orden": int(subtarea_data.get("orden") or 0),
                        "firebase_id": sub_firebase_id,
                        "firebase_source_id": sub_source_id,
                    }

                    if subtarea is None:
                        BitacoraSubtarea.objects.create(tarea=tarea, **subtarea_values)
                    else:
                        for key, value in subtarea_values.items():
                            setattr(subtarea, key, value)
                        subtarea.save()

        if sync_asignaciones:
            asignaciones_docs = (
                client.collection(asignaciones_collection)
                .where("planificacionSourceId", "==", str(planificacion.id))
                .stream()
            )
            for doc in asignaciones_docs:
                if BitacoraAsignacion.objects.filter(firebase_document_id=doc.id).exists():
                    continue
                data = doc.to_dict() or {}
                fecha_str = data.get("fecha") or ""
                try:
                    fecha_val = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                except Exception:
                    fecha_val = timezone.localdate()

                tecnico_email = (data.get("tecnicoEmail") or "").strip().lower()
                tecnico_nombre = data.get("tecnicoNombre") or tecnico_email
                colaborador = None
                if tecnico_email:
                    colaborador = Colaborador.objects.filter(email__iexact=tecnico_email).first()

                tarea = None
                subtarea = None
                tarea_id = data.get("tareaId") or ""
                subtarea_id = data.get("subtareaId") or ""
                if subtarea_id:
                    subtarea = BitacoraSubtarea.objects.filter(id=subtarea_id).first()
                if tarea_id:
                    tarea = BitacoraTarea.objects.filter(id=tarea_id).first()

                porcentaje_val = int(data.get("porcentaje") or 0)
                asignacion = BitacoraAsignacion.objects.create(
                    planificacion=planificacion,
                    tarea=tarea,
                    subtarea=subtarea,
                    colaborador=colaborador,
                    tecnico_email=tecnico_email,
                    tecnico_nombre=tecnico_nombre,
                    fecha=fecha_val,
                    porcentaje=porcentaje_val,
                    estado=data.get("estado") or _estado_por_porcentaje(porcentaje_val),
                    comentario=data.get("comentario") or "",
                    creado_por=actor or planificacion.creado_por,
                    firebase_document_id=doc.id,
                    firebase_synced_at=timezone.now(),
                )
                asignacion.save()

        if sync_avances_diarios:
            avances_diarios_docs = (
                client.collection(avances_diarios_collection)
                .where("planificacionSourceId", "==", str(planificacion.id))
                .stream()
            )
            for doc in avances_diarios_docs:
                if BitacoraAvanceDiario.objects.filter(firebase_document_id=doc.id).exists():
                    continue
                data = doc.to_dict() or {}
                asignacion_id = data.get("asignacionId") or ""
                asignacion = None
                if asignacion_id:
                    asignacion = BitacoraAsignacion.objects.filter(firebase_document_id=asignacion_id).first()
                if asignacion is None:
                    continue
                fecha_str = data.get("fecha") or ""
                try:
                    fecha_val = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                except Exception:
                    fecha_val = timezone.localdate()
                porcentaje_val = int(data.get("porcentaje") or 0)
                avance = BitacoraAvanceDiario.objects.create(
                    asignacion=asignacion,
                    fecha=fecha_val,
                    porcentaje=porcentaje_val,
                    comentario=data.get("comentario") or "",
                    registrado_por=actor or planificacion.creado_por,
                    firebase_document_id=doc.id,
                    firebase_source="mobile",
                    firebase_synced_at=timezone.now(),
                )
                avance.save()

                asignacion.porcentaje = porcentaje_val
                asignacion.comentario = avance.comentario
                asignacion.actualizar_estado_porcentaje()
                asignacion.save(update_fields=["porcentaje", "comentario", "estado"])

                if asignacion.porcentaje < 100:
                    siguiente_fecha = asignacion.fecha + timezone.timedelta(days=1)
                    existente = BitacoraAsignacion.objects.filter(
                        asignacion_origen=asignacion,
                        fecha=siguiente_fecha,
                    ).exists()
                    if not existente:
                        BitacoraAsignacion.objects.create(
                            planificacion=asignacion.planificacion,
                            tarea=asignacion.tarea,
                            subtarea=asignacion.subtarea,
                            colaborador=asignacion.colaborador,
                            tecnico_email=asignacion.tecnico_email,
                            tecnico_nombre=asignacion.tecnico_nombre,
                            fecha=siguiente_fecha,
                            porcentaje=asignacion.porcentaje,
                            estado=asignacion.estado,
                            comentario="",
                            asignacion_origen=asignacion,
                            creado_por=actor or planificacion.creado_por,
                        )

        if sync_avances:
            avances_docs = (
                client.collection(avances_collection)
                .where("planificacionSourceId", "==", str(planificacion.id))
                .stream()
            )

            for doc in avances_docs:
                if AvancePlanificacion.objects.filter(firebase_document_id=doc.id).exists():
                    continue
                data = doc.to_dict() or {}
                descripcion = (data.get("descripcion") or data.get("comentario") or "").strip()
                if not descripcion:
                    continue
                fecha_avance = _parse_firestore_timestamp(
                    data.get("createdAtMs") or data.get("createdAt")
                ) or timezone.localtime(timezone.now())
                avance = AvancePlanificacion.objects.create(
                    planificacion=planificacion,
                    descripcion=descripcion,
                    fecha_avance=fecha_avance,
                    registrado_por=actor or planificacion.creado_por,
                    firebase_document_id=doc.id,
                    firebase_source="mobile",
                    firebase_user_id=str(data.get("userId") or ""),
                    firebase_user_name=str(data.get("userName") or ""),
                    firebase_user_email=str(data.get("userEmail") or ""),
                )
                avance.firebase_synced_at = timezone.now()
                avance.save(update_fields=["firebase_synced_at"])

        return FirebaseSyncResult(ok=True)
    except Exception as exc:
        logger.error("Error sincronizando bitácora desde Firebase: %s", exc)
        return FirebaseSyncResult(ok=False, message=str(exc))


def fetch_firestore_collection_docs(collection_name, limit=None, include_drafts=False):
    client, error = _get_firestore_client()
    if client is None:
        return [], error

    try:
        query = client.collection(collection_name)
        if limit:
            query = query.limit(limit)
        docs = query.stream()
        items = []
        for doc in docs:
            data = doc.to_dict() or {}
            if not include_drafts and data.get("isDraft") is True:
                continue
            items.append({"id": doc.id, "data": data})
        return items, ""
    except Exception as exc:
        logger.error("Error obteniendo documentos de Firebase: %s", exc)
        return [], str(exc)


def fetch_firestore_document(collection_name, document_id):
    client, error = _get_firestore_client()
    if client is None:
        return None, error

    try:
        doc = client.collection(collection_name).document(document_id).get()
        if not doc.exists:
            return None, "Documento no encontrado"
        data = doc.to_dict() or {}
        return {"id": doc.id, "data": data}, ""
    except Exception as exc:
        logger.error("Error obteniendo documento de Firebase: %s", exc)
        return None, str(exc)


def fetch_firebase_team_leaders():
    docs, error = fetch_firestore_collection_docs("users")
    if error:
        return [], error
    leaders = []
    for doc in docs:
        data = doc.get("data", {}) or {}
        if data.get("role") != "TEAM_LEADER":
            continue
        leaders.append({
            "id": doc.get("id"),
            "name": data.get("name") or "",
            "email": data.get("email") or "",
            "balance": data.get("balance") or 0,
        })
    leaders.sort(key=lambda item: (item.get("name") or "").lower())
    return leaders, ""


def fetch_firebase_transactions_for_user(user_id, start_ms=None, end_ms=None):
    client, error = _get_firestore_client()
    if client is None:
        return [], error
    try:
        query = client.collection("transactions").where("userId", "==", user_id)
        docs = query.stream()
        items = []
        tz = timezone.get_current_timezone()
        for doc in docs:
            data = doc.to_dict() or {}
            if data.get("type") not in ("DEPOSIT", "EXPENSE"):
                continue
            timestamp_ms = data.get("timestamp") or 0
            if start_ms and timestamp_ms < start_ms:
                continue
            if end_ms and timestamp_ms > end_ms:
                continue
            data["id"] = data.get("id") or doc.id
            if timestamp_ms:
                try:
                    data["timestamp_dt"] = datetime.fromtimestamp(
                        float(timestamp_ms) / 1000.0, tz=tz
                    )
                except Exception:
                    data["timestamp_dt"] = None
            items.append(data)
        items.sort(key=lambda item: item.get("timestamp", 0))
        return items, ""
    except Exception as exc:
        logger.error("Error obteniendo transacciones de Firebase: %s", exc)
        return [], str(exc)


def fetch_firebase_cuadres(user_id=None, limit=20):
    client, error = _get_firestore_client()
    if client is None:
        return [], error
    try:
        query = client.collection("cuadres")
        if user_id:
            query = query.where("userId", "==", user_id)
        docs = query.stream()
        items = []
        tz = timezone.get_current_timezone()
        for doc in docs:
            data = doc.to_dict() or {}
            data["id"] = data.get("id") or doc.id
            start_ms = data.get("startMs")
            end_ms = data.get("endMs")
            created_ms = data.get("createdAtMs")
            if start_ms:
                try:
                    data["start_dt"] = datetime.fromtimestamp(float(start_ms) / 1000.0, tz=tz)
                except Exception:
                    data["start_dt"] = None
            if end_ms:
                try:
                    data["end_dt"] = datetime.fromtimestamp(float(end_ms) / 1000.0, tz=tz)
                except Exception:
                    data["end_dt"] = None
            if created_ms:
                try:
                    data["created_dt"] = datetime.fromtimestamp(float(created_ms) / 1000.0, tz=tz)
                except Exception:
                    data["created_dt"] = None
            items.append(data)
        items.sort(key=lambda item: item.get("endMs", 0), reverse=True)
        return items[:limit], ""
    except Exception as exc:
        logger.error("Error obteniendo cuadres de Firebase: %s", exc)
        return [], str(exc)


def create_firebase_cuadre(
    user_id,
    user_name,
    start_ms,
    end_ms,
    ingresos,
    egresos,
    balance,
    status,
    created_by,
):
    client, error = _get_firestore_client()
    if client is None:
        return FirebaseSyncResult(ok=False, message=error)
    try:
        cuadre_id = uuid.uuid4().hex
        payload = {
            "id": cuadre_id,
            "userId": user_id,
            "userName": user_name,
            "startMs": int(start_ms),
            "endMs": int(end_ms),
            "ingresos": float(ingresos),
            "egresos": float(egresos),
            "balance": float(balance),
            "status": status,
            "carryover": float(balance),
            "nextCycleStartMs": int(end_ms) + 1,
            "createdAtMs": int(timezone.now().timestamp() * 1000),
            "createdBy": created_by,
            "source": "web",
        }
        client.collection("cuadres").document(cuadre_id).set(payload, merge=True)
        return FirebaseSyncResult(ok=True, document_id=cuadre_id)
    except Exception as exc:
        logger.error("Error creando cuadre en Firebase: %s", exc)
        return FirebaseSyncResult(ok=False, message=str(exc))


def fetch_firebase_auth_emails():
    client, error = _get_firestore_client()
    if client is None:
        return set(), error
    if auth is None:
        return set(), "Dependencia firebase-admin no instalada"

    try:
        emails = set()
        for user in auth.list_users().iterate_all():
            if user.email:
                emails.add(user.email.strip().lower())
        return emails, ""
    except Exception as exc:
        logger.error("Error obteniendo usuarios de Firebase Auth: %s", exc)
        return set(), str(exc)

