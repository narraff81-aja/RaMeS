import pypdf
from pypdf import PdfReader, PdfWriter
#from pypdf import PdfMerger
import random
import os

import intervalli
## pagesCount
def pagesCount(pdfFilePath: str) -> int:
    try:
        # 1. Tentativo di apertura (Check struttura base)
        reader = PdfReader(pdfFilePath)
        if len(reader.pages) == 0:
            raise ValueError(f"Errore: File senza pagine: '{pdfFilePath}'")
        return len(reader.pages)
    except Exception as e:
        raise ValueError(f"Errore Inaspettato: {str(e)}")
# /pagesCount

## Split
def split(inputPath, outputPath,intervallo):
    try:
        reader = PdfReader(inputPath)
        total_pages = len(reader.pages)
        print(f"File sorgente: {inputPath}, Pagine totali: {total_pages}")

        writer = PdfWriter()
        # Aggiunge le pagine da start_page_index (incluso) a end_page_index (escluso)
        #start_page_index=5
        #end_page_index=10
        if intervallo.da <= intervallo.a:
            for page_index in range(intervallo.da - 1, intervallo.a):
                writer.add_page(reader.pages[page_index])
        else:
            for page_index in range(intervallo.da - 1, intervallo.a - 2,-1):
                writer.add_page(reader.pages[page_index])


        with open(outputPath, "xb") as output_file: #"wb"
            writer.write(output_file)

        print(f"Creato: {outputPath} ({(abs(intervallo.a - intervallo.da) + 1)} pagine)")
    except Exception as e:
        print(f"Si è verificato un errore durante lo split: {e}")
# /split

## Merge
def merge(input_files, output_path):
    """Unisce una lista di file PDF in un unico documento."""
    merger = pypdf.PdfMerger()
    print(f"Inizio unione di {len(input_files)} file in {output_path}...")

    files_to_merge = []

    # Verifica l'esistenza dei file prima di iniziare
    for filename in input_files:
        if os.path.exists(filename):
            files_to_merge.append(filename)
        else:
            print(f"ATTENZIONE: File non trovato e saltato: {filename}")

    if not files_to_merge:
        print("Nessun file valido da unire. Operazione annullata.")
        return

    # Aggiunge tutti i file al PdfMerger
    for filename in files_to_merge:
        try:
            merger.append(filename)
            #merger.append_pages([])
            print(f"  Aggiunto: {filename}")
        except Exception as e:
            print(f"  ERRORE nell'aggiungere {filename}: {e}. File saltato.")

    # Scrive il file finale
    with open(output_path, "wb") as output_file:
        merger.write(output_file)

    merger.close()
    print(f"\nUnione completata. File creato: {output_path}")
# /merge

## Rotate
def rotateRandom(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"ERRORE: File non trovato: {input_path}")
        return

    try:
        reader = pypdf.PdfReader(input_path)
        writer = pypdf.PdfWriter()

        angles = [0, 90, 180, 270]
        for i in range(16):
            # Sceglie un angolo casuale
            # rotation_angle = angles[(i//4)%4] # 0*4, 90*4, 180*4, 270*4
            rotation_angle = angles[i % 4] # (0,90,180,270)*4
            page = reader.pages[i]
            print(page.rotation)
            # Applica la rotazione. Nota: page.rotate() aggiunge alla rotazione esistente.
            # Se la pagina ha già una rotazione di 90°, e scegliamo 90°, la rotazione finale sarà 180°.
            # Per azzerare prima, useremmo page.add_transformation(...) ma per la rotazione casuale va bene così.
            #page.rotate(rotation_angle) # add rot
            page.rotate(rotation_angle-page.rotation) # set rot
            writer.add_page(page)
            print(f"Pagina {i + 1}: Rotazione applicata di {rotation_angle}°")
        with open(output_path, "wb") as output_file:
            writer.write(output_file)

        print(f"\nRotazione completata. File creato: {output_path}")
    except Exception as e:
        print(f"Si è verificato un errore durante la rotazione: {e}")
# /rotate_random

## Dimensione pagine
def pagesSizeAndFormat(pdfFilePath: str):
    """Restituisce le dimensioni e il formato standard di ogni pagina."""
    if not os.path.exists(pdfFilePath):
        return f"ERRORE: File non trovato: {pdfFilePath}"

    from pypdf.generic import RectangleObject

    # Dimensioni standard comuni in punti (1 punto = 1/72 pollice)
    # Fonte: ReportLab/Standard PDF specs
    STANDARD_SIZES_PT = {
        "A4": (595.276, 841.89),  # circa 210 x 297 mm
        "LETTER": (612.0, 792.0),  # circa 8.5 x 11 pollici
        "A3": (841.89, 1190.55),
        "A5": (420.94, 595.276),
    }

    results = []
    try:
        reader = PdfReader(pdfFilePath)

        for i, page in enumerate(reader.pages):
            # Ottiene la dimensione della pagina (RectangleObject)
            # Usa page.cropbox o page.mediabox a seconda di cosa vuoi misurare.
            # Qui usiamo .mediabox che è la dimensione fisica totale.
            media_box: RectangleObject = page.mediabox
            width_pt = float(media_box.width)
            height_pt = float(media_box.height)

            # Normalizza le dimensioni per il confronto (larg x alt)
            size = tuple(sorted((round(width_pt, 2), round(height_pt, 2))))

            format_name = "Personalizzato"

            # Confronto con i formati standard (con tolleranza)
            for name, standard_size in STANDARD_SIZES_PT.items():
                standard_size_normalized = tuple(sorted((round(standard_size[0], 2), round(standard_size[1], 2))))

                # Confronto diretto, potrebbe essere necessaria una tolleranza più generosa per i file reali
                if size == standard_size_normalized:
                    format_name = name
                    break

            results.append({
                "Pagina": i + 1,
                "Larghezza (pt)": f"{width_pt:.2f}",
                "Altezza (pt)": f"{height_pt:.2f}",
                "Formato stimato": format_name
            })

        return results

    except Exception as e:
        return f"Errore di lettura PDF: {e}"
# /pagesSizeAndFormat