from src.door import Door

class ShippingDoor(Door):
    def __init__(self, name, station):
        Door.__init__(self, name, station)
        self.truck_list = []
        self.behaviour_list = ['empty', 'waiting', 'loading']
        self.function_list = [self.empty, self.waiting, self.loading]
        self.next_truck_number = 0
        self.waiting_name = 'waiting_to_load'

    def run(self, current_time):
        self.current_time = current_time
        self.function_list[self.current_state]()

    def loading(self):
        pass

    def waiting(self):
        pass
