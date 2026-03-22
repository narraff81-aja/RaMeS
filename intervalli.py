from enum import Enum
import re
### This Module will be Deprecated: Use intervals.py ###
class Rotazione(Enum):
    """Rotazione a multipli di 90°.\n
    I valori ricordano i punti cardinali.
    """
    N = 0
    E = 90
    S = 180
    W = 270
    def __str__(self):
        if self.name.upper()=='N':
            return ''
        return self.name.upper()
    # def _value_(self):
    #     return self.value
# /Rotazione

class Intervallo:
    """Indica il singolo intervallo con la rotazione. 'N' può essere sottinteso\n
    Es: '1-5 S', '7 E', '13-10 [N]', '15-20 W'.
    """
    def __init__(self, daPag: int, aPag: int=None, rot: Rotazione=Rotazione.N):
        self.da = daPag
        if aPag is not None:
            self.a = aPag
        else:
            self.a = daPag
        self.rotazione = rot

    def __str__(self) -> str:
        """
        Conversione di Intervallo in stringa
        :return:
        """
        if self.da == self.a:
            return f"{self.da} {self.rotazione.__str__()}".strip()
        return f"{self.da}-{self.a} {self.rotazione.__str__()}".strip()

    def string(self) -> str:
        """
        ToString() con tutte le proprietà
        :return:
        """
        return f"{self.da=} {self.a=} {self.rotazione=}"
# /Intervallo

def intDaStr(stringa: str, primo:bool, maxPagine:int) -> int:
    """Simile a int.Parse() per trovare il primo/ultimo int da una stringa che contiene spazi

    :param stringa: stringa in input
    :param primo: prende il 1° intero che trova oppure l'ultimo?
    :param maxPagine: il risultato deve essere tra 1 e maxPagine compresi
    :return:
    """
    stringa=stringa.strip()
    if primo:
        idSpazio = stringa.find(' ')
        if idSpazio > -1:
            stringa = stringa[:idSpazio]
        pag= int(stringa)
    else:
        idSpazio = stringa.rfind(' ')
        if idSpazio > -1:
            stringa = stringa[idSpazio:].strip()
        pag= int(stringa)

    if pag < 1:
        return 1
    elif pag > maxPagine:
        return maxPagine
    else:
        return pag
# /intDaStr

