from src.door import Door
from src.good_store import GoodStore


class ShippingDoor(Door):
    def __init__(self, name, station):
        Door.__init__(self, name, station)
        self.truck_list = []
        self.behaviour_list = ['empty', 'waiting_to_load', 'loading', "waiting"]
        self.function_list = [self.empty, self.waiting_to_load, self.loading, self.waiting]
        self.next_truck_number = 0
        self.waiting_name = 'waiting_to_load'
        self.good_ready = False
        self.current_goods = []
        self.goods = GoodStore()

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

    def loading(self):
        #print('loading')
        truck = self.truck_list[self.next_truck_number]
        self.needed_goods = truck.needed_goods
        self.check_self()
        # for i, amount enumerate(self.needed_goods):
        #     for station_goods in self.station.goods_list:

    def check_self(self):
        print(self.station.goods_list.good_amounts())

    def waiting(self):
        print('waiting')
