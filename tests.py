import os
from pathlib import Path
import re
from intervals import (Rotation, Interval, signedIntegersParse, unsignedIntegersParse,
                       pageFromString, intervalsParse, intervalsToString, intervalsPagesCount)
from pdf_engine import checkPdf, pagesCount, split, merge

def _test_Rotation_Interval_():
    ## uso Rotation
    Cardinals = [Rotation.n, Rotation.e, Rotation.s, Rotation.w,
                 Rotation.North, Rotation.East, Rotation.South, Rotation.West]
    for c in Cardinals:
        print(c, '|', c.value, c.toString(), c.toLongString())
    print('')

    ## uso Rotation errati
    Cardinals = [Rotation.fromInt(None),  # 'n'
                 Rotation.fromInt(170),  # 'e'
                 Rotation.fromInt(Rotation.e),  # 'e'
                 Rotation.fromInt('s'),  # 's'
                 Rotation.fromInt(-120),  # 600 -> 540 'S'
                 Rotation.fromChar(None),  # 'n'
                 Rotation.fromChar(Rotation.East),  # 'E'
                 Rotation.fromChar(100),  # 'e'
                 Rotation.fromChar('South'),  # 's'
                 Rotation.fromChar('g west')]  # 'w'
    for c in Cardinals:
        print(c, c.value, c.toString())
    print('')

    ## uso Interval
    interv0 = Interval(1, 5, Rotation.South)
    interv1 = Interval(7, rot=Rotation.e)
    interv2 = Interval(13, 10, Rotation.n)
    interv3 = Interval(15, 20, Rotation.West)
    interv = [interv0, interv1, interv2, interv3]
    for i in interv:
        print(i, f"|{i.toString()}|", i.toLongString())
    print(', '.join([i.toString() for i in interv]))
    print(intervalsToString(interv), intervalsPagesCount(interv), 'pagine')
    print('')

    ## uso Interval errati
    interv0 = Interval("ciao!", Rotation.e, Rotation.South)
    interv1 = Interval("7", rot="r east")
    interv2 = Interval(13.7, "bye bye!", Rotation.n)
    interv3 = Interval(None, "20", "West")
    interv = [interv0, interv1, interv2, interv3]
    for i in interv:
        print(i, f"|{i.toString()}|")
    print(', '.join([i.toString() for i in interv]))
    print('')
    ...
# /_test_Rotation_Interval_
_test_Rotation_Interval_()

