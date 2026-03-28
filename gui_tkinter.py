import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pdf_engine import pagesCountAndCheck

# Inizio GUI
class GUI_Tkinter(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Edtor")
        self.geometry("800x600")
        self.iconbitmap("./assets/icon.ico")

        ### contenitore di tab
        notebook = ttk.Notebook(self)
        notebook.pack(pady=10, fill='both', expand=True)

        ### i tab
        frmSplit = ttk.Frame(notebook, width=780, height=550, padding="3 3 12 12")
        frmMerge = ttk.Frame(notebook, width=780, height=550, padding="3 3 12 12")
        frmInfo = ttk.Frame(notebook, width=780, height=550, padding="3 3 12 12")
        frmSplit.pack(fill='both', expand=True)
        frmMerge.pack(fill='both', expand=True)
        frmInfo.pack(fill='both', expand=True)

        ### creazione delle etichette dei tab
        notebook.add(frmSplit, text='Ruota e Separa')
        notebook.add(frmMerge, text='Ruota e Unisci')
        notebook.add(frmInfo, text='Informazioni')

        ### variabili d'istanza
        self.pathInputSplit = StringVar()
        self.pagesInputSplit = StringVar()
        self.id = 0 # numero righe della treeTable
        self.treeTable = ttk.Treeview()

        ### init tabs
        self.initSplit(frmSplit)
        self.initMerge(frmMerge)
        self.initInfo(frmInfo)
    # /__init__
    def initSplit(self,frmSplit: ttk.Frame):
        """ Initialize the frmSplit Frame

        :param frmSplit:
        :return:
        """
        ### contenuto x Split tab
        ttk.Label(frmSplit, text='Rotate & Split').grid(row=0, column=0)
        frmInputSplit = ttk.Frame(frmSplit, width=780, height=450)
        frmInputSplit.grid(row=1, column=0)

        ## contenuto di frmInputSplit

        ttk.Label(frmInputSplit, text='Percorso file di input:').grid(row=0, column=0)
        ttk.Button(frmInputSplit, text='...', width=4, command=self.getPathInputSplit).grid(row=0,
                                                                                       column=1)  # btnPathInputSplit
        ttk.Entry(frmInputSplit, width=60, textvariable=self.pathInputSplit).grid(row=0, column=2)  # txtPathInputSplit
        ttk.Label(frmInputSplit, text='Pagine:').grid(row=1, column=0, sticky='e')
        ttk.Label(frmInputSplit, width=4, textvariable=self.pagesInputSplit).grid(row=1, column=1, columnspan=2,
                                                                             sticky='w')  # lblPagesInputSplit
        ## /contenuto di frmInputSplit

        ttk.Label(frmSplit, text='Tabella di output:').grid(row=2, column=0)
        frmButtonsTable = ttk.Frame(frmSplit, width=400, height=280)
        frmButtonsTable.grid(row=3, column=0, sticky='ew')

        ## contenuto di frmButtonsTable
        btnAddPathOutputSplit = ttk.Button(frmButtonsTable, text='Agg. File ...', command=self.addFileSplitOnTreeview)
        btnAddPathOutputSplit.grid(row=0, column=0)
        btnAddIntervalSplit = ttk.Button(frmButtonsTable, text='Modifica \nIntervalli ...', command=self.addIntervalSplit)
        btnAddIntervalSplit.grid(row=0, column=1)
        btnUpperRowSplit = ttk.Button(frmButtonsTable, text='Upper')
        btnUpperRowSplit.grid(row=0, column=3)
        btnUpRowSplit = ttk.Button(frmButtonsTable, text='Up')
        btnUpRowSplit.grid(row=0, column=4)
        btnLowRowSplit = ttk.Button(frmButtonsTable, text='Low')
        btnLowRowSplit.grid(row=0, column=5)
        btnLowerRowSplit = ttk.Button(frmButtonsTable, text='Lower')
        btnLowerRowSplit.grid(row=0, column=6)
        ## /contenuto di frmButtonsTable

        # Treeview / Table
        frmTable = ttk.Frame(frmSplit, width=400, height=280)
        frmTable.grid(row=4, column=0, sticky='ew')

        ## contenuto di frmTable
        # intestazioni colonna
        columns = ('PathFile', 'Intervals', 'PagesIntervals', 'Result')
        treeTable = ttk.Treeview(frmTable, columns=columns, show='headings', selectmode='browse')
        # ora ha le colonne visualizzate con l'etichetta (text)
        treeTable.heading('PathFile', text='Path file')
        treeTable.heading('Intervals', text='Intervalli')
        treeTable.heading('PagesIntervals', text='Pagine da intervalli')
        treeTable.heading('Result', text='Risultato')
        treeTable.grid(column=0, row=0, sticky='nsew')
        # scrollbar destra
        scrollbarDX = ttk.Scrollbar(frmTable, orient=VERTICAL, command=treeTable.yview)
        scrollbarDX.grid(column=1, row=0, sticky='ns')
        treeTable.configure(yscrollcommand=scrollbarDX.set)
        # scrollbar sotto
        scrollbarDown = ttk.Scrollbar(frmTable, orient=HORIZONTAL, command=treeTable.xview)
        scrollbarDown.grid(column=0, row=1, sticky='ew')
        treeTable.configure(xscrollcommand=scrollbarDown.set)
        ## /contenuto di frmTable

        btnSplit = ttk.Button(frmSplit, text='Split')
        btnSplit.grid(row=5, column=0)
        progressBarSplit = ttk.Progressbar(frmSplit, maximum=100, orient=HORIZONTAL, value=24)
        progressBarSplit.grid(row=6, column=0, sticky='ew')
        ...
    # /initSplit
    def initMerge(self, frmMerge: ttk.Frame):
        """ Initialize the frmMerge Frame

        :param frmMerge:
        :return:
        """
        # contenuto temporaneo
        Label(frmMerge, text='Merge').pack(expand=True)
        ...
    # /initMerge
    def initInfo(self, frmInfo: ttk.Frame):
        """ Initialize the frmInfo Frame

        :param frmInfo:
        :return:
        """
        # contenuto temporaneo
        Label(frmInfo, text='Info').pack(expand=True)
        ...
    # /initInfo
    def getPathInputSplit(self):
        """

        :return:
        """
        filetypes = (
            ('File Adobe PDF (*.pdf)', '*.pdf'),
            ('Tutti i file (*.*)', '*.*')
        )
        filename = filedialog.askopenfilename(title="Scegli un file PDF", initialdir="/", filetypes=filetypes)
        print(filename)
        try:
            pages = pagesCountAndCheck(filename)
            self.pathInputSplit.set(filename)
            self.pagesInputSplit.set(str(pages))
        except Exception as e:
            self.pathInputSplit.set('')
            self.pagesInputSplit.set('')
            messagebox.showinfo('Errore!', f'{str(e)}\nnel file: {filename}')

    # /getPathInputSplit
    def addIntervalSplit(self):
        # treeTable.index()
        try:
            idRow = self.treeTable.selection()[0]
            i = self.treeTable.index(idRow)
            row = self.treeTable.item(idRow, 'values')
            if isinstance(row, tuple):
                row = [c for c in row]
                row.append(len(row[0]))
                row.append(len(row[1]))
            print(type(row))
            print(row)

        except Exception as e:
            # messagebox.showinfo('Errore!', 'Seleziona almeno una riga della tabella!')
            raise e

    # /addIntervalSplit

    def addFileSplitOnTreeview(self):
        row = [f'PathFile {self.id}', f'Intervals {self.id}']
        self.treeTable.insert('', 'end', values=row)
        self.id += 1
        ...
    # /addFileSplitOnTreeview

# /GUI_Tkinter

if __name__ == '__main__':
    root = GUI_Tkinter()
    root.mainloop()
# /if
