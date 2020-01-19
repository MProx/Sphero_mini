from copy import copy, deepcopy
from tracker import *
from util import color
from util import vector


class TraceableObject(object):
    """
    Represents a single traceable object
    Holds the filter to use for the tracking of this object and holds
    the samples tracked and logic for handling this data
    """
    default_x = None
    default_y = None

    def __init__(self, name="no-name"):
        super(TraceableObject, self).__init__()
        self._calibration_start_sample = None
        self.object_name = name

        # Filter used to find the object in the image
        self.filter = None

        # Size of the tracked image
        self.screen_size = (0, 0)

        # TRACKING
        self.tracking_samples = []

        # CONFIG
        self.max_samples_in_memory = 20
        self.max_samples_dir_determination = 8
        self.max_samples_speed_determination = 1

        self.is_moving_threshold = 1.0

        self.last_tracking_successful = False
        """ :param last_tracking_successful: Check if last tracking was successful"""

        self.store_invalid_samples = False
        """ :param store_invalid_samples: Should store non successful tracking samples"""

        # Graphics
        self.color = Color((255, 0, 0))
        self.direction_length = 20

    def add_tracking(self, pos, timestamp):
        sample = TrackingSample()
        self.last_tracking_successful = False
        if pos:
            self.last_tracking_successful = True
            sample.valid = True
        elif not self.store_invalid_samples:
            return
        sample.pos = pos
        sample.timestamp = timestamp
        self._save_tracking(sample)

    def _save_tracking(self, tracking_sample):
        """
        Add a new tracking sample to saved samples

        :param tracking_sample:
         :type tracking_sample: tracker.sample.TrackingSample
        """
        self.tracking_samples.insert(0, tracking_sample)
        try:
            self.tracking_samples[0].prev_sample = self.tracking_samples[1]
        except IndexError:
            pass
        if len(self.tracking_samples) > self.max_samples_in_memory:
            self.tracking_samples.pop(-1)
            self.tracking_samples[-1].prev_sample = None

    @property
    def last_valid_pos(self):
        """
        Gives the position of the last successfully tracked sample

        :return: Vector2D or None
         :rtype: Vector2D or None
        """
        for tracking in self.tracking_samples:
            if tracking.valid:
                return tracking.pos
        else:
            return None

    @property
    def pos(self):
        """
        Return the last tracked position. Position is set to none if the tracking was not successful
        Returns None if objects has now tracked samples

        :return: Vector2D of last tracked position (x and y are set not None if object was not succesfully tracked)
        :rtype: Vector2D or None
        """
        if self.tracking_samples and self.last_tracking_successful:
            return self.tracking_samples[0].pos
        return None

    @property
    def speed(self):
        """
        Liner speed between the two last successful samples

        :return: The linear speed, None if only one sample
        :rtype: float or None
        """
        speed = 0.0
        samples = self.get_valid_samples(max_samples=self.max_samples_speed_determination)
        num_samples = len(samples)
        try:
            for sample in samples:
                try:
                    speed += sample.speed
                except TypeError:
                    num_samples -= 1
            return speed / num_samples
        except ZeroDivisionError:
            return None

    @property
    def is_moving(self):
        """
        Returns true if the tracked movement is larger than the is_moving_threshold.s

        :return: True if moving False else
         :rtype: bool
        """
        return self.speed >= self.is_moving_threshold

    def do_before_tracked(self, *args, **kwargs):
        """
        This method is called right before the object is tracked in the image
        """
        pass

    def do_after_tracked(self, *args, **kwargs):
        """
        This method is called right after the object is tracked in the image
        """
        pass

    def draw_direction_vector(self, image, pos):
        if self.direction:
            try:
                label = round(self.direction.angle, 2)
                if self.is_moving:
                    vector = self.direction.set_length(self.direction_length)
                    Ig.draw_vector_with_label(image, str(label), pos, vector, self.color)
                Ig.draw_circle(image, pos, 2, self.color)
            except tracker.graphics.DrawError:
                pass

    def draw_graphics(self, image):
        """
        Insert all the code for drawing in this method. Is executed after the tracking

        :param image: The image to draw the image on. (Numpy Vector)
        """
        self.draw_direction_vector(image, self.pos)

    def draw_name(self, image):
        """
        Draws the name of the object to the given image at the objects latest successfully traced position

        :param image:
        """
        try:
            Ig.draw_text(image, self.object_name, self.pos + (15, 5), 0.35, Color((255, 255, 255)))
        except TypeError:
            pass  # Pos is not set or is None

    def get_valid_samples(self, max_samples=-1):
        """
        Return a list of the all the valid samples currently stored in the traceable.

        :param max_samples: The maximum number of samples to return
        :type max_samples: int
        :return: list of the valid samples
        :rtype: list
        """
        valid_samples = []
        for tracking in self.tracking_samples:
            if tracking.valid:
                valid_samples.append(tracking)
                max_samples -= 1
            if max_samples == 0:
                break
        return valid_samples

    @staticmethod
    def get_avg_pos_of_samples(tracking_samples):
        """
        Gets the average of the given samples

        :raise ZeroDivisionError: If number of samples is Zero
        :param tracking_samples: list of samples
        :type tracking_samples: list
        :return: the average
        :rtype: Vector2D
        """
        avg_sample = Vector2D(0, 0)
        for tracking_sample in tracking_samples:
            avg_sample += tracking_sample.pos
        return avg_sample / len(tracking_samples)

    @staticmethod
    def get_avg_angle_offset_of_samples(tracing_samples):
        # TODO: Add docs - 4/18/14
        # TODO: WRONG HERE NEED TO CALC ANGLE CORRECT: NEED TO FIND ANGLE BETWEEN 3 SAMPLES - 4/18/14

        avg_offset = 0
        tmp = None
        for tracing_sample in tracing_samples:
            if tmp:
                angle = tmp.angle_from_other_sample(tracing_sample)
                avg_offset += angle
            tmp = tracing_sample
        return avg_offset / (len(tracing_samples) - 1)

    @property
    def direction(self):
        """
        Returns a vector with the tracked direction of the object
        :return: The direction vector
        :rtype: Vector2D
        """
        samples = self.get_valid_samples(max_samples=5)
        num_samples = len(samples)
        direction = Vector2D(0.0, 0.0)

        for sample in samples:
            try:
                direction += sample.distance_vector()
            except (TypeError, AttributeError):
                num_samples -= 1
        if not num_samples:
            return Vector2D(None, None)

        #print samples[0].distance_vector().angle, direction.angle, direction.get_offset(samples[0].distance_vector())
        try:
            direction.angle -= 2*direction.get_offset(samples[0].distance_vector())
        except AttributeError:
            print ("ATTR ERROR")
        return direction

    def get_calculated_path(self, turn_rate, samples=5):
        # TODO: REFACTOR - 4/22/14

        samples = []
        try:
            current_dir = self.direction.angle
            avg_speed = self.speed
            avg_turn = self.get_avg_angle_offset_of_samples(self.get_valid_samples(max_samples=8))

            vector = Vector2D(self.pos.x, self.pos.y)

            tmp_vector_b = Vector2D(0, 0)
            tmp_vector_b.set_length(avg_speed / 10.0)
            tmp_vector_b.angle = current_dir

            for _ in range(10):
                samples.append(vector.copy())
                tmp_vector_b.angle += avg_turn
                vector = vector + tmp_vector_b

            return samples
        except (TypeError, AttributeError):
            pass
        return samples

    # TESTING FOR LINEAR CALIBRATION
    def start_linear_calibration(self):
        try:
            sample = self.tracking_samples[0]
            if sample.valid:
                self._calibration_start_sample = deepcopy(sample)
            else:
                self._calibration_start_sample = None
                raise IndexError("cant find object in last tracking")
        except (IndexError, AttributeError):
            self._calibration_start_sample = None
            raise IndexError("No samples to use as start point for the calibration")

    def stop_linear_calibration(self):
        try:
            sample = deepcopy(self.tracking_samples[0])
            if sample.valid:
                sample.prev_sample = self._calibration_start_sample
                angle = sample.angle
                speed = sample.speed
                return angle, speed
            else:
                raise IndexError("cant find object in last tracking")
        except (IndexError, AttributeError):
            raise IndexError("No sample to use for end point of calibration")


