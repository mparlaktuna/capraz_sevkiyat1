from src.good import Good
import copy

class GoodStore(object):
    loading_time = 0

    def __init__(self):
        self.good_list = {}

    def clear_goods(self):
        self.good_list = {}

    def calculate_load_time(self):

        return self.loading_time * self.total_good_amount()

    def good_amounts(self):
        self.clean_zeros()
        amounts = {}
        for i in self.good_list.keys():
            amounts[i] = sum(goods.amount for goods in self.good_list[i])
        return amounts

    def total_good_amount(self):
        self.clean_zeros()
        good_amount = 0
        for goods in self.good_list.values():
            for good in goods:
                good_amount += good.amount
        return good_amount

    def remove_good(self, good_name, needed_amount):
        self.clean_zeros()
        removed_goods = []
        if good_name in self.good_list:
            for goods in self.good_list[good_name]:
                if goods.amount == 0:
                    continue
                elif goods.amount > needed_amount:
                    goods.amount -= needed_amount
                    removed_goods.append([needed_amount, goods.coming_truck_name])
                    needed_amount = 0
                elif goods.amount <= needed_amount:
                    removed_goods.append([copy.deepcopy(goods.amount), goods.coming_truck_name])
                    needed_amount -= goods.amount
                    goods.amount = 0
                    self.good_list[good_name].pop(self.good_list[good_name].index(goods))
        return removed_goods

    def clean_zeros(self):
        delete = []
        for good_name, goods in self.good_list.items():
            for good in goods:
                if good.amount == 0:
                    self.good_list[good_name].pop(self.good_list[good_name].index(good))
            total = sum(a.amount for a in goods)
            #print(total)
            if total == 0:
                delete.append(good_name)
        if delete:
            for name in delete:
                del self.good_list[name]

    def add_good(self, name, amount, truck=None):
        self.clean_zeros()
        if name in self.good_list.keys():
            good = Good(name, amount, truck)
            self.good_list[name].append(good)
            return True
        else:
            good = Good(name, amount, truck)
            self.good_list[name] = [good]
            return False

    def goods_in_text(self):
        self.clean_zeros()
        text = ''
        try:
            for goods in self.good_list.values():
                for good in goods:
                    text += 'Good {0} from {1}: {2}\n'.format(good.good_name, good.coming_truck_name, good.amount)
            return text
        except:
            return 'empty'

    def return_goods(self):
        self.clean_zeros()
        good_amounts = {}
        try:
            for goods in self.good_list.values():
                for good in goods:
                    if good.coming_truck_name in good_amounts.keys():
                        good_amounts[good.coming_truck_name] += 'Type:{0} Amount {1}\n'.format(good.good_name, good.amount)
                    else:
                        good_amounts[good.coming_truck_name] = 'Type:{0} Amount {1}\n'.format(good.good_name, good.amount)
        except:
            pass
        return good_amounts
