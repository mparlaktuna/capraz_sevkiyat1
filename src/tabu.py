from src.algorithms import Algorithms
from src.sequence import AnnealingSequence
import copy
import math
import random


class Annealing(Algorithms):

    def __init__(self, data):
        Algorithms.__init__(self, data)
        self.sequence = AnnealingSequence()
        self.best_sequence = AnnealingSequence()
        self.prev_sequence_error = float('inf')
        self.prev_sequence = AnnealingSequence()
        self.decrease_constant = 0.9

    def next_iteration(self, sequence):
        if sequence.error <= self.prev_sequence_error:
            self.prev_sequence = copy.deepcopy(sequence)
            self.prev_sequence_error = sequence.error
            if sequence.error < self.best_sequence.error:
                self.best_sequence = copy.deepcopy(sequence)

        else:
            p_accept = math.exp((self.prev_sequence_error - sequence.error) / self.prev_sequence.values['temperature'])
            random_number = random.random()
            sequence.values['random_number'] = random_number
            sequence.values['p_accept'] = p_accept

            if p_accept >= random_number:
                sequence.values['decision'] = 1
                self.prev_sequence = copy.deepcopy(sequence)
                self.prev_sequence_error = sequence.error


        new_sequence = AnnealingSequence()
        new_sequence.coming_sequence = self.generate_random(self.prev_sequence.coming_sequence)
        new_sequence.going_sequence = self.generate_random(self.prev_sequence.going_sequence)
        new_sequence.values['temperature'] = self.prev_sequence.values['temperature'] * self.decrease_constant

        return new_sequence

