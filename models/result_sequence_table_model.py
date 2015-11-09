from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ResultSequenceTableModel(QAbstractTableModel):
    def __init__(self, results, data):
        super(ResultSequenceTableModel, self).__init__()
        self.coming_sequence = results.sequence.coming_sequence
        self.going_sequence = results.sequence.going_sequence
        self.v_header = ('coming', 'going')

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return 2

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return max(len(self.coming_sequence), len(self.going_sequence))

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        if int_role == Qt.DisplayRole:
            if Qt_Orientation == Qt.Vertical:
                return QVariant(self.v_header[p_int])
            elif Qt_Orientation == Qt.Horizontal:
                return QVariant(p_int + 1)
        else:
            return QVariant()

    def data(self, QModelIndex, int_role=None):
        if not QModelIndex.isValid():
            return QVariant()
        if int_role == Qt.DisplayRole:
            if QModelIndex.row() == 0:
                if QModelIndex.column() < len(self.coming_sequence):
                    return QVariant(self.coming_sequence[QModelIndex.column()])
                else:
                    return QVariant()
            elif QModelIndex.row() == 1:
                if QModelIndex.column() < len(self.going_sequence):
                    return QVariant(self.going_sequence[QModelIndex.column()])
                else:
                    return QVariant()
        else:
            return QVariant()

