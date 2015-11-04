from src.truck import Truck
from src.good_store import GoodStore
import copy


class InboundTruck(Truck):
    """
    Inbound truck object
    """
    def __init__(self):
        Truck.__init__(self)
        self.behaviour_list = ['coming', 'waiting_to_deploy', 'changeover', 'deploying', 'changeover2', 'done']
        self.function_list = [self.coming, self.waiting, self.changeover, self.deploying, self.changeover2, self.done]

        self.good = GoodStore()

    def waiting(self):
        pass

    def changeover(self):
        if self.current_time == self.next_state_time:
            self.next_state()
            self.current_door.next_state()
            self.next_state_time = self.good.calculate_load_time() + self.current_time

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
            self.next_state()
            self.current_door.next_state()

    def done(self):
        pass

