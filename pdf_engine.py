import os
from os.path import isdir
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError
from pathlib import Path
from intervals import Interval, Rotation,intervalsToString,intervalsPagesCount

def pagesCount(pdfFilePath: str):
    """ Returns the total number of pages.

    :param pdfFilePath: Full file PDF path
    :return: Total number of pages or raise a [TypeError | ValueError | FileNotFoundError]
    """
    if not (isinstance(pdfFilePath, str) or isinstance(pdfFilePath, Path)):
        raise TypeError(f"Errore: Path deve essere una stringa! Non '{str(pdfFilePath)}'")
    if isdir(Path(pdfFilePath)):
        raise ValueError(f"Errore: Path è una cartella! '{pdfFilePath}'")
    if not str.endswith(pdfFilePath, ".pdf"):
        raise ValueError(f"Errore: Path non ha estensione PDF! '{pdfFilePath}'")
    if not os.path.exists(Path(pdfFilePath)):
        raise FileNotFoundError (f"Errore: File non trovato: '{pdfFilePath}'")

    try:
        reader = PdfReader(pdfFilePath)
        if len(reader.pages) == 0:
            raise ValueError("FILE_EMPTY")
        return len(reader.pages)
    except Exception as e:
        raise ValueError(f"UNEXPECTED_ERROR: {str(e)}")
# /pagesCount

def checkPdf(pdfFilePath: str) -> bool:
    """ Check for any Errors in PDF file.

    :param pdfFilePath: Full file PDF path
    :return: True or False (a [TypeError | ValueError | FileNotFoundError])
    """
    try:
        if not (isinstance(pdfFilePath, str) or isinstance(pdfFilePath, Path)):
            raise TypeError(f"Errore: Path deve essere una stringa! Non '{str(pdfFilePath)}'")
        if isdir(Path(pdfFilePath)):
            raise ValueError(f"Errore: Path è una cartella! '{pdfFilePath}'")
        if not str.endswith(pdfFilePath, ".pdf"):
            raise ValueError(f"Errore: Path non ha estensione PDF! '{pdfFilePath}'")
        if not os.path.exists(Path(pdfFilePath)):
            raise FileNotFoundError (f"Errore: File non trovato: '{pdfFilePath}'")

        # 1. Tentativo di apertura (Check struttura base)
        reader = PdfReader(pdfFilePath)
        # 2. Check Password
        if reader.is_encrypted:
            #raise ValueError("FILE_ENCRYPTED")
            raise ValueError(f"Errore: File protetto da password: '{pdfFilePath}'")
        # 3. Check Moduli complessi, se ha un catalogo /AcroForm
        if "/AcroForm" in reader.trailer["/Root"]:
            #raise ValueError("FILE_WITH_ACROFORM")
            raise ValueError(f"Errore: File con AcroForm: '{pdfFilePath}'")
        # 4. Check pagine (Minimo sindacale)
        if len(reader.pages) == 0:
            #raise ValueError("FILE_EMPTY")
            raise ValueError(f"Errore: File senza pagine: '{pdfFilePath}'")
        return True
    except Exception as e:
        return False
# /checkPdf

