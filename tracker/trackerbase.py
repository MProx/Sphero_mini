from copy import copy
import numpy as np
import cv2
import time
from .graphics import *
from .trackingfilter import FilterSpheroBlueCover, FilterSpheroYellowCover, FilterSpheroOrangeCover, FilterGlow
from .traceable import TraceableObject
import sys
sys.path.append("..")
from util.vector import Vector2D
import util 

class ImageHandler(object):
    @staticmethod
    def image_bgr_to_hsv(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    @staticmethod
    def noise_reduction(mask, erode=1, dilate=1, kernel_size=3, blur=9):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        mask = cv2.erode(mask, kernel, iterations=erode)
        mask = cv2.dilate(mask, kernel, iterations=dilate)
        mask = cv2.medianBlur(mask, blur)
        return mask

    @staticmethod
    def adjust_contrast_and_brightness(img, contrast, brightness):
        mul_img = cv2.multiply(img, np.array([contrast]))
        img = cv2.add(mul_img, np.array([brightness]))
        return img


class TrackerBase(object):
    TRACK_TYPE_STROBE = 0
    TRACK_TYPE_COLOR = 1
    TRACK_TYPE_DEPTH = 2

    def __init__(self):
        self.track_type = None

        self.cam = cv2.VideoCapture(0)

        if not self.cam.isOpened():
            self.cam.open()

        self.image_size = (int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        ## VIDEO CAPTURE
        # fourcc = cv2.cv.CV_FOURCC(*'XVID')
        # self.video_out = cv2.VideoWriter('video/cameraController{}.avi'.format(time.time()), fourcc, 15, self.image_size)

    def track_objects(self, traceable_obj):
        if traceable_obj is None:
            traceable_obj = TraceableObject()
        return traceable_obj

    def get_video_frame(self):
        # TODO FIX HERE FOR KINECT OR WEBCAM
        ret, frame = self.cam.read()
        return frame

    @staticmethod
    def find_largest_contour_in_image(img):
        contours = TrackerBase.find_all_contours(img)
        largest_contour = TrackerBase.find_largest_contour(contours)

        cx, cy = TrackerBase.get_contour_coordinates(largest_contour)
        return cx, cy

    @staticmethod
    def find_all_contours(img):
        contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    @staticmethod
    def find_largest_contour(contours):
        max_area = 0
        max_contour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if max_area < area:
                max_area = area
                max_contour = contour
        return max_contour

    @staticmethod  # TODO Get bounding box
    def get_contour_coordinates(contour):
        cx, cy = None, None
        if contour is not None:
            try:
                m = cv2.moments(contour)
                # TODO return bounding box
                cx, cy = int(m['m10'] / m['m00']), int(m['m01'] / m['m00'])
            except ZeroDivisionError:
                pass
        return cx, cy


class ColorTracker(TrackerBase):
    """
    Implements a simple color tracker. The color tracker is used to find positions of a single glowing
    object
    """
    def __init__(self):
        super(ColorTracker, self).__init__()
        self._masks = None

        self.t1 = None

        # TESTING
        self.number_of_samples = 0
        self.avg_samples = [util.AvgValueSampleHolder(), util.AvgValueSampleHolder(), util.AvgValueSampleHolder(), util.AvgValueSampleHolder()]

    def track_objects(self, traceable_objects):
        image = self.get_video_frame()
        timestamp = time.time()

        for traceable_obj in traceable_objects:
            # UPDATE SCREEN POSITION
            traceable_obj.screen_size = self.image_size

            # PREPARE FOR TRACKING
            traceable_obj.do_before_tracked()

            # DO TRACKING
            x, y = self._find_traceable_in_image(image, traceable_obj)

            traceable_obj.add_tracking(Vector2D(x, y), timestamp)

            # DRAW GRAPHICS
            traceable_obj.draw_name(self._masks)
            traceable_obj.draw_name(image)
            traceable_obj.draw_graphics(image)

            # FINNISH TRACKING
            traceable_obj.do_after_tracked()

        t2 = time.time()
        if self.t1 is not None:
            fps = int(util.calc_fps(self.t1, t2))
        else:
            fps = 0
        label_fps = "Tracking/sec: {}".format(fps)
        ImageGraphics.draw_text(image, label_fps, (10, 10), 0.5, util.Color((255, 255, 0)))

        label_n_tracables = "Num objects: {}".format(len(traceable_objects))
        ImageGraphics.draw_text(image, label_n_tracables, (200, 10), 0.5, util.Color((255, 255, 0)))

        self._draw_masks()

        # self.video_out.write(image)

        self.t1 = time.time()

        cv2.imshow("img", image)
        cv2.waitKey(1)
        return traceable_objects

    def _find_traceable_in_image(self, image, traceable_obj):
        mask = traceable_obj.filter.get_mask(image)
        mask = ImageHandler.noise_reduction(mask, erode=1, dilate=1, kernel_size=2)  # TODO Erode, dilate
        self._add_mask(mask)
        x, y = self.find_largest_contour_in_image(mask)
        if y is not None:
            y = self.image_size[1] - y
        return x, y

    def _draw_masks(self):
        if self._masks is not None:
            cv2.imshow("All masks", self._masks)
            self._masks = None

    def _add_mask(self, mask):
        if self._masks is None:
            self._masks = mask
        else:
            self._masks = self.merge_masks(self._masks, mask)

    @staticmethod
    def merge_masks(mask_a, mask_b):
        return cv2.bitwise_or(src1=mask_a, src2=mask_b)

## EXAMPLE CODE
if __name__ == "__main__":
    tracker = ColorTracker()

    traceable_glow = TraceableObject("GLOW")
    traceable_glow.filter = FilterGlow()

    traceable_blue = TraceableObject("BLUE")
    traceable_blue.filter = FilterSpheroBlueCover()

    traceable_yellow = TraceableObject("YELLOW")
    traceable_yellow.filter = FilterSpheroYellowCover()

    traceable_orange = TraceableObject("ORANGE")
    traceable_orange.filter = FilterSpheroOrangeCover()

    traceable_object = [traceable_blue, traceable_orange, traceable_yellow, traceable_glow]

    while True:
        traceable_object = tracker.track_objects(traceable_object)
        cv2.waitKey(5)





