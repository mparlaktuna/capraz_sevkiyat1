from src.truck import Truck
from src.good_store import GoodStore
import copy


class OutboundTruck(Truck):
    """
    Outbound truck object
    """
    def __init__(self):
        Truck.__init__(self)
        self.behaviour_list = ('coming', 'waiting_to_load', 'changeover', 'loading', 'done')
        self.current_state = 0
        self.function_list = [self.coming, self.waiting_to_load, self.changeover, self.loading, self.done]
        self.current_time = 0
        self.good = GoodStore()
        needed_goods = []

    def waiting(self):
        pass

    def changeover(self):
        if self.current_time == self.next_state_time:
            self.next_state()
            self.current_door.next_state()

    def waiting_to_load(self):
        pass

    def loading(self):
        pass

    def done(self):
        pass