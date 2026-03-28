import os
from pathlib import Path
from intervals import infoIntervals, intervalsParse,intervalsToString
from pdf_engine import pagesCountAndCheck, split, merge


def askExistingPdfPathFile(inputPrompt: str) -> tuple[str, int]:
    """ Ask the user to enter an existing Pdf file path.

    :param inputPrompt: Message displayed for input()
    :return: Path of the Pdf file or raise an error
    """
    while True:
        userInput = input(f"{inputPrompt}:\n> ").strip()
        if not userInput:
            print("Errore: Indica il percorso di un file pdf!")
            continue

        # il path va sistemato se fanno parte le coppie di caratteri '\n' o '\t' es:
        # '...cartella\nome...' o '...cartella\tabella...'
        # p=pathFile.replace('\\','/') # alternativa
        p = Path(userInput) # alternativa moderna
        if p.is_dir():
            print("Errore: Il percorso indicato è una cartella. Occorre un file pdf!")
            continue
        if not str.endswith(p.suffix, '.pdf'):
            print("Errore: Il percorso indicato non ha estensione .pdf!")
            continue
        if not os.path.exists(p):
            print("Errore: Il percorso indicato non è di un file .pdf esistente!")
            continue
        try:
            maxPages=pagesCountAndCheck(str(p.absolute()))
        # except (TypeError, ValueError) as e:
        #     print(f"{e}")
        #     continue
        except Exception as e:
            print(f"{e}")
            continue
        return (str(p.absolute()) , maxPages)

    # /while
# /askExistingPdfPathFile

def askNotExistingPdfPathFile(inputPrompt: str) -> str:
    """ Ask the user to enter a not-existing Pdf file path.

    :param inputPrompt: Message displayed for input()
    :return: Path of the Pdf file or raise an error
    """
    while True:
        userInput = input(f"{inputPrompt}:\n> ").strip()
        if not userInput:
            print("Errore: Indica il percorso di un file pdf!")
            continue

        p = Path(userInput)

        if not p.parent.exists():
            print(f"Errore: La cartella '{p.parent}' non esiste!")
            continue
        if p.is_dir():
            print("Errore: Il percorso indicato è una cartella, serve un nome file .pdf")
            continue
        if not str.endswith(p.suffix, '.pdf'):
            print("Errore: Il percorso indicato non è nome file .pdf")
            continue
        if p.exists():
            conferma = input(f"Il file {p.name} esiste già. Vuoi sovrascriverlo? [s/N]: ")
            if conferma.lower() != 's':
                continue

        return str(p.absolute())
    # /while
# /askNotExistingPdfPathFile

isShowUseOfIntervals=False

def reportProgress(dictCallback):
    if 'index' in dictCallback:
        print(f"Avanzamento: {1+dictCallback['index']}/{dictCallback['total']}")
        if dictCallback['status']=='OK':
            print(f"Creato: {Path(dictCallback['pathFile']).name}")
        else:
            print(f"Errore su {Path(dictCallback['pathFile']).name}: {dictCallback['status']}")
    #else:
        #print(dictCallback['status'])
    # sarebbe callback({'status':'End Split'})
    # oppure callback({'status':'End Merge'})
# /segnalaProgresso