def _test_intParse_pageFromString_():
    ## test int.parse()
    testo="Pagine: intervallo 13-10, rotazione -90"
    print(signedIntegersParse(testo))
    print(unsignedIntegersParse(testo))
    print(f"primo intero (signed): {signedIntegersParse(testo)[0]}") # 13
    print(f"ultimo intero (signed): {signedIntegersParse(testo)[-1]}") # -90
    print(f"primo intero (unsigned): {unsignedIntegersParse(testo)[0]}") # 13
    print(f"ultimo intero (unsigned): {unsignedIntegersParse(testo)[-1]}") # 90
    print('')
    print(f"primo intero (signed): {signedIntegersParse(-15.78)[0]}") # -15
    print(f"ultimo intero (signed): {signedIntegersParse(-17.45)[-1]}") # -17
    print(f"primo intero (unsigned): {unsignedIntegersParse(-15.78)[0]}") # 15
    print(f"ultimo intero (unsigned): {unsignedIntegersParse(-17.45)[-1]}") # 17
    print('')
    ## test int.parse() errati
    # print(signedIntegersParse("ciao")) # ValueError: intero non trovato!
    # print(signedIntegersParse(None)) # TypeError: <class 'NoneType'>
    print(signedIntegersParse(True)) # 1
    print(signedIntegersParse(False)) # 0
    s={0,7,5,8,7}
    # print(s)
    # print(signedIntegersParse(s)) # TypeError: <class 'set'>
    dict={'id1':9,"id2":15,'id3':'ciao'}
    # print(dict)
    # print(signedIntegersParse(dict)) # TypeError: <class 'dict'>
    arr = [7, 5, 'bye', 8, 7, True, 0, None, 4, -12]
    print(arr)
    print(unsignedIntegersParse(arr)) # [7, 5, 8, 7, 1, 0, 4, 12]
    arr=['bye', None, Rotation.West]
    #print(arr)
    #print(unsignedIntegersParse(arr)) # TypeError
    tupla = (7, 5, 'bye', 8, 7, True, 0, None, 4, -12)
    print(tupla)
    print(unsignedIntegersParse(tupla))  # [7, 5, 8, 7, 1, 0, 4, 12]
    tupla = ('bye', None, Rotation.West)
    #print(tupla)
    #print(unsignedIntegersParse(tupla)) # TypeError

    # xxxx
    # print(signedIntegerParse(testo, "ciao")) # isFirst=True
    # print(unsignedIntegerParse(testo, "bye")) # isFirst=True
    # print(signedIntegerParse(testo, "")) # isFirst=False
    # print(unsignedIntegerParse(testo, "")) # isFirst=False
    # print(signedIntegerParse(testo, 1)) # isFirst=True
    # print(unsignedIntegerParse(testo, 1)) # isFirst=True
    # print(signedIntegerParse(testo, 0)) # isFirst=False
    # print(unsignedIntegerParse(testo, 0)) # isFirst=False
    # print(signedIntegerParse(testo, None)) # isFirst=False
    # print(unsignedIntegerParse(testo, None)) # isFirst=False
    # /xxxx


    ## pagine singole e spazi multipli
    stringhe = [
        '15',
        '5 10',  # '5'
        '5 10 7'  # '5'
    ]
    for stringa in stringhe:
        if stringa.find('-') == -1:
            # pagina singola
            pag = pageFromString(stringa, True, 100)
            print(pag)
    stringhe = [
        '15', # '9'
        '5 10',  # '5'
        '5 10 7'  # '7'
    ]
    for stringa in stringhe:
        if stringa.find('-') == -1:
            # pagina singola
            pag = pageFromString(stringa, False, 9)
            print(pag)
# /_test_intParse_pageFromString_
_test_intParse_pageFromString_()

def _test_regex_():
    ## uso regex NESW
    stringhe =[ ' e13N - 10 W ',
                'w270e90s',
                '88E180w90',
                'sud 0 Gradi',
                '90',
                "123 Pagina_A (5-10) \t fine-11\n456"]
    for stringa in stringhe:
        match = re.search(r'[NESWnesw]', stringa.strip())
        if match:
            rotazione_enum = Rotation.fromChar(match.group(0))
        else:
            rotazione_enum = Rotation.n
        print(stringa, '|', match, '|', rotazione_enum)

    ## uso regex per pulizia chars
    for stringa in stringhe:
        stringa_pulita = re.sub(r'[^0-9 -]', ' ', stringa)
        while True:
            if stringa_pulita.find('  ') >= 0:
                stringa_pulita = stringa_pulita.replace('  ', ' ')
            else:
                break
        print('|' + stringa_pulita.strip() + '|')
    ...
# /_test_regex_
#_test_regex_()

