from src.door import Door
from src.good_store import GoodStore
import copy


class ShippingDoor(Door):
    def __init__(self, name, station, door_list):
        Door.__init__(self, name, station)
        self.truck_list = []
        self.behaviour_list = ['empty', 'waiting_to_load', 'start_loading', 'must_load', 'loading', "waiting"]
        self.function_list = [self.empty, self.waiting_to_load, self.start_loading, self.must_load, self.loading, self.waiting]
        self.next_truck_number = 0
        self.waiting_name = 'waiting_to_load'
        self.good_ready = False
        self.current_goods = []
        self.goods = GoodStore()
        self.transfer_amounts = {}
        self.door_list = door_list
        self.critic = False

    def run(self, current_time):
        self.current_time = current_time
        self.function_list[self.current_state]()

    def empty(self):
        try:
            self.truck = self.truck_list[self.next_truck_number]
            if self.truck.behaviour_list[self.truck.current_state] == self.waiting_name:
                self.good_ready = False
                self.current_goods = []
                self.transfer_amounts = {}
                self.needed_goods = []
                self.next_state()
                self.truck.next_state()
                self.truck.times['waiting_finish'] = self.current_time
                self.truck.relevant_data = self.door_name
                self.truck.next_state_time = self.current_time + self.truck.changeover_time
                self.truck.current_door = self
                self.next_truck_number += 1
                self.needed_goods = self.truck.needed_goods
        except:
            pass

    def waiting_to_load(self):
        pass
        #print('waiting_to_load')

    def start_loading(self):
        self.check_self()
        self.transfer_goods(self.station)
        self.check_ready()
        if self.check_other_trucks():
            self.next_state()
            self.truck.next_state()

    def check_other_trucks(self):
        for i, truck in enumerate(self.truck_list):
            if i >= self.next_truck_number:
                if truck.upper_bound < self.current_time:
                    return True
        return False

    def must_load(self):
        self.critic = True
        self.check_self()
        self.transfer_goods(self.station)
        #self.critic_transfer_goods()
        self.check_ready()

    def loading(self):
        pass

    def check_self(self):
        self.current_goods = self.goods.good_amounts()
        for good_name, good_amount in self.needed_goods.items():
            if good_name in self.current_goods:
                if self.current_goods[good_name] >= self.needed_goods[good_name]:
                    self.transfer_amounts[good_name] = 0
                    continue
                elif self.current_goods[good_name] < self.needed_goods[good_name]:
                    self.transfer_amounts[good_name] = self.needed_goods[good_name] - self.current_goods[good_name]
            else:
                self.transfer_amounts[good_name] = copy.deepcopy(self.needed_goods[good_name])

    def transfer_goods(self, transfor_from=None):
        try:
            if not self.good_ready:
                for good_name, good_amount in self.transfer_amounts.items():
                    remove_goods = transfor_from.goods_list.remove_good(good_name, good_amount)
                    for remove_good in remove_goods:
                        self.goods.add_good(good_name, remove_good[0], remove_good[1])
        except:
            pass

    def critic_transfer_goods(self):
        for transfer_from in self.door_list.values():
            if not transfer_from == self:
                if type(transfer_from) is ShippingDoor:
                    if transfer_from.critic == False:
                        self.check_ready()
                        self.check_self()
                        if self.good_ready:
                            break
                        self.transfer_goods(transfer_from)

    def check_ready(self):
        if sum(self.transfer_amounts.values()) == 0:
            self.good_ready = True

    def waiting(self):
        self.critic = False
