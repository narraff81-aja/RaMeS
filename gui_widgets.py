from pathlib import Path

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QDialog, QApplication, QVBoxLayout, QLabel, QHBoxLayout, QMainWindow, QPushButton, \
    QTableWidget, QHeaderView, QAbstractItemView, QMenu, QSpinBox, QComboBox, QWidget, QTableWidgetItem, QFrame, \
    QLineEdit, QMessageBox

from pdf_engine import pagesCountAndCheck


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
    # 'add-row': str(ASSETS_DIR / 'aggiungi-32.png'),
    #'edit-interval': str(ASSETS_DIR / 'edit-32.png'),
    # 'copy-row': str(ASSETS_DIR / 'copia-48.png'),
    # 'del-row': str(ASSETS_DIR / 'cancel-32.png'),
    # 'clear': str(ASSETS_DIR / 'clear.png'),
    # 'upper': str(ASSETS_DIR / 'upper-arrows.png'),
    # 'up': str(ASSETS_DIR / 'up-arrows.png'),
    # 'low': str(ASSETS_DIR / 'low-arrows.png'),
    # 'lower': str(ASSETS_DIR / 'lower-arrows.png'),
    'swap': str(ASSETS_DIR / 'swap.png'),
    # 'degree0-add': str(ASSETS_DIR / 'icons8-0-gradi-40.png'),
    # 'degree90-add': str(ASSETS_DIR / 'icons8-90-gradi-40.png'),
    # 'degree180-add': str(ASSETS_DIR / 'icons8-180-gradi-40.png'),
    # 'degree270-add': str(ASSETS_DIR / 'icons8-270-gradi-40.png'),
    # 'degree0-set': str(ASSETS_DIR / 'icons8-0-gradi-80.png'),
    # 'degree90-set': str(ASSETS_DIR / 'icons8-90-gradi-80.png'),
    # 'degree180-set': str(ASSETS_DIR / 'icons8-180-gradi-80.png'),
    # 'degree270-set': str(ASSETS_DIR / 'icons8-270-gradi-80.png'),
}

def createItemHandle():
    """ Create a table row handle for easier Drag & Drop

    :return:
    """
    # itemHandle =QTableWidgetItem("↕")
    # itemHandle.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    # itemHandle.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsDragEnabled)

    itemHandle = QTableWidgetItem()
    itemHandle.setIcon(QIcon(DICT_ASSETS['swap']))
    itemHandle.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsDragEnabled)

    return itemHandle
# /createItemHandle

def createHorizontalLine()-> QFrame:
    """Create Horizontal Line
    :return: return a fake line, is a QFrame
    """
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine) # Imposta la forma come linea orizzontale
    line.setFrameShadow(QFrame.Shadow.Sunken) # Dà l'effetto "inciso" (stile 3D leggero)
    line.setStyleSheet("color: #000000;")
    return line
# /createHorizontalLine

