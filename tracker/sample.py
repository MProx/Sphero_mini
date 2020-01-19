from util import vector


class TrackingSample(object):
    """
    Holds one single tracking result
    """
    def __init__(self):
        self.pos = None
        self.timestamp = None
        self.valid = False

        self.prev_sample = None

    def distance_vector(self):
        """
        :return: Vector2D
        """
        try:
            return self.pos - self.prev_sample.pos
        except (AttributeError, TypeError):
            return None

    @property
    def speed(self):
        """
        Calculates the linear speed from this sample to the given sample
        :return: The given speed in pixels per second
        :rtype: float
        """
        try:
            distance = self.distance_vector().magnitude
            time_diff = abs(self.timestamp - self.prev_sample.timestamp)
            return distance / time_diff
        except (ZeroDivisionError, AttributeError, ValueError):
            return None

    @property
    def angle(self):
        """
        Returns the direction between this sample and the
        previous_sample.

        Returns None if prev_sample or this sample is not valid

        :return: float or None
        """
        try:
            return (self.distance_vector()).angle
        except (AttributeError, TypeError, ZeroDivisionError):
            return None

    # def dps(self):
    #     try:
    #         angle = self.angle
    #         time_diff = abs(self.timestamp - self.prev_sample.timestamp)
    #         return angle / time_diff
    #     except (AttributeError, TypeError, ZeroDivisionError):
    #         return None

    def angle_from_other_sample(self, other):
        # TODO FIX CORRECT OFFSET
        vector_a = Vector2D(10, 0).set_angle(other.angle)
        vector_b = Vector2D(10, 0).set_angle(self.angle)
        return vector_a.get_offset(vector_b)

    # TODO: ADD degrees per second turn - 4/22/14

    # TODO: Add a areal/bounding box field?

    # TODO is accelerating?
    # MAYBE STORE TRACKED IMAGE HERE?