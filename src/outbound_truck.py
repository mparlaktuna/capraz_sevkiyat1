from src.truck import Truck
from src.good_store import GoodStore
import copy


class OutboundTruck(Truck):
    """
    Outbound truck object
    """
    def __init__(self):
        Truck.__init__(self)
        self.behaviour_list = ('coming', 'waiting_to_load', 'changeover', 'not_ready_to_load', 'ready_to_load', 'must_load', 'loading', 'done')
        self.current_state = 0
        self.function_list = [self.coming, self.waiting_to_load, self.changeover, self.not_ready_to_load, self.ready_to_load, self.must_load, self.loading, self.done]
        self.current_time = 0
        self.good = GoodStore()
        self.needed_goods = []
        self.lower_Bound = 0
        self.upper_bound = 0
        self.good_amount = 0

    def waiting(self):
        pass

    def waiting_to_load(self):
        pass

    def changeover(self):
        if self.current_time == self.next_state_time:
            self.next_state()

    def not_ready_to_load(self):
        self.good_amount = sum(self.needed_goods)
        self.next_state_time = self.good_amount * self.good.loading_time + self.current_time
        if self.lower_Bound < self.next_state_time:
            self.next_state()
            self.current_door.next_state()
        elif self.next_state_time > self.upper_bound:
            self.current_door.next_state()
            self.next_state()
            self.next_state()

    def ready_to_load(self):
        pass

    def must_load(self):
        pass

    def loading(self):
        pass

    def done(self):
        pass