from src.sequence import Sequence
import operator
import random
import copy
from math import ceil


class Algorithms(object):
    def __init__(self, data):
        self.data_set_number = 0
        self.data = data
        self.arrivals = self.data.arrival_times[self.data_set_number]
        self.sequence = Sequence()
        self.best_sequence = Sequence()
        self.best_iteration = 0

    def start1(self):
        sorted_in = sorted(self.arrivals.items(), key=operator.itemgetter(1))
        self.sequence.coming_sequence = [x[0] for x in sorted_in if x[0] in self.data.coming_truck_name_list]
        step = ceil(self.data.number_of_coming_trucks / (self.data.number_of_receiving_doors))
        for i in range(self.data.number_of_receiving_doors - 1):
            self.sequence.coming_sequence.insert(step * (i+1), '0')

        out_trucks = [('outbound' + str(i)) for i in range(self.data.number_of_outbound_trucks)]
        comp_trucks = [('compound' + str(i)) for i in range(self.data.number_of_compound_trucks)]
        sorted_out = sorted(self.arrivals.items(), key=operator.itemgetter(1))
        self.sequence.going_sequence = [x[0] for x in sorted_out if x[0] in out_trucks]
        self.sequence.going_sequence.extend([x[0] for x in sorted_out if x[0] in comp_trucks])
        step = ceil(self.data.number_of_going_trucks / (self.data.number_of_shipping_doors))
        for i in range(self.data.number_of_shipping_doors - 1):
            self.sequence.going_sequence.insert(step * (i+1), '0')

        self.best_sequence = copy.deepcopy(self.sequence)

        return self.sequence

    def generate_random(self, prev_sequence):
        sequence = copy.deepcopy(prev_sequence)
        a = random.choice(range(len(sequence)))
        b = random.choice(range(len(sequence)))
        if a == b:
            sequence = self.generate_random(sequence)
        else:
            sequence[b], sequence[a] = sequence[a], sequence[b]
        return sequence
