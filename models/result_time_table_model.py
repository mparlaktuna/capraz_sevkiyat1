from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ResultTimeTableModel(QAbstractTableModel):
    def __init__(self, results, number_of_trucks, truck_name):
        super(ResultTimeTableModel, self).__init__()
        self.times = results.times
        try:
            self.v_header = [truck_name + str(i) for i in range(number_of_trucks)]

            self.h_header = [a[0] for a in self.times[self.v_header[0]]]
        except:
            pass

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        try:
            a = len(self.v_header)
        except:
            a = 0
        return a

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        try:
            a = len(self.h_header)
        except:
            a = 0
        return a

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        if int_role == Qt.DisplayRole:
            if Qt_Orientation == Qt.Vertical:
                try:
                    return QVariant(self.v_header[p_int])
                except:
                    return QVariant()
            elif Qt_Orientation == Qt.Horizontal:
                try:
                    return QVariant(self.h_header[p_int])
                except:
                    return QVariant()
        else:
            return QVariant()

    def data(self, QModelIndex, int_role=None):
        if not QModelIndex.isValid():
            return QVariant()
        if int_role == Qt.DisplayRole:
            try:
                return QVariant(self.times[self.v_header[QModelIndex.row()]][QModelIndex.column()][1])
            except:
                return QVariant()
        else:
            return QVariant()

