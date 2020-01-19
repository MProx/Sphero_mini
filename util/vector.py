import math

class Vector2D(object):
    """
    A class for representing a 2D vector with its start point in origin
    """
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return "(x: " + str(self.x) + ", y:" + str(self.y) + ", deg:" + str(self.angle) + ")"

    def __repr__(self):
        return self
        # return Vector2D(self.x, self.y)

    def __nonzero__(self):
        x = self.x is not None
        y = self.y is not None
        return x and y

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError("value must be integer")
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError("Index out of range, must be value in the range of 0 to 1")

    def __setitem__(self, index, value):
        if not isinstance(index, int):
            raise TypeError("value must be integer")
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Index out of range, must be value in the range of 0 to 1")

    def __add__(self, other):
        tmp = Vector2D()
        tmp.x = self.x + other[0]
        tmp.y = self.y + other[1]
        return tmp

    def __iadd__(self, other):
        v, w = self._unpack(other)
        self.x += v
        self.y += w
        return self

    def __sub__(self, other):
        tmp = Vector2D()
        v, w = self._unpack(other)
        tmp.x = self.x - v
        tmp.y = self.y - w
        return tmp

    def __isub__(self, other):
        v, w = self._unpack(other)
        self.x -= v
        self.y -= w
        return self

    def __mul__(self, other):
        tmp = Vector2D()
        v, w = self._unpack(other)
        tmp.x = self.x * v
        tmp.y = self.y * w
        return tmp

    def __imul__(self, other):
        v, w = self._unpack(other)
        self.x *= v
        self.y *= w
        return self

    def __div__(self, other):
        tmp = Vector2D()
        v, w = self._unpack(other)
        tmp.x = float(self.x) / v
        tmp.y = float(self.y) / w
        return tmp

    def __idiv__(self, other):
        v, w = self._unpack(other)
        self.x = float(self.x) / v
        self.y = float(self.y) / w
        return self

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def _unpack(other):
        """
        Helper method: Unpacks a value, vector, list or tuple to x and y values
        :param other: the value to unpack
        :type other: int or float or list or tuple or Vector2D
        :rtype : tuple
        """
        if isinstance(other, (tuple, Vector2D)):
            v = other[0]
            w = other[1]
        else:
            v = other
            w = other
        return v, w

    @property
    def inverted(self):
        """
        Returns an inverted copy if itself
        :return: inverted copy
        :rtype: Vector2D
        """
        return Vector2D(self.x * -1, self.y * -1)

    def invert(self):
        """
        Inverts is x and y values
        """
        self.x *= -1
        self.y *= -1

    @property
    def magnitude(self):
        """
        Return the magnitude of the vector. If x or y is set to None. Returns None
        :return: magnitude
        :rtype: int or float or None
        """
        if self:
            return math.sqrt(self.x**2 + self.y**2)
        return None

    @property
    def normalized(self):
        """
        Returns a normalized copy of itself
        :return: Normalized vector of itself
        :rtype: Vector2D
        """
        m = self.magnitude
        if m:
            return Vector2D(self.x / m, self.y / m)
        return Vector2D(0, 0)

    def copy(self):
        """
        Returns a copy of the vector
        :return: A copy of the vector
        :rtype: Vector2D
        """
        return Vector2D(self.x, self.y)

    def set_values(self, x, y):
        """
        Set new values for the vector
        :param x: the new x value
         :type x: int or float
        :param y: the new y value
         :type y: int or float
        """
        self.x = x
        self.y = y

    def get_values(self):
        """
        Returns self as a Vector2D object
        :return: self as vector 2D object
        :rtype: Vector2D
        """
        return Vector2D(self.x, self.y)

    @property
    def angle(self):
        """
        Get the angle of the vector in degrees
        :return: the angle of the vector in degrees
        :rtype: int or float
        """
        deg = math.degrees(self.angle_radians)
        if deg < 0:
            return 360 - abs(deg)
        return deg

    @angle.setter
    def angle(self, angle_deg):
        """
        Changes the angle of the vector, but not it magnitude. Note if the magnitude is zero the
        vector will not change is angle
        :param angle_deg: The new angle in degrees
        """
        self.set_angle(angle_deg)

    @property
    def angle_radians(self):
        """
        Get the current angle of the vector in radians
        :return: The angle of the vector in radians
        """
        return math.atan2(self.y, self.x)

    @angle_radians.setter
    def angle_radians(self, angle_rad):
        """
        Changes the angle of the vector, but not it magnitude. Note if the magnitude is zero the
        vector will not change is angle
        :param angle_rad: The new angle in radians
        """
        self.set_angle_radians(angle_rad)

    def set_angle(self, angle_deg):
        """
        Changes the angle of the vector, but not it magnitude. Note if the magnitude is zero the
        vector will not change is angle
        :param angle_deg: The new angle in degrees
        :return: A copy of the new vector
        :rtype: Vector2D
        """
        return self.set_angle_radians(math.radians(angle_deg))

    def set_angle_radians(self, angle_radians):
        """
        Changes the angle of the vector, but not it magnitude. Note if the magnitude is zero the
        vector will not change is angle
        :param angle_radians: The new angle in radians
        :return: A copy of the new vector
        :rtype: Vector2D
        """
        mag = self.magnitude
        self.x = math.cos(angle_radians) * mag
        self.y = math.sin(angle_radians) * mag
        return Vector2D(self.x, self.y)

    def rotate(self, angle_deg):
        """
        Rotates the vector the given number of degrees and returns a copy of this vector
        :param angle_deg: The angle to rotate
        :return: the new rotated vector
        """
        angle = math.radians(angle_deg)
        return self.rotate_radians(angle)

    def rotate_radians(self, angle):
        """
        Rotates the vector the given angle from it current angle
        :param angle: rotation offset in radians
        :return: a copy of the new vector
        :rtype: Vector2D
        """
        x = self.x
        y = self.y
        self.x = x * math.cos(angle) - y * math.sin(angle)
        self.y = y * math.cos(angle) + x * math.sin(angle)
        return Vector2D(self.x, self.y)

    def angle_between(self, other_vector):
        """
        Returns the shortest angle between two vectors
        :param other_vector: The other vector
        :return: the angle in degrees
        :rtype: float
        """
        return math.degrees(self.angle_between_radians(other_vector))

    def angle_between_radians(self, other_vector):
        """
        Returns the shortest angle between two vectors
        :param other_vector: the other vector
        :return: the shortest angle in radians
        :rtype: float
        """
        mag_a = self.magnitude
        mag_b = other_vector.magnitude
        try:
            return math.acos((self.x * other_vector.x + self.y * other_vector.y) / (mag_a * mag_b))
        except ZeroDivisionError:
            return 0.0

    def set_length(self, length):
        """
        Changes the length of the vector but does not change is angle. If the vectors
        magnitude is 0 before this command the angle will be set to 0
        :param length: The new length of the vector
        :type: length: int or float
        :return: A copy of the itself with the new length
        :rtype: Vector2D
        """
        if self.magnitude == 0.0:
            self.x = 1.0
        vector = self.normalized * length
        self.x = vector.x
        self.y = vector.y
        return self.copy()

    def get_offset(self, other, n_digits=4):
        """
        Gets the offset in the range of -180, 180 degrees between two vectors
        :param other: Vector A
        :type other: Vector2D
        :param n_digits: the decimal precision to set on the returned result
        :type n_digits: int
        """
        angle = round(self.angle - other.angle, n_digits)
        return angle if angle < 180 else angle - 360

if __name__ == "__main__":
    a = Vector2D(0, 1)
    b = Vector2D(3, 10)
    print (a.set_angle_radians(a.angle_radians))

    print (b.angle, b)
    b.angle += 1
    print (b.angle, b)