class DropQLineEdit(QLineEdit):
    """ A QLineEdit that accepts Drop of PDF file from File System
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True) # Abilita il drop sul widget
        self.maxPages = 0 # Per passare il valore all'altro QLineEdit
    # /__init__
    def dragEnterEvent(self, event):
        # L'utente sta trascinando effettivamente dei file (URL)?
        if event.mimeData().hasUrls():
            event.accept() # Mostra l'icona "Copia/Sposta"
        else:
            event.ignore()
    # /dragEnterEvent
    def dropEvent(self, event):
        # Prendiamo il primo file della lista (nel caso l'utente ne trascini 1+)
        files = event.mimeData().urls()
        if files:
            path = files[0].toLocalFile().strip()
            try:
                self.maxPages = pagesCountAndCheck(path)
                self.setText(path)
                self.editingFinished.emit()  # Avvisa la MainWindow
            except Exception as e:
                self.maxPages = 0
                self.setText("")
                self.editingFinished.emit()
                # NO clipboard per Drag & Drop
                QMessageBox.critical(self, "Errore PDF nel Drag & Drop!", str(e))
        # /if
    # /dropEvent
    def clearAll(self):
        """ Reset QLineEdit state """
        self.clear()
        self.maxPages = 0
    # /clearAll
# /PDFDropLineEdit

class BaseQTable(QTableWidget):
    """ QTableWidget with improved internal drag & drop management and
    basic functions to move/create/delete a row
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimumWidth(20)
        # setup Drag & Drop
        self.viewport().setAcceptDrops(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove) # NO .DragDrop
    # /__init__

    def getRowData(self,idRow: int)->dict:
        """ Get row values as dictionary. (raise a NotImplementedError)

        :param idRow: Ref. ID Row
        """
        raise NotImplementedError
    # /getRowData
    def setRowData(self, idRow: int, args: dict):
        """ Set row values from a dictionary. (raise a NotImplementedError)

        :param idRow: Ref. ID Row
        :param args: Dictionary
        """
        raise NotImplementedError
    # /setRowData
    def addRow(self,idRow: int, **kwargs):
        """ Adds a row to the table. (raise a NotImplementedError)

        :param idRow: Ref. ID Row
        :param kwargs: args as dictionary
        """
        raise NotImplementedError
    # /addRow
    def swapRows(self, idRowFrom: int, idRowTo: int):
        """ Swap 2 rows to the table. (Basic implementation)

        :param idRowFrom: Ref. ID Row origin
        :param idRowTo: Ref. ID Row destination
        """
        d1, d2 = self.getRowData(idRowFrom), self.getRowData(idRowTo)
        self.setRowData(idRowFrom, d2)
        self.setRowData(idRowTo, d1)
        self.setCurrentCell(idRowTo, 0)
    # /swapRows

    def tableAddRow(self):
        """ Appends a row to the table. (raise a NotImplementedError)
        """
        raise NotImplementedError
    # /tableAddRow
    def tableCopyRow(self):
        """ Copy below a pre-selected row in the table
        """
        idRow = self.currentRow()
        if idRow<0:
            return
        data = self.getRowData(idRow)
        self.addRow(idRow+1,**data)
        self.setCurrentCell(idRow+1, 0)
    # /tableCopyRow
    def tableRemoveRow(self):
        """ Remove a pre-selected row in the table
        """
        idRow = self.currentRow()
        if idRow>=0:
            self.removeRow(idRow)
    # /tableRemoveRow
    def tableClear(self):
        """ Remove all rows in the table
        """
        # table.clear() # NO, perché azzererebbe anche le colonne!
        self.setRowCount(0)
    # /tableClear
    def tableMoveUpperRow(self):
        """ Moves a pre-selected table row to the top
        """
        idRow = self.currentRow()
        if idRow > 0:
            self.swapRows(idRow,0)
            self.setCurrentCell(0, 0)
    # /tableMoveUpperRow
    def tableMoveUpRow(self):
        """ Move a pre-selected table row up one position
        """
        idRow = self.currentRow()
        if idRow > 0:
            self.swapRows(idRow, idRow-1)
            self.setCurrentCell(idRow - 1, 0)
    # /tableMoveUpRow
    def tableMoveLowRow(self):
        """ Moves a pre-selected table row down one position
        """
        idRow = self.currentRow()
        rowMax = self.rowCount()
        if idRow < rowMax - 1:
            self.swapRows(idRow, idRow + 1)
            self.setCurrentCell(idRow+1, 0)
    # /tableMoveLowRow
    def tableMoveLowerRow(self):
        """ Move a pre-selected row of the table to the bottom
        """
        idRow = self.currentRow()
        rowMax = self.rowCount()
        if idRow < rowMax - 1:
            self.swapRows(idRow, rowMax - 1)
            self.setCurrentCell(rowMax-1, 0)
    # /tableMoveLowerRow

    def dropEvent(self, event):
        sourceRow = self.currentRow()

        # Punto di rilascio relativo al viewport della tabella
        pos = event.position().toPoint()
        targetRow = self.rowAt(pos.y())

        # CASO A: Drop nello spazio vuoto sotto l'ultima riga
        if targetRow == -1:
            targetRow = self.rowCount() - 1
        # Se siamo ancora a -1 (tabella vuota), ignoriamo
        if targetRow < 0:
            event.ignore()
            return

        # CASO B: Drop a destra fuori dalle colonne
        if pos.x() > self.horizontalHeader().length():
            # Qui decidiamo: o ignoriamo o accettiamo comunque la riga (scelta consigliata)
            pass

        # 3. Eseguiamo lo SWAP se le righe sono diverse
        if sourceRow != -1 and sourceRow != targetRow:
            self.swapRows(sourceRow, targetRow)
            self.setCurrentCell(targetRow, 0)
            event.accept()
        else:
            event.ignore()
    # /dropEvent
# /BasePDFTable