def _test_Intervals_parse_():
    # Test di Stress per Parse ()
    maxPagine = 20
    stringhe=[
        # 0. test miei
        '-1', # come indici negativi. NO! Non stamperà l'ultima, ma da 1 a 1, ovvero solo 1
        # '1' | '1' 1 pagine
        '3 5 -', # => '5-' fregandomene dei confronti 3?5
        # '5-20' | '5-20' 16 pagine
        '-  10 13 17', # => '-10' ignorando 10?13?17
        # '1-10' | '1-10' 10 pagine
        '3 5-7 10', # => '5-7' fregandomene dei confronti 3?5 e 7?10
        # '5-7' | '5-7' 3 pagine
        '3 5 7-10 13 17', # => '7-10' ignorando 3?5?7 e 10?13?17
        # '7-10' | '7-10' 4 pagine
        '--',  # => tutto il file
        # '1-20' | '1-20' 20 pagine
        '--10',  # => '-C0'
        # '1-10' | '1-10' 10 pagine
        '3--',  # => 'An-'
        # '3-20' | '3-20' 18 pagine
        '3--10',  # => 'An-C0'
        # '3-10' | '3-10' 8 pagine
        '13--10',  # => 'An-C0'
        # '13-10' | '13-10' 4 pagine
        '-7-',  # => 'B0'
        # '7' | '7' 1 pagine
        '-7-10',  # => B<=C ? '-C0' : 'Bn-C0'
        # '1-10' | '1-10' 10 pagine
        '-17-10',  # => B<=C ? '-C0'1 : 'Bn-C0'
        # '17-10' | '17-10' 8 pagine
        '3-7-',  # => A<=B ? 'An-' : 'An-B0'
        # '3-20' | '3-20' 18 pagine
        '13-7-',  # => A<=B ? 'An-' : 'An-B0'
        # '13-7' | '13-7' 7 pagine

        '7-7-7', # A=C -> '7' 1 pagine
        '7-7-17', # A<=B<=C -> '7-17' 11 pagine
        '7-7-25', # A<=B<=C -> '7-20' 14 pagine
        '7-17-7', # A=C -> '7' 1 pagine
        '7-17-17', # A<=B<=C -> '7-17' 11 pagine
        '7-17-25', # A<=B<=C -> '7-20' 14 pagine
        '7-25-7', # A=C -> '7' 1 pagine
        '7-25-17', # ? A-B -> '7-20' 14 pagine
        '7-25-25', # A<=B<=C -> '7-20' 14 pagine
        '17-7-7', # A>=B>=C -> '17-7' 11 pagine
        '17-7-17', # A=C -> '17' 1 pagine
        '17-7-25', # ? A-B -> '17-7' 11 pagine
        '17-17-7', # A>=B>=C -> '17-7' 11 pagine
        '17-17-17', # A=C -> '17' 1 pagine
        '17-17-25', # A<=B<=C -> '17-20' 4 pagine
        '17-25-7', # ? A-B -> '17-20' 4 pagine
        '17-25-17', # A=C -> '17' 1 pagine
        '17-25-25', # A<=B<=C -> '17-20' 4 pagine
        '25-7-7', # A>=B>=C -> '20-7' 14 pagine
        '25-7-17', # ? A-B -> '20-7' 14 pagine
        '25-7-25', # A=C -> '20' 1 pagine
        '25-17-7', # A>=B>=C -> '20-7' 14 pagine
        '25-17-17', # A>=B>=C -> '20-17' 4 pagine
        '25-17-25', # A=C -> '20' 1 pagine
        '25-25-7', # A>=B>=C -> '20-7' 14 pagine
        '25-25-17', # A>=B>=C -> '20-17' 4 pagine
        '25-25-25', # A=C -> '20' 1 pagine

        # creati da Gemini 3
        # 1. Estremi mancanti e "vuoti":
        "", # tutto
        # '1-20' | '1-20' 20 pagine
        "- 5, 15   -",  # (Dovrebbe interpretare 1-5 e 15-20)
        # '1-5' | '1-5, 15-20' 11 pagine
        "-  ",  # (Dovrebbe restituire l'intero documento 1-20)
        # '1-20' | '1-20' 20 pagine

        # 2. Inversioni e Rotazioni:
        "10  -  2 S",  # (Decrescente con rotazione imposta Sud)
        # '10-2 S' | '10-2 S' 9 pagine
        "5-5 n",  # (Singola pagina espressa come intervallo con rotazione aggiuntiva Nord)
        # '5' | '5' 1 pagine

        # 3. Stringhe con spazi "creativi":
        " 1 - 3 E , 18-20 w ",  # (Spazi prima, dopo e tra i trattini/virgole)
        # '1-3 E' | '1-3 E, 18-20 w' 6 pagine

        # 4. Casi Limite (Out of Bounds):
        "18-25",  # (Il 25 supera il maxPages. Il parser lo taglia a 20 o solleva errore?)
        # '18-20' | '18-20' 3 pagine
        "0-5",  # (Esiste la pagina 0 o il tuo sistema parte da 1?)
        # '1-5' | '1-5' 5 pagine

        # 5. Input Malformato (Il "Dito dell'Utente"):
        "1-5-10 N",  # (Doppio trattino: errore o prende il primo e l'ultimo?)
        # '1-20 N' | '1-20 N' 20 pagine
        "1--10 N", # interpretato "1-10 N"
        # '1-10 N' | '1-10 N' 10 pagine
        "7:W",  # (Uso dei due punti invece del trattino o spazio)
        # '7 W' | '7 W' 1 pagine
        "abc-def",  # (Lettere dove dovrebbero esserci numeri)
        # '1-20 e' | '1-20 e' 20 pagine (per ogni intervallo, la 1° direzione è quella che conta!)

        # 6. Intervalli Sovrapposti:
        "1-10, 5-15",  # (Pypdf estrarrà le pagine 5-10 due volte o le unificherà?)
        # '1-10' | '1-10, 5-15' 21 pagine (l'user vuole duplicarle)

        # 7. Solo Rotazione (Senza numeri):
        "S, n",  # (Se scrivo solo la lettera senza numeri, il parser fallisce o ruota tutto?)
        # '1-20 S' | '1-20 S, 1-20' 40 pagine

        # 8. Separatori e trattini multipli:
        "1---5 ,,, 10--12 S",  # (L'utente ha il dito pesante sui tasti)
        # Error | '10-12 S' 3 pagine (intervals ignora gli errori e gli intervalli vuoti)
        ", , 5-8 , ,",  # (Virgole senza numeri all'inizio, in mezzo e alla fine)
        # '1-20' | '5-8' 4 pagine (intervals ignora gli intervalli vuoti)

        # 9. Caratteri di rotazione ripetuti o contrastanti:
        "1-5 NNEESS",  # (Tante lettere di rotazione: prende l'ultima? Somma i gradi?)
        # '1-5 N' | '1-5 N' 5 pagine (vale la 1° direzione)
        "10-15 n W S e",  # (Un mix di minuscole e maiuscole sparse)
        # '10-15' | '10-15' 6 pagine (ha preso 'n' che è di default)

        # 10. Inversioni estreme con rotazione:
        "20-1 W , 1-20 E",  # (Tutto il documento al contrario verso Ovest, poi tutto dritto verso Est)
        # '20-1 W' | '20-1 W, 1-20 E' 40 pagine (l'user vuole duplicare le pagine)

        # 11. Sintassi "sporca" ma comprensibile:
        "1- 5 , 10 -15 S , 20 - 18",  # (Spazi messi a caso tra i trattini e i numeri)
        # '1-5' | '1-5, 10-15 S, 20-18' 14 pagine
        "5-5-5-5 N",  # (Cosa succede con 4 numeri e 3 trattini?)
        # Error | '' 0 pagine (intervalli non validi!)

        # 12. Lettere senza numeri in mezzo a intervalli:
        "1-5, S, 10-15",  # (La 'S' da sola in mezzo a due intervalli numerici viene applicata a tutto o ignorata?)
        # '1-5' | '1-5, 1-20 S, 10-15' 31 pagine

        # 13. Il test "Gatto sulla tastiera":
        "1-5 n, , - , 10-12, e, w, 20-15"
        # '1-5' | '1-5, 1-20, 10-12, 1-20 e, 1-20 w, 20-15' 74 pagine
        # ricorda: ', ,' produce '' mentre ', - ,' produce '1-20'
    ]
    print('1° intervallo')
    for stringa in stringhe:
        try:
            interv=Interval.parse(stringa, maxPagine)
            print(repr(interv.toString()), '|', stringa)
        except ValueError as e:
            print(e,'|', stringa)
    print('')
    print('intervalli')
    for stringa in stringhe:
        try:
            intervalli= intervalsParse(stringa, maxPagine)
            print(repr(intervalsToString(intervalli)),intervalsPagesCount(intervalli),'pagine','|', stringa)
        except ValueError as e:
            print(e,'|', stringa)
    ...
