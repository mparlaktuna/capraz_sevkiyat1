from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class SequenceTableModel(QAbstractTableModel):
    def __init__(self, results, table_type, data):
        super(SequenceTableModel, self).__init__()
        self.data = data
        self.results = results
        self.table_type = table_type #0 for coming 1 for going

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.results)

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        if self.table_type == 0:
            return len(self.data.coming_truck_name_list) + self.data.number_of_receiving_doors - 1
        else:
            return len(self.data.going_truck_name_list) + self.data.number_of_shipping_doors - 1

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        if int_role == Qt.DisplayRole:
            return QVariant(p_int + 1)
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
            if self.table_type == 0:
                return QVariant(self.results[QModelIndex.row()].sequence.coming_sequence[QModelIndex.column()])
            else:
                return QVariant(self.results[QModelIndex.row()].sequence.going_sequence[QModelIndex.column()])
        else:
            return QVariant()