def tuiSplit():
    global isShowUseOfIntervals

    try:
        ## Split: fileInputSplit verrà splittato in filesOutput
        print("2) 'Split'")
        print('2.1) Indica il percorso completo del file PDF da cui eseguire lo Split')
        fileInput, pagesCount = askExistingPdfPathFile('Il file non verrà modificato. OCCHIO! Deve esistere!')
        print(f'Il file contiene {pagesCount} pagine. Rammentalo per gli intervalli.')

        print('2.2) Scelta dei files di Output e degli intervalli di pagine')
        # utilizzare una list per filesOutput è un problema se ci sono duplicati di pathFile
        # poiché significa riscrittura del file. Per questo chiede all'user se ha sbagliato gli intervalli
        filesOutput = {}

        # informa l'user di come usare gli intervalli
        if not isShowUseOfIntervals:
            isShowUseOfIntervals = True
            infoIntervals()

        while True:
            nFilesOut = len(filesOutput) + 1
            print(f'Indica il percorso completo del file PDF di output n° {nFilesOut}')
            fileOut = askNotExistingPdfPathFile('OCCHIO! Non deve esistere!')

            question = None  # nuova coppia chiave/valore
            if fileOut in filesOutput:
                # chiedi se l'user vuole cambiare intervalli
                question = input(f'Hai già inserito {fileOut} vuoi ridefinire gli intervalli? [s/n]: ')
                question = question.lower() == 's'
            # question può valere: [None / True / False]
            if question != False:
                while True:
                    intervalsOut = input(f'Indica gli intervalli delle pagine che il file n° {nFilesOut} conterrà: ')
                    intervalsOut = intervalsParse(intervalsOut, pagesCount)
                    print(f'Gli intervalli sono stati interpretati così:\n{intervalsToString(intervalsOut)}')
                    question = input(f'Vuoi utilizzare questi intervalli? [s/n]: ')
                    question = question.lower() == 's'
                    if question:
                        # modifica o aggiunta sono uguali in Python
                        filesOutput[fileOut] = intervalsOut
                        break
                # /while
            if len(filesOutput) > 0:
                question = input(f'Vuoi aggiungere altri files di output? [s/n]: ')
                if question.lower() != 's':
                    break
            # qui question==False or question.lower() == 's', ma cmq l'iterazione è finita
        # /while

        # ora può eseguire effettivamente lo split
        resultSplit = split(fileInput, filesOutput, reportProgress)
        print('2.3) Risultato:')
        if len(resultSplit['errors']) == 0:
            print('Split eseguito senza errori!')
        else:
            print('Split contiene i seguenti errori:')
            for error in resultSplit['errors']:
                print(f'\tfile: {error['path']} ; errore: {error['status']}')
    except Exception as e:
        print(str(e))
    # /try
    #print('fine tuiSplit')
# /tuiSplit

def tuiMerge():
    global isShowUseOfIntervals

    try:
        ## Merge: filesInput verranno fusi in fileOutput
        print("2) 'Merge' scelta dei files e degli intervalli di pagine")
        print('2.1) Indica il percorso completo del file PDF che sarà il risultato del Merge')
        fileOutput = askNotExistingPdfPathFile(
            'Indica il percorso completo del nuovo file PDF che conterrà il Merge/nOCCHIO! Non deve esistere!')

        print('2.2) Scelta dei files di Input e degli intervalli di pagine')
        # utilizzare una list per filesInput non comporta problemi, è consentito avere il merge
        # con: ..., pagine del file1, pagine del file2, pagine del file1, ...
        filesInput = []

        # informa l'user di come usare gli intervalli
        if not isShowUseOfIntervals:
            isShowUseOfIntervals = True
            infoIntervals()

        while True:
            nroFiles = len(filesInput) + 1
            fileIn, pagesCount = askExistingPdfPathFile(
                f'Indica il percorso completo del file PDF di input n° {nroFiles}/nOCCHIO! Deve esistere!')
            print(f'Il file contiene {pagesCount} pagine. Rammentalo per gli intervalli.')
            # Niente domande di cambio intervalli

            while True:
                intervalsIn = input(f'Indica gli intervalli delle pagine che verranno copiate dal file n° {nroFiles}: ')
                intervalsIn = intervalsParse(intervalsIn, pagesCount)
                print(f'Gli intervalli sono stati interpretati così: {intervalsToString(intervalsIn)}')
                question = input(f'Vuoi utilizzare questi intervalli? [s/n]: ')
                question = question.lower() == 's'
                if question:
                    filesInput.append([fileIn, intervalsIn])
                    break
            # /while
            if len(filesInput) > 0:
                question = input(f'Vuoi aggiungere altri files di input? [s/n]: ')
                if question.lower() != 's':
                    break
        # /while

        # Da ora esegue effettivamente il merge
        resultMerge = merge(filesInput,fileOutput,reportProgress )
        print('2.3) Risultato:')
        if len(resultMerge['errors']) == 0:
            print('Merge eseguito senza errori!')
        else:
            print('Merge contiene i seguenti errori:')
            for error in resultMerge['errors']:
                print(f'\tfile: {error['path']} ; errore: {error['status']}')
    except Exception as e:
        print(str(e))
    # /try
    #print('fine tuiMerge')
# /tuiMerge

def runTextUI():
    """Run the text UI
    """
    print('### Text UI ###')

    while True:
        print('1) Scelta comando')
        action = input('Comando: [S]plit, [M]erge (o altro per uscire): ').strip().lower()

        if not action: # nel caso di invio
            print('Uscita in corso dalla Text UI ...')
            break
        elif action[0] == 's':
            tuiSplit()
        elif action[0] == 'm':
            tuiMerge()
        else:
            print('Uscita in corso dalla Text UI ...')
            break
    # /while True
# /runTextUI

if __name__ == '__main__':
    runTextUI()
# /if