def split(pathfileInput: str, filesOutput: dict[str, list[Interval]]):
    """ *** Split PDF placeholder ***

    :param pathfileInput: Full file PDF path, Split source file
    :param filesOutput: Dictionary of Split ''child'' files
    :return: True success; False some Error
    """
    try:
        if checkPdf(pathfileInput):
            pagesMax =pagesCount(pathfileInput)
        else:
            return False
    except Exception as e:
        raise e # non può continuare se ci sono errori
    if not isinstance(filesOutput, dict):
        raise TypeError("filesOutput DEVE essere un dict[str, list[Interval]]")
    if len(filesOutput) == 0:
        raise ValueError("filesOutput non ha elementi!")

    reader = PdfReader(pathfileInput)
    idFilesOut = -1 # è sempre un index e deve partire da 0
    totalOutput=len(filesOutput.items())
    for outPath, outIntervals in filesOutput.items():
        try:
            idFilesOut += 1

            # outIntervals può essere None per riferirsi a tutto il file?
            # E una lista vuota? O deve avere minimo 1 Interval?
            # E se viene passato 1 Interval invece di una list[Interval]?
            if ((outIntervals is not None) and (not isinstance(outIntervals, list))
                    and (not isinstance(outIntervals, Interval))):
                raise TypeError(f'{outPath} non ha una list[Interval]') ######

            #writer = PdfWriter()

            # il singolo intervallo viene impacchettato in una list
            if isinstance(outIntervals, Interval):
                outIntervals=[outIntervals]
                print('1 intervallo impacchettato!')

            if (outIntervals is None) or len(outIntervals)==0:
                # copia il file mantenendo segnalibri e commenti
                #writer.append(reader)
                print(f'writer: 1-{pagesMax}; {pagesMax} pagine')
            elif (len(outIntervals)==1 and isinstance(outIntervals[0], Interval) and
                outIntervals[0].fromPage==1 and outIntervals[0].toPage==pagesMax):
                # #copia il file mantenendo segnalibri e commenti
                # writer.append(reader)
                # rot = outIntervals[0].rotation
                # if rot != Rotation.n:
                #     # qui son dolori con segnalibri e commenti!
                #     for page in writer.pages:
                #         if rot.isAddedRotation():
                #             page.rotate(rot.angle())
                #         else:
                #             page.rotation = rot.angle()
                #         writer.add_page(page)
                print(f'writer: {outIntervals[0].toString()}; {outIntervals[0].pagesCount()} pagine')
            else:
                # arrivato fin qui outIntervals è una list non vuota di
                # chissà cosa ed ignora i non-Interval
                # Segnalibri e commenti si perderanno
                if not any(type(x) is Interval for x in outIntervals):
                    raise TypeError(f'{outPath} non ha almeno un Interval valido!')

                for interval in outIntervals:
                    if not isinstance(interval, Interval):
                        continue # lo ignora e basta
                    # # crea il range adatto
                    # if interval.fromPage <= interval.toPage:
                    #     rng=range(interval.fromPage - 1, interval.toPage)
                    # else:
                    #     rng=range(interval.fromPage - 1, interval.toPage - 2, -1)
                    # rot = interval.rotation
                    # for pageIndex in rng:
                    #     page=reader.pages[pageIndex]
                    #     if rot.isAddedRotation():
                    #         page.rotate(rot.angle())
                    #     else:
                    #         page.rotation = rot.angle()
                    #     writer.add_page(page)
                    #print(f'writer: {interval.toString()}; {interval.pagesCount()} pagine')
                # /for
                print(f'writer: {intervalsToString(outIntervals)}; {intervalsPagesCount(outIntervals)} pagine')
            # /if

            # if len(writer.pages)==0:
            #     # Non va bene! Creerebbe un file vuoto!
            #     raise ValueError
            # else:
            #     # scrive effettivamente sul file
            #     with open(outPath, "wb") as f:
            #         writer.write(f)
            # writer.close()
            print(f'writer {idFilesOut} chiuso!')
        except Exception as e:
            # cattura l'eccezione al file output e va avanti con gli altri
            print(f'{idFilesOut}: {str(e)}')
    # /for
    reader.close()
    #print(f'reader chiuso!')
    return True
# /split


