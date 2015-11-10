from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from collections import OrderedDict


class GoodTableModel(QAbstractTableModel):
    def __init__(self, truck_number, good_numbers, good_data, truck_name):
        super(GoodTableModel, self).__init__()
        self.good_data = good_data
        self.number_of_goods = good_numbers
        self.number_of_trucks = truck_number
        self.truck_name = truck_name

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return self.number_of_trucks

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return self.number_of_goods

    def flags(self, QModelIndex):
        if not QModelIndex.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        if not(0 < self.number_of_trucks):
            return QVariant()
        if Qt_Orientation == Qt.Vertical:
            if int_role == Qt.DisplayRole:
                return QVariant(self.truck_name + str(p_int))
            else:
                return QVariant()
        if Qt_Orientation == Qt.Horizontal:
            if int_role == Qt.DisplayRole:
                return QVariant(p_int + 1)
            else:
                return QVariant()

    def change_good_number(self, amount):
        if self.number_of_goods < amount:
            self.insertColumns(self.number_of_goods, amount)
            for good in self.good_data:
                good.extend([0] * (amount - self.number_of_goods))
        elif self.number_of_goods > amount:
            self.removeColumns(self.number_of_goods, amount)
            for good in self.good_data:
                del(good[amount:])
        self.number_of_goods = amount

    def truck_number(self, amount):
        if self.number_of_trucks < amount:
            self.insertRows(self.number_of_trucks, amount)
            self.good_data.append([0] * self.number_of_goods)
        elif self.number_of_trucks > amount:
            self.removeRows(self.number_of_trucks, amount)
            self.good_data.pop()
        self.number_of_trucks = amount

    def insertRows(self, p_int, p_int_1, QModelIndex_parent=None, *args, **kwargs):
        self.beginInsertRows(QModelIndex(), p_int, p_int_1 - 1)
        self.endInsertRows()
        return True

    def removeRows(self, p_int, p_int_1, QModelIndex_parent=None, *args, **kwargs):
        self.beginRemoveRows(QModelIndex(), p_int_1, p_int - 1)
        self.endRemoveRows()
        return True

    def insertColumns(self, p_int, p_int_1, QModelIndex_parent=None, *args, **kwargs):
        self.beginInsertColumns(QModelIndex(), p_int, p_int_1 - 1)
        self.endInsertColumns()
        return True

    def removeColumns(self, p_int, p_int_1, QModelIndex_parent=None, *args, **kwargs):
        self.beginRemoveColumns(QModelIndex(), p_int_1, p_int - 1)
        self.endRemoveColumns()
        return True

    def setData(self, QModelIndex, QVariant, int_role=None):
        if int_role == Qt.EditRole:
            if QModelIndex.isValid():
                try:
                    self.good_data[QModelIndex.row()][QModelIndex.column()] = float(QVariant)
                except:
                    pass
                return True
            return False
        return False


    def data(self, QModelIndex, int_role=None):
        if not QModelIndex.isValid() or not(0 < len(self.good_data)):
            return QVariant()
        if int_role == Qt.DisplayRole:
            return QVariant(self.good_data[QModelIndex.row()][QModelIndex.column()])

        else:
            return QVariant()

