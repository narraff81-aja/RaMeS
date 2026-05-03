from pathlib import Path
from typing import cast
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QDialog, QApplication, QVBoxLayout, QLabel, QHBoxLayout, QMainWindow, QPushButton, \
    QTableWidget, QHeaderView, QAbstractItemView, QMenu, QSpinBox, QComboBox, QWidget, QTableWidgetItem

from gui_widgets import BaseQTable, createItemHandle
from intervals import Rotation, Interval, intervalsParse, intervalsToString

# BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = Path(__file__).resolve().parent / "assets"
"""Assets directory
"""
SIZE_ICON = 24
DICT_ASSETS={
    'icon': str(ASSETS_DIR / 'icon.ico'),
    #'tab-split': str(ASSETS_DIR / 'split.png'),
    #'tab-merge': str(ASSETS_DIR / 'merge.png'),
    #'tab-info': str(ASSETS_DIR / 'information.png'),
    #'load': str(ASSETS_DIR / 'load-32.png'),
    'add-row': str(ASSETS_DIR / 'aggiungi-32.png'),
    #'edit-interval': str(ASSETS_DIR / 'edit-32.png'),
    'copy-row': str(ASSETS_DIR / 'copia-48.png'),
    'del-row': str(ASSETS_DIR / 'cancel-32.png'),
    'clear': str(ASSETS_DIR / 'clear.png'),
    'upper': str(ASSETS_DIR / 'upper-arrows.png'),
    'up': str(ASSETS_DIR / 'up-arrows.png'),
    'low': str(ASSETS_DIR / 'low-arrows.png'),
    'lower': str(ASSETS_DIR / 'lower-arrows.png'),
    'swap': str(ASSETS_DIR / 'swap.png'),
    'degree0-add': str(ASSETS_DIR / 'icons8-0-gradi-40.png'),
    'degree90-add': str(ASSETS_DIR / 'icons8-90-gradi-40.png'),
    'degree180-add': str(ASSETS_DIR / 'icons8-180-gradi-40.png'),
    'degree270-add': str(ASSETS_DIR / 'icons8-270-gradi-40.png'),
    'degree0-set': str(ASSETS_DIR / 'icons8-0-gradi-80.png'),
    'degree90-set': str(ASSETS_DIR / 'icons8-90-gradi-80.png'),
    'degree180-set': str(ASSETS_DIR / 'icons8-180-gradi-80.png'),
    'degree270-set': str(ASSETS_DIR / 'icons8-270-gradi-80.png'),
}

