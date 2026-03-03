from generar_reporte_nokia import generar_pdf_nokia

if __name__ == "__main__":
    documento_ids = [
        #"axfICpVXp40rqzzQ5Io6",   # Primer documento
        "hC3pxfNGjxpWCvcYvD7S"    # Segundo documento
    ]

    for doc_id in documento_ids:
        generar_pdf_nokia(doc_id, f"reporte_nokia_{doc_id}.pdf")
