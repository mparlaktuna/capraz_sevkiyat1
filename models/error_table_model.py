from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class AnnealingErrorTableModel(QAbstractTableModel):
    def __init__(self, results, data):
        super(AnnealingErrorTableModel, self).__init__()
        self.data = data
        self.results = results
        self.header = ('error', 'temperature', 'p_accept', 'random number', 'decision')

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.results)

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return 5

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        if Qt_Orientation == Qt.Vertical:
            if int_role == Qt.DisplayRole:
                return QVariant(p_int + 1)
        if Qt_Orientation == Qt.Horizontal:
            if int_role == Qt.DisplayRole:
                return QVariant(self.header[p_int])
            else:
                return QVariant()

    def insertRows(self, p_int, p_int_1, QModelIndex_parent=None, *args, **kwargs):
        self.beginInsertRows(QModelIndex(), len(self.results), len(self.results))
        self.endInsertRows()
        return True

    def data(self, QModelIndex, int_role=None):
        if not QModelIndex.isValid() or not(0 < len(self.results)):
            return QVariant()
        if int_role == Qt.DisplayRole:
            if QModelIndex.column() == 0:
                return QVariant(self.results[QModelIndex.row()].sequence.error)
            if QModelIndex.column() == 1:
                return QVariant(self.results[QModelIndex.row()].sequence.values['temperature'])
            if QModelIndex.column() == 2:
                return QVariant(self.results[QModelIndex.row()].sequence.values['p_accept'])
            if QModelIndex.column() == 3:
                return QVariant(self.results[QModelIndex.row()].sequence.values['random_number'])
            if QModelIndex.column() == 4:
                return QVariant(self.results[QModelIndex.row()].sequence.values['decision'])
        if int_role == Qt.BackgroundRole:
            if self.results[QModelIndex.row()].sequence.values['decision'] == 'best sequence':
                return QBrush(Qt.yellow)
        else:
            return QVariant()


class TabuErrorTableModel(QAbstractTableModel):
    def __init__(self, results, data):
        super(TabuErrorTableModel, self).__init__()
        self.data = data
        self.results = results
        self.header = ('error', 'iteration number', 'decision')

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.results)

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return 3

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        if Qt_Orientation == Qt.Vertical:
            if int_role == Qt.DisplayRole:
                return QVariant(p_int + 1)
        if Qt_Orientation == Qt.Horizontal:
            if int_role == Qt.DisplayRole:
                return QVariant(self.header[p_int])
            else:
                return QVariant()

    def insertRows(self, p_int, p_int_1, QModelIndex_parent=None, *args, **kwargs):
        self.beginInsertRows(QModelIndex(), len(self.results), len(self.results))
        self.endInsertRows()
        return True

    def data(self, QModelIndex, int_role=None):
        if not QModelIndex.isValid() or not(0 < len(self.results)):
            return QVariant()
        if int_role == Qt.DisplayRole:
            if QModelIndex.column() == 0:
                return QVariant(self.results[QModelIndex.row()].sequence.error)
            if QModelIndex.column() == 1:
                return QVariant(self.results[QModelIndex.row()].sequence.values['iteration number'])
            if QModelIndex.column() == 2:
                return QVariant(self.results[QModelIndex.row()].sequence.values['decision'])
        if int_role == Qt.BackgroundRole:
            if self.results[QModelIndex.row()].sequence.values['decision'] == 'best sequence':
                return QBrush(Qt.yellow)
            if self.results[QModelIndex.row()].sequence.values['decision'] == 'tabu':
                return QBrush(Qt.red)
        else:
            return QVariant()