class IntervalsQTable(BaseQTable):
    """ QTableWidget that manages page Intervals
    """
    def __init__(self, maxPages: int):
        super().__init__(0, 4)
        self.maxPages=maxPages
        self.setHorizontalHeaderLabels(["", "Da pagina", "A pagina", "Rotazione"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Layout della tabella
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.setColumnWidth(0, 25)
        self.model().setHeaderData(3, Qt.Orientation.Horizontal,
                                         "Rotazione di ogni intervallo:\n"
                                         "- rotazioni aggiuntive: +0°, +90°, +180°, +270°\n"
                                         "- rotazioni imposte: 0°, 90°, 180°, 270°",
                                         Qt.ItemDataRole.ToolTipRole)
    # /__init__

    def addRow(self,idRow: int, start: int =1, end: int =1, idRot: int =0):
        """Adds a row to the table

        :param idRow: Ref. ID Row
        :param start: Value for FromPage
        :param end: Value for ToPage
        :param idRot: Value for Interval Rotation
        """
        self.insertRow(idRow)

        # 0.
        self.setItem(idRow, 0, createItemHandle())

        # 1. SpinBox per 'Da Pagina'
        spinStart = QSpinBox()
        spinStart.setRange(1, self.maxPages)
        spinStart.setValue(start)
        spinStart.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setCellWidget(idRow, 1, spinStart)

        # 2. SpinBox per 'A Pagina'
        spinEnd = QSpinBox()
        spinEnd.setRange(1, self.maxPages)
        spinEnd.setValue(end)
        spinEnd.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setCellWidget(idRow, 2, spinEnd)

        # 3. ComboBox per Rotazione
        comboRot = QComboBox()
        self.setupRotationComboBox(comboRot)
        comboRot.setCurrentIndex(idRot)
        self.setCellWidget(idRow, 3, comboRot)
    # /addRow
    def setupRotationComboBox(self, combo: QComboBox):
        """ Function to fill the single QComboBox with text and images

        :param combo: Ref. QComboBox
        """
        rotations = [
            ("+0°", 0, DICT_ASSETS['degree0-add']),
            ("+90°", 90, DICT_ASSETS['degree90-add']),
            ("+180°", 180, DICT_ASSETS['degree180-add']),
            ("+270°", 270, DICT_ASSETS['degree270-add']),
            ("0°", 360, DICT_ASSETS['degree0-set']),
            ("90°", 450, DICT_ASSETS['degree90-set']),
            ("180°", 540, DICT_ASSETS['degree180-set']),
            ("270°", 630, DICT_ASSETS['degree270-set']),
        ]
        for text, val, icon_name in rotations:
            combo.addItem(QIcon(icon_name), text, val)
    # /setupRotationComboBox
    def getRowData(self,idRow: int)->dict:
        """ Get row values as dictionary

        :param idRow: Ref. ID Row
        :return:
        """
        start = cast(QSpinBox,self.cellWidget(idRow, 1)).value()
        end = cast(QSpinBox,self.cellWidget(idRow, 2)).value()
        rot = cast(QComboBox,self.cellWidget(idRow, 3)).currentIndex()
        return {'start':start, 'end':end, 'idRot':rot}
    # /getRowData
    def setRowData(self, idRow: int, data: dict):
        # Se per qualche motivo l'item della maniglia è sparito durante il drag, lo ricreiamo
        #if not self.item(idRow, 0):
        self.setItem(idRow, 0, createItemHandle())
        obj1 =cast(QSpinBox, self.cellWidget(idRow, 1))
        obj1.setValue(data['start'])
        obj2 = cast(QSpinBox,self.cellWidget(idRow, 2))
        obj2.setValue(data['end'])
        obj3 =cast(QComboBox, self.cellWidget(idRow, 3))
        obj3.setCurrentIndex(data['idRot'])
    # /setRowData
    def tableAddRow(self):
        """ Appends a row to the table
        """
        idRow = self.rowCount()
        self.addRow(idRow,1,1,0)
        self.setCurrentCell(idRow, 0)
    # /tableAddRow
    def tableCopyRow(self):
        """ Copy below a pre-selected row in the table
        """
        idRow = self.currentRow()
        if idRow < 0:
            return
        data = self.getRowData(idRow)
        self.addRow(idRow + 1, data['start'], data['end'], data['idRot'])
        self.setCurrentCell(idRow + 1, 0)
    # /mergeTableCopyRow
# /IntervalsTable

class IntervalsHelper(QDialog):
    """ QDialog Modal window to help end-user choose pages Intervals
    """
    def __init__(self, parent, maxPages: int, currentIntervals: str):
        super().__init__(parent)
        self.setWindowTitle('RaMeS - Gestore Intervalli')
        self.setModal(True)  # 1: Finestra modale
        self.resize(450, 400)
        self.setMinimumSize(450, 400)
        self.maxPages = maxPages
        self.oldIntervals = currentIntervals

        layout = QVBoxLayout(self)

        # 2. Titolo
        title = QLabel('Finestra di gestore di intervalli')
        title.setFont(QFont('Arial', 14))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 6-7. info MaxPages
        lblMaxPages=QLabel(f'Pagine max: {self.maxPages}')
        lblMaxPages.setFont(QFont("Arial", 12))
        lblMaxPages.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lblMaxPages)

        # Bottoni laterali 10-12-13-14-15-16-17-18 e Tabella 19.
        tableArea = QHBoxLayout()
        layout.addLayout(tableArea)
        groupButtons = QVBoxLayout()  # 10-11-12-13-14-15-16-17-18
        tableArea.addLayout(groupButtons)

        # 10 Aggiungi\nriga
        btnTableAddRow = QPushButton()
        btnTableAddRow.setIcon(QIcon(DICT_ASSETS['add-row']))
        btnTableAddRow.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnTableAddRow.setToolTip('Aggiungi riga alla tabella')
        btnTableAddRow.clicked.connect(self.tableAddRow)
        groupButtons.addWidget(btnTableAddRow)
        # 12 Copia\nriga
        btnTableCopyRow = QPushButton()
        btnTableCopyRow.setIcon(QIcon(DICT_ASSETS['copy-row']))
        btnTableCopyRow.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnTableCopyRow.setToolTip("Copia la riga selezionata alla tabella")
        btnTableCopyRow.clicked.connect(self.tableCopyRow)
        groupButtons.addWidget(btnTableCopyRow)
        # 13 Elimina\nriga
        btnTableDelRow = QPushButton()
        btnTableDelRow.setIcon(QIcon(DICT_ASSETS['del-row']))
        btnTableDelRow.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnTableDelRow.setToolTip('Rimuovi la riga selezionata dalla tabella')
        btnTableDelRow.clicked.connect(self.tableRemoveRow)
        groupButtons.addWidget(btnTableDelRow)
        # 14 Svuota
        btnTableClear = QPushButton()
        btnTableClear.setIcon(QIcon(DICT_ASSETS['clear']))
        btnTableClear.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnTableClear.setToolTip('Svuota la tabella')
        btnTableClear.clicked.connect(self.tableClear)
        groupButtons.addWidget(btnTableClear)
        # Spazio elastico.Spinge i bottoni in alto
        groupButtons.addStretch()
        # 15 ^^
        btnTableUpper = QPushButton()
        btnTableUpper.setIcon(QIcon(DICT_ASSETS['upper']))
        btnTableUpper.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnTableUpper.setToolTip('Sposta la riga selezionata in cima')
        btnTableUpper.clicked.connect(self.tableMoveUpperRow)
        groupButtons.addWidget(btnTableUpper)
        # 16 ^
        btnTableUp = QPushButton()
        btnTableUp.setIcon(QIcon(DICT_ASSETS['up']))
        btnTableUp.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnTableUp.setToolTip('Sposta la riga selezionata in alto di una posizione')
        btnTableUp.clicked.connect(self.tableMoveUpRow)
        groupButtons.addWidget(btnTableUp)
        # 17 v
        btnTableLow = QPushButton()
        btnTableLow.setIcon(QIcon(DICT_ASSETS['low']))
        btnTableLow.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnTableLow.setToolTip('Sposta la riga selezionata in basso di una posizione')
        btnTableLow.clicked.connect(self.tableMoveLowRow)
        groupButtons.addWidget(btnTableLow)
        # 18 vv
        btnTableLower = QPushButton()
        btnTableLower.setIcon(QIcon(DICT_ASSETS['lower']))
        btnTableLower.setIconSize(QSize(SIZE_ICON, SIZE_ICON))
        btnTableLower.setToolTip('Sposta la riga selezionata in fondo')
        btnTableLower.clicked.connect(self.tableMoveLowerRow)
        groupButtons.addWidget(btnTableLower)

        # 19 Tabella
        self.table =  IntervalsQTable(maxPages)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(
            lambda pos: self.showContextMenu(pos)
        )
        tableArea.addWidget(self.table)
        # aggiungi righe in base agli ntervalli passati
        currIntervals=intervalsParse(currentIntervals,maxPages)
        for interval in currIntervals:
            idRow = self.table.rowCount()
            self.table.addRow(idRow, interval.fromPage, interval.toPage, interval.rotation.value // 90)

        # 23-24. Bottoni OK / Cancel
        layout1=QHBoxLayout()
        layout.addLayout(layout1)#, alignment=Qt.AlignmentFlag.AlignCenter
        # 23
        btnOk = QPushButton("OK")
        btnOk.clicked.connect(self.accept)
        layout1.addWidget(btnOk)
        # 24
        btnCancel = QPushButton("Cancel")
        btnCancel.clicked.connect(self.reject)
        layout1.addWidget(btnCancel)
    # /__init__

    def tableAddRow(self):
        """ Appends a row to the table
        """
        self.table.tableAddRow()
    # /tableAddRow
    def tableCopyRow(self):
        """ Copy below a pre-selected row in the table
        """
        self.table.tableCopyRow()
    # /mergeTableCopyRow
    def tableRemoveRow(self):
        """ Remove a pre-selected row in the table
        """
        self.table.tableRemoveRow()
    # /tableRemoveRow
    def tableClear(self):
        """ Remove all rows in the table
        """
        self.table.tableClear()
    # /tableClear
    def tableMoveUpperRow(self):
        """ Moves a pre-selected table row to the top
        """
        self.table.tableMoveUpperRow()
    # /tableMoveUpperRow
    def tableMoveUpRow(self):
        """ Move a pre-selected table row up one position
        """
        self.table.tableMoveUpRow()
    # /tableMoveUpRow
    def tableMoveLowRow(self):
        """ Moves a pre-selected table row down one position
        """
        self.table.tableMoveLowRow()
    # /tableMoveLowRow
    def tableMoveLowerRow(self):
        """ Move a pre-selected row of the table to the bottom
        """
        self.table.tableMoveLowerRow()
    # /tableMoveLowerRow
    def showContextMenu(self, pos):
        """ ContextMenu of the table
        """
        menu = QMenu()
        actionTableAddRow = menu.addAction(QIcon(DICT_ASSETS['add-row']), "Aggiungi riga")
        actionTableAddRow.triggered.connect(self.tableAddRow)
        actionTableAddRow.setToolTip("Aggiungi riga alla tabella")

        actionTableCopyRow = menu.addAction(QIcon(DICT_ASSETS['copy-row']), "Copia riga")
        actionTableCopyRow.setToolTip("Copia riga alla tabella")
        actionTableCopyRow.triggered.connect(self.tableCopyRow)

        actionTableRemoveRow = menu.addAction(QIcon(DICT_ASSETS['del-row']), "Rimuovi riga")
        actionTableRemoveRow.triggered.connect(self.tableRemoveRow)
        actionTableRemoveRow.setToolTip("Rimuovi la riga selezionata dalla tabella")

        actionTableClear = menu.addAction(QIcon(DICT_ASSETS['clear']), "Svuota tabella")
        actionTableClear.triggered.connect(self.tableClear)
        actionTableClear.setToolTip("Svuota la tabella")

        menu.addSeparator()

        actionTableMoveUpperRow = menu.addAction(QIcon(DICT_ASSETS['upper']), 'Sposta in cima')
        actionTableMoveUpperRow.triggered.connect(self.tableMoveUpperRow)
        actionTableMoveUpperRow.setToolTip('Sposta la riga selezionata in cima')

        actionTableMoveUpRow = menu.addAction(QIcon(DICT_ASSETS['up']), 'Sposta in alto')
        actionTableMoveUpRow.triggered.connect(self.tableMoveUpRow)
        actionTableMoveUpRow.setToolTip('Sposta la riga selezionata in alto di una posizione')

        actionTableMoveLowRow = menu.addAction(QIcon(DICT_ASSETS['low']), 'Sposta in basso')
        actionTableMoveLowRow.triggered.connect(self.tableMoveLowRow)
        actionTableMoveLowRow.setToolTip('Sposta la riga selezionata in basso di una posizione')

        actionTableMoveLowerRow = menu.addAction(QIcon(DICT_ASSETS['lower']), 'Sposta in fondo')
        actionTableMoveLowerRow.triggered.connect(self.tableMoveLowerRow)
        actionTableMoveLowerRow.setToolTip('Sposta la riga selezionata in fondo')

        menu.exec(self.table.mapToGlobal(pos))
    # /show_context_menu

    def getIntervalsString(self)->str:
        """ Transforms the table contents into a string of Intervals
        :return: String of Intervals
        """
        resultIntervals = []
        for idRow in range(self.table.rowCount()):
            data = self.table.getRowData(idRow)
            resultIntervals.append(Interval(data['start'], data['end'],Rotation.fromInt( data['idRot']*90)))

        return intervalsToString(resultIntervals)
    # /get_intervals_data
# /IntervalsHelper


