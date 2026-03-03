
from generar_reporte_ericsson import generar_pdf_ericsson

if __name__ == "__main__":
    documento_ids = [
        "dfYPsmdPSD6I7BGRMK7U"
    ]

    for doc_id in documento_ids:
        generar_pdf_ericsson(doc_id, f"reporte_ericsson_{doc_id}.pdf")
