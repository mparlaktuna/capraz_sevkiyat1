from src.algorithms import Algorithms
from src.sequence import AnnealingSequence
import copy
import math
import random


class Annealing(Algorithms):

    def __init__(self, data, temperature, decay_factor):
        Algorithms.__init__(self, data)
        self.sequence = AnnealingSequence()
        self.sequence.values['temperature'] = temperature
        self.best_sequence = AnnealingSequence()
        self.prev_sequence_error = float('inf')
        self.prev_sequence = AnnealingSequence()
        self.temperature = temperature

        self.decrease_constant = decay_factor

    def next_iteration(self, sequence, iteration_number):
        if sequence.error <= self.prev_sequence_error:
            sequence.values['decision'] = 'better sequence'
            self.prev_sequence = copy.deepcopy(sequence)
            self.prev_sequence_error = sequence.error
            if sequence.error <= self.best_sequence.error:
                sequence.values['decision'] = 'best sequence'
                self.best_sequence = copy.deepcopy(sequence)
                self.best_iteration = iteration_number

        else:
            p_accept = math.exp((self.prev_sequence_error - sequence.error) / self.prev_sequence.values['temperature'])
            random_number = random.random()
            sequence.values['random_number'] = random_number
            sequence.values['p_accept'] = p_accept
            sequence.values['decision'] = 'not accepted'
            if p_accept >= random_number:
                sequence.values['decision'] = 'accepted'
                self.prev_sequence = copy.deepcopy(sequence)
                self.prev_sequence_error = sequence.error


        new_sequence = AnnealingSequence()
        new_sequence.coming_sequence = self.generate_random(self.prev_sequence.coming_sequence)
        new_sequence.going_sequence = self.generate_random(self.prev_sequence.going_sequence)
        self.temperature = self.temperature * self.decrease_constant
        new_sequence.values['temperature'] = self.temperature

        return new_sequence
