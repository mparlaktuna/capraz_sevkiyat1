from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ResultGoodTableModel(QAbstractTableModel):
    def __init__(self, results, data):
        super(ResultGoodTableModel, self).__init__()
        self.goods = results.goods
        self.data = data
        self.v_header = list(self.goods.keys())
        self.h_header = self.data.coming_truck_name_list

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.v_header)

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.h_header)

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        if int_role == Qt.DisplayRole:
            if Qt_Orientation == Qt.Vertical:
                return QVariant(self.v_header[p_int])
            elif Qt_Orientation == Qt.Horizontal:
                return QVariant(self.h_header[p_int])
        else:
            return QVariant()

    def data(self, QModelIndex, int_role=None):
        if not QModelIndex.isValid():
            return QVariant()
        if int_role == Qt.DisplayRole:
            going_truck_name = self.v_header[QModelIndex.row()]
            coming_truck_name = self.h_header[QModelIndex.column()]
            if coming_truck_name in self.goods[going_truck_name]:
                return QVariant(self.goods[going_truck_name][coming_truck_name])
            else:
                return QVariant(0)
        else:
            return QVariant()
