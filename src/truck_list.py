from PyQt5.QtCore import *
from src.inbound_truck import InboundTruck
from src.outbound_truck import OutboundTruck
from src.compound_truck import CompoundTruck


class TruckList(QObject):
    """
    Truck list
    """
    def __init__(self):
        QObject.__init__(self)
        self.number_of_inbound_trucks = 0
        self.number_of_outbound_trucks = 0
        self.number_of_compound_trucks = 0

        self.inbound_trucks = {}
        self.outbound_trucks = {}
        self.compound_trucks = {}
        self.trucks = {}

    def add_truck(self, type):
        pass


