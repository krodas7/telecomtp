import importlib.util
import logging
import os
import sys
import tempfile

from django.conf import settings

logger = logging.getLogger(__name__)

REPORT_PDF_CONFIG = {
    "routers_nokia": {
        "module_path": os.path.join(
            settings.BASE_DIR,
            "reportes",
            "Routers Nokia Tigo",
            "exportar_reportes.py",
        ),
        "function": "generar_pdf_routers_tigo",
    },
    "enlaces_ericsson": {
        "module_path": os.path.join(
            settings.BASE_DIR,
            "reportes",
            "Enlaces Ericsson Tigo",
            "generar_reporte_ericsson.py",
        ),
        "function": "generar_pdf_ericsson",
    },
    "ran_setar": {
        "module_path": os.path.join(
            settings.BASE_DIR,
            "reportes",
            "Radiobases n78 Nokia",
            "generar_reporte_nokia.py",
        ),
        "function": "generar_pdf_nokia",
    },
    "metro_celdas": {
        "module_path": os.path.join(
            settings.BASE_DIR,
            "reportes",
            "Metro Celdas Nokia",
            "generar_reporte_nokia_metrocell.py",
        ),
        "function": "generar_pdf_nokia_metrocell",
    },
}

_MODULE_CACHE = {}


def _load_report_module(tipo, module_path):
    if tipo in _MODULE_CACHE:
        return _MODULE_CACHE[tipo]

    if not os.path.exists(module_path):
        raise FileNotFoundError(f"Modulo de exportacion no encontrado: {module_path}")

    module_dir = os.path.dirname(module_path)
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)

    spec = importlib.util.spec_from_file_location(f"reportes_{tipo}", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"No se pudo cargar el modulo {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _MODULE_CACHE[tipo] = module
    return module


def generar_pdf_reporte(tipo, doc_id, data):
    config = REPORT_PDF_CONFIG.get(tipo)
    if not config:
        return None, "Tipo de reporte no soportado para PDF"

    try:
        module = _load_report_module(tipo, config["module_path"])
    except Exception as exc:
        logger.exception("Error cargando modulo PDF para %s", tipo)
        return None, f"No se pudo cargar el exportador: {exc}"

    generator = getattr(module, config["function"], None)
    if generator is None:
        return None, "Exportador PDF no disponible"

    temp_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    temp_path = temp_file.name
    temp_file.close()

    try:
        if tipo == "routers_nokia":
            generator(doc_id, temp_path, data=data, debug_save_images=False)
        else:
            generator(doc_id, temp_path, data=data)
        with open(temp_path, "rb") as handle:
            pdf_bytes = handle.read()
    except Exception as exc:
        logger.exception("Error generando PDF %s", tipo)
        return None, f"No se pudo generar el PDF: {exc}"
    finally:
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception:
            pass

    return pdf_bytes, ""

