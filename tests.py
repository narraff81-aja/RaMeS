from pathlib import Path
from intervalli import Rotazione, Intervallo, intDaStr, intervalliToString, intervalliParse
from pdf_esempi import pagesCount, split, merge, rotateRandom, pagesSizeAndFormat


def _test_Rotazioni_Intervalli_():
    ## uso Rotation
    Cardinali = [Rotazione.N, Rotazione.E, Rotazione.S, Rotazione.W]
    for c in Cardinali:
        print(c, '|', c.__str__())
    print('')

    ## uso Interval
    interv0 = Intervallo(1, 5, Rotazione.S)
    interv1 = Intervallo(7, rot=Rotazione.E)
    interv2 = Intervallo(13, 10, Rotazione.N)
    interv3 = Intervallo(15, 20, Rotazione.W)
    interv = [interv0, interv1, interv2, interv3]
    for i in interv:
        print(i, f"|{i.__str__()}|", i.string())
    print(', '.join([i.__str__() for i in interv]))
    print('intervalli: ',f"|{intervalliToString(interv)}|")
    print('')

    ## uso Interval errati
    interv0 = Intervallo("ciao!", Rotazione.E, Rotazione.S) # NO # ciao!-E S |ciao!-E S|
    interv1 = Intervallo("7", rot="r east") # NO # 7 r east |7 r east|
    interv2 = Intervallo(13.7, "bye bye!", Rotazione.N) # NO # 13.7-bye bye! |13.7-bye bye!|
    interv3 = Intervallo(None, "20", "West")# NO # None-20 West |None-20 West|
    interv = [interv0, interv1, interv2, interv3]
    for i in interv:
        print(i, f"|{i.__str__()}|")
    print(', '.join([i.__str__() for i in interv]))# NO # ciao!-E S, 7 r east, 13.7-bye bye!, None-20 West
    print('')
# /_test_Rotazioni_Intervalli_
_test_Rotazioni_Intervalli_()

def _test_intDaStr_():
    ## test intDaStr()
    ## pagine singole e spazi multipli
    stringhe = [
        '15',
        '5 10',  # '5'
        '5 10 7'  # '5'
    ]
    for stringa in stringhe:
        # pagina singola
        pag = intDaStr(stringa, True, 100)
        print(pag)
    stringhe = [
        '15',  # '9'
        '5 10',  # '9'
        '5 10 7'  # '7'
    ]
    for stringa in stringhe:
        # pagina singola
        pag = intDaStr(stringa, False, 9)
        print(pag)

    ## test in un testo
    testo="Pagine: intervallo 13-10, rotazione -90" # NO, occorre regex
    max=60
    # print(f"primo intero: {intDaStr(testo,True,max)}")
    # print(f"ultimo intero: {intDaStr(testo,False,max)}")
    # print('')
    # print(f"primo intero: {intDaStr(-15.78,True,max)}")
    # print(f"ultimo intero: {intDaStr(-17.45,False,max)}")
    # print('')

    ## test intDaStr() errati
    # print(intDaStr("ciao",True,max)) # ValueError: invalid literal for int() with base 10: 'ciao'
    # print(intDaStr(None,True,max)) # AttributeError: 'NoneType' object has no attribute 'strip'
    # print(intDaStr(True,True,max)) # AttributeError: 'bool' object has no attribute 'strip'
    # print(intDaStr(False,True,max)) # AttributeError: 'bool' object has no attribute 'strip'
# /_test_intDaStr_
_test_intDaStr_()

