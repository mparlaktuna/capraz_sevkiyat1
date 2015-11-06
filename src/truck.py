from PyQt5.QtCore import *


class Truck(QObject):
    """
    General truck class with common types and functions
    """
    def __init__(self):
        QObject.__init__(self)
        self.truck_name = None
        self.current_time = 0
        self.function_list = []
        self.times = {'arrival_time': 0}
        self.current_state = 0
        self.state_signal = False
        self.behaviour_list = []
        self.relevant_data = None
        self.changeover_time = 0
        self.next_state_time = 0
        self.current_door = None
        self.finish_time = 0

    def run(self, current_time):
        self.current_time = current_time
        self.function_list[self.current_state]()
        if self.state_signal:
            self.state_signal = False
            return 1
        return 0

    def coming(self):
        if self.times['arrival_time'] == self.current_time:
            self.times['arrived'] = self.current_time
            self.next_state()

    def next_state(self, name=None):
        self.state_signal = True
        if name:
            print('name')
            print(self.behaviour_list.index('loading'))
            self.current_state = self.behaviour_list.index(name)
        else:
            self.current_state += 1