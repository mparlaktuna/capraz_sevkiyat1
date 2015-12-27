from src.algorithms import Algorithms
from src.sequence import TabuSequence
import copy
from math import ceil
import operator
import random
from collections import deque


class Tabu(Algorithms):

    def __init__(self, data, number_of_tabu, number_of_neighbours):
        Algorithms.__init__(self, data)
        self.number_of_tabu = number_of_tabu
        self.number_of_neighbours = number_of_neighbours

        self.sequence = TabuSequence()
        self.best_sequence = TabuSequence()
        self.prev_sequence_error = float('inf')
        self.prev_sequence = TabuSequence()
        self.prev_sequence_list = deque(maxlen=number_of_tabu)
        self.iteration_finish = True
        self.generated_neighbour_number = 0
        self.generated_neighbour_list = []

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
        self.prev_sequence_list.append(self.sequence)
        self.prev_sequence = self.sequence
        return self.sequence

    def next_iteration(self, iteration_number):
        print('next iteration')
        new_sequence = TabuSequence()
        new_sequence.values['iteration number'] = iteration_number
        new_sequence.coming_sequence = self.generate_random(self.prev_sequence.coming_sequence)
        new_sequence.going_sequence = self.generate_random(self.prev_sequence.going_sequence)
        if self.same_generated(new_sequence):
            print('same')
            self.next_iteration(iteration_number)
        else:
            print('diff')
            self.generated_neighbour_list.append(new_sequence)
        return new_sequence

    def same_generated(self, sequence):
        for generated_sequence in self.generated_neighbour_list:
            coming_same = sequence.coming_sequence == generated_sequence.coming_sequence
            going_same = sequence.going_sequence == generated_sequence.going_sequence
            same = coming_same and going_same
            if same:
                return True
        return False

    def choose_sequence(self):
        selected_sequence = TabuSequence()
        sequence_decision = []

        for i, generated_sequence in enumerate(self.generated_neighbour_list):
            if not generated_sequence.values['decision'] == 'tabu':
                print('neighbour error', generated_sequence.error)
                if generated_sequence.error <= self.best_sequence.error:
                    self.best_sequence = copy.deepcopy(generated_sequence)
                    selected_sequence = copy.deepcopy(self.best_sequence)
                    sequence_decision.append('best sequence')
                elif generated_sequence.error < selected_sequence.error:
                    selected_sequence = copy.deepcopy(generated_sequence)
                    selected_sequence.values['decision'] = 'selected sequence'
                    sequence_decision.append('selected sequence')
                else:
                    sequence_decision.append('not_chosen')
            else:
                sequence_decision.append('tabu')

        self.prev_sequence_list.append(selected_sequence)
        self.prev_sequence = selected_sequence
        self.generated_neighbour_list = []
        print('decision', sequence_decision)
        return sequence_decision


    def check_tabu(self, sequence):
        for past_sequence in self.prev_sequence_list:
            coming_tabu = sequence.coming_sequence == past_sequence.coming_sequence
            going_tabu = sequence.going_sequence == past_sequence.going_sequence
            tabu = coming_tabu and going_tabu
            if tabu:

                print(sequence.coming_sequence)
                print(sequence.going_sequence)

                print(past_sequence.coming_sequence)
                print(past_sequence.going_sequence)

                sequence.values['decision'] = 'tabu'
                return True

        return False