# /_test_Intervals_parse_
_test_Intervals_parse_()

def _create_pdf_examples_():
    from pypdf import PdfWriter
    # crea un file protetto da password con una pagina vuota
    pdfPath='D:\\PDF_tests\\file_protetto.pdf'
    if not os.path.exists(pdfPath):
        writer=PdfWriter()
        writer.add_blank_page(width=595.276, height= 841.89) #A4
        writer.encrypt('12345')
        with open(pdfPath, 'wb') as f:
            writer.write(f)
        print('creato', pdfPath)

    # crea un file con 0 pagine
    pdfPath='D:\\PDF_tests\\file_vuoto.pdf'
    if not os.path.exists(pdfPath):
        writer = PdfWriter()
        with open(pdfPath, 'wb') as f:
            writer.write(f)
        print('creato', pdfPath)

    from pypdf.generic import NameObject, DictionaryObject, ArrayObject, TextStringObject
    # crea un file compilabile (AcroForm)
    pdfPath = 'D:\\PDF_tests\\file_compilabile.pdf'
    if not os.path.exists(pdfPath):
        writer = PdfWriter()
        writer.add_blank_page(width=595.276, height=841.89)  # A4
        if '/AcroForm' not in writer.root_object:
            writer.root_object.update({NameObject('/AcroForm'):
                                           DictionaryObject({NameObject('/Fields'):ArrayObject(),
                                                             NameObject('/NeedAppearances'):NameObject('true')})})
        writer.update_page_form_field_values(writer.pages[0], {"Campo1": "Scrivi campo 1 ..."})
        with open(pdfPath, 'wb') as f:
            writer.write(f)
        print('creato', pdfPath)

    ### NO
    # crea un file compilabile (AcroForm)
    pdfPath = 'D:\\PDF_tests\\file_compilabile2.pdf'
    if not os.path.exists(pdfPath):
        writer = PdfWriter()
        writer.add_blank_page(width=595.276, height=841.89)  # A4
        writer.add_blank_page(width=595.276, height=841.89)  # A4
        if '/AcroForm' not in writer.root_object:
            writer.root_object.update({NameObject('/AcroForm'):
                                           DictionaryObject({NameObject('/Fields'): ArrayObject(),
                                                             NameObject('/NeedAppearances'): NameObject('true')})})
        campiDaCreare=['Nome', 'Cognome', 'Note']
        for nome in campiDaCreare:
            campoDict=DictionaryObject({NameObject('/T'):TextStringObject(nome),
                                        NameObject('/FT'):NameObject('/Tx'),})
            # Tx = Text field
            dObj: DictionaryObject=writer.root_object['/AcroForm']
            dObj['/Fields'].append(campoDict)
        writer.update_page_form_field_values(writer.pages[0],
                                             {"Nome": "Scrivi Nome ...", "Cognome": "Scrivi Cognome ..."})
        writer.update_page_form_field_values(writer.pages[1], {"Note": "Scrivi Note ..."})
        with open(pdfPath, 'wb') as f:
            writer.write(f)
        print('creato', pdfPath)
    ...
