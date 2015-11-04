import copy
from src.door import Door


class ReceivingDoor(Door):
    def __init__(self, name, station):
        Door.__init__(self, name, station)
        self.truck_list = []
        self.behaviour_list = ['empty', 'waiting', 'loading', 'waiting2']
        self.function_list = [self.empty, self.waiting, self.loading, self.waiting]
        self.good_times = []

        self.door_name = name
        self.waiting_name = 'waiting_to_deploy'

    def run(self, current_time):
        self.current_time = current_time
        self.check_good_transfer()
        self.function_list[self.current_state]()

    def waiting(self):
        pass

    def loading(self):
        pass

    def check_good_transfer(self):
        if self.current_time in self.good_times:
            good = self.goods_list[self.good_times.index(self.current_time)]
            self.station.goods_list.append(copy.deepcopy(good))
            good.clear_goods()