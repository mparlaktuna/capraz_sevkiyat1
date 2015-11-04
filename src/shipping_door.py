from src.door import Door
from src.good_store import GoodStore
import copy


class ShippingDoor(Door):
    def __init__(self, name, station):
        Door.__init__(self, name, station)
        self.truck_list = []
        self.behaviour_list = ['empty', 'waiting_to_load', 'start_loading', 'loading', "waiting"]
        self.function_list = [self.empty, self.waiting_to_load, self.start_loading, self.loading, self.waiting]
        self.next_truck_number = 0
        self.waiting_name = 'waiting_to_load'
        self.good_ready = False
        self.current_goods = []
        self.goods = GoodStore()
        self.transfer_amounts = {}

    def run(self, current_time):
        self.current_time = current_time
        self.function_list[self.current_state]()

    def empty(self):
        try:
            truck = self.truck_list[self.next_truck_number]
            if truck.behaviour_list[truck.current_state] == self.waiting_name:
                self.next_state()
                truck.next_state()
                truck.times['waiting_finish'] = self.current_time
                truck.relevant_data = self.door_name
                truck.next_state_time = self.current_time + truck.changeover_time
                truck.current_door = self
        except:
            pass

    def waiting_to_load(self):
        pass
        #print('waiting_to_load')

    def start_loading(self):
        #print('start_loading')
        truck = self.truck_list[self.next_truck_number]
        self.needed_goods = truck.needed_goods
        self.check_self()
        self.transfer_goods()
        self.check_ready()
        print('needed goods {0} in {1}'.format(self.needed_goods, truck.truck_name))
        if self.good_ready:
            print('good ready {0}'.format(truck.truck_name))
            truck.next_state_time = self.current_time + GoodStore.loading_time * self.goods.total_good_amount()
            truck.next_state('loading')
            self.next_state()
            self.next_truck_number += 1
            self.good_ready = False

    def loading(self):
        pass
        #print('loading')

    def check_self(self):
        self.current_goods = self.goods.good_amounts()
        for good_name, good_amount in self.needed_goods.items():
            if good_name in self.current_goods:
                if self.current_goods[good_name] == self.needed_goods[good_name]:
                    self.transfer_amounts[good_name] = 0
                    continue
                elif self.current_goods[good_name] < self.needed_goods[good_name]:
                    self.transfer_amounts[good_name] = self.needed_goods[good_name] - self.current_goods[good_name]
            else:
                self.transfer_amounts[good_name] = copy.deepcopy(self.needed_goods[good_name])

    def transfer_goods(self):
        self.check_ready()
        if not self.good_ready:
            for good_name, good_amount in self.transfer_amounts.items():
                remove_goods = self.station.goods_list.remove_good(good_name, good_amount)
                for remove_good in remove_goods:
                    self.goods.add_good(good_name, remove_good[0], remove_good[1])



    def check_ready(self):
        if sum(self.transfer_amounts.values()) == 0:
            self.good_ready = True

    def waiting(self):
        print('waiting')