def _test_intervalli_parse_():
    # Test di Stress per Parse ()
    maxPagine = 20
    stringhe=[
        # 0. test miei
        '-1', # come indici negativi. NO! Non stamperà l'ultima, ma da 1 a 1, ovvero solo 1
        # '1'
        '3 5 -', # => '5-' fregandomene dei confronti 3?5
        # '5-20'
        '-  10 13 17', # => '-10' ignorando 10?13?17
        # '1-10'
        '3 5-7 10', # => '5-7' fregandomene dei confronti 3?5 e 7?10
        # '5-7'
        '3 5 7-10 13 17', # => '7-10' ignorando 3?5?7 e 10?13?17
        # '7-10'
        '--',  # => tutto il file
        # '1-20'
        '--10',  # => '-C0'
        # '1-10'
        '3--',  # => 'An-'
        # '3-20'
        '3--10',  # => 'An-C0'
        # '3-10'
        '13--10',  # => 'An-C0'
        # '13-10'
        '-7-',  # => 'B0'
        # '7'
        '-7-10',  # => B<=C ? '-C0' : 'Bn-C0'
        # '1-10'
        '-17-10',  # => B<=C ? '-C0'1 : 'Bn-C0'
        # '17-10'
        '3-7-',  # => A<=B ? 'An-' : 'An-B0'
        # '3-20'
        '13-7-',  # => A<=B ? 'An-' : 'An-B0'
        # '13-7'

        # "A<=B" ? "u'A-'" : "u'A-B'1" Tende ad ignorare C (meglio da modificare)
        '7-7-7', # '7-20'
        '7-7-17', # '7-20'
        '7-7-25', # '7-20'
        '7-17-7', # '7-20'
        '7-17-17', # '7-20'
        '7-17-25', # '7-20'
        '7-25-7', # '7-20'
        '7-25-17', # '7-20'
        '7-25-25', # '7-20'
        '17-7-7', # '17-7'
        '17-7-17', # '17-7'
        '17-7-25', # '17-7'
        '17-17-7', # '17-20'
        '17-17-17', # '17-20'
        '17-17-25', # '17-20'
        '17-25-7', # ? '17-20'
        '17-25-17', # '17-20'
        '17-25-25', # '17-20'
        '25-7-7', # '20-7'
        '25-7-17', # '20-7'
        '25-7-25', # '20-7'
        '25-17-7', # '20-17'
        '25-17-17', # '20-17'
        '25-17-25', # '20-17'
        '25-25-7', # '20'
        '25-25-17', # '20'
        '25-25-25', # '20'

        # creati da Gemini 3
        # 1. Estremi mancanti e "vuoti":
        "", # tutto
        # '1-20'
        "- 5, 15   -",  # (Dovrebbe interpretare 1-5 e 15-20)
        # '1-5, 15-20'
        "-  ",  # (Dovrebbe restituire l'intero documento 1-20)
        # '1-20'

        # 2. Inversioni e Rotazioni:
        "10  -  2 S",  # (Decrescente con rotazione imposta Sud)
        # '10-2 S'
        "5-5 n",  # (Singola pagina espressa come intervallo con rotazione aggiuntiva Nord)
        # '5'

        # 3. Stringhe con spazi "creativi":
        " 1 - 3 E , 18-20 w ",  # (Spazi prima, dopo e tra i trattini/virgole)
        # '1-3 E, 18-20 W'

        # 4. Casi Limite (Out of Bounds):
        "18-25",  # (Il 25 supera il maxPages. Il parser lo taglia a 20 o solleva errore?)
        # '18-20'
        "0-5",  # (Esiste la pagina 0 o il tuo sistema parte da 1?)
        # '1-5'

        # 5. Input Malformato (Il "Dito dell'Utente"):
        "1-5-10 N",  # (Doppio trattino: errore o prende il primo e l'ultimo?)
        # '1-20'
        "1--10 N", # interpretato "1-10 N"
        # '1-10'
        "7:W",  # (Uso dei due punti invece del trattino o spazio)
        # '7 W'
        "abc-def",  # (Lettere dove dovrebbero esserci numeri)
        # '1-20 E' (per ogni intervallo, la 1° direzione è quella che conta!)

        # 6. Intervalli Sovrapposti:
        "1-10, 5-15",  # (Pypdf estrarrà le pagine 5-10 due volte o le unificherà?)
        # '1-10, 5-15' (l'user vuole duplicarle)

        # 7. Solo Rotazione (Senza numeri):
        "S, n",  # (Se scrivo solo la lettera senza numeri, il parser fallisce o ruota tutto?)
        # '1-20 S, 1-20'

        # 8. Separatori e trattini multipli:
        "1---5 ,,, 10--12 S",  # (L'utente ha il dito pesante sui tasti)
        # '10-12 S' (intervals ignora gli errori '---' e gli intervalli vuoti)
        ", , 5-8 , ,",  # (Virgole senza numeri all'inizio, in mezzo e alla fine)
        # '5-8' (intervals ignora gli intervalli vuoti)

        # 9. Caratteri di rotazione ripetuti o contrastanti:
        "1-5 NNEESS",  # (Tante lettere di rotazione: prende l'ultima? Somma i gradi?)
        # '1-5' (vale la 1° direzione)
        "10-15 n W S e",  # (Un mix di minuscole e maiuscole sparse)
        # '10-15' (ha preso 'n' che è di default)

        # 10. Inversioni estreme con rotazione:
        "20-1 W , 1-20 E",  # (Tutto il documento al contrario verso Ovest, poi tutto dritto verso Est)
        # '20-1 W, 1-20 E' (l'user vuole duplicare le pagine)

        # 11. Sintassi "sporca" ma comprensibile:
        "1- 5 , 10 -15 S , 20 - 18",  # (Spazi messi a caso tra i trattini e i numeri)
        # '1-5, 10-15 S, 20-18'
        "5-5-5-5 N",  # (Cosa succede con 4 numeri e 3 trattini?)
        # '' (intervalli non validi perché 3x '-'!)

        # 12. Lettere senza numeri in mezzo a intervalli:
        "1-5, S, 10-15",  # (La 'S' da sola in mezzo a due intervalli numerici viene applicata a tutto o ignorata?)
        # '1-5, 1-20 S, 10-15'

        # 13. Il test "Gatto sulla tastiera":
        "1-5 n, , - , 10-12, e, w, 20-15"
        # '1-5, 1-20, 10-12, 1-20 E, 1-20 W, 20-15'
        # ricorda: ', ,' produce '' mentre ', - ,' produce '1-20'
    ]
    print('intervalli')
    for stringa in stringhe:
        try:
            intervalli= intervalliParse(stringa, maxPagine)
            print(repr(intervalliToString(intervalli)),'|', stringa)
        except ValueError as e:
            print(e,'|', stringa)
    ...
# /_test_intervalli_parse_
_test_intervalli_parse_()

def _text_pdf_esempi_():
    # test pagesCount
    print(f"Pagine: {pagesCount('EsempioSplit.pdf')}")
    pathEs = 'D:\\A1\\C Corner\\copilot-handbook.pdf'
    # pathEs=input('path pdf: ')
    print(f"Pagine: {pagesCount(pathEs)}")

    # test per split/merge
    for page_index in range(10 - 1, 14):
        print(page_index)
    for page_index in range(14 - 1, 10 - 2,-1):
        print (page_index)

    ## split
    outputPath1 = 'D:\\A1\\C Corner\\copilot-handbook_5.pdf'
    # interv=Intervallo(10,14,Rotazione.S)
    # interv=Intervallo(53,rot= Rotazione.S)
    interv = Intervallo(14, 10, Rotazione.S)
    split(pathEs,outputPath1,interv)

    ## merge
    # Esecuzione dell'esempio
    input_list = [
        'D:\\A1\\C Corner\\copilot-handbook_1.pdf',
        'D:\\A1\\C Corner\\copilot-handbook_2.pdf',
        'D:\\A1\\C Corner\\copilot-handbook_3.pdf',
        'D:\\A1\\C Corner\\copilot-handbook_4.pdf',
        'D:\\A1\\C Corner\\copilot-handbook_5.pdf'
    ]
    # Nota: Prima di eseguire, crea alcuni file fittizi o rinomina i file esistenti
    merge(input_list, 'D:\\A1\\C Corner\\EsempioMerge.pdf')

    ## Rotate
    rotateRandom('EsempioRotate.pdf', 'RotatedOutput.pdf')
    pathEs = outputPath1
    # outputPath1='D:\\A1\\C Corner\\copilot-handbook_aggiunta.pdf'
    outputPath1 = 'D:\\A1\\C Corner\\copilot-handbook_settata.pdf'
    rotateRandom(pathEs, outputPath1)

    ## Dimensione pagine
    info = pagesSizeAndFormat('EsempioRotate.pdf')
    for page_info in info:
        print(page_info)
    ...
# /_text_pdf_esempi_
_text_pdf_esempi_()
