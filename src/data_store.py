from src.good_store import GoodStore
from collections import OrderedDict

class DataStore(object):
    """
    stores data for a solution
    """
    def __init__(self):
        self.truck_name_list = []
        self.coming_truck_name_list = []
        self.going_truck_name_list = []
        self.loading_time = 0
        self.unloading_time = 0
        self.changeover_time = 0
        self.makespan_factor = 0
        self.truck_transfer_time = 0
        self.inbound_arrival_time = 0
        self.outbound_arrival_time = 0
        self.good_transfer_time = 0
        self.number_of_data_sets = 0

        self.data_sets = []

        self.number_of_inbound_trucks = 0
        self.number_of_outbound_trucks = 0
        self.number_of_compound_trucks = 0
        self.number_of_coming_trucks = 0
        self.number_of_going_trucks = 0
        self.number_of_trucks = 0
        self.number_of_goods = 0

        self.number_of_receiving_doors = 0
        self.number_of_shipping_doors = 0

        self.inbound_goods = []
        self.outbound_goods = []
        self.compound_coming_goods = []
        self.compound_going_goods = []

        self.arrival_times = []
        self.lower_boundaries = []
        self.upper_boundaries = []

        self.coming_mu = 0
        self.going_mu = 0
        self.product_per_coming_truck = 0
        self.product_per_going_truck = 0

    def calculate_truck_related_data(self):
        """
        such as mu and product per truck
        :return:
        """
        self.update_truck_numbers()
        self.coming_mu = self.number_of_coming_trucks / self.number_of_receiving_doors
        self.going_mu = self.number_of_going_trucks / self.number_of_shipping_doors

        self.product_per_coming_truck = (sum(sum(m) for m in self.inbound_goods) + sum(sum(n) for n in self.compound_coming_goods)) / self.number_of_coming_trucks
        self.product_per_going_truck = (sum(sum(m) for m in self.outbound_goods) + sum(sum(n) for n in self.compound_going_goods)) / self.number_of_going_trucks

    def update_truck_numbers(self):
        """
        updates the summation of truck numbers
        :return:
        """
        self.number_of_coming_trucks = self.number_of_inbound_trucks + self.number_of_compound_trucks
        self.number_of_going_trucks = self.number_of_outbound_trucks + self.number_of_compound_trucks
        self.number_of_trucks = self.number_of_inbound_trucks + self.number_of_outbound_trucks + self.number_of_compound_trucks

    def set_loading_time(self, value):
        try:
            self.loading_time = int(value)
        except:
            pass

    def set_unloading_time(self, value):
        try:
            self.unloading_time = int(value)
        except:
            pass

    def set_changeover_time(self, value):
        try:
            self.changeover_time = int(value)
        except:
            pass

    def set_makespan_factor(self, value):
        try:
            self.makespan_factor = float(value)
        except:
            pass

    def set_truck_transfer_time(self, value):
        try:
            self.truck_transfer_time = int(value)
        except:
            pass

    def set_inbound_arrival_time(self, value):
        try:
            self.inbound_arrival_time = int(value)
        except:
            pass

    def set_outbound_arrival_time(self, value):
        try:
            self.outbound_arrival_time = int(value)
        except:
            pass

    def set_good_transfer_time(self, value):
        try:
            self.good_transfer_time = int(value)
        except:
            pass

    def set_receiving_door_number(self, value):
        try:
            self.number_of_receiving_doors = int(value)
        except:
            pass

    def set_shipping_door_number(self, value):
        try:
            self.number_of_shipping_doors = int(value)
        except:
            pass

