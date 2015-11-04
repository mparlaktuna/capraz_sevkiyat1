from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class TimeTableModel(QAbstractTableModel):
    def __init__(self, times):
        super(TimeTableModel, self).__init__()
        self.times = times
        self.header = []
        if len(self.times) > 0:
            self.header = sorted(list(self.times[0].keys()))

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        if len(self.times) > 0:
             return len(self.times[0])
        return 0

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.times)

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        if Qt_Orientation == Qt.Vertical:
            if int_role == Qt.DisplayRole:
                return QVariant(self.header[p_int])
            else:
                return QVariant()
        if Qt_Orientation == Qt.Horizontal:
            if int_role == Qt.DisplayRole:
                return QVariant(p_int + 1)
            else:
                return QVariant()

    def data(self, QModelIndex, int_role=None):
        if not QModelIndex.isValid() or not(0 < len(self.times)):
            return QVariant()
        if int_role == Qt.DisplayRole:
            return QVariant(self.times[QModelIndex.column()][str(self.header[QModelIndex.row()])])

        else:
            return QVariant()