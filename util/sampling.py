

class AvgValueSampleHolder(object):
    """
    Helper class for handling multiple samples average value
    """
    def __init__(self):
        super(AvgValueSampleHolder, self).__init__()
        self.sum_samples = 0.0
        self.num_samples = 0

    def add_sample(self, value):
        self.sum_samples += value
        self.num_samples += 1

    def reset(self):
        self.num_samples = 0.0
        self.sum_samples = 0

    @property
    def avg(self):
        try:
            return self.sum_samples / self.num_samples
        except ZeroDivisionError:
            return 0.0