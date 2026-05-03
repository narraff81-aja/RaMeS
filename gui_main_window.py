from pathlib import Path
from typing import cast

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont, QAction
from PyQt6.QtWidgets import QMainWindow, QApplication, QTabWidget, QStatusBar, QWidget, QVBoxLayout, QLabel, \
    QGridLayout, QLineEdit, QPushButton, QFrame, QHBoxLayout, QTableWidget, QStackedLayout, QProgressBar, QSpinBox, \
    QFileDialog, QMessageBox, QHeaderView, QAbstractItemView, QMenu, QTableWidgetItem, QTextBrowser

from gui_helper_intervals import IntervalsHelper
from gui_widgets import BaseQTable, createHorizontalLine, DropQLineEdit
from intervals import intervalsParse, intervalsToString, intervalsPagesCount
from pdf_engine import pagesCountAndCheck

# BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = Path(__file__).resolve().parent / "assets"
SIZE_ICON = 24
DICT_ASSETS={
    'icon': str(ASSETS_DIR / 'icon.ico'),
    'tab-split': str(ASSETS_DIR / 'split.png'),
    'tab-merge': str(ASSETS_DIR / 'merge.png'),
    'tab-info': str(ASSETS_DIR / 'information.png'),
    'load': str(ASSETS_DIR / 'load-32.png'),
    'add-row': str(ASSETS_DIR / 'aggiungi-32.png'),
    'edit-interval': str(ASSETS_DIR / 'edit-32.png'),
    'copy-row': str(ASSETS_DIR / 'copia-48.png'),
    'del-row': str(ASSETS_DIR / 'cancel-32.png'),
    'clear': str(ASSETS_DIR / 'clear.png'),
    'upper': str(ASSETS_DIR / 'upper-arrows.png'),
    'up': str(ASSETS_DIR / 'up-arrows.png'),
    'low': str(ASSETS_DIR / 'low-arrows.png'),
    'lower': str(ASSETS_DIR / 'lower-arrows.png'),
}

