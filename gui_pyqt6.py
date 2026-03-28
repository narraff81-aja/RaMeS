from pathlib import Path
from tokenize import group

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont, QAction
from PyQt6.QtWidgets import QMainWindow, QApplication, QTabWidget, QStatusBar, QWidget, QVBoxLayout, QLabel, \
    QGridLayout, QLineEdit, QPushButton, QFrame, QHBoxLayout, QTableWidget, QStackedLayout, QProgressBar, QSpinBox, \
    QFileDialog, QMessageBox, QHeaderView, QAbstractItemView, QMenu, QTableWidgetItem

import pdf_engine

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
    #'clear': str(ASSETS_DIR / 'cleaning.png'),
    'upper': str(ASSETS_DIR / 'upper-arrows.png'),
    'up': str(ASSETS_DIR / 'up-arrows.png'),
    'low': str(ASSETS_DIR / 'low-arrows.png'),
    'lower': str(ASSETS_DIR / 'lower-arrows.png'),
}

def createHorizontalLine():
    """Create Horizontal Line
    :return: return a fake line, is a QFrame
    """
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine) # Imposta la forma come linea orizzontale
    line.setFrameShadow(QFrame.Shadow.Sunken) # Dà l'effetto "inciso" (stile 3D leggero)
    line.setStyleSheet("color: #000000;") # Puoi colorarla via QSS o codice
    return line
