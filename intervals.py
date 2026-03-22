from enum import Enum
import re

def unsignedIntegersParse(string: str) -> list[int]:
    """Gets the (unsigned) integers from a string.

    :param string: String to parse
    :return: Returns a list[int] or raise a TypeError or raise a ValueError
    """
    intArray = []
    # se string è di tipo list o tuple può cercare se ci sono interi
    if isinstance(string, (list,tuple)):
        for s in string:
            try:
                i=int(float(s))
                intArray.append(abs(i))
            except:
                pass # non lanciare errori
        if len(intArray)>0:
            return intArray
        else:
            raise TypeError('Input non valido! Attesa: stringa o numero o list[numeri] o tupla(numeri)')
    # se string è di tipo float o int lo converte e lo restituisce
    if not isinstance(string, str):
        try:
            i = int(float(string))
            intArray.append(abs(i))
            return intArray
        except:
            raise TypeError(f'Input non valido! Attesa: stringa o numero o list[numeri] o tupla(numeri).\n'
                            f'Non {type(string)}')

    matches = re.findall(r'\d+', string)
    if not matches:
        raise ValueError('Intero (senza segno) non trovato nella stringa!')
    for m in matches:
        intArray.append(int(m))
    return intArray
# /integersParse

def signedIntegersParse(string: str) -> list[int]:
    """Gets the (signed) integers from a string.

    :param string: String to parse
    :return: Returns a list[int] or raise a TypeError or raise a ValueError
    """
    intArray=[]
    # se string è di tipo list o tuple può cercare se ci sono interi
    if isinstance(string, (list,tuple)):
        for s in string:
            try:
                i=int(float(s))
                intArray.append(i)
            except:
                pass # non lanciare errori
        if len(intArray)>0:
            return intArray
        else:
            raise TypeError('Input non valido! Attesa: stringa o numero o list[numeri] o tupla(numeri)')
    # se string è di tipo float o int lo converte e lo restituisce
    if not isinstance(string, str):
        try:
            i=int(float(string))
            intArray.append(i)
            return intArray
        except:
            raise TypeError(f'Input non valido! Attesa: stringa o numero o list[numeri] o tupla(numeri).\n'
                            f'Non {type(string)}')

    matches=re.findall(r'[+-]?\d+', string)
    if not matches:
        raise ValueError('Intero (con segno) non trovato nella stringa!')
    for m in matches:
        intArray.append(int(m))
    return intArray
# /integersParse

def pageFromString(string: str, isFirst: bool, maxPages: int) -> int:
    """Gets the page number from a string.

    :param string: String to parse
    :param isFirst: Does it have to find the first int or the last one?
    :param maxPages: Maximum page limit
    :return: The result must be between 1 and maxPages (inclusive) or raise a TypeError
    """
    # a prova di stupido
    if not isinstance(string, (str,bytes)):
        raise TypeError(f"string deve essere di tipo str non {type(string)}")
    if not isinstance(maxPages, int):
        raise TypeError(f"maxPages deve essere di tipo int non {type(maxPages)}")

    try:
        # cerca tutti gli interi della stringa
        pages = unsignedIntegersParse(string)
        if not isFirst:
            pages=list(reversed(pages))
        for pag in pages:
            if 0 < pag <= maxPages:
                return pag
        # per arrivare qui vuol dire che la lista ha items: == 0 o > maxPages
        if pages[0] > maxPages:
            return maxPages
        #if pages[0] == 0:
        return 1
    except ValueError, TypeError:
        return 1 # sarebbe da gestire meglio
# /pageFromString