def _split_(pathfileInput: str, filesOutput: dict[str, list[Interval]]):
    """ It actually Split PDF on the FileSystem.

    :param pathfileInput: Full file PDF path, Split source file
    :param filesOutput: Dictionary of Split ''child'' files
    :return: True success; False some Error
    """
    try:
        if checkPdf(pathfileInput):
            pagesMax = pagesCount(pathfileInput)
        else:
            return False
    except Exception as e:
        raise e # non può continuare se ci sono errori
    if not isinstance(filesOutput, dict):
        raise TypeError("filesOutput DEVE essere un dict[str, list[Interval]]")
    if len(filesOutput) == 0:
        raise ValueError("filesOutput non ha elementi!")

    reader = PdfReader(pathfileInput)
    idFilesOut = -1  # è sempre un index e deve partire da 0
    totalOutput = len(filesOutput.items())
    for outPath, outIntervals in filesOutput.items():
        try:
            idFilesOut += 1
            # outIntervals può essere None per riferirsi a tutto il file?
            # E una lista vuota? O deve avere minimo 1 Interval?
            # E se viene passato 1 Interval invece di una list[Interval]?
            if ((outIntervals is not None) and (not isinstance(outIntervals, list))
                    and (not isinstance(outIntervals, Interval))):
                raise TypeError(f'{outPath} non ha una list[Interval]')

            writer = PdfWriter()

            # il singolo intervallo viene impacchettato in una list
            if isinstance(outIntervals, Interval):
                outIntervals=[outIntervals]

            if (outIntervals is None) or len(outIntervals)==0:
                # copia il file mantenendo segnalibri e commenti
                writer.append(reader)
                print(f'writer: 1-{pagesMax}; {pagesMax} pagine')
            elif (len(outIntervals)==1 and isinstance(outIntervals[0], Interval) and
                  outIntervals[0].fromPage==1 and outIntervals[0].toPage==pagesMax):
                #copia il file mantenendo segnalibri e commenti
                writer.append(reader)
                rot = outIntervals[0].rotation
                if rot != Rotation.n:
                    # qui son dolori con segnalibri e commenti!
                    for page in writer.pages:
                        if rot.isAddedRotation():
                            page.rotate(rot.angle())
                        else:
                            page.rotation = rot.angle()
                        writer.add_page(page)
                print(f'writer: {outIntervals[0].toString()}; {outIntervals[0].pagesCount()} pagine')
            else:
                # arrivato fin qui outIntervals è una list non vuota di
                # chissà cosa ed ignora i non-Interval
                # Segnalibri e commenti si perderanno
                if not any(type(x) is Interval for x in outIntervals):
                    raise TypeError(f'{outPath} non ha almeno un Interval valido!')

                for interval in outIntervals:
                    if not isinstance(interval, Interval):
                        continue  # lo ignora e basta
                    # crea il range adatto
                    if interval.fromPage <= interval.toPage:
                        rng=range(interval.fromPage - 1, interval.toPage)
                    else:
                        rng=range(interval.fromPage - 1, interval.toPage - 2, -1)
                    rot = interval.rotation
                    for pageIndex in rng:
                        page=reader.pages[pageIndex]
                        if rot.isAddedRotation():
                            page.rotate(rot.angle())
                        else:
                            page.rotation = rot.angle()
                        writer.add_page(page)
                    # /for
                # /for
                print(f'writer: {intervalsToString(outIntervals)}; {intervalsPagesCount(outIntervals)} pagine')
            # /if

            if len(writer.pages)==0:
                # Non va bene! Creerebbe un file vuoto!
                raise ValueError('filesOutput senza pagine!')
            else:
                # scrive effettivamente sul file
                with open(outPath, "wb") as f:
                    writer.write(f)

            writer.close()
            print(f'writer {idFilesOut} chiuso!')
        except Exception as e:
            # cattura l'eccezione al file output e va avanti con gli altri
            print(f'{idFilesOut}: {str(e)}')
    # /for
    reader.close()
    # print(f'reader chiuso!')
    return True
# /split

