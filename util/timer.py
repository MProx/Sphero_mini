import time

def calc_fps(t0, t1):
    """
    Calculates the current update rate from the two given time samples
    :param t0:
    :param t1:
    :return: current fps
    """
    try:
        return 1.0 / (t1 - t0)
    except ZeroDivisionError:
        return -1.


class StopWatch(object):
    def __init__(self):
        super(StopWatch, self).__init__()
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        return time.time() - self.start_time
