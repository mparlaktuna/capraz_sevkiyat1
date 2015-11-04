from src.good import Good


class GoodStore(object):
    loading_time = 0

    def __init__(self):
        self.good_list = {}

    def clear_goods(self):
        self.good_list = {}

    def calculate_load_time(self):

        return self.loading_time * self.total_good_amount()

    def total_good_amount(self):
        good_amount = 0
        for goods in self.good_list.values():
            for good in goods:
                good_amount += good.amount
        return good_amount

    def add_good(self, name, amount, truck=None):
        if name in self.good_list.keys():
            good = Good(name, amount, truck)
            self.good_list[name].append(good)
            #print(self.good_list)
            return True
        else:
            good = Good(name, amount, truck)
            self.good_list[name] = [good]
            #print(self.good_list)
            return False

    def goods_in_text(self):
        text = ''
        try:
            for goods in self.good_list.values():
                for good in goods:
                    text += 'Good {0} from {1}: {2}\n'.format(good.good_name, good.coming_truck_name, good.amount)
            return text
        except:
            return 'empty'
