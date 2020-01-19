import numpy as np

import cv2

from util.color import Color


class BaseFilter(object):
    def get_mask(self, img):
        return img


class ColorFilter(BaseFilter):
    def __init__(self):
        self.lower = Color()
        self.upper = Color()

    def hsv_lower_filter(self, data_size=np.uint8):
        return ColorFilter.to_np_array(self.lower.hsv, data_size)

    def hsv_upper_filter(self, data_size=np.uint8):
        return ColorFilter.to_np_array(self.upper.hsv, data_size)

    @staticmethod
    def to_np_array(color_tuple, data_size):
        return np.array(list(color_tuple), data_size)

    def get_mask(self, img):
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv_lower_limit = self.hsv_lower_filter()
        hsv_upper_limit = self.hsv_upper_filter()
        return cv2.inRange(hsv_img, hsv_lower_limit, hsv_upper_limit)


class FilterGlow(ColorFilter):
    def __init__(self):
        super(FilterGlow, self).__init__()
        self.lower.hsv = (0, 0, 0)
        self.upper.hsv = (0, 255, 255)


class FilterSpheroBlueCover(ColorFilter):
    def __init__(self):
        ColorFilter.__init__(self)
        self.lower.hsv = (100, 100, 100)
        self.upper.hsv = (120, 255, 255)


class FilterSpheroYellowCover(ColorFilter):
    def __init__(self):
        ColorFilter.__init__(self)
        self.lower.hsv = (20, 100, 100)
        self.upper.hsv = (40, 255, 255)


class FilterSpheroOrangeCover(ColorFilter):
    def __init__(self):
        ColorFilter.__init__(self)
        self.lower.hsv = (160, 113, 146)
        self.upper.hsv = (180, 201, 255)

if __name__ == "__main__":
    color = Color()

    color.rgb = (0, 0, 0)
    print ("RGB", color.rgb, "HSV", color.hsv)

    color.hsv = (0, 0, 255)
    print ("RGB", color.rgb, "HSV", color.hsv)

    color.hsv = (0, 255, 255)
    print ("RGB", color.rgb, "HSV", color.hsv)

    color.hsv = (0, 255, 255)
    print (color.rgb, color.hsv, color.bgr)

    print (hex(color), color.hex)
