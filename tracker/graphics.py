import numpy as np

import cv2
from util import vector, color

class DrawError(ValueError):
    pass


class ImageGraphics(object):
    """
    Simple graphics library for drawing to tracking image and masks
    """

    @staticmethod
    def draw_circle(img, pos, radius, color, border=-1):
        """
        Draw a circle object to the given image
        :param img: Target image
        :param pos: Center position of the circle
        :type pos: tuple or list or Vector2D
        :param radius: The radius of the circle
        :type radius: int or float
        :param color: The color of the circle
        :type color: Color
        :raise DrawError: Raises draw error on wrong input parameters
        """
        ImageGraphics._validate_image(img)
        ImageGraphics._validate_color(color)

        pos = ImageGraphics.convert_to_screen_coordinates(img, pos)
        cv2.circle(img, (int(pos[0]), int(pos[1])), radius, color.bgr, border)

    @staticmethod
    def draw_line(img, pos_a, pos_b, color):
        """
        Draw a line

        :param img: Target image
        :param pos_a: Start position of line
        :type pos_b: tuple or list or Vector2D
        :param pos_b: End position of line
        :type pos_b: tuple or list or Vector2D
        :param color: The color of the line
        :type color: Color
        :raise DrawError: Raises draw error on wrong input parameters
        """
        ImageGraphics._validate_image(img)
        ImageGraphics._validate_color(color)

        pos_a = ImageGraphics.convert_to_screen_coordinates(img, pos_a)
        pos_b = ImageGraphics.convert_to_screen_coordinates(img, pos_b)
        cv2.line(img, (int(pos_a[0]), int(pos_a[1])), (int(pos_b[0]), int(pos_b[1])), color.bgr)

    @staticmethod
    def draw_rectangle(img, pos, width, height, color, thickness=1):
        """
        Draw a square

        :param img: Target image
        :param pos: start position of the rectangle
        :type pos: tuple or list or Vector2D
        :param width: The width of the rectangle
        :type width: int or float
        :param height: Height of the rectangle
        :type height: int or float
        :param color: The color of the rectangle
        :type color: Color
        :param thickness: The thickness of the lines in the rectangle
        :type thickness: int
        :raise DrawError: Raises draw error on wrong input parameters
        """
        ImageGraphics._validate_image(img)
        ImageGraphics._validate_color(color)

        pos = ImageGraphics.convert_to_screen_coordinates(img, pos)
        #pos2 = ImageGraphics.convert_to_screen_coordinates(img, (pos[0], pos[1]))
        pos2 = (pos[0] + width, pos[1] - height)
        cv2.rectangle(img, tuple(pos), (pos2[0], pos2[1]), color.bgr, thickness=thickness)

    @staticmethod
    def draw_text(img, txt, pos, size, color):
        """
        Draw text string

        :param img: Target image
        :param txt: The string to draw
        :type txt: str or float or int
        :param pos: Start position of the text
        :type pos: tuple or list or Vector2D
        :param size: Font size
        :type size: int or float
        :param color: Color of the text
        :type color: Color
        :raise DrawError: Raises draw error on wrong input parameters
        """
        ImageGraphics._validate_image(img)
        ImageGraphics._validate_color(color)
        pos = ImageGraphics.convert_to_screen_coordinates(img, pos)
        cv2.putText(img, str(txt), (int(pos[0]), int(pos[1])), cv2.FONT_ITALIC, size, color.bgr)

    @staticmethod
    def draw_vector(img, start_pos, vector, color):
        """
        Draw a given vector
        :param img: Target image
        :param start_pos: Start position of the vector to draw
        :type start_pos: tuple or list or Vector2D
        :param vector: The vector to draw
        :type vector: Vector2D or tuples
        :param color: The color of the vector
        :type color: Color
        """
        ImageGraphics._validate_image(img)
        ImageGraphics._validate_color(color)
        ImageGraphics._validate_pos(start_pos)
        ImageGraphics._validate_pos(vector)
        if vector and start_pos and vector.magnitude:
            vector = vector + start_pos
            ImageGraphics.draw_circle(img, vector, 3, color)
            ImageGraphics.draw_line(img, start_pos, vector, color)

    @staticmethod
    def draw_vector_with_label(img, text, start_pos, vector, color):
        """
        Draw a given vector with a text label at the end position
        :param img: Target image
        :param text: Label of the vector
        :type text: str
        :param start_pos: Start position of the vector to draw
        :type start_pos: tuple or list or Vector2D
        :param vector: The vector to draw
        :type vector: Vector2D or tuples
        :param color: The color of the vector
        :type color: Color
        """
        try:
            text_pos = vector + start_pos + (5, 5)
        except TypeError:
            raise DrawError("Unsupported operands for position fo graphics, Draw vector with label")
        ImageGraphics.draw_text(img, str(text), text_pos, 0.3, color)
        ImageGraphics.draw_vector(img, start_pos, vector, color)

    @staticmethod
    def convert_to_screen_coordinates(img, pos):
        """
        Method to convert euclidean positions to image positions
        :param img: Image to convert coordinates to
        :param pos: The position to convert
        :return: The new positions
        :rtype: Vector2D
        """
        ImageGraphics._validate_pos(pos)

        shape = np.shape(img)
        return Vector2D(int(pos[0]), int(shape[0] - pos[1]))

    @staticmethod
    def draw_tracked_path(img, tracked_samples, max_samples=None):
        # TODO refactor and docs
        last_sample = None
        color = Color((255, 0, 0))
        for sample in tracked_samples:
            if max_samples is not None:
                max_samples -= 1
                if max_samples < 0:
                    break

            if last_sample is not None:
                ImageGraphics.draw_line(img, last_sample.pos, sample.pos, color)
                ImageGraphics.draw_circle(img, sample.pos, 2, color)
            last_sample = sample

    @staticmethod
    def draw_tracked_path_pos(img, tracked_samples, max_samples=None):
        # TODO refactor and docs
        last_sample = None
        color = Color((0, 255, 0))
        for sample in reversed(tracked_samples):
            if max_samples is not None:
                max_samples -= 1
                if max_samples < 0:
                    break

            if last_sample is not None:
                ImageGraphics.draw_line(img, last_sample, sample, color)
                ImageGraphics.draw_circle(img, sample, 2, color)
            last_sample = sample

    @staticmethod
    def _validate_pos(pos):
        """
        Helper method: Validates that the position parameter is valid
        :raise DrawError:
        """
        if not isinstance(pos, (list, tuple, Vector2D)):
            raise DrawError("Type error, position needs to be: list, tuple or Vector2D. Given type is: " +
                            str(type(pos)))

    @staticmethod
    def _validate_image(img):
        """
        Helper method: Validates that the image is the correct type
        :raise DrawError:
        """
        if not isinstance(img, np.ndarray):
            raise DrawError("Image need to be a numpy array, given type is: %s" % type(img))

    @staticmethod
    def _validate_color(color):
        """
        Helper method: Validates that the color is a Color object
        :raise DrawError:
        """
        if not isinstance(color, Color):
            raise DrawError("Color need to be a Color object, given type is: %s" % type(color))

if __name__ == "__main__":
    image = np.zeros([800, 600, 3], dtype=np.uint8)

    ImageGraphics.draw_rectangle(image, (200, 300), 20, 30, Color((245, 3, 23)))

    ImageGraphics.draw_circle(image, (10, 10), 10, Color((255, 255, 0)))

    ImageGraphics.draw_vector(image, Vector2D(100, 100), Vector2D(100, 100), Color((255, 255, 255)))

    cv2.imshow("test", image)
    while True:
        cv2.waitKey(1)
