from collections import namedtuple
import colorsys


class Color(object):
    max_deg_value = 180.0
    RGB_tuple = namedtuple('RGB', 'r g b')
    HSV_tuple = namedtuple('HSV', 'h s v')
    BGR_tuple = namedtuple('BGR', 'b g r')

    def __init__(self, rgb_color=None):
        self._color = (0, 0, 0)
        if rgb_color is not None:
            self.rgb = rgb_color

    @property
    def rgb(self):
        """
        Returns the color as a RGB color value
        :return: The RGB color tuple
        :rtype: Color.RGB_tuple
        """
        return Color.RGB_tuple(*self._color)

    @rgb.setter
    def rgb(self, rgb_color):
        """
        Sets color value from a RGB tuple (r, g, b)
        :param rgb_color: The new RGB color value
        :type rgb_color: tuple
        """
        self._color = rgb_color

    @property
    def hsv(self):
        """
        Get color as HSV tuple
        :return: Tuple of color coordinates
        :rtype: Color.HSV_tuple
        """
        r, g, b = self.rgb
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        h *= self.max_deg_value
        s *= 255
        v *= 255
        return Color.HSV_tuple(int(h), int(s), int(v))

    @hsv.setter
    def hsv(self, hsv_color):
        """
        Set color from HSV tuple (h, s, v)
        :param hsv_color: The tuple of values
        :type hsv_color: tuple
        """
        h, s, v = hsv_color
        h = float(h) / float(self.max_deg_value)
        s = float(s) / 255.0
        self._color = colorsys.hsv_to_rgb(h, s, v)

    @property
    def bgr(self):
        """
        Get color as BGR tuple
        :return: The color as a BGR tuple
        :rtype: Color.BGR_tuple
        """
        r, g, b = self.rgb
        return Color.BGR_tuple(b, g, r)

    @bgr.setter
    def bgr(self, bgr_color):
        """
        Set color from BGR tuple
        :param bgr_color: Bgr color
        :type bgr_color: tuple
        """
        b, g, r = bgr_color
        self.rgb = (r, g, b)

    @property
    def hex(self):
        """
        Get color as rgb hex string
        :return: Color value as RGB Hex string
        :rtype: str
        """
        return hex(self)

    @hex.setter
    def hex(self, value):
        # TODO: implemet set from HEX str
        raise NotImplementedError

    def __hex__(self):
        r, g, b = self.rgb
        return '#%02x%02x%02x' % (r, g, b)