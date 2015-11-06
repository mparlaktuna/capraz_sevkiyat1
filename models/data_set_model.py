from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class DataSetModel(QAbstractTableModel):
    def __init__(self, data_set):
        super(DataSetModel, self).__init__()
        self.data = data_set.data_sets
        self.header = ['alpha', 'gamma', 'tightness']

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.data)

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.header)

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        if Qt_Orientation == Qt.Horizontal:
            if int_role == Qt.DisplayRole:
                return QVariant(self.header[p_int])
            else:
                return QVariant()

    def data(self, QModelIndex, int_role=None):
        if not QModelIndex.isValid() or not(0 < len(self.data)):
            return QVariant()
        if int_role == Qt.DisplayRole:
            return QVariant(self.data[QModelIndex.row()][QModelIndex.column()])
        else:
            return QVariant()

    def insertRows(self, p_int, p_int_1, QModelIndex_parent=None, *args, **kwargs):
        self.beginInsertRows(QModelIndex(), p_int, p_int_1 - 1)
        for i in range(p_int_1 - p_int):
            self.data.append([0, 0, 0])
        self.endInsertRows()
        return True

    def flags(self, QModelIndex):
        if not QModelIndex.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def removeRows(self, p_int, p_int_1, QModelIndex_parent=None, *args, **kwargs):
        self.beginRemoveRows(QModelIndex(), p_int_1, p_int - 1)
        for i in range(p_int - p_int_1):
            self.data.pop()
        self.endRemoveRows()
        return True

    def setData(self, QModelIndex, QVariant, int_role=None):
        if int_role == Qt.EditRole:
            if QModelIndex.isValid():
                try:
                    self.data[QModelIndex.row()][QModelIndex.column()] = float(QVariant)
                except:
                    pass
                return True
            return False
        return False



