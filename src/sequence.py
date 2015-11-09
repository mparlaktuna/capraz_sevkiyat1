class Sequence(object):
    def __init__(self):
        self.coming_sequence = []
        self.going_sequence = []
        self.error = float('inf')
        self.values = {}


class AnnealingSequence(Sequence):

    def __init__(self):
        Sequence.__init__(self)
        self.values['temperature'] = 100
        self.values['random_number'] = 0
        self.values['decision'] = 0
        self.values['p_accept'] = -1

class TabuSequence(Sequence):

    def __init__(self):
        Sequence.__init__(self)
        self.values['iteration number'] = 0
        self.values['decision'] = 0
