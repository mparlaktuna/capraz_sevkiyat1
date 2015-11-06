from src.sequence import Sequence
import operator


class Algorithms(object):
    def __init__(self, solver_type, start_type, data_set_number, data):
        self.data_set_number = data_set_number
        self.solver_type = solver_type
        self.start_type = start_type
        self.algorithms = {'annealing': self.annealing, 'start1': self.start1}
        self.data = data
        self.arrivals = self.data.arrival_times[self.data_set_number]
        self.sequence = Sequence

    def start1(self):
        sorted_in = sorted(self.arrivals.items(), key=operator.itemgetter(1))
        self.sequence.coming_sequence= [x[0] for x in sorted_in if x[0] in self.data.coming_truck_name_list]
        step = int(self.data.number_of_coming_trucks / self.data.number_of_receiving_doors)
        for i in range(self.data.number_of_receiving_doors - 1):
            self.sequence.coming_sequence.insert(step * (i+1), '0')

        out_trucks = [('outbound' + str(i)) for i in range(self.data.number_of_outbound_trucks)]
        comp_trucks = [('compound' + str(i)) for i in range(self.data.number_of_compound_trucks)]
        sorted_out = sorted(self.arrivals.items(), key=operator.itemgetter(1))
        self.sequence.going_sequence = [x[0] for x in sorted_out if x[0] in out_trucks]
        self.sequence.going_sequence.extend([x[0] for x in sorted_out if x[0] in comp_trucks])
        step = int(self.data.number_of_going_trucks / self.data.number_of_shipping_doors)
        for i in range(self.data.number_of_receiving_doors - 1):
            self.sequence.going_sequence.insert(step * (i+1), '0')

        return self.sequence

    def get_sequence(self, error, prev_seqeunce):
        self.annealing(prev_seqeunce)

    def annealing(self, prev_sequence):
        pass