def _merge_(filesInput: list[tuple[str, list[Interval]]], pathfileOutput: str):
    """ It actually Merges PDF on the FileSystem.

    :param filesInput: List of source merge files
    :param pathfileOutput: Full file PDF path, Merge result file
    :return: True success; False some Error
    """
    if not isinstance(pathfileOutput, str):
        raise TypeError("pathfileOutput DEVE essere una stringa!")
    if isdir(Path(pathfileOutput)) :
        raise ValueError(f"pathfileOutput è una cartella! '{pathfileOutput}'")
    if not os.path.exists(Path(pathfileOutput).parent):
        raise ValueError(f"Cartella che conterrà il file non trovata: {pathfileOutput}")
    if not str.endswith(pathfileOutput, ".pdf"):
        raise ValueError("pathfileOutput non ha estensione PDF!")
    if not isinstance(filesInput, list):
        raise TypeError("filesInput DEVE essere un list[tuple[str, list[Interval]]]")
    if len(filesInput) == 0:
        raise ValueError("filesInput non ha elementi!")
    if not any(type(x) is tuple for x in filesInput):
        raise ValueError("filesInput non ha almeno una tupla valida!")

    writer = PdfWriter()
    readers = []  # Per tenere vivi i riferimenti ai file aperti
    idPagesOut = 0
    idFilesIn = -1  # è sempre un index e deve partire da 0
    hasErrors=False
    for inPath, inIntervals in filesInput:
        try:
            idFilesIn += 1
            # print('in:', inPath)
            # inIntervals può essere None per riferirsi a tutto il file?
            # E una lista vuota? O deve avere minimo 1 Interval?
            # E se viene passato 1 Interval invece di una list[Interval]?
            if ((inIntervals is not None) and (not isinstance(inIntervals, list))
                    and (not isinstance(inIntervals, Interval))):
                raise TypeError(f'{inPath} non ha una list[Interval]')

            if checkPdf(inPath):
                pagesMax = pagesCount(inPath)
            else:
                return False
            reader = PdfReader(inPath)
            readers.append(reader)

            print('reader',idFilesIn,'aperto')

            # il singolo intervallo viene impacchettato in una list
            if isinstance(inIntervals, Interval):
                inIntervals = [inIntervals]

            if (inIntervals is None) or len(inIntervals) == 0:
                # copia il file mantenendo segnalibri e commenti
                writer.append(reader)
                print(f'writer uguale: 1-{pagesMax}; {pagesMax} pagine')
            elif (len(inIntervals) == 1 and isinstance(inIntervals[0], Interval) and
                  inIntervals[0].fromPage == 1 and inIntervals[0].toPage == pagesMax):
                # copia il file mantenendo segnalibri e commenti
                writer.append(reader)
                rot = inIntervals[0].rotation
                if rot != Rotation.n:
                    # qui son dolori con segnalibri e commenti!
                    for page in writer.pages:
                        if rot.isAddedRotation():
                            page.rotate(rot.angle())
                        else:
                            page.rotation = rot.angle()
                        writer.add_page(page)
                print(f'writer uguale: {inIntervals[0].toString()}; {inIntervals[0].pagesCount()} pagine')
            else:
                # arrivato fin qui outIntervals è una list non vuota di
                # chissà cosa ed ignora i non-Interval
                # i segnalibri e commenti originali vengono eliminati!
                if not any(type(x) is Interval for x in inIntervals):
                    raise TypeError(f'{inPath} non ha almeno un Interval valido!')
                # ---
                # Aggiungiamo un segnalibro per l'inizio di questo file
                writer.add_outline_item(Path(inPath).stem, idPagesOut)
                # print(f'segnalibro id pagina {idPagesOut}')
                for interval in inIntervals:
                    if not isinstance(interval, Interval):
                        continue
                    # crea il range adatto
                    if interval.fromPage <= interval.toPage:
                        rng = range(interval.fromPage - 1, interval.toPage)
                    else:
                        rng = range(interval.fromPage - 1, interval.toPage - 2, -1)
                    rot = interval.rotation
                    for pageIndex in rng:
                        page = reader.pages[pageIndex]
                        if rot.isAddedRotation():
                            page.rotate(rot.angle())
                        else:
                            page.rotation = rot.angle()
                        writer.add_page(page)
                    idPagesOut += interval.pagesCount()
                    print(f'writer: {interval.toString()}; {interval.pagesCount()} pagine')
                # /for
            # /if

            print(f'reader {idFilesIn} in sospeso!')
        except Exception as e:
            # cattura l'eccezione al file output e va avanti con gli altri
            print(f'{inPath}: {str(e)}')
            hasErrors = True
    # /for

    if hasErrors == True:
        # se ha errori, da cmq un risultato ma purtroppo incompleto!
        pathfileOutput=str.replace('.pdf','_[incomplete].pdf')
    # Scrittura finale. Non si può fare ad ogni iterazione (in mode ["wb", "ab", "ab", ...])
    # perchè ad ogni riapertura deve rileggere tutto il file, molto sconveniente!
    # readers serve aiutare nella scrittura
    with open(pathfileOutput, "wb") as f:
        writer.write(f)

    #print(f'writer chiuso!')
    writer.close()
    readers.clear()  # Libera i file
    return True
# /merge

