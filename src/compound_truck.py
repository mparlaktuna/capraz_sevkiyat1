from src.truck import Truck
from src.good_store import GoodStore
import copy


class CompoundTruck(Truck):
    """
    Compound truck object
    """
    def __init__(self):
        Truck.__init__(self)
        self.behaviour_list = ('coming', 'waiting_to_deploy', 'changeover', 'deploying', 'changeover2', 'truck_transfer', 'waiting_to_load')
        self.current_state = 0
        self.function_list = [self.coming, self.waiting, self.changeover, self.deploying, self.changeover2, self.truck_transfer, self.waiting_to_load]
        self.current_time = 0
        self.good = GoodStore()
        needed_goods = []
        self.transfer_time = 0
        self.lower_Bound = 0
        self.upper_bound = 0
        self.good_amount = 0

    def waiting(self):
        pass

    def changeover(self):
        if self.current_time == self.next_state_time:
            self.next_state()
            self.next_state_time = self.good.calculate_load_time() + self.current_time
            self.current_door.next_state()

    def deploying(self):
        if self.current_time == self.next_state_time:
            self.next_state_time = self.changeover_time + self.current_time
            self.current_door.goods_list.append(copy.deepcopy(self.good))
            self.current_door.good_times.append(self.current_time + self.current_door.good_transfer_time)
            self.good.clear_goods()
            self.current_door.next_state()
            self.next_state()

    def changeover2(self):
        if self.current_time == self.next_state_time:
            self.current_door.next_state()
            self.next_state()
            self.next_state_time = self.transfer_time + self.current_time

    def truck_transfer(self):
        pass

    def waiting_to_load(self):
        pass

    def changeover3(self):
        if self.current_time == self.next_state_time:
            self.next_state()

    def changeover4(self):
        if self.current_time == self.next_state_time:
            self.next_state()


    def done(self):
        pass