# /createHorizontalLine

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Editor")
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
        """Tab Split GUI ctor
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
        grid.addWidget(btnSplitPathInput, 0, 1)
        # 5
        self.txtSplitPathInput = QLineEdit()
        self.txtSplitPathInput.setToolTip('Inserisci il percorso del file PDF di origine')
        self.txtSplitPathInput.setPlaceholderText('Percorso del file PDF di origine')
        grid.addWidget(self.txtSplitPathInput, 0, 2)
        # 6
        grid.addWidget(QLabel("Pagine:"), 1, 0)
        # 7 # QSpinBox()
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

        # Bottoni laterali 10-11-11a-11b-12-13-14-15 e Tabella 16.
        tableArea = QHBoxLayout()
        layout0.addLayout(tableArea)
        groupButtons =QVBoxLayout() # 10-11-11a-11b-12-13-14-15
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
        # 11b Elimina\nriga
        btnSplitTableDelRow = QPushButton()
        btnSplitTableDelRow.setIcon(QIcon(DICT_ASSETS['del-row']))
        btnSplitTableDelRow.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnSplitTableDelRow.setToolTip('Rimuovi la riga selezionata dalla tabella')
        groupButtons.addWidget(btnSplitTableDelRow)
        # 11c Svuota
        btnSplitTableClear = QPushButton()
        btnSplitTableClear.setIcon(QIcon(DICT_ASSETS['clear']))
        btnSplitTableClear.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnSplitTableClear.setToolTip('Svuota la tabella')
        groupButtons.addWidget(btnSplitTableClear)
        # Spazio elastico.Spinge i bottoni in alto
        groupButtons.addStretch()
        # 12 ^^
        btnSplitTableUpper=QPushButton()
        btnSplitTableUpper.setIcon(QIcon(DICT_ASSETS['upper']))
        btnSplitTableUpper.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnSplitTableUpper.setToolTip('Sposta la riga selezionata in cima')
        groupButtons.addWidget(btnSplitTableUpper)
        # 13 ^
        btnSplitTableUp = QPushButton()
        btnSplitTableUp.setIcon(QIcon(DICT_ASSETS['up']))
        btnSplitTableUp.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnSplitTableUp.setToolTip('Sposta la riga selezionata in alto di una posizione')
        groupButtons.addWidget(btnSplitTableUp)
        # 14 v
        btnSplitTableLow = QPushButton()
        btnSplitTableLow.setIcon(QIcon(DICT_ASSETS['low']))
        btnSplitTableLow.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnSplitTableLow.setToolTip('Sposta la riga selezionata in basso di una posizione')
        groupButtons.addWidget(btnSplitTableLow)
        # 15 vv
        btnSplitTableLower = QPushButton()
        btnSplitTableLower.setIcon(QIcon(DICT_ASSETS['lower']))
        btnSplitTableLower.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnSplitTableLower.setToolTip('Sposta la riga selezionata in fondo')
        groupButtons.addWidget(btnSplitTableLower)
        # 16
        self.tableSplitOutput =QTableWidget(0,4)
        self.tableSplitOutput.setHorizontalHeaderLabels(["Percorso File", "Intervalli", "Pagine", "Eseguito"])
        # Layout della tabella
        header = self.tableSplitOutput.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Il path si allunga
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.tableSplitOutput.setColumnWidth(2, 60)
        self.tableSplitOutput.setColumnWidth(3, 60)
        # Selezione e Drag & Drop interno
        self.tableSplitOutput.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableSplitOutput.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        tableArea.addWidget(self.tableSplitOutput)

        # 17 separatore
        layout0.addWidget(createHorizontalLine())

        # 18
        btnSplit =QPushButton('Split')
        btnSplit.setToolTip('Esegue effettivamente lo Split e Ruota sul File System')
        layout0.addWidget(btnSplit, alignment=Qt.AlignmentFlag.AlignCenter)

        # 19
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
        grid.addWidget(btnMergePathOutput, 0, 1)
        # 5
        self.txtMergePathOutput = QLineEdit()
        self.txtMergePathOutput.setToolTip('Inserisci il percorso del file PDF che verrà riunito')
        self.txtMergePathOutput.setPlaceholderText('Percorso del file PDF che verrà riunito')
        grid.addWidget(self.txtMergePathOutput, 0, 2)
        layout0.addLayout(grid)

        # 8 separatore
        layout0.addWidget(createHorizontalLine())

        # 9 sottotitolo
        subtitle = QLabel("Tabella di Input")
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout0.addWidget(subtitle)

        # Bottoni laterali 10-11-11a-11b-12-13-14-15 e Tabella 16.
        tableArea = QHBoxLayout()
        layout0.addLayout(tableArea)
        groupButtons = QVBoxLayout()  # 10-11-11a-11b-12-13-14-15
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
        # 11a Copia\nriga
        btnMergeTableCopyRow = QPushButton()
        btnMergeTableCopyRow.setIcon(QIcon(DICT_ASSETS['copy-row']))
        btnMergeTableCopyRow.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnMergeTableCopyRow.setToolTip("Copia la riga selezionata alla tabella")
        groupButtons.addWidget(btnMergeTableCopyRow)

        # 11b Elimina\nriga
        btnMergeTableDelRow = QPushButton()
        btnMergeTableDelRow.setIcon(QIcon(DICT_ASSETS['del-row']))
        btnMergeTableDelRow.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnMergeTableDelRow.setToolTip('Rimuovi la riga selezionata dalla tabella')
        groupButtons.addWidget(btnMergeTableDelRow)
        # 11c Svuota
        btnMergeTableClear = QPushButton()
        btnMergeTableClear.setIcon(QIcon(DICT_ASSETS['clear']))
        btnMergeTableClear.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnMergeTableClear.setToolTip('Svuota la tabella')
        groupButtons.addWidget(btnMergeTableClear)
        # Spazio elastico.Spinge i bottoni in alto
        groupButtons.addStretch()
        # 12 ^^
        btnMergeTableUpper = QPushButton()
        btnMergeTableUpper.setIcon(QIcon(DICT_ASSETS['upper']))
        btnMergeTableUpper.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnMergeTableUpper.setToolTip('Sposta la riga selezionata in cima')
        groupButtons.addWidget(btnMergeTableUpper)
        # 13 ^
        btnMergeTableUp = QPushButton()
        btnMergeTableUp.setIcon(QIcon(DICT_ASSETS['up']))
        btnMergeTableUp.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnMergeTableUp.setToolTip('Sposta la riga selezionata in alto di una posizione')
        groupButtons.addWidget(btnMergeTableUp)
        # 14 v
        btnMergeTableLow = QPushButton()
        btnMergeTableLow.setIcon(QIcon(DICT_ASSETS['low']))
        btnMergeTableLow.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnMergeTableLow.setToolTip('Sposta la riga selezionata in basso di una posizione')
        groupButtons.addWidget(btnMergeTableLow)
        # 15 vv
        btnMergeTableLower = QPushButton()
        btnMergeTableLower.setIcon(QIcon(DICT_ASSETS['lower']))
        btnMergeTableLower.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnMergeTableLower.setToolTip('Sposta la riga selezionata in fondo')
        groupButtons.addWidget(btnMergeTableLower)
        # 16
        self.tableMergeInput =QTableWidget(0,5)
        self.tableMergeInput.setHorizontalHeaderLabels(["Percorso File", "MaxPag", "Intervalli", "Pagine", "Eseguito"])
        # Layout della tabella
        header = self.tableMergeInput.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Il path si allunga
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.tableMergeInput.setColumnWidth(1, 60)
        self.tableMergeInput.setColumnWidth(3, 60)
        self.tableMergeInput.setColumnWidth(4, 60)
        # Selezione e Drag & Drop interno
        self.tableMergeInput.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableMergeInput.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        tableArea.addWidget(self.tableMergeInput)

        # 17 separatore
        layout0.addWidget(createHorizontalLine())

        # 18
        btnMerge = QPushButton('Merge')
        btnMerge.setToolTip('Esegue effettivamente il Merge e Ruota sul File System')
        layout0.addWidget(btnMerge, alignment=Qt.AlignmentFlag.AlignCenter)

        # 19
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
        """ Initialize Tab Info
        :return:
        """
        layout0 = QVBoxLayout(self.tabInfo)
        # 2. Titolo
        title = QLabel("Informazioni")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout0.addWidget(title)

    # /initTabInfo
# /MainWindow


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
# /if