from src.algorithms import Algorithms
from src.sequence import TabuSequence
import copy
import math
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

    def next_iteration(self, sequence):
        self.prev_sequence_list.append(sequence)
        if self.generated_neighbour_number == 0:
            self.generate_neighbour(self.number_of_neighbours)
        print(self.generated_neighbour_number)
        if self.generated_neighbour_number < self.number_of_neighbours:
            for i in range(self.generated_neighbour_number, len(self.generated_neighbour_list)):
                generated = self.generated_neighbour_list[i]
                for prev_sequence in self.prev_sequence_list:
                    coming_tabu = False
                    going_tabu = False
                    if generated.coming_sequence == prev_sequence.coming_sequence:
                        coming_tabu = True
                    if generated.going_sequence == prev_sequence.going_sequence:
                        going_tabu = True

                # if coming_tabu and going_tabu:
                #     print('tabu')
                #     continue
                else:
                    sequence = generated
                    break
            self.generated_neighbour_number = i + 1
        else:
            self.generated_neighbour_number = 0
            self.iteration_finish = True
            minimum = float('inf')
            for generated in self.generated_neighbour_list:
                if generated.error < minimum:
                    self.prev_sequence_list.append(copy.deepcopy(generated))
                    if generated.error < self.best_sequence.error:
                        self.best_sequence = copy.deepcopy(generated)

        return sequence

    def generate_neighbour(self, number):
        for i in range(number):
            new_sequence = TabuSequence()
            new_sequence.coming_sequence = self.generate_random(self.prev_sequence_list[-1].coming_sequence)
            new_sequence.going_sequence = self.generate_random(self.prev_sequence_list[-1].going_sequence)
            self.generated_neighbour_list.append(copy.deepcopy(new_sequence))
