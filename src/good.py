class Good(object):
    def __init__(self, name=None, amount=0, truck=None):
        self.good_name = name
        self.amount = amount
        self.coming_truck_name = truck

    def remove_good(self, amount):
        if self.check_enough(amount):
            self.amount -= amount
            return True
        else:
            return False

    def check_enough(self, amount):
        if amount > self.amount:
            return False
        else:
            return True

