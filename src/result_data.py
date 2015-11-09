from src.sequence import Sequence


class ResultData(object):
    def __init__(self, data):
        self.sequence = Sequence()
        self.data = data
        self.error = {}
        self.times = {}
        self.goods = {}
