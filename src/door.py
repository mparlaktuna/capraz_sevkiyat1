from src.good_store import GoodStore


class Door(object):
    good_transfer_time = 0
    def __init__(self, name, station):
        self.station = station
        self.door_name = name
        self.goods_list = []
        self.current_state = 0
        self.current_time = 0
        self.behaviour_list = []
        self.waiting_name = ''
        self.next_truck_number = 0

    def next_state(self):
        self.current_state += 1
        if self.current_state == len(self.behaviour_list):
            self.current_state = 0

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
