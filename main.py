import sys
import time
import pickle
from random import uniform
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from windows.main_window import Ui_MainWindow
from src.data_store import DataStore
from models.data_set_model import DataSetModel
from models.good_table_model import GoodTableModel
from models.time_table_model import TimeTableModel
from src.solver import Solver
from src.sequence import Sequence
from src.good_store import GoodStore
from src.door import Door


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.data = DataStore()
        self.data = pickle.load(open('deneme', 'rb'))
        self.truck_states = {}
        self.update_data_table()
        self.setup_data()
        self.connections()
        self.results = {}
        self.combobox_coming_sequence = []
        self.combobox_going_sequence = []
        self.statusBar().showMessage('Ready')
        self.setup_sequence_solver()
        self.load_generated_data()
        self.graphicsView.data = self.data
        self.setup_simulator()
        self.graphicsView.parent = self


    def setup_data(self):
        self.data_set_model = DataSetModel(self.data)
        self.datasettable.setModel(self.data_set_model)
        self.inbound_table_model = GoodTableModel(self.data.number_of_inbound_trucks, self.data.number_of_goods, self.data.inbound_goods, 'inbound')
        self.inbound_good_table.setModel(self.inbound_table_model)
        self.outbound_table_model = GoodTableModel(self.data.number_of_outbound_trucks, self.data.number_of_goods, self.data.outbound_goods, 'outbound')
        self.outbound_good_table.setModel(self.outbound_table_model)
        self.compound_coming_table_model = GoodTableModel(self.data.number_of_compound_trucks, self.data.number_of_goods, self.data.compound_coming_goods, 'compound_coming')
        self.compound_coming_good_table.setModel(self.compound_coming_table_model)
        self.compound_going_table_model = GoodTableModel(self.data.number_of_compound_trucks, self.data.number_of_goods, self.data.compound_going_goods, 'compound_going')
        self.compound_going_good_table.setModel(self.compound_going_table_model)

    def generate_times(self):
        self.data.arrival_times = []
        self.data.lower_boundaries = []
        self.data.upper_boundaries = []
        for k, data_set in enumerate(self.data.data_sets):
            self.data.arrival_times.append({})
            self.data.lower_boundaries.append({})
            self.data.upper_boundaries.append({})

            self.data.calculate_truck_related_data()
            for i in range(self.data.number_of_inbound_trucks):
                name = 'inbound' + str(i)
                two_gdj = self.calculate_2dgj(data_set[2], self.data.coming_mu, self.data.product_per_coming_truck)
                self.data.arrival_times[k][name] = int(uniform(self.data.inbound_arrival_time, two_gdj))

            for i in range(self.data.number_of_outbound_trucks):
                name = 'outbound' + str(i)
                two_gdj = self.calculate_2dgj(data_set[2], self.data.going_mu, self.data.product_per_going_truck)
                gdj = int(uniform(self.data.outbound_arrival_time, two_gdj))
                self.data.arrival_times[k][name] = gdj
                A = gdj + (self.data.going_mu - 1) * self.data.changeover_time + self.data.going_mu * self.data.product_per_going_truck * self.data.loading_time
                self.data.lower_boundaries[k][name] = A * data_set[0]
                self.data.upper_boundaries[k][name] = A * data_set[1]

            for i in range(self.data.number_of_compound_trucks):
                name = 'compound' + str(i)
                two_gdj = self.calculate_2dgj(data_set[2], self.data.coming_mu, self.data.product_per_coming_truck)
                gdj = int(uniform(self.data.outbound_arrival_time, two_gdj))
                self.data.arrival_times[k][name] = gdj
                A = gdj + (self.data.coming_mu - 1) * self.data.changeover_time + self.data.coming_mu * self.data.product_per_coming_truck * self.data.loading_time + self.data.changeover_time + self.data.truck_transfer_time +(self.data.going_mu - 1) * self.data.changeover_time + self.data.going_mu * self.data.product_per_going_truck * self.data.loading_time
                self.data.lower_boundaries[k][name] = A * data_set[0]
                self.data.upper_boundaries[k][name] = A * data_set[1]

        self.load_generated_data()

    def load_generated_data(self):
        self.arrival_time_table_model = TimeTableModel(self.data.arrival_times)
        self.arrival_time_table.setModel(self.arrival_time_table_model)
        self.leaving_lower_table_model = TimeTableModel(self.data.lower_boundaries)
        self.leaving_lower_table.setModel(self.leaving_lower_table_model)
        self.leaving_upper_table_model = TimeTableModel(self.data.upper_boundaries)
        self.leaving_upper_table.setModel(self.leaving_upper_table_model)

    def calculate_2dgj(self, tightness_factor, mu, product_per_truck):
        return (2 * mu * tightness_factor * product_per_truck) / (2 - tightness_factor * mu * self.data.makespan_factor)

    def connections(self):
        """
        create connections from buttons to functions
        :return:
        """
        self.numberOfDataSetsSpinBox.valueChanged.connect(self.set_data_set_table)
        self.loadingTumeLineEdit.textChanged.connect(self.data.set_loading_time)
        self.truckChangeoverTimeLineEdit.textChanged.connect(self.data.set_changeover_time)
        self.effectOfTheArrivalTimesOnMakespanLineEdit.textChanged.connect(self.data.set_makespan_factor)
        self.truckTransferTimeLineEdit.textChanged.connect(self.data.set_truck_transfer_time)
        self.inboundArrivalTimeLineEdit.textChanged.connect(self.data.set_inbound_arrival_time)
        self.outboundArrivalTimeLineEdit.textChanged.connect(self.data.set_outbound_arrival_time)
        self.goodTransferTimeLineEdit.textChanged.connect(self.data.set_good_transfer_time)

        self.numberOfInboundTrucksSpinBox.valueChanged.connect(self.set_inbound_truck_number)
        self.numberOfOutboundTrucksSpinBox.valueChanged.connect(self.set_outbound_truck_number)
        self.numberOfCompoundTrucksSpinBox.valueChanged.connect(self.set_compound_truck_number)
        self.numberOfCompoundTrucksSpinBox.valueChanged.connect(self.set_compound_truck_number)
        self.numberOfShippingDoorsSpinBox.valueChanged.connect(self.set_shipping_door_number)
        self.numberOfReceivingDoorsSpinBox.valueChanged.connect(self.set_receiving_door_number)
        self.numberOfGoodsSpinBox.valueChanged.connect(self.update_number_of_goods)

        self.solve_data_set_button.clicked.connect(self.solve_data_set)
        self.solve_one_sequence_button.clicked.connect(self.solve_one_sequence)
        self.actionNew_Data.triggered.connect(self.new_data)
        self.actionSave_Data.triggered.connect(self.save_data)
        self.actionLoad_Data.triggered.connect(self.load_data)
        self.pause_button.clicked.connect(self.pause)
        self.resume_button.clicked.connect(self.resume)
        self.generate_times_button.clicked.connect(self.generate_times)


    def new_data(self):
        self.data = DataStore()
        self.update_data_table()

    def set_inbound_truck_number(self, value):
        self.inbound_table_model.truck_number(value)
        self.data.number_of_inbound_trucks = value
        self.data.update_truck_numbers()
        self.setup_sequence_solver()

    def set_outbound_truck_number(self, value):
        self.outbound_table_model.truck_number(value)
        self.data.number_of_outbound_trucks = value
        self.data.update_truck_numbers()
        self.setup_sequence_solver()

    def set_compound_truck_number(self, value):
        self.compound_coming_table_model.truck_number(value)
        self.compound_going_table_model.truck_number(value)
        self.data.number_of_compound_trucks = value
        self.data.update_truck_numbers()
        self.setup_sequence_solver()

    def set_receiving_door_number(self, value):
        self.data.set_receiving_door_number(value)
        self.setup_sequence_solver()
        self.setup_simulator()

    def set_shipping_door_number(self, value):
        self.data.set_shipping_door_number(value)
        self.setup_sequence_solver()
        self.setup_simulator()

    def update_data_table(self):
        """
        update table values
        :return:
        """
        self.loadingTumeLineEdit.setText(str(self.data.loading_time))
        self.truckChangeoverTimeLineEdit.setText(str(self.data.changeover_time))
        self.effectOfTheArrivalTimesOnMakespanLineEdit.setText(str(self.data.makespan_factor))
        self.truckTransferTimeLineEdit.setText(str(self.data.truck_transfer_time))
        self.inboundArrivalTimeLineEdit.setText(str(self.data.inbound_arrival_time))
        self.outboundArrivalTimeLineEdit.setText(str(self.data.outbound_arrival_time))
        self.goodTransferTimeLineEdit.setText(str(self.data.good_transfer_time))
        self.numberOfInboundTrucksSpinBox.setValue(self.data.number_of_inbound_trucks)
        self.numberOfOutboundTrucksSpinBox.setValue(self.data.number_of_outbound_trucks)
        self.numberOfCompoundTrucksSpinBox.setValue(self.data.number_of_compound_trucks)
        self.numberOfReceivingDoorsSpinBox.setValue(self.data.number_of_receiving_doors)
        self.numberOfShippingDoorsSpinBox.setValue(self.data.number_of_shipping_doors)
        self.numberOfGoodsSpinBox.setValue(self.data.number_of_goods)
        self.numberOfDataSetsSpinBox.setValue(self.data.number_of_data_sets)

    def update_number_of_goods(self, amount):
        self.inbound_table_model.change_good_number(amount)
        self.outbound_table_model.change_good_number(amount)
        self.compound_coming_table_model.change_good_number(amount)
        self.compound_going_table_model.change_good_number(amount)
        self.data.number_of_goods = amount

    def set_data_set_table(self):
        self.data.number_of_data_sets = self.numberOfDataSetsSpinBox.value()
        if self.numberOfDataSetsSpinBox.value() > len(self.data_set_model.data):
            self.data_set_model.insertRows(len(self.data_set_model.data), self.numberOfDataSetsSpinBox.value())
        elif self.numberOfDataSetsSpinBox.value() < len(self.data_set_model.data):
            self.data_set_model.removeRows(len(self.data_set_model.data), self.numberOfDataSetsSpinBox.value())

    def load_data(self):
        """
        loads prev saved data
        :return:
        """
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        try:
            self.data = pickle.load(open(file_name, 'rb'))
        except Exception as e:
            pass
        self.graphicsView.data = self.data
        self.setup_data()
        self.update_data_table()
        self.load_generated_data()

    def save_data(self):
        """
        saves current data
        :return:
        """
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save file', '/home')
        try:
            pickle.dump(self.data,  open(file_name, 'wb'))
        except Exception as e:
            pass

    def setup_sequence_solver(self):
        self.combobox_coming_sequence = []
        self.combobox_going_sequence = []
        self.setup_truck_names()
        self.coming_truck_list = self.data.coming_truck_name_list + ['0'] * (self.data.number_of_receiving_doors - 1)
        self.going_truck_list = self.data.going_truck_name_list + ['0'] * (self.data.number_of_shipping_doors - 1)

        for i in range(self.data.number_of_coming_trucks + self.data.number_of_receiving_doors - 1):
            newbox = QComboBox()
            newbox.addItems(self.coming_truck_list)
            self.combobox_coming_sequence.append(newbox)

        for i in range(self.data.number_of_going_trucks + self.data.number_of_shipping_doors - 1):
            newbox = QComboBox()
            newbox.addItems(self.going_truck_list)
            self.combobox_going_sequence.append(newbox)

        for i, box in enumerate(self.combobox_coming_sequence):
            self.sequence_grid.addWidget(box, 0, i)

        for i, box in enumerate(self.combobox_going_sequence):
            self.sequence_grid.addWidget(box, 1, i)

    def setup_truck_names(self):
        GoodStore.loading_time = self.data.loading_time
        Door.good_transfer_time = self.data.good_transfer_time
        self.data.truck_name_list = []
        self.data.coming_truck_name_list = []
        self.data.going_truck_name_list = []
        for i in range(self.data.number_of_inbound_trucks):
            name = 'inbound'+str(i)
            self.data.truck_name_list.append(name)
            self.data.coming_truck_name_list.append(name)
            self.truck_states[name] = 'coming'
        for i in range(self.data.number_of_outbound_trucks):
            name = 'outbound'+str(i)
            self.data.truck_name_list.append(name)
            self.data.going_truck_name_list.append(name)
            self.truck_states[name] = 'coming'
        for i in range(self.data.number_of_compound_trucks):
            name = 'compound'+str(i)
            self.data.truck_name_list.append(name)
            self.data.coming_truck_name_list.append(name)
            self.data.going_truck_name_list.append(name)
            self.truck_states[name] = 'coming'

    def solve_data_set(self):
        self.data_set_number = self.data_set_spin_box.value()
        self.solver = Solver(self.data_set_number, self.data)
        # get sequence
        #self.solver.set_sequence(sequence)
        self.solver.solve()

    def next_iteration(self):
        # signal from solver
        # increase iteration
        pass

    def solve_one_sequence(self):
        self.data_set_number = self.data_set_spin_box.value() - 1
        self.setup_truck_names()
        self.solver = Solver(self.data_set_number, self.data)
        self.solver.time_signal.connect(self.time.display)
        self.solver.value_signal.connect(self.solver_truck_signal)
        self.time_constant.textChanged.connect(self.solver.time_step_change)

        sequence = Sequence()
        for box in self.combobox_coming_sequence:
            sequence.coming_sequence.append(box.currentText())
        for box in self.combobox_going_sequence:
            sequence.going_sequence.append(box.currentText())
        self.graphicsView.reset()
        self.graphicsView.update_scene()
        self.solver.set_sequence(sequence)
        self.solver.solve()

    def solver_truck_signal(self, name, state, arg):
        self.truck_states[name] = [state, arg]
        self.graphicsView.update_scene()

    def pause(self):
        try:
            self.solver.pause = True
        except:
            pass

    def resume(self):
        try:
            self.solver.pause = False
        except:
            pass

    def step_solve(self):
        time.sleep(0.5)

    def setup_simulator(self):
        self.graphicsView.reset()
        self.graphicsView.truck_states = self.truck_states

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # app.setStyle('Fusion')
    #
    # palette = QtGui.QPalette()
    # palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53,53,53))
    # palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    # palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15,15,15))
    # palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53,53,53))
    # palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    # palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    # palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    # palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53,53,53))
    # palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    # palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    # palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142,45,197).lighter())
    # palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    # app.setPalette(palette)

    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()
    sys.exit(0)