class Rotation(Enum):
    """Clockwise rotation in multiple of 90°.\n
    The values resemble the Cardinal Points.\n
    If the value is less than 360°, it indicates the added rotation;
    otherwise, it indicates the imposed rotation.
    """
    # le coppie [n,N] [north, North] possono confondere perciò ha fatto così:
    n = 0 # <- valore di default
    e = 90
    s = 180
    w = 270
    North = 360
    East = 450
    South = 540
    West = 630
    def __str__(self) -> str:
        # Es invece di 'Rotation.North' restituisce solo 'North'
        return self.name
    # def _value_(self):
    #     return self.value
    def toString(self) -> str:
        """Gets the string abbreviation with an only character.

        :return: ['' | 'e' | 's' | 'w' | 'N' | 'E' | 'S' | 'W']
        """
        if self.name=='n':
            return ''
        return self.name[0]
    # /toString

    def angle(self) ->int:
        """Gets the angle of the clockwise rotation.

        :return: [0 | 90 | 180 | 270]
        """
        return self.value % 360
    # /angle

    def isAddedRotation(self) -> bool:
        """This is an added rotation?

        :return: [added rotation == True | imposed rotation == False]
        """
        return self.value < 360
    # /isAddedRotation

    def toLongString(self) -> str:
        """Gets the long string with all the information.

        :return: '<name: ..., value: ..., angle: ..., isAdded: ...>'
        """
        return f'<name: {self.name}, value: {self.value}, angle: {self.angle()}, isAdded: {self.isAddedRotation()}>'
    # /toString

    @staticmethod
    def fromInt(value: int) -> Rotation:
        """Gets the Rotation from a clockwise angle.

        :param value: Clockwise angle
        :return: Rotation
        """
        if value is None:
            return Rotation.n
        if isinstance(value, Rotation):
            return value
        elif isinstance(value, str):
            return Rotation.fromChar(value)
        # qualsiasi altro type sia, lo converte in int
        try:
            v = int(value)
            # v finisce nel range [0, 720) e come multiplo di 90
            v = ((v % 720) // 90) * 90
            return Rotation(v)
        except (ValueError,TypeError):
            return Rotation.n
    # /fromInt

    @staticmethod
    def fromChar(string:str) -> Rotation:
        """Gets the rotation from a character.

        :param string: From the string it will take the first character
        :return: Rotation
        """
        if string is None:
            return Rotation.n
        if isinstance(string, Rotation):
            return string
        if isinstance(string, int):
            return Rotation.fromInt(string)
        # qualsiasi altro type sia, lo converte in str
        s = str(string).strip()
        if not s:
            return Rotation.n
        # cerca il 1° carattere valido da una stringa sporca
        searchChar = re.search(r'[NESWnesw]',s)
        if not searchChar:
            return Rotation.n

        match searchChar.group(0):
            case 'e':
                return Rotation.e
            case 's':
                return Rotation.s
            case 'w':
                return Rotation.w
            case 'N':
                return Rotation.North
            case 'E':
                return Rotation.East
            case 'S':
                return Rotation.South
            case 'W':
                return Rotation.West
            case _:
                return Rotation.n
    # /fromChar
# /Rotation

class Interval:
    """Indicates the single interval with a rotation. ('n' is implied)\n
    Ex: '1-5 S', '7 E', '13-10 [n]', '15-20 w'.
    """
    def __init__(self, fromPag: int, toPag: int=None, rot: Rotation=Rotation.n):
        """Interval constructor.

        :param fromPag: First page of the range (index from 1)
        :param toPag: Last page of the range (inclusive, index from 1). If None toPag == fromPag
        :param rot: Interval Rotation (default Rotation.n)
        """
        # se fromPage non è int lo diventa SEMPRE!
        try:
            self.fromPage = int(fromPag)
        except (ValueError,TypeError):
            self.fromPage = 1
        if self.fromPage < 1:
            self.fromPage = 1

        # se toPage non è int lo diventa SEMPRE!
        if toPag is None:
            self.toPage = self.fromPage
        else:
            try:
                self.toPage = int(toPag)
            except (ValueError, TypeError):
                self.toPage = self.fromPage
            if self.toPage < 1:
                self.toPage = self.fromPage

        # se rot non è Rotation lo diventa SEMPRE!
        if isinstance(rot, Rotation):
            self.rotation = rot
        elif isinstance(rot, str):
            self.rotation = Rotation.fromChar(rot)
        else:
            self.rotation = Rotation.n
    # /__init__

    def __str__(self) -> str:
        """Gets the string with the base information.

        :return: '<self.fromPage= ..., self.toPage= ..., self.rotation=<Rotation...: ...>>'
        """
        return f"<{self.fromPage=} {self.toPage=} {self.rotation=}>"

    def toString(self) -> str:
        """Convert from Interval to string.

        :return: ex: ['9 E' | '5-10 w']
        """
        if self.fromPage == self.toPage:
            return f"{self.fromPage} {self.rotation.toString()}".strip()
        return f"{self.fromPage}-{self.toPage} {self.rotation.toString()}".strip()
    # /toString

    def pagesCount(self)-> int:
        """Gets the total number of pages in the Interval.

        :return: ex: '5-10 w' gets 6 (pages)
        """
        return abs(self.toPage - self.fromPage) + 1
    # /pagesCount

    def toLongString(self) -> str:
        """Gets the long string with all the information.

        :return: '<fromPage: ..., toPage: ..., rotation: ..., pages: ...>'
        """
        return f'<fromPage: {self.fromPage}, value: {self.toPage}, rotation: {self.rotation.name}, pages: {self.pagesCount()}>'
    # /toString

    @staticmethod
    def parse(string: str, maxPages: int, index: int=0)-> Interval:
        """Get an Interval from a string.

        :param string: String to parse
        :param maxPages: Total pages of the PDF (this is used to stay within the Interval limits)
        :param index: If 'string' is a list of interval, which one do you want to extract based on the index?
        :return: Interval or raise a [TypeError | ValueError | IndexError]
        """
        # a prova di stupido
        if isinstance(string, Interval):
            return string
        if isinstance(string, (int, float)):
            pag=int(float(string))
            return Interval(pag)
        if not isinstance(string, str):
            raise TypeError(f"'string' non valido! Attesa stringa o numero o Interval, non {type(string)}")
        if not isinstance(maxPages, int):
            raise TypeError(f"'maxPages' non valido! Atteso un intero positivo, non {type(string)}")
        if maxPages < 1:
            raise ValueError(f"'maxPages' = {maxPages}! Il valore deve essere maggiore di 0!")
        if not isinstance(index, int):
            # magari fosse un float o un str
            try:
                index = int(float(index))
            except:
                raise TypeError(f"'index' non valido! Atteso un numero, non {type(string)}")
        if len(string) == 0:
            return Interval(1,maxPages)

        # ',' è il separatore di intervalli
        subStrings = string.split(',')
        subStrings = [s.strip() for s in subStrings]

        # ora occorre sapere quale analizzare
        if -len(subStrings) > index or index >= len(subStrings):
            # gli index corrispondono a quelli usati per i chars di una stringa
            # o per una list, quindi ok [0, len()) e ok [-len(), -1]
            # ovvero ok [-len(), len())
            raise IndexError(
                f"'index' = {index}! Il valore deve essere compreso tra {-len(subStrings)} e {len(subStrings) - 1} inclusi!")
        string = subStrings[index]
        if len(string) == 0:
            return Interval(1,maxPages)

        # trova la direzione/rotazione
        match = re.search(r'[NESWnesw]', string.strip())
        if match:
            rotEnum = Rotation.fromChar(match.group(0))
        else:
            rotEnum = Rotation.n
        # rimuove tutti i caratteri non validi
        string = re.sub(r'[^0-9 -]', ' ', string)
        while True:
            if string.find('  ') >= 0:
                string = string.replace('  ', ' ')
            else:
                break
        string=string.strip()
        if len(string) == 0:
            return Interval(1,maxPages,rotEnum)

        # inizia la vera analisi dell'intervallo!
        # OCCHIO! Non vengono gestiti gli _Error di pageFromString perché li passa
        # al chiamante di Interval.parse(), quest'ultimo li gestirà!
        if string.find('-')==-1:
            # pagina singola
            pag = pageFromString(string,True, maxPages)
            return Interval(pag,rot=rotEnum)

        # diventerà: 'A-B' (con A, B interi o gruppi di interi)
        subStrings = string.split('-')
        subStrings = [s.strip() for s in subStrings]
        if len(subStrings) == 2:
            # 4 casi ideali
            # se la sottostringa ha più A 'A0 A1 A2 ... An' prende l'ultima 'An'
            # se la sottostringa ha più B 'B0 B1 B2 ... Bn' prende la prima 'B0'
            if subStrings[0] == '' and subStrings[1] == '':
                # '-'
                return Interval(1,maxPages, rotEnum)
            elif subStrings[0] == '':
                # '-B'
                B = pageFromString(subStrings[1],True, maxPages)
                return Interval(1, B, rotEnum)
            elif subStrings[1] == '':
                # 'A-'
                A = pageFromString(subStrings[0],False, maxPages)
                return Interval(A,maxPages, rotEnum)
            else:
                # 'A-B'
                A = pageFromString(subStrings[0],False, maxPages)
                B = pageFromString(subStrings[1], True, maxPages)
                return Interval( A,  B, rotEnum)
            # /4 casi ideali
        elif len(subStrings) == 3:
            # 8 casi particolari accettati (2**3=8)
            # la stringa è nel formato 'A-B-C' (A, B, C interi o gruppi di interi)
            if subStrings[1] == '':
                # '?--?'
                if subStrings[0] == '' and subStrings[2] == '':
                    # '--' = '-'
                    return Interval(1,maxPages, rotEnum)
                elif subStrings[0] == '':
                    # '--C' = '-C' e prende il primo tra 'C0 C1 ... Cn'
                    C = pageFromString(subStrings[2], True, maxPages)
                    return Interval(1, C, rotEnum)
                elif subStrings[2] == '':
                    # 'A--' = 'A-' e prende l'ultima tra 'A0 A1 ... An'
                    A = pageFromString(subStrings[0], False, maxPages)
                    return Interval(A, maxPages, rotEnum)
                else:
                    # 'A--C' = 'A-C' e prende l'ultima tra 'A0 A1 ... An' e il primo tra 'C0 C1 ... Cn'
                    A = pageFromString(subStrings[0], False, maxPages)
                    C = pageFromString(subStrings[2], True, maxPages)
                    return Interval(A, C, rotEnum)
            elif subStrings[0] == '':
                # '-B-?'
                if subStrings[2] == '':
                    # '-B-' = 'B' e prende il primo 'B0 B1 ... Bn'
                    B = pageFromString(subStrings[1], True, maxPages)
                    return Interval(B,rot= rotEnum)
                else:
                    # '-B-C'
                    B = pageFromString(subStrings[1], False, maxPages)
                    C = pageFromString(subStrings[2], True, maxPages)
                    if B<=C:
                        # se B<=C viene interpretato come un mancato '-C' o '1-C'
                        # e prende il primo 'C0 C1 ... Cn'
                        return Interval(1, C, rotEnum)
                    else:
                        # altrimenti viene interpretato come 'B-C' con step -1,
                        # prende l'ultimo 'B0 B1 ... Bn' e il primo 'C0 C1 ... Cn'
                        return Interval(B, C, rotEnum)
            else:
                # 'A-B-?'
                A = pageFromString(subStrings[0], False, maxPages)
                B = pageFromString(subStrings[1], True, maxPages)
                if subStrings[2] == '':
                    # 'A-B-'
                    if A<=B:
                        # viene interpretato come 'A-' o 'A-max'
                        # e prende l'ultima 'A0 A1 ... An'
                        return Interval(A, maxPages, rotEnum)
                    else:
                        # viene considerato come 'A-B' con step -1,
                        # prende l'ultima 'A0 A1 ... An' e prende il primo 'B0 B1 ... Bn'
                        return Interval(A, B, rotEnum)
                else:
                    # 'A-B-C'. Per ogni confronto a coppia (es: C# ha X.CompareTo(Y))
                    # si ottengono 3 valori e per 3 confronti diventano 3**3=27 mini-casi
                    # Es: si prendono 3 interi: [7, 17, 27] e A, B, C possono assumere questi
                    # valori, si ottengono così i 27 mini-casi
                    C = pageFromString(subStrings[2], True, maxPages)
                    if A == C:
                        # raccoglie 9 mini-casi
                        # B viene ignorato e Interval diventa il mono-pagina 'A-C'
                        return Interval(A, C, rotEnum)
                    elif A<=B<=C:
                        # raccoglie 7 mini-casi
                        # B viene ignorato ancora e Interval diventa il range 'A-C'
                        return Interval(A, C, rotEnum)
                    elif A>=B>=C:
                        # raccoglie altri 7 mini-casi
                        # B viene ignorato ancora una volta e Interval diventa il range 'A-C' con step -1
                        return Interval(A, C, rotEnum)
                    else:
                        # rimangono 4 mini-casi: '7-25-17', '17-7-25', '17-25-7', '25-7-17'
                        # si potrebbero creare 2 Interval, ma cozzerebbe sia con la 1° condizione
                        # (ove i mini casi sarebbero 3 e non 9) e col fatto che Interval.parse()
                        # restituisce 1 intervallo solo! Quindi C è finalmente ignorato!
                        return Interval(A, B, rotEnum)
                    # /27 mini-casi
            # /8 casi particolari
        # NO '-' > 2, l'intervallo è formato male!
        raise ValueError(f"Intervallo non trovato nella stringa!")
    # /parse
# /Interval

def _intervalsParseOld_(stringOfIntervals: str, maxPages:int):
    """ Get list[Interval] from string.

    :param stringOfIntervals: String of intervals
    :param maxPages: Total pages of the PDF (this is used to stay within the Interval limits)
    :return: list[Interval]
    """
    # a prova di stupido
    if not isinstance(stringOfIntervals, (str, bytes)):
        raise TypeError(f"string deve essere di tipo str non {type(stringOfIntervals)}")
    if not isinstance(maxPages, int):
        raise TypeError(f"maxPages deve essere di tipo int non {type(maxPages)}")

    intervals=[]
    stringOfIntervals=stringOfIntervals.strip()
    # casi base
    if len(stringOfIntervals) == 0:
        interv = Interval(1, maxPages, Rotation.n)
        intervals.append(interv)
        return intervals
    match (stringOfIntervals):
        case '-' | 'n':
            interv = Interval(1, maxPages, Rotation.n)
            intervals.append(interv)
            return intervals
        case 'e':
            interv = Interval(1, maxPages, Rotation.e)
            intervals.append(interv)
            return intervals
        case 's':
            interv = Interval(1, maxPages, Rotation.s)
            intervals.append(interv)
            return intervals
        case 'w':
            interv = Interval(1, maxPages, Rotation.w)
            intervals.append(interv)
            return intervals
        case 'N':
            interv = Interval(1, maxPages, Rotation.North)
            intervals.append(interv)
            return intervals
        case 'E':
            interv = Interval(1, maxPages, Rotation.East)
            intervals.append(interv)
            return intervals
        case 'S':
            interv = Interval(1, maxPages, Rotation.South)
            intervals.append(interv)
            return intervals
        case 'W':
            interv = Interval(1, maxPages, Rotation.West)
            intervals.append(interv)
            return intervals
    # /casi base

    # ',' è il separatore di intervalli
    listOfIntervals=stringOfIntervals.split(',')
    listOfIntervals=[s.strip() for s in listOfIntervals]
    # '[NESWnesw]' è il carattere della rotazione (vale il 1° trovato)
    for strInterval in listOfIntervals:
        if len(strInterval)==0: # qui ignora gli intervalli vuoti, ci vuole almeno '-'
            continue
        # trova la direzione/rotazione
        match = re.search(r'[NESWnesw]', strInterval.strip())
        if match:
            rotEnum = Rotation.fromChar(match.group(0))
        else:
            rotEnum = Rotation.n
        # rimuove tutti i caratteri non validi
        strInterval = re.sub(r'[^0-9 -]', ' ', strInterval)
        while True:
            if strInterval.find('  ') >= 0:
                strInterval = strInterval.replace('  ', ' ')
            else:
                break
        strInterval=strInterval.strip()
        # inizia la vera analisi dell'intervallo
        if strInterval.find('-')==-1:
            # pagina singola
            pag = pageFromString(strInterval,True, maxPages)
            interv=Interval(pag,rot=rotEnum)
            intervals.append(interv)
        else:
            # diventerà: 'pagine da A a B' (A, B possono essere interi o gruppi di interi)
            partsInterval = strInterval.split('-')
            partsInterval = [s.strip() for s in partsInterval]
            if len(partsInterval) == 2:
                # 4 casi ideali
                # se la sottostringa ha più A 'A0 A1 A2 ... An' prende l'ultima 'An'
                # se la sottostringa ha più B 'B0 B1 B2 ... Bn' prende la prima 'B0'
                if partsInterval[0] == '' and partsInterval[1] == '':
                    # '-'
                    interv = Interval(1,maxPages, rotEnum)
                elif partsInterval[0] == '':
                    # '-B'
                    pag = pageFromString(partsInterval[1],True, maxPages)
                    interv = Interval(1, pag, rotEnum)
                elif partsInterval[1] == '':
                    # 'A-'
                    pag = pageFromString(partsInterval[0],False, maxPages)
                    interv = Interval(pag,maxPages, rotEnum)
                else:
                    # 'A-B'
                    fromPag = pageFromString(partsInterval[0],False, maxPages)
                    toPag = pageFromString(partsInterval[1], True, maxPages)
                    interv = Interval( fromPag,  toPag, rotEnum)
                intervals.append(interv)
                # /4 casi ideali
            elif len(partsInterval) == 3:
                # 8 casi particolari accettati (2**3=8)
                # la stringa è nel formato 'A-B-C' (A, B, C interi o gruppi di interi)
                if partsInterval[1] == '':
                    # '?--?'
                    if partsInterval[0] == '' and partsInterval[2] == '':
                        # '--' = '-'
                        interv = Interval(1,maxPages, rotEnum)
                    elif partsInterval[0] == '':
                        # '--C' prende il primo 'C0 C1 ... Cn'
                        pag = pageFromString(partsInterval[2], True, maxPages) # C
                        interv = Interval(1, pag, rotEnum)
                    elif partsInterval[2] == '':
                        # 'A--' prende l'ultima 'A0 A1 ... An'
                        pag = pageFromString(partsInterval[0], False, maxPages) # A
                        interv = Interval(pag, maxPages, rotEnum)
                    else:
                        # 'A--C' prende l'ultima 'A0 A1 ... An' e il primo 'C0 C1 ... Cn'
                        fromPag = pageFromString(partsInterval[0], False, maxPages) # A
                        toPag = pageFromString(partsInterval[2], True, maxPages) # C
                        interv = Interval(fromPag, toPag, rotEnum)
                elif partsInterval[0] == '':
                    # '-B-?'
                    if partsInterval[2] == '':
                        # '-B-' prende il primo 'B0 B1 ... Bn'
                        pag = pageFromString(partsInterval[1], True, maxPages) # B
                        interv = Interval(pag,rot= rotEnum)
                    else:
                        # '-B-C'
                        fromPag = pageFromString(partsInterval[1], False, maxPages) # B
                        toPag = pageFromString(partsInterval[2], True, maxPages) # C
                        if fromPag<=toPag:
                            # se B<=C viene interpretato come un mancato '-C' o '1-C'
                            # e prende il primo 'C0 C1 ... Cn'
                            interv = Interval(1, toPag, rotEnum)
                        else:
                            # altrimenti viene interpretato come 'B-C' con step -1,
                            # prende l'ultimo 'B0 B1 ... Bn' e il primo 'C0 C1 ... Cn'
                            interv = Interval(fromPag, toPag, rotEnum)
                else:
                    # 'A-B-?' = 'A-B-' oppure 'A-B-C', C viene ignorato!
                    fromPag = pageFromString(partsInterval[0], False, maxPages)  # A
                    toPag = pageFromString(partsInterval[1], True, maxPages)  # B
                    if fromPag<=toPag:
                        # se A<=B viene interpretato come un mancato 'A-' o 'A-max'
                        # e prende l'ultima 'A0 A1 ... An'
                        interv = Interval(fromPag, maxPages, rotEnum)
                    else:
                        # altrimenti viene considerato come 'A-B' con step -1,
                        # prende l'ultima 'A0 A1 ... An' e prende il primo 'B0 B1 ... Bn'
                        interv = Interval(fromPag, toPag, rotEnum)
                # /8 casi particolari
                intervals.append(interv)
            else:
                # NO '-' > 2, l'intervallo è ignorato!
                continue
        # /if con '-'
    # /for strInterv in listInterv:
    return intervals
# /_intervalsParseOld_

def intervalsParse(stringOfIntervals: str, maxPages:int) -> list[Interval]:
    """ Get list[Interval] from string.

    :param stringOfIntervals: String of intervals
    :param maxPages: Total pages of the PDF (this is used to stay within the Interval limits)
    :return: list[Interval] or raise a TypeError
    """
    # a prova di stupido
    if not isinstance(stringOfIntervals, (str, bytes)):
        raise TypeError(f"string deve essere di tipo str non {type(stringOfIntervals)}")
    if not isinstance(maxPages, int):
        # magari fosse un float o un str
        try:
            maxPages = int(float(maxPages))
        except:
            raise TypeError(f"maxPages deve essere di tipo int non {type(maxPages)}")

    intervals=[]
    stringOfIntervals=stringOfIntervals.strip()
    # casi base
    if len(stringOfIntervals) == 0:
        interv = Interval(1, maxPages, Rotation.n)
        intervals.append(interv)
        return intervals
    match (stringOfIntervals):
        case '-' | 'n':
            interv = Interval(1, maxPages, Rotation.n)
            intervals.append(interv)
            return intervals
        case 'e':
            interv = Interval(1, maxPages, Rotation.e)
            intervals.append(interv)
            return intervals
        case 's':
            interv = Interval(1, maxPages, Rotation.s)
            intervals.append(interv)
            return intervals
        case 'w':
            interv = Interval(1, maxPages, Rotation.w)
            intervals.append(interv)
            return intervals
        case 'N':
            interv = Interval(1, maxPages, Rotation.North)
            intervals.append(interv)
            return intervals
        case 'E':
            interv = Interval(1, maxPages, Rotation.East)
            intervals.append(interv)
            return intervals
        case 'S':
            interv = Interval(1, maxPages, Rotation.South)
            intervals.append(interv)
            return intervals
        case 'W':
            interv = Interval(1, maxPages, Rotation.West)
            intervals.append(interv)
            return intervals
    # /casi base

    # ',' è il separatore di intervalli
    listOfIntervals=stringOfIntervals.split(',')
    listOfIntervals=[s.strip() for s in listOfIntervals]

    for strInterval in listOfIntervals:
        if len(strInterval)==0: # qui ignora gli intervalli vuoti, ci vuole almeno '-'
            continue
        try:
            interv = Interval.parse(strInterval,maxPages,0)
            intervals.append(interv)
        except (TypeError, ValueError, IndexError):
            # ogni intervallo che da problemi viene ignorato
            continue
    # /for strInterv in listInterv:
    return intervals
# /intervalsParse

def intervalsToString(intervals: list[Interval]) -> str:
    """Gets a string from a list of Interval.

    :param intervals: list[Interval]
    :return: well-formatted string of intervals
    """
    # return ', '.join([i.toString() for i in intervals])

    # a prova di stupido
    if not isinstance(intervals,(list,tuple)):
        return ''
    filteredStrings=[]
    for item in intervals:
        if isinstance(item,Interval):
            filteredStrings.append(item.toString())
    return ', '.join(filteredStrings)
# /intervalsToString

def intervalsPagesCount(intervals: list[Interval]) -> int:
    """Get the total number of (duplicate) pages of the intervals.

    :param intervals: list[Interval]
    :return: ex: '5-10, 8-12 e' gets 6+5 = 13 (pages)
    """
    #return sum(i.pagesCount() for i in intervals)

    # a prova di stupido
    if not isinstance(intervals,(list,tuple)):
        return 0
    sum=0
    for item in intervals:
        if isinstance(item,Interval):
            sum +=item.pagesCount()
    return sum
# /intervalsPagesCount

def infoIntervals():
    print("Esempi intervalli: '15 S', '5-10 W', '13-9 E', '7 N' o '7'")

def _infoIntervals_():
    """Provides information on using Intervals
    """
    print("""\
Negli intervalli:
    - La pagina singola è indicata da un intero (es '9')
    - Un gruppo di pagine consecutive da un trattino '-' tra i 2 interi (es '5-8' corrisponde a '5,6,7,8')
    - E' permesso il gruppo invertito (es '9-6' corrisponde a '9,8,7,6')
    - Sia al gruppo che alla singola pagina si può aggiungere il suffisso della rotazione ['N','E','S','W']
      che corrisponde alla rotazione in output rispettivamente di [0°,90°,180°,270°]. Di default 'N' = 0°.
      (es '15 S', '5-10 W', '13-9 E', '7 N' o '7')
    - Gli intervalli (pagina singola o gruppo) vengono separati dalla virgola ',' 
      (es '9, 13-9 E, 15 S, 5-10'. Da notare che in questo caso la pagina 9 comparirà 3 volte nell'output
       e la pagina 10 comaprirà 2 volte, poiché è quest'esempio è l'abbreviazione di: 
       '9 N, 13 E, 12 E, 11 E, 10 E, 9 E, 15 S, 5 N, 6 N, 7 N, 8 N, 9 N, 10 N'
     """)
    ...
# /infoIntervals