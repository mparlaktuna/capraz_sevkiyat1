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

    def empty(self):
        try:
            truck = self.truck_list[self.next_truck_number]
            if truck.behaviour_list[truck.current_state] == self.waiting_name:
                self.next_state()
                self.next_truck_number += 1
                truck.next_state()
                truck.times['waiting_finish'] = self.current_time
                truck.relevant_data = self.door_name
                truck.next_state_time = self.current_time + truck.changeover_time
                truck.current_door = self
        except:
            pass

    def waiting(self):
        pass

    def loading(self):
        pass

    def check_good_transfer(self):
        if self.current_time in self.good_times:
            good_store = self.goods_list[self.good_times.index(self.current_time)]
            #print(goods.goods_list)
            for goods in good_store.good_list.values():
                for good in goods:
                    self.station.goods_list.add_good(good.good_name, good.amount, good.coming_truck_name)
            good_store.clear_goods()