def intervalliParse(stringaIntervalli: str, maxPagine:int):
    """ Ottiene list[Intervallo] dalla stringa.

    :param stringaIntervalli: lista di Intervallo in formato stringa
    :param maxPagine: pagine totali del PDF (serve a rimanere nei limiti dell'Intervallo)
    :return: lista di Intervallo
    """
    intervalli=[]
    stringaIntervalli=stringaIntervalli.upper().strip()
    # casi base
    if len(stringaIntervalli)==0 or stringaIntervalli=='-' or stringaIntervalli=='N':
        interv=Intervallo(1,maxPagine,Rotazione.N)
        intervalli.append(interv)
        return intervalli
    if stringaIntervalli=='E':
        interv=Intervallo(1,maxPagine,Rotazione.E)
        intervalli.append(interv)
        return intervalli
    if stringaIntervalli=='S':
        interv=Intervallo(1,maxPagine,Rotazione.S)
        intervalli.append(interv)
        return intervalli
    if stringaIntervalli=='W':
        interv=Intervallo(1,maxPagine,Rotazione.W)
        intervalli.append(interv)
        return intervalli

    # ',' è il separatore di intervalli
    listInterv=stringaIntervalli.split(',')
    listInterv=[s.strip() for s in listInterv]
    # '[NESW]' è la rotazione (vale la 1° trovata)
    for strInterv in listInterv:
        strInterv=strInterv.strip()
        if len(strInterv)==0: # ignora gli intervalli vuoti
            continue
        # trova la direzione/rotazione
        match = re.search(r'[NESW]', strInterv, re.IGNORECASE)
        if match:
            rotEnum = Rotazione[match.group(0).upper()]
        else:
            rotEnum = Rotazione.N
        # rimuove tutti i caratteri non validi
        strInterv = re.sub(r'[^0-9 -]', ' ', strInterv)
        while True:
            if strInterv.find('  ') >= 0:
                strInterv = strInterv.replace('  ', ' ')
            else:
                break
        strInterv=strInterv.strip()
        # ora rimangono: 'pagine singole' o 'pagine da _ a _'
        if len(strInterv)==0 or strInterv=='-':
            interv = Intervallo(1, maxPagine, rot=rotEnum)
            intervalli.append(interv)
            continue
        if strInterv.find('-')==-1:
            # pagina singola
            pag = intDaStr(strInterv,True, maxPagine)
            interv=Intervallo(pag,rot=rotEnum)
            intervalli.append(interv)
        else:
            # pagine da _ a _
            partiInterv=strInterv.split('-')
            partiInterv = [s.strip() for s in partiInterv]
            if len(partiInterv) == 2:
                # casi ideali
                if partiInterv[0] == '' and partiInterv[1] == '':
                    interv = Intervallo(1,maxPagine, rotEnum)
                elif partiInterv[0] == '':
                    pag = intDaStr(partiInterv[1],True, maxPagine)
                    interv = Intervallo(1, pag, rotEnum)
                elif partiInterv[1] == '':
                    pag = intDaStr(partiInterv[0],False, maxPagine)
                    interv = Intervallo(pag,maxPagine, rotEnum)
                else:
                    pagDa = intDaStr(partiInterv[0],False, maxPagine)
                    pagA = intDaStr(partiInterv[1], True, maxPagine)
                    interv = Intervallo( pagDa,  pagA, rotEnum)
                intervalli.append(interv)
                # |casi ideali
            elif len(partiInterv) == 3:
                # (2**3=) 8 casi particolari accettati
                # nella stringa possono essere presenti o meno i 3 numeri A, B, C
                if partiInterv[1] == '':  # '_--_'
                    if partiInterv[0] == '' and partiInterv[2] == '':  # '--'
                        # print('tutto')
                        interv = Intervallo(1,maxPagine, rotEnum)
                    elif partiInterv[0] == '':  # '--C'
                        # print("'-C'1")
                        pag = intDaStr(partiInterv[2], True, maxPagine) # C
                        interv = Intervallo(1, pag, rotEnum)
                    elif partiInterv[2] == '':  # 'A--'
                        # print("u'A-'")
                        pag = intDaStr(partiInterv[0], False, maxPagine) # A
                        interv = Intervallo(pag, maxPagine, rotEnum)
                    else:  # 'A--C'
                        # print("u'A-C'1")
                        pagDa = intDaStr(partiInterv[0], False, maxPagine) # A
                        pagA = intDaStr(partiInterv[2], True, maxPagine) # C
                        interv = Intervallo(pagDa, pagA, rotEnum)
                elif partiInterv[0] == '':  # '-B-_'
                    if partiInterv[2] == '':  # '-B-'
                        # print("'B'1")
                        pag = intDaStr(partiInterv[1], True, maxPagine) # B
                        interv = Intervallo(pag,rot= rotEnum)
                    else:  # '-B-C'
                        # print("B<=C ? '-C'1 : u'B-C'1")
                        pagDa = intDaStr(partiInterv[1], False, maxPagine) # B
                        pagA = intDaStr(partiInterv[2], True, maxPagine) # C
                        if pagDa<=pagA:
                            interv = Intervallo(1, pagA, rotEnum)
                        else:
                            interv = Intervallo(pagDa, pagA, rotEnum)
                else:  # 'A-B-_'
                    # 'A-B-' e 'A-B-C'
                    # print("A<=B ? u'A-' : u'A-B'1")
                    pagDa = intDaStr(partiInterv[0], False, maxPagine)  # A
                    pagA = intDaStr(partiInterv[1], True, maxPagine)  # B
                    if pagDa<=pagA:
                        interv = Intervallo(pagDa, maxPagine, rotEnum)
                    else:
                        interv = Intervallo(pagDa, pagA, rotEnum)
                # |if 8 casi
                intervalli.append(interv)
            else: # NO '-' > 2
                continue
        # /if con '-'
    # /for strInterv in listInterv:
    return intervalli
# /intervalliParse

def intervalliToString(intervalli):
    """ Da list[Intervallo] a stringa

    :param intervalli: lista di Intervalli
    :return: stringa di intervalli ben formattata
    """
    return ', '.join([i.__str__() for i in intervalli])
# /intervalliToString

def infoIntervalli():
    """Fornisce info sull'uso degli Intervalli

    :return:
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
# /infoIntervalli