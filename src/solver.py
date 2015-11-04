import time
from PyQt5.QtCore import *
from src.inbound_truck import InboundTruck
from src.outbound_truck import OutboundTruck
from src.compound_truck import CompoundTruck
from src.data_store import DataStore
from src.station import Station
from src.shipping_door import ShippingDoor
from src.receiving_door import ReceivingDoor
from src.sequence import Sequence


class Solver(QThread):
    time_signal = pyqtSignal(int, name='time')
    value_signal = pyqtSignal(str, str, str, name='time_values')
    done_signal = pyqtSignal(int, name='done')

    def __init__(self, data_set_number, data=DataStore()):
        QThread.__init__(self)
        self.pause = False
        self.data = data
        self.data_set_number = data_set_number
        self.truck_list = {}
        self.station = Station()
        self.door_list = {}
        self.setup_solver()

        self.current_time = 0
        self.time_constant = 0.1

    def setup_solver(self):
        self.setup_doors()
        self.setup_trucks()

    def setup_trucks(self):
        for i in range(self.data.number_of_inbound_trucks):
            name = 'inbound' + str(i)
            truck = InboundTruck()
            truck.truck_name = name
            truck.times['arrival_time'] = self.data.arrival_times[self.data_set_number][name]
            truck.changeover_time = self.data.changeover_time
            for k, good_amount in enumerate(self.data.inbound_goods[i]):
                truck.good.add_good(str(k + 1), good_amount, truck.truck_name)
            self.truck_list[name] = truck

        for i in range(self.data.number_of_outbound_trucks):
            name = 'outbound' + str(i)
            truck = OutboundTruck()
            truck.truck_name = name
            truck.times['arrival_time'] = self.data.arrival_times[self.data_set_number][name]
            truck.changeover_time = self.data.changeover_time
            truck.needed_goods = self.data.outbound_goods[i]
            truck.lower_Bound = self.data.lower_boundaries[i][name]
            truck.upper_bound = self.data.upper_boundaries[i][name]
            self.truck_list[name] = truck

        for i in range(self.data.number_of_compound_trucks):
            name = 'compound' + str(i)
            truck = CompoundTruck()
            truck.truck_name = name
            truck.transfer_time = self.data.truck_transfer_time
            truck.times['arrival_time'] = self.data.arrival_times[self.data_set_number][name]
            truck.changeover_time = self.data.changeover_time
            truck.lower_Bound = self.data.lower_boundaries[i][name]
            truck.upper_bound = self.data.upper_boundaries[i][name]
            for k, good_amount in enumerate(self.data.compound_coming_goods[i]):
                truck.good.add_good(str(k + 1), good_amount, truck.truck_name)
            truck.needed_goods = self.data.compound_going_goods[i]
            self.truck_list[name] = truck


    def setup_doors(self):
        for i in range(self.data.number_of_receiving_doors):
            name = 'receiving' + str(i)
            self.door_list[name] = ReceivingDoor(name, self.station)

        for i in range(self.data.number_of_shipping_doors):
            name = 'shipping' + str(i)
            self.door_list[name] = ShippingDoor(name, self.station)

    def set_sequence(self, sequence=Sequence()):
        self.sequence = sequence
        i = 0
        for truck in self.sequence.coming_sequence:
            name = 'receiving' + str(i)
            if truck == '0':
                i += 1
                continue
            self.door_list[name].truck_list.append(self.truck_list[truck])
        i = 0
        for truck in self.sequence.going_sequence:
            name = 'shipping' + str(i)
            if truck == '0':
                i += 1
                continue
            self.door_list[name].truck_list.append(self.truck_list[truck])

    def solve(self):
        self.start()

    def run(self):
        while self.current_time < 200:
            if not self.pause:
                time.sleep(self.time_constant)
                self.step()
        self.done_signal.emit(self.current_time)

    def step(self):
        self.current_time += 1
        self.time_signal.emit(self.current_time)
        for truck in self.truck_list.values():
            signal = truck.run(self.current_time)
            if signal:
                 self.value_signal.emit(truck.truck_name, truck.behaviour_list[truck.current_state], truck.relevant_data)

        for door in self.door_list.values():
            door.run(self.current_time)

    def time_step_change(self, value):
        try:
            if value == 0:
                self.time_constant = 0.1
            else:
                self.time_constant = float(value)
        except:
            self.time_constant = 0.1