# /_create_pdf_examples_
#_create_pdf_examples_()

def segnala_progresso(dictCallback):
    if 'index' in dictCallback:
        print(f"Avanzamento: {1+dictCallback['index']}/{dictCallback['total']}")
        if dictCallback['status']=='OK':
            print(f"Creato: {Path(dictCallback['pathFile']).name}")
        else:
            print(f"{Path(dictCallback['pathFile']).name}: {dictCallback['status']}")
    else:
        print(dictCallback['status'])

def _test_pdf_engine_():
    ## pagesCountAndCheck()
    paths =[
        123456, # NO non stringa
        'D:\\PDF_tests\\', # NO cartella
        'D:\\PDF_tests\\file_compilabile', # NO estensione
        'D:\\PDF_tests\\file_protetto.pdf', # NO crittografato
        'D:\\PDF_tests\\file_vuoto.pdf',  # NO vuoto
        'D:\\PDF_tests\\esempio modulo.pdf', # creato da LibreOffice con AcroForm
        'D:\\PDF_tests\\Modulo di esempio.pdf', # OK, creato da Word, ma appiattito
        'D:\\PDF_tests\\Metalinguaggi.pdf', # tenuto aperto, ma ok
        'D:\\PDF_tests\\Meta linguaggi.pdf', # NO inesistente
        'D:\\PDF_tests\\file_compilabile.pdf', # NO con AcroForm
        'D:\\PDF_tests\\copilot-handbook.pdf', # ok
    ]
    for path in paths:
        try:
            if checkPdf(path):
                pagine = pagesCount(path)
            print(path,'ha',pagine,'pagine')
        except Exception as e:
            print(e)

    ## fake split()
    pathInput='D:\\PDF_tests\\copilot-handbook.pdf'
    esempiErratifilesOutputs=[
        'ciao ciao', # str NO
        ['ciao', 'bau','miao'], # list NO
        dict(), # NO vuoto
        {'pippo':'pinco pallino'}, # value non List
        {'pippo': ['Qui','Quo','Qua']},  # value List ma non di Interval
        {'pippo': None}, # value OK, key no!
        {'pippo': []}, # value OK, key no!
        {'pippo': Interval(1,6,Rotation.e)}, # value OK, key no!
        {'pippo': [Interval(1, 6, Rotation.e), Interval(5,10)]}, # value OK, key no!
        {'pippo': [Interval(1, 6, Rotation.e), Interval(5, 10)],
         'pluto': [Interval(1, 5), Interval(7, 10,Rotation.s)]},  # value OK, key no!
    ]
    for esempio in esempiErratifilesOutputs:
        try:
            print(str(esempio))
            result = split(pathInput, esempio)
            print(result)
        except Exception as e:
            print(e)
        print()

    ## fake merge()
    paths =[
        123456, # NO non stringa
        'D:\\PDF_tests\\', # NO cartella
        'D:\\PDF_tests\\file_compilabile', #NO estensione
        'D:\\PDF_tests\\file_prova.pdf',
    ]
    for path in paths:
        try:
            print(str(path))
            result = merge([], path)
            print(result)
        except Exception as e:
            print(e)
        print()

    path='D:\\PDF_tests\\file_prova.pdf'
    esempiErratifilesInputs=[
        'ciao ciao', # str NO
        {'ciao', 'bau','miao'}, # set NO
        {'ciao':1, 'bau':2, 'miao':3},  # dict NO
        list(), # NO vuoto
        ['pippo', 'pinco pallino'],  # ha elementi sbagliati
        [('pippo','pinco pallino')], # value non List
        {'pippo': ['Qui','Quo','Qua']},  # value List ma non di Interval
        {'pippo': None}, # value OK, key no!
        {'pippo': []}, # value OK, key no!
        {'pippo': Interval(1,6,Rotation.e)}, # value OK, key no!
        {'pippo': [Interval(1, 6, Rotation.e), Interval(5,10)]}, # value OK, key no!
    ]
    for esempio in esempiErratifilesInputs:
        try:
            result = merge(esempio, path)
            print(result)
        except Exception as e:
            print(e)
        print()
    ...
# /_test_pdf_engine_
_test_pdf_engine_()
