from generar_reporte_nokia_metrocell import generar_pdf_nokia_metrocell

if __name__ == "__main__":
    documento_ids = [
        #"axfICpVXp40rqzzQ5Io6",   # Primer documento
        "1oNX0jLN4aCsvovWCg8t"    # Segundo documento
    ]

    for doc_id in documento_ids:
        generar_pdf_nokia_metrocell(doc_id, f"reporte_nokia_metrocell_{doc_id}.pdf")