def merge(filesInput: list[tuple[str, list[Interval]]], pathfileOutput: str):
    """ *** Merges PDF placeholder ***

    :param filesInput: List of source merge files
    :param pathfileOutput: Full file PDF path, Merge result file
    :return: True success; False some Error
    """
    if not isinstance(pathfileOutput, str):
        raise TypeError("pathfileOutput DEVE essere una stringa!")
    if isdir(Path(pathfileOutput)) :
        raise ValueError(f"pathfileOutput è una cartella! '{pathfileOutput}'")
    if not os.path.exists(Path(pathfileOutput).parent):
        raise ValueError(f"Cartella che conterrà il file non trovata: {pathfileOutput}")
    if not str.endswith(pathfileOutput, ".pdf"):
        raise ValueError("pathfileOutput non ha estensione PDF!")
    if not isinstance(filesInput, list):
        raise TypeError("filesInput DEVE essere un list[tuple[str, list[Interval]]]")
    if len(filesInput) == 0:
        raise ValueError("filesInput non ha elementi!")
    if not any(type(x) is tuple for x in filesInput):
        raise ValueError("filesInput non ha almeno una tupla valida!")

    writer = PdfWriter()
    readers = []  # Per tenere vivi i riferimenti ai file aperti
    idPagesOut = 0
    idFilesIn = -1  # è sempre un index e deve partire da 0
    hasErrors = False
    for inPath, inIntervals in filesInput:
        try:
            idFilesIn += 1
            print('in:', inPath)
            # inIntervals può essere None per riferirsi a tutto il file?
            # E una lista vuota? O deve avere minimo 1 Interval?
            # E se viene passato 1 Interval invece di una list[Interval]?
            if ((inIntervals is not None) and (not isinstance(inIntervals, list))
                    and (not isinstance(inIntervals, Interval))):
                raise TypeError(f'{inPath} non ha una list[Interval]')

            if checkPdf(inPath):
                pagesMax = pagesCount(inPath)
            else:
                return False
            reader = PdfReader(inPath)
            readers.append(reader)

            print('reader',idFilesIn,'aperto')

            # il singolo intervallo viene impacchettato in una list
            if isinstance(inIntervals, Interval):
                inIntervals = [inIntervals]
                print('1 intervallo impacchettato!')


            if (inIntervals is None) or len(inIntervals) == 0:
                # copia il file mantenendo segnalibri e commenti
                #writer.append(reader)
                print(f'writer uguale: 1-{pagesMax}; {pagesMax} pagine')
            elif (len(inIntervals) == 1 and isinstance(inIntervals[0], Interval) and
                  inIntervals[0].fromPage == 1 and inIntervals[0].toPage == pagesMax):
                # copia il file mantenendo segnalibri e commenti
                # writer.append(reader)
                # rot = inIntervals[0].rotation
                # if rot != Rotation.n:
                #     # qui son dolori con segnalibri e commenti!
                #     for page in writer.pages:
                #         if rot.isAddedRotation():
                #             page.rotate(rot.angle())
                #         else:
                #             page.rotation = rot.angle()
                #         writer.add_page(page)
                print(f'writer uguale: {inIntervals[0].toString()}; {inIntervals[0].pagesCount()} pagine')
            else:
                # arrivato fin qui outIntervals è una list non vuota di
                # chissà cosa ed ignora i non-Interval
                # i segnalibri e commenti originali vengono eliminati!
                if not any(type(x) is Interval for x in inIntervals):
                    raise TypeError(f'{inPath} non ha almeno un Interval valido!')
                # ---
                # Aggiungiamo un segnalibro per l'inizio di questo file
                #writer.add_outline_item(Path(inPath).stem, idPagesOut)
                print(f'segnalibro id pagina {idPagesOut}')
                for interval in inIntervals:
                    if not isinstance(interval, Interval):
                        continue
                    # crea il range adatto
                    # if interval.fromPage <= interval.toPage:
                    #     rng = range(interval.fromPage - 1, interval.toPage)
                    # else:
                    #     rng = range(interval.fromPage - 1, interval.toPage - 2, -1)
                    # rot = interval.rotation
                    # for pageIndex in rng:
                    #     page = reader.pages[pageIndex]
                    #     if rot.isAddedRotation():
                    #         page.rotate(rot.angle())
                    #     else:
                    #         page.rotation = rot.angle()
                    #     writer.add_page(page)
                    # idPagesOut += interval.pagesCount()
                    print(f'writer: {interval.toString()}; {interval.pagesCount()} pagine')
                # /for
            # /if

            print(f'reader {idFilesIn} in sospeso!')
        except Exception as e:
            # cattura l'eccezione al file output e va avanti con gli altri
            print(f'{inPath}: {str(e)}')
            hasErrors = True
    # /for

    if hasErrors == True:
        # se ha errori, da cmq un risultato ma purtroppo incompleto!
        pathfileOutput=str.replace('.pdf','_[incomplete].pdf')
    # Scrittura finale. Non si può fare ad ogni iterazione (in mode ["wb", "ab", "ab", ...])
    # perchè ad ogni riapertura deve rileggere tutto il file, molto sconveniente!
    # readers serve aiutare nella scrittura
    with open(pathfileOutput, "wb") as f:
        writer.write(f)

    print(f'writer chiuso!')
    writer.close()
    readers.clear()  # Libera i file
    return True
# /merge