class SplitQTable(BaseQTable):
    """ QTableWidget that handles output files for Split
    """
    def __init__(self, statusBar1: QStatusBar,txtSplitPathInput: DropQLineEdit, txtSplitNumPages:QLineEdit):
        super().__init__(0, 5)
        self.setHorizontalHeaderLabels(["", "Percorso File", "Intervalli", "Pagine", "Eseguito"])
        # Layout della tabella
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Interactive)
        self.setColumnWidth(0, 25)
        # self.setColumnWidth(3, 60)
        # self.setColumnWidth(4, 60)
        self.statusBar=statusBar1
        self.txtSplitPathInput=txtSplitPathInput
        self.txtSplitNumPages=txtSplitNumPages
        self.pathsSet= set()
    # /__init__
    def addRow(self,idRow: int, pathStr: str ="", intervalsStr: str ="",
                    intPagesStr: str ="", executeStr: str ="-"):
        self.pathsSet.add(pathStr) # aggiunge elemento al set
        self.insertRow(idRow)
        # 0.
        itemHandle = QTableWidgetItem("↕")
        itemHandle.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        itemHandle.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsDragEnabled)
        self.setItem(idRow, 0, itemHandle)

        # 1. "Percorso File"
        pathFile =QLineEdit(pathStr)
        pathFile.editingFinished.connect(lambda: self.validatePathCell(pathFile))
        self.setCellWidget(idRow, 1, pathFile)

        # 2. "Intervalli"
        intervalsString = QLineEdit(intervalsStr)
        intervalsString.editingFinished.connect(lambda: self.validateIntervalsCell(intervalsString))
        self.setCellWidget(idRow, 2, intervalsString)

        # 3. "Pagine"
        interPages = QLabel(intPagesStr)
        interPages.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        interPages.setMargin(5)
        self.setCellWidget(idRow, 3, interPages)

        # 4. "Eseguito"
        execute = QLabel(executeStr)
        execute.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        execute.setMargin(5)
        self.setCellWidget(idRow, 4, execute)
    # /addRow
    def getRowData(self,idRow):
        pathStr=cast(QLineEdit,self.cellWidget(idRow, 1)).text()
        intervalsStr=cast(QLineEdit,self.cellWidget(idRow, 2)).text()
        intPagesStr=cast(QLabel,self.cellWidget(idRow, 3)).text()
        executeStr=cast(QLabel,self.cellWidget(idRow, 4)).text()
        return {
            'pathStr': pathStr,
            'intervalsStr': intervalsStr,
            'intPagesStr': intPagesStr,
            'executeStr': executeStr
        }
    # /splitGetRowData
    def setRowData(self, idRow: int, data: dict):
        # Se per qualche motivo l'item della maniglia è sparito durante il drag, lo ricreiamo
        if not self.item(idRow, 0):
            itemHandle = QTableWidgetItem("↕")
            itemHandle.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            itemHandle.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsDragEnabled)
            self.setItem(idRow, 0, itemHandle)

        obj1 =cast(QLineEdit, self.cellWidget(idRow, 1))
        obj1.setText(data['pathStr'])
        obj2 = cast(QLineEdit,self.cellWidget(idRow, 2))
        obj2.setText(data['intervalsStr'])
        obj3 =cast(QLabel, self.cellWidget(idRow, 3))
        obj3.setText(str(data['intPagesStr']))
        obj4 = cast(QLabel, self.cellWidget(idRow, 4))
        obj4.setText(data['executeStr'])
    # /setRowData
    def saveOnClipboard(self,clipboardText: str, messageQMB: str):
        clipboard = QApplication.clipboard()
        clipboard.setText(clipboardText)
        QMessageBox.critical(self, "Errore PDF",messageQMB)
    # /saveOnClipboard
    def updatePathsSet(self):
        # altrimenti dovrei trovare il valore vecchio e confrontarlo col nuovo
        self.pathsSet.clear()
        for idRow in range(self.rowCount()):
            pathStr=cast(QLineEdit, self.cellWidget(idRow, 1)).text()
            self.pathsSet.add(pathStr)
    # /updatePathsSet
    def validatePathCell(self, pathQLE: QLineEdit):
        # Troviamo la riga attuale del widget
        index = self.indexAt(pathQLE.pos())
        idRow = index.row()
        text = pathQLE.text()
        if not text:
            for i in range(2,5):
                widget=self.cellWidget(idRow, i)
                if i==2:
                    # Copia gli intervalli negli appunti
                    self.saveOnClipboard(widget.text(),
                                         "Percorso vuoto!\nLa lista degli intervalli è stata copiata negli appunti!"
                                         )
                # Reset dei widget
                widget.setText("")
            # /for
            self.statusBar.showMessage(f"File PDF non valido alla riga {idRow + 1}!", 5000)
            return
        # /if
        p = Path(text)

        if p.is_dir():
            # print("Errore: Il percorso indicato è una cartella, serve un nome file .pdf")
            self.statusBar.showMessage("Il percorso indicato è una cartella.", 5000)
            QMessageBox.critical(self, "Errore Percorso",
                                 "Il percorso indicato è una cartella, qui serve un nome file .pdf!")
            pathQLE.setFocus()
            return

        if not str.endswith(p.suffix, '.pdf'):
            p = Path(text + ".pdf")
            pathQLE.setText(text + ".pdf")

        if p.exists():
            # Esiste già?
            if pathQLE.text() == self.txtSplitPathInput.text():
                QMessageBox.warning(self, "Errore", "Il file di output non può essere uguale a quello di input!")
                self.statusBar.showMessage("Errore: Il file di output non può essere uguale a quello di input!", 5000)
                pathQLE.setFocus()
                return
            else:
                # occorre la conferma manuale dell'user
                question = QMessageBox.question(self, "Sovrascrittura File",
                                                f"Il file {p.name} esiste già. Vuoi sovrascriverlo? [y/N]",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                                QMessageBox.StandardButton.No)
                if question == QMessageBox.StandardButton.No:
                    QMessageBox.information(self, "Errore Percorso", "Scegli un nuovo file .pdf!")
                    pathQLE.setFocus()
                    return
                else:
                    self.statusBar.showMessage("File PDF verrà sovrascritto!", 5000)
        else:
            self.statusBar.showMessage("File PDF valido.", 5000)
        self.updatePathsSet()
    # /validatePathCell
    def validateIntervalsCell(self, intervalsQLE: QLineEdit):
        # Troviamo la riga attuale del widget
        index = self.indexAt(intervalsQLE.pos())
        idRow = index.row()
        text = intervalsQLE.text().strip()
        maxPages=int(self.txtSplitNumPages.text())
        intervals = intervalsParse(text, maxPages)
        intervalsStr = intervalsToString(intervals)
        intervalsPages= intervalsPagesCount(intervals)
        intervalsQLE.setText(intervalsStr)
        lblPages = self.cellWidget(idRow, 3)
        lblPages.setText(str(intervalsPages))
        self.statusBar.showMessage(f"Intervallo aggiornato alla riga {idRow + 1}", 3000)
    # /validateIntervalsCell

    def tableAddRow(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Salva frammento PDF", "", "PDF Files (*.pdf)")

        if filePath:
            # Check: non deve essere uguale all'input originale!
            if filePath == self.txtSplitPathInput.text():
                QMessageBox.warning(self, "Errore", "Il file di output non può essere uguale a quello di input!")
                self.statusBar.showMessage("Errore: Il file di output non può essere uguale a quello di input!", 5000)
                return
            # Check: non deve essere già presente, poichè sovrascriverebbe un output!
            if filePath in self.pathsSet:
                QMessageBox.warning(self, "Errore", "Il file di output è già presente!")
                self.statusBar.showMessage("Errore: Il file di output è già presente!", 5000)
                return
            p = Path(filePath)
            if not str.endswith(p.suffix, '.pdf'):
                filePath+='.pdf'
            if p.exists():
                self.statusBar.showMessage(f"File {filePath} verrà sovrascritto!", 3000)

            row = self.rowCount()
            self.addRow(row,filePath)
            self.statusBar.showMessage(f"File aggiunto: {filePath} ", 3000)
    # /tableAddRow
    def tableRemoveRow(self):
        """ Remove a pre-selected row in the table
        """
        idRow = self.currentRow()
        pathFile= cast(QLineEdit,self.cellWidget(idRow, 1)).text()
        self.pathsSet.discard(pathFile)
        super().tableRemoveRow()
    # /tableRemoveRow
    def tableClear(self):
        """ Remove all rows in the table
        """
        self.pathsSet.clear() # azzera il set
        super().tableClear()
    # /tableClear
# /SplitQTable

class MergeQTable(BaseQTable):
    """ QTableWidget that handles input files for the Merge
    """
    def __init__(self, statusBar1: QStatusBar):
        super().__init__(0, 6)
        self.setHorizontalHeaderLabels(
            ["", "Percorso File", "MaxPag", "Intervalli", "Pagine", "Eseguito"])
        # Layout della tabella
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.setColumnWidth(0, 25)
        self.setColumnWidth(2, 60)
        # self.setColumnWidth(4, 60)
        # self.setColumnWidth(5, 60)
        self.statusBar = statusBar1
    # /__init__
    def addRow(self,idRow: int, pathStr: str ="", maxPagesInt: int=0,
                    intervalsStr: str ="", intPagesStr: str ="", executeStr: str ="-"):
        self.insertRow(idRow)

        # 0.
        itemHandle = QTableWidgetItem("↕")
        itemHandle.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        itemHandle.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsDragEnabled)
        self.setItem(idRow, 0, itemHandle)

        # 1. "Percorso File"
        pathFile = QLineEdit(pathStr)
        pathFile.editingFinished.connect(lambda: self.validatePathCell(pathFile))
        self.setCellWidget(idRow, 1, pathFile)

        # 2. "MaxPag"
        maxPathPages = QLabel(str(maxPagesInt))
        maxPathPages.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        maxPathPages.setMargin(5)
        self.setCellWidget(idRow, 2, maxPathPages)

        # 3. "Intervalli"
        intervalsString = QLineEdit(intervalsStr)
        intervalsString.editingFinished.connect(lambda: self.validateIntervalsCell(intervalsString))
        self.setCellWidget(idRow, 3, intervalsString)

        # 4. "Pagine"
        interPages = QLabel(intPagesStr)
        interPages.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        interPages.setMargin(5)
        self.setCellWidget(idRow, 4, interPages)

        # 5. "Eseguito"
        execute = QLabel(executeStr)
        execute.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        execute.setMargin(5)
        self.setCellWidget(idRow, 5, execute)
    # /addRow
    def getRowData(self,idRow):
        pathStr=cast(QLineEdit,self.cellWidget(idRow, 1)).text()
        maxPagesInt=int(cast(QLabel,self.cellWidget(idRow, 2)).text())
        intervalsStr=cast(QLineEdit,self.cellWidget(idRow, 3)).text()
        intPagesStr=cast(QLabel,self.cellWidget(idRow, 4)).text()
        executeStr=cast(QLabel,self.cellWidget(idRow, 5)).text()
        return {
            'pathStr': pathStr,
            'maxPagesInt':maxPagesInt,
            'intervalsStr': intervalsStr,
            'intPagesStr': intPagesStr,
            'executeStr': executeStr
        }
    # /getRowData
    def setRowData(self, idRow: int, data: dict):
        # Se per qualche motivo l'item della maniglia è sparito durante il drag, lo ricreiamo
        if not self.item(idRow, 0):
            itemHandle = QTableWidgetItem("↕")
            itemHandle.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            itemHandle.setFlags(
                Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsDragEnabled)
            self.setItem(idRow, 0, itemHandle)

        obj1 =cast(QLineEdit, self.cellWidget(idRow, 1))
        obj1.setText(data['pathStr'])
        obj2 = cast(QLabel,self.cellWidget(idRow, 2))
        obj2.setText(str(data['maxPagesInt']))
        obj3 =cast(QLineEdit, self.cellWidget(idRow, 3))
        obj3.setText(data['intervalsStr'])
        obj4 = cast(QLabel, self.cellWidget(idRow, 4))
        obj4.setText(str(data['intPagesStr']))
        obj5 = cast(QLabel, self.cellWidget(idRow, 5))
        obj5.setText(data['executeStr'])
    # /setRowData
    def saveOnClipboard(self,clipboardText: str, messageQMB: str):
        clipboard = QApplication.clipboard()
        clipboard.setText(clipboardText)
        QMessageBox.critical(self, "Errore PDF",messageQMB)
    # /saveOnClipboard
    def validatePathCell(self, pathQLE: QLineEdit):
        # Troviamo la riga attuale del widget
        index = self.indexAt(pathQLE.pos())
        idRow = index.row()
        text = pathQLE.text().strip()
        if not text:
            for i in range(2,6):
                widget=self.cellWidget(idRow, i)
                if i==3:
                    # Copia gli intervalli negli appunti
                    self.saveOnClipboard(widget.text(),
                                         "Percorso vuoto!\nLa lista degli intervalli è stata copiata negli appunti!"
                                         )
                # Reset dei widget
                widget.setText("")
            # /for
            self.statusBar.showMessage(f"File PDF non valido alla riga {idRow + 1}!", 5000)
            return
        # /if
        try:
            pages = pagesCountAndCheck(text)
            maxPagesQL=self.cellWidget(idRow, 2)
            maxPagesQL.setText(str(pages))
            # tenta una sistemazione degli intervalli
            intervals = intervalsParse(text, pages)
            intervalsStr = intervalsToString(intervals)
            intervalsPages = intervalsPagesCount(intervals)
            self.cellWidget(idRow, 3).setText(intervalsStr)
            self.cellWidget(idRow, 4).setText(str(intervalsPages))
            self.statusBar.showMessage(f"PDF aggiornato alla riga {idRow + 1}: {pages} pagine.", 3000)
        except Exception as e:
            for i in range(2,6):
                widget=self.cellWidget(idRow, i)
                if i==3:
                    # Copia gli intervalli negli appunti
                    self.saveOnClipboard(widget.text(),
                                         f"{str(e)}\nLa lista degli intervalli è stata copiata negli appunti!"
                                         )
                # Reset dei widget
                widget.setText("")
            # /for
            self.statusBar.showMessage(f"{str(e)} alla riga {idRow + 1}", 5000)
        # /try
    # /validatePathCell
    def validateIntervalsCell(self, intervalsQLE: QLineEdit):
        # Troviamo la riga attuale del widget
        index = self.indexAt(intervalsQLE.pos())
        idRow = index.row()
        text = intervalsQLE.text().strip()
        maxPages = int(self.cellWidget(idRow, 2).text())
        intervals = intervalsParse(text, maxPages)
        intervalsStr = intervalsToString(intervals)
        intervalsPages = intervalsPagesCount(intervals)
        intervalsQLE.setText(intervalsStr)
        lblPages = self.cellWidget(idRow, 4)
        lblPages.setText(str(intervalsPages))
        self.statusBar.showMessage(f"Intervallo aggiornato alla riga {idRow + 1}", 3000)
    # /validateIntervalsCell

    def tableAddRow(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Carica frammento PDF", "", "PDF Files (*.pdf)")
        if filePath:
            # Check: può essere uguale all'input originale! La sovrascrittura avviene alla fine del Merge!
            p = Path(filePath)
            if not str.endswith(p.suffix, '.pdf'):
                filePath += '.pdf'

            try:
                pages = pagesCountAndCheck(filePath)
                row = self.rowCount()
                self.addRow(row,filePath,pages)
                self.statusBar.showMessage(f"File aggiunto: {filePath} ", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"{str(e)} su\n{filePath}")
                self.statusBar.showMessage(f"{str(e)} su {filePath}", 5000)
                return
    # /tableAddRow
    def tableCopyRow(self):
        """ Copy below a pre-selected row in the table
        """
        idRow = self.currentRow()
        if idRow < 0:
            return
        data = self.getRowData(idRow)
        self.addRow(idRow + 1, data['pathStr'], data['maxPagesInt'], data['intervalsStr'],
                         data['intPagesStr'], data['executeStr'])
        self.setCurrentCell(idRow + 1, 0)
    # /tableCopyRow
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super().dragEnterEvent(event)
    # /dragEnterEvent
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            for url in event.mimeData().urls():
                filePath = url.toLocalFile().strip()
                try:
                    maxPages = pagesCountAndCheck(filePath)
                    idRow=self.rowCount()
                    self.addRow(idRow,filePath,maxPages)
                    self.statusBar.showMessage(f"File aggiunto: {filePath} ", 3000)
                except Exception as e:
                    QMessageBox.critical(self, "Errore PDF nel Drag & Drop!", str(e))
            # /for
        else:
            # Se è un drag interno (spostamento righe), usa il comportamento standard
            super().dropEvent(event)
    # /dropEvent
# /MergeQTable

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RaMeS - Raffaele's Merge & Split - mini PDF editor")
        self.setWindowIcon(QIcon(DICT_ASSETS['icon']))
        self.resize(800, 600)

        # 0. Contenitore principale
        tabs = QTabWidget()
        self.setCentralWidget(tabs)
        self.statusBar1 = QStatusBar()
        self.setStatusBar(self.statusBar1)
        # 1 variabili inizializzate per evitare i warning
        self.txtSplitPathInput = None
        self.txtSplitNumPages = None
        self.tableSplitOutput = None
        # 1.1 Creazione Tab Split
        self.tabSplit = QWidget()
        self.initTabSplit()
        tabs.addTab(self.tabSplit,QIcon(DICT_ASSETS['tab-split']), "Split e Ruota")
        # 2 variabili inizializzate per evitare i warning
        self.txtMergePathOutput = None
        self.tableMergeInput = None
        # 2.1 Creazione Tab Merge
        self.tabMerge = QWidget()
        self.initTabMerge()
        tabs.addTab(self.tabMerge,QIcon(DICT_ASSETS['tab-merge']), "Merge e Ruota")
        # 3 variabili inizializzate per evitare i warning

        # 3.1 Creazione Tab Info
        self.tabInfo = QWidget()
        self.initTabInfo()
        tabs.addTab(self.tabInfo, QIcon(DICT_ASSETS['tab-info']), "Informazioni")
    # /__init__

    def initTabSplit(self):
        """Initialize Tab Split
        :return:
        """
        layout0 = QVBoxLayout(self.tabSplit)

        # 2. Titolo
        title = QLabel("Split & Ruota PDF")
        title.setFont(QFont("Arial", 14))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout0.addWidget(title)

        # 3-4-5-6-7. Grid Layout per Input
        grid = QGridLayout()
        # 3
        grid.addWidget(QLabel("Percorso file:"), 0, 0)
        # 4
        btnSplitPathInput = QPushButton()
        btnSplitPathInput.setIcon(QIcon(DICT_ASSETS['load']))
        btnSplitPathInput.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnSplitPathInput.setToolTip('Cerca il percorso del file PDF di origine')
        btnSplitPathInput.clicked.connect(self.openSplitDialog)
        grid.addWidget(btnSplitPathInput, 0, 1)
        # 5
        #self.txtSplitPathInput = QLineEdit()
        self.txtSplitPathInput = DropQLineEdit()
        self.txtSplitPathInput.setToolTip('Inserisci il percorso del file PDF di origine')
        self.txtSplitPathInput.setPlaceholderText('Percorso del file PDF di origine')
        self.txtSplitPathInput.editingFinished.connect(self.validateInputPdfPath)
        self.txtSplitPathInput.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        openPdfAction = QAction(QIcon(DICT_ASSETS['load']), "Scegli file...", self)
        openPdfAction.triggered.connect(self.openSplitDialog)
        self.txtSplitPathInput.addAction(openPdfAction)
        grid.addWidget(self.txtSplitPathInput, 0, 2)
        # 6
        grid.addWidget(QLabel("Pagine:"), 1, 0)
        # 7
        self.txtSplitNumPages = QLineEdit()
        self.txtSplitNumPages.setText('')
        self.txtSplitNumPages.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.txtSplitNumPages.setFixedWidth(50)
        self.txtSplitNumPages.setReadOnly(True)
        grid.addWidget(self.txtSplitNumPages, 1, 1)
        layout0.addLayout(grid)

        # 8 separatore
        layout0.addWidget(createHorizontalLine())

        # 9 sottotitolo
        subtitle =QLabel("Tabella di Output")
        layout0.addWidget(subtitle)
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Bottoni laterali 10-11-13-14-15-16-17-18 e Tabella 19.
        tableArea = QHBoxLayout()
        layout0.addLayout(tableArea)
        groupButtons =QVBoxLayout() # 10-11-13-14-15-16-17-18
        tableArea.addLayout(groupButtons)

        # 10 Aggiungi\nriga
        btnSplitTableAddRow = QPushButton()
        btnSplitTableAddRow.setIcon(QIcon(DICT_ASSETS['add-row']))
        btnSplitTableAddRow.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnSplitTableAddRow.setToolTip('Aggiungi riga alla tabella')

        groupButtons.addWidget(btnSplitTableAddRow)
        # 11 Modifica\nintervalli
        btnSplitTableModifyIntervals = QPushButton()
        btnSplitTableModifyIntervals.setIcon(QIcon(DICT_ASSETS['edit-interval']))
        btnSplitTableModifyIntervals.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnSplitTableModifyIntervals.setToolTip('Modifica intervalli della riga selezionata tramite finestra')

        groupButtons.addWidget(btnSplitTableModifyIntervals)
        # 13 Elimina\nriga
        btnSplitTableDelRow = QPushButton()
        btnSplitTableDelRow.setIcon(QIcon(DICT_ASSETS['del-row']))
        btnSplitTableDelRow.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnSplitTableDelRow.setToolTip('Rimuovi la riga selezionata dalla tabella')
        groupButtons.addWidget(btnSplitTableDelRow)
        # 14 Svuota
        btnSplitTableClear = QPushButton()
        btnSplitTableClear.setIcon(QIcon(DICT_ASSETS['clear']))
        btnSplitTableClear.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnSplitTableClear.setToolTip('Svuota la tabella')
        groupButtons.addWidget(btnSplitTableClear)
        # Spazio elastico.Spinge i bottoni in alto
        groupButtons.addStretch()
        # 15 ^^
        btnSplitTableUpper=QPushButton()
        btnSplitTableUpper.setIcon(QIcon(DICT_ASSETS['upper']))
        btnSplitTableUpper.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnSplitTableUpper.setToolTip('Sposta la riga selezionata in cima')
        groupButtons.addWidget(btnSplitTableUpper)
        # 16 ^
        btnSplitTableUp = QPushButton()
        btnSplitTableUp.setIcon(QIcon(DICT_ASSETS['up']))
        btnSplitTableUp.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnSplitTableUp.setToolTip('Sposta la riga selezionata in alto di una posizione')
        groupButtons.addWidget(btnSplitTableUp)
        # 17 v
        btnSplitTableLow = QPushButton()
        btnSplitTableLow.setIcon(QIcon(DICT_ASSETS['low']))
        btnSplitTableLow.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnSplitTableLow.setToolTip('Sposta la riga selezionata in basso di una posizione')
        groupButtons.addWidget(btnSplitTableLow)
        # 18 vv
        btnSplitTableLower = QPushButton()
        btnSplitTableLower.setIcon(QIcon(DICT_ASSETS['lower']))
        btnSplitTableLower.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnSplitTableLower.setToolTip('Sposta la riga selezionata in fondo')
        groupButtons.addWidget(btnSplitTableLower)
        # 19 Tabella
        #self.tableSplitOutput =QTableWidget(0,5)
        self.tableSplitOutput = SplitQTable(self.statusBar1,self.txtSplitPathInput, self.txtSplitNumPages)

        # connects
        btnSplitTableAddRow.clicked.connect(self.tableSplitOutput.tableAddRow)
        btnSplitTableModifyIntervals.clicked.connect(self.splitTableEditInterval)
        # btnSplitTableDelRow.clicked.connect(lambda: self.tableRemoveRow(self.tableSplitOutput))
        # btnSplitTableClear.clicked.connect(lambda: self.tableClear(self.tableSplitOutput))
        # btnSplitTableUpper.clicked.connect(lambda: self.tableMoveUpperRow(self.tableSplitOutput))
        # btnSplitTableUp.clicked.connect(lambda: self.tableMoveUpRow(self.tableSplitOutput))
        # btnSplitTableLow.clicked.connect(lambda: self.tableMoveLowRow(self.tableSplitOutput))
        # btnSplitTableLower.clicked.connect(lambda: self.tableMoveLowerRow(self.tableSplitOutput))
        btnSplitTableDelRow.clicked.connect(self.tableSplitOutput.tableRemoveRow)
        btnSplitTableClear.clicked.connect(self.tableSplitOutput.tableClear)
        btnSplitTableUpper.clicked.connect(self.tableSplitOutput.tableMoveUpperRow)
        btnSplitTableUp.clicked.connect(self.tableSplitOutput.tableMoveUpRow)
        btnSplitTableLow.clicked.connect(self.tableSplitOutput.tableMoveLowRow)
        btnSplitTableLower.clicked.connect(self.tableSplitOutput.tableMoveLowerRow)
        # Selezione e Drag & Drop interno
        self.tableSplitOutput.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableSplitOutput.customContextMenuRequested.connect(
            lambda pos: self.showContextMenu(pos, self.tableSplitOutput)
        )
        tableArea.addWidget(self.tableSplitOutput)

        # 20 separatore
        layout0.addWidget(createHorizontalLine())

        # 21 avvia
        btnSplit =QPushButton('Split')
        btnSplit.setToolTip('Esegue effettivamente lo Split e Ruota sul File System')
        layout0.addWidget(btnSplit, alignment=Qt.AlignmentFlag.AlignCenter)

        # 22 QProgressBar
        # layoutProgressBar = QStackedLayout()
        self.splitProgressBar=QProgressBar()
        self.splitProgressBar.setRange(0,100)
        self.splitProgressBar.setValue(40)
        # layoutProgressBar.addWidget(self.splitProgressBar)
        # self.splitTextProgressBar=QLabel(str(self.splitProgressBar.value))
        # layoutProgressBar.addWidget(self.splitTextProgressBar)
        # layout0.addLayout(layoutProgressBar)
        layout0.addWidget(self.splitProgressBar)

    # /initTabSplit
    def initTabMerge(self):
        """Initialize Tab Merge
        :return:
        """
        layout0 = QVBoxLayout(self.tabMerge)

        # 2. Titolo
        title = QLabel("Merge & Ruota PDF")
        title.setFont(QFont("Arial", 14))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout0.addWidget(title)

        # 3-4-5-6-7. Grid Layout per Input
        grid = QGridLayout()
        # 3
        grid.addWidget(QLabel("Percorso file:"), 0, 0)
        # 4 "..."
        btnMergePathOutput = QPushButton()
        btnMergePathOutput.setIcon(QIcon(DICT_ASSETS['load']))
        btnMergePathOutput.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnMergePathOutput.setToolTip('Clicca per selezionare il percorso del file PDF riunito')
        btnMergePathOutput.clicked.connect(self.openMergeDialog)
        grid.addWidget(btnMergePathOutput, 0, 1)
        # 5
        self.txtMergePathOutput = QLineEdit()
        self.txtMergePathOutput.setToolTip('Inserisci il percorso del file PDF che verrà riunito')
        self.txtMergePathOutput.setPlaceholderText('Percorso del file PDF che verrà riunito')
        self.txtMergePathOutput.editingFinished.connect(self.validateOutputPdfPath)
        self.txtMergePathOutput.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        openPdfAction = QAction(QIcon(DICT_ASSETS['load']), "Scegli file...", self)
        openPdfAction.triggered.connect(self.openMergeDialog)
        self.txtMergePathOutput.addAction(openPdfAction)
        grid.addWidget(self.txtMergePathOutput, 0, 2)
        layout0.addLayout(grid)

        # 8 separatore
        layout0.addWidget(createHorizontalLine())

        # 9 sottotitolo
        subtitle = QLabel("Tabella di Input")
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout0.addWidget(subtitle)

        # Bottoni laterali 10-11-12-13-14-15-16-17-18 e Tabella 19.
        tableArea = QHBoxLayout()
        layout0.addLayout(tableArea)
        groupButtons = QVBoxLayout()  # 10-11-12-13-14-15-16-17-18
        tableArea.addLayout(groupButtons)

        # 10 Aggiungi\nriga
        btnMergeTableAddRow = QPushButton()
        btnMergeTableAddRow.setIcon(QIcon(DICT_ASSETS['add-row']))
        btnMergeTableAddRow.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnMergeTableAddRow.setToolTip('Aggiungi riga alla tabella')

        groupButtons.addWidget(btnMergeTableAddRow)
        # 11 Modifica\nintervalli
        btnMergeTableModifyIntervals = QPushButton()
        btnMergeTableModifyIntervals.setIcon(QIcon(DICT_ASSETS['edit-interval']))
        btnMergeTableModifyIntervals.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnMergeTableModifyIntervals.setToolTip('Modifica intervalli della riga selezionata tramite finestra')

        groupButtons.addWidget(btnMergeTableModifyIntervals)
        # 12 Copia\nriga
        btnMergeTableCopyRow = QPushButton()
        btnMergeTableCopyRow.setIcon(QIcon(DICT_ASSETS['copy-row']))
        btnMergeTableCopyRow.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnMergeTableCopyRow.setToolTip("Copia la riga selezionata")

        groupButtons.addWidget(btnMergeTableCopyRow)

        # 13 Elimina\nriga
        btnMergeTableDelRow = QPushButton()
        btnMergeTableDelRow.setIcon(QIcon(DICT_ASSETS['del-row']))
        btnMergeTableDelRow.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnMergeTableDelRow.setToolTip('Rimuovi la riga selezionata dalla tabella')
        groupButtons.addWidget(btnMergeTableDelRow)
        # 14 Svuota
        btnMergeTableClear = QPushButton()
        btnMergeTableClear.setIcon(QIcon(DICT_ASSETS['clear']))
        btnMergeTableClear.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnMergeTableClear.setToolTip('Svuota la tabella')
        groupButtons.addWidget(btnMergeTableClear)
        # Spazio elastico.Spinge i bottoni in alto
        groupButtons.addStretch()
        # 15 ^^
        btnMergeTableUpper = QPushButton()
        btnMergeTableUpper.setIcon(QIcon(DICT_ASSETS['upper']))
        btnMergeTableUpper.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnMergeTableUpper.setToolTip('Sposta la riga selezionata in cima')
        groupButtons.addWidget(btnMergeTableUpper)
        # 16 ^
        btnMergeTableUp = QPushButton()
        btnMergeTableUp.setIcon(QIcon(DICT_ASSETS['up']))
        btnMergeTableUp.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnMergeTableUp.setToolTip('Sposta la riga selezionata in alto di una posizione')
        groupButtons.addWidget(btnMergeTableUp)
        # 17 v
        btnMergeTableLow = QPushButton()
        btnMergeTableLow.setIcon(QIcon(DICT_ASSETS['low']))
        btnMergeTableLow.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnMergeTableLow.setToolTip('Sposta la riga selezionata in basso di una posizione')
        groupButtons.addWidget(btnMergeTableLow)
        # 18 vv
        btnMergeTableLower = QPushButton()
        btnMergeTableLower.setIcon(QIcon(DICT_ASSETS['lower']))
        btnMergeTableLower.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnMergeTableLower.setToolTip('Sposta la riga selezionata in fondo')
        groupButtons.addWidget(btnMergeTableLower)
        # 19 Tabella # QTableWidget()
        self.tableMergeInput = MergeQTable(self.statusBar1) # PDFTableWidget()
        # connects
        btnMergeTableAddRow.clicked.connect(self.tableMergeInput.tableAddRow)
        btnMergeTableModifyIntervals.clicked.connect(self.mergeTableEditInterval)
        btnMergeTableCopyRow.clicked.connect(self.tableMergeInput.tableCopyRow)
        # btnMergeTableDelRow.clicked.connect(lambda: self.tableRemoveRow(self.tableMergeInput))
        # btnMergeTableClear.clicked.connect(lambda: self.tableClear(self.tableMergeInput))
        # btnMergeTableUpper.clicked.connect(lambda: self.tableMoveUpperRow(self.tableMergeInput))
        # btnMergeTableUp.clicked.connect(lambda: self.tableMoveUpRow(self.tableMergeInput))
        # btnMergeTableLow.clicked.connect(lambda: self.tableMoveLowRow(self.tableMergeInput))
        # btnMergeTableLower.clicked.connect(lambda: self.tableMoveLowerRow(self.tableMergeInput))
        btnMergeTableDelRow.clicked.connect(self.tableMergeInput.tableRemoveRow)
        btnMergeTableClear.clicked.connect(self.tableMergeInput.tableClear)
        btnMergeTableUpper.clicked.connect(self.tableMergeInput.tableMoveUpperRow)
        btnMergeTableUp.clicked.connect(self.tableMergeInput.tableMoveUpRow)
        btnMergeTableLow.clicked.connect(self.tableMergeInput.tableMoveLowRow)
        btnMergeTableLower.clicked.connect(self.tableMergeInput.tableMoveLowerRow)
        # Selezione e Drag & Drop interno
        self.tableMergeInput.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableMergeInput.customContextMenuRequested.connect(
            lambda pos: self.showContextMenu(pos, self.tableMergeInput)
        )
        tableArea.addWidget(self.tableMergeInput)

        # 20 separatore
        layout0.addWidget(createHorizontalLine())

        # 21
        btnMerge = QPushButton('Merge')
        btnMerge.setToolTip('Esegue effettivamente il Merge e Ruota sul File System')
        layout0.addWidget(btnMerge, alignment=Qt.AlignmentFlag.AlignCenter)

        # 22
        # layoutProgressBar = QStackedLayout()
        self.mergeProgressBar = QProgressBar()
        self.mergeProgressBar.setRange(0, 100)
        self.mergeProgressBar.setValue(40)
        # layoutProgressBar.addWidget(self.mergeProgressBar)
        # self.splitTextProgressBar=QLabel(str(self.mergeProgressBar.value))
        # layoutProgressBar.addWidget(self.splitTextProgressBar)
        # layout0.addLayout(layoutProgressBar)
        layout0.addWidget(self.mergeProgressBar)

    # /initTabMerge
    def initTabInfo(self):
        """Initialize Tab Merge
        :return:
        """
        layout0 = QVBoxLayout(self.tabInfo)
        # # 2. Titolo
        # title = QLabel("Informazioni")
        # title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # layout0.addWidget(title)

        # browser di testo
        infoDisplay = QTextBrowser()

        # contenuto in HTML
        infoHtml = """
            <h1>Informazioni</h1>
            <h2>PDF Editor Tool</h2>
            <p>Versione 1.0.0</p>
            <hr>
            <h3>Guida Rapida:</h3>
            <ul>
                <li><b>Split:</b> Trascina un file, definisci gli intervalli e premi Split.</li>
                <li><b>Merge:</b> Trascina più file nella tabella e uniscili.</li>
            </ul>
            <p style="color: gray;">Sviluppato per fini didattici - 2026</p>
            """
        infoDisplay.setHtml(infoHtml)

        # Rende il testo cliccabile se ci sono link
        infoDisplay.setOpenExternalLinks(True)
        layout0.addWidget(infoDisplay)
    # /initTabInfo
    def openSplitDialog(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Carica PDF", "", "PDF Files (*.pdf)")
        if filePath:
            self.txtSplitPathInput.setText(filePath)
            self.validateInputPdfPath() # Forza la validazione/sincronizzazione
    # /openSplitDialog
    def validateInputPdfPath(self):
         #"""Gestisce l'aggiornamento della UI in base allo stato del path input"""
         # Forza la validazione se il widget è quello personalizzato
         if not isinstance(self.txtSplitPathInput, DropQLineEdit):
             return
         # Se l'utente ha digitato ma non abbiamo ancora le pagine
         path = self.txtSplitPathInput.text().strip()
         if not path:
             self.txtSplitNumPages.clear()
             return
         try:
            pages = pagesCountAndCheck(path)
            self.txtSplitPathInput.maxPages = pages
            self.txtSplitNumPages.setText(str(pages))
            self.statusBar1.showMessage(f"PDF caricato: {pages} pagine.", 3000)
         except Exception as e:
            # Copia il path errato negli appunti
            clipboard = QApplication.clipboard()
            clipboard.setText(path)
            # Reset dei widget
            self.txtSplitPathInput.clearAll()
            self.txtSplitNumPages.clear()
            # Messaggi all'utente
            QMessageBox.critical(self, "Errore PDF",
                f"{str(e)}\n\n"
                f"Il percorso è stato copiato negli appunti!"
            )
            self.statusBar1.showMessage(f"File PDF non valido!", 5000)
        # /try
    # /syncPagesCount

    def openMergeDialog(self):
        """ validate a not-existing Pdf file path.
        """
        # Apre il dialogo di salvataggio
        filePath, _ = QFileDialog.getSaveFileName(self,"Salva PDF risultante","","PDF Files (*.pdf)")
        if filePath:
            # Assicuriamoci che l'estensione ci sia (Qt a volte non la aggiunge se l'utente non la scrive)
            if not filePath.lower().endswith('.pdf'):
                filePath += ".pdf"
            self.txtMergePathOutput.setText(filePath)
            self.statusBar1.showMessage("File PDF valido.", 5000)
            self.validateOutputPdfPath(True) # Forza la validazione/sincronizzazione
    # /openMergeDialog
    def validateOutputPdfPath(self, alreadyConfirmed=False):
        pathString = self.txtMergePathOutput.text().strip()
        if not pathString:
            return
        p = Path(pathString)
        if not str.endswith(p.suffix, '.pdf'):
            #print("Errore: Il percorso indicato non è nome file .pdf")
            # la GUI è clemente! Lo aggiunge in automatico
            self.txtMergePathOutput.setFocus(pathString + ".pdf")
            p = Path(pathString + ".pdf")
        if alreadyConfirmed:
            self.statusBar1.showMessage("File PDF valido.", 5000)
            return
        if p.is_dir():
            #print("Errore: Il percorso indicato è una cartella, serve un nome file .pdf")
            self.statusBar1.showMessage("Il percorso indicato è una cartella.", 5000)
            QMessageBox.critical(self, "Errore Percorso", "Il percorso indicato è una cartella, qui serve un nome file .pdf!")
            self.txtMergePathOutput.setFocus()
            return
        if p.exists():
            # Esiste già? occorre la conferma manuale dell'user
            question = QMessageBox.question(self, "Sovrascrittura File",
                f"Il file {p.name} esiste già. Vuoi sovrascriverlo? [y/N]",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if question == QMessageBox.StandardButton.No:
                self.txtMergePathOutput.clear()
                QMessageBox.information(self, "Errore Percorso", "Scegli un nuovo file .pdf!")
            else:
                self.statusBar1.showMessage("File PDF verrà sovrascritto!", 5000)
        else:
            self.statusBar1.showMessage("File PDF valido.", 5000)
    # /validateOutputPdfPath

    def splitTableEditInterval(self):
        idRow = self.tableSplitOutput.currentRow()
        maxPages = int(cast(QLineEdit,self.txtSplitNumPages).text())
        currentIntervals =cast(QLineEdit, self.tableSplitOutput.cellWidget(idRow, 2)).text()
        dialog = IntervalsHelper(self, maxPages, currentIntervals)
        if dialog.exec():  # Se preme OK
            newIntervals = dialog.getIntervalsString()
            # Aggiorna Tabella 19
            # print(newIntervals)
            cast(QLineEdit, self.tableMergeInput.cellWidget(idRow, 2)).setText(newIntervals)
    # /tableEditInterval

    def mergeTableEditInterval(self):
        idRow = self.tableMergeInput.currentRow()
        maxPages = int(cast(QLineEdit, self.tableMergeInput.cellWidget(idRow, 2)).text())
        currentIntervals =cast(QLineEdit, self.tableMergeInput.cellWidget(idRow, 3)).text()
        dialog = IntervalsHelper(self, maxPages, currentIntervals)
        if dialog.exec():  # Se preme OK
            newIntervals = dialog.getIntervalsString()
            # Aggiorna Tabella 19
            # print(newIntervals)
            cast(QLineEdit, self.tableMergeInput.cellWidget(idRow, 3)).setText(newIntervals)
    # /tableEditInterval

    # def tableRemoveRow(self, table: BaseQTable):
    #     table.tableRemoveRow()
    # # /tableRemoveRow
    # def tableClear(self, table: BaseQTable):
    #     table.tableClear()
    # # /tableClear
    # def tableMoveUpperRow(self, table: BaseQTable):
    #     table.tableMoveUpperRow()
    # # /tableMoveUpperRow
    # def tableMoveUpRow(self, table: BaseQTable):
    #     table.tableMoveUpRow()
    # # /tableMoveUpRow
    # def tableMoveLowRow(self, table: BaseQTable):
    #     table.tableMoveLowRow()
    # # /tableMoveLowRow
    # def tableMoveLowerRow(self, table: BaseQTable):
    #     table.tableMoveLowerRow()
    # # /tableMoveLowerRow

    def showContextMenu(self, pos, table: BaseQTable):
        menu = QMenu()
        actionTableAddRow = menu.addAction(QIcon(DICT_ASSETS['add-row']), "Aggiungi riga")
        actionTableAddRow.triggered.connect(table.tableAddRow)
        actionTableAddRow.setToolTip("Aggiungi riga alla tabella")

        actionTableEditInterval = menu.addAction(QIcon(DICT_ASSETS['edit-interval']), "Modifica intervalli ...")
        actionTableEditInterval.setToolTip("Modifica intervalli della riga selezionata tramite finestra")
        if table == self.tableSplitOutput:
            #actionTableAddRow.triggered.connect(self.tableSplitOutput.tableAddRow)
            actionTableEditInterval.triggered.connect(self.splitTableEditInterval)
        elif table == self.tableMergeInput:
            #actionTableAddRow.triggered.connect(self.tableMergeInput.tableAddRow)
            actionTableEditInterval.triggered.connect(self.mergeTableEditInterval)
            actionTableCopyRow = menu.addAction(QIcon(DICT_ASSETS['copy-row']), "Copia riga")
            actionTableCopyRow.setToolTip("Copia riga alla tabella")
            actionTableCopyRow.triggered.connect(self.tableMergeInput.tableCopyRow)

        actionTableRemoveRow = menu.addAction(QIcon(DICT_ASSETS['del-row']), "Rimuovi riga")
        #actionTableRemoveRow.triggered.connect(lambda: self.tableRemoveRow(table))
        actionTableRemoveRow.triggered.connect(table.tableRemoveRow)
        actionTableRemoveRow.setToolTip("Rimuovi la riga selezionata dalla tabella")

        actionTableClear = menu.addAction(QIcon(DICT_ASSETS['clear']), "Svuota tabella")
        #actionTableClear.triggered.connect(lambda: self.tableClear(table))
        actionTableClear.triggered.connect(table.tableClear)
        actionTableClear.setToolTip("Svuota la tabella")

        menu.addSeparator()

        actionTableMoveUpperRow = menu.addAction(QIcon(DICT_ASSETS['upper']), 'Sposta in cima')
        # actionTableMoveUpperRow.triggered.connect(lambda: self.tableMoveUpperRow(table))
        actionTableMoveUpperRow.triggered.connect(table.tableMoveUpperRow)
        actionTableMoveUpperRow.setToolTip('Sposta la riga selezionata in cima')

        actionTableMoveUpRow = menu.addAction(QIcon(DICT_ASSETS['up']), 'Sposta in alto')
        # actionTableMoveUpRow.triggered.connect(lambda: self.tableMoveUpRow(table))
        actionTableMoveUpRow.triggered.connect(table.tableMoveUpRow)
        actionTableMoveUpRow.setToolTip('Sposta la riga selezionata in alto di una posizione')

        actionTableMoveLowRow = menu.addAction(QIcon(DICT_ASSETS['low']), 'Sposta in basso')
        # actionTableMoveLowRow.triggered.connect(lambda: self.tableMoveLowRow(table))
        actionTableMoveLowRow.triggered.connect(table.tableMoveLowRow)
        actionTableMoveLowRow.setToolTip('Sposta la riga selezionata in basso di una posizione')

        actionTableMoveLowerRow = menu.addAction(QIcon(DICT_ASSETS['lower']), 'Sposta in fondo')
        # actionTableMoveLowerRow.triggered.connect(lambda: self.tableMoveLowerRow(table))
        actionTableMoveLowerRow.triggered.connect(table.tableMoveLowerRow)
        actionTableMoveLowerRow.setToolTip('Sposta la riga selezionata in fondo')

        menu.exec(table.mapToGlobal(pos))
    # /show_context_menu

# /MainWindow

app = QApplication([])

window = MainWindow()
window.show()

app.exec()