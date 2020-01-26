import pygame
from pygame import joystick
from threading import Thread
from .controller import PS4C
from .constants import *
import time


class PS4manager(object):
    def __init__(self):
        super(PS4manager, self).__init__()
        self._controllers = []
        self._listen = False

        # print("Initializing pygame")
        pygame.init()
        pygame.display.init()
    
        joystick.init()

        self._init_controllers()

    def start(self):
        """
        Start listening for PS4 controller events
        """
        if not self._listen:
            thread = Thread(target=self._run_event_loop, name="PS4ManagerEventThread")
            thread.daemon = True
            thread.start()

    def stop(self):
        """
        Stops listening for PS4 controller events
        """
        self._listen = False

    @property
    def num_controllers(self):
        return len(self._controllers)

    def get_available_controller(self):
        for ctrl in self.controllers():
            if not ctrl.in_use:
                ctrl.in_use = True
                return ctrl
        else:
            return None

    def controllers(self):
        """
        Returns a list of all the available PS4 controllers
        :return: list of PS4C objects of available controllers
        :rtype: list
        """
        return self._controllers

    def _init_controllers(self):
        """
        Helper method: Setup available PS4 controllers
        """
        if not joystick.get_init():
            joystick.init()
        for joy_id in range(joystick.get_count()):
            js = joystick.Joystick(joy_id)
            if PS4C.is_ps4_controller(js.get_name()):
                js.init()
                ps4ctrl = PS4C(js)
                self._controllers.append(ps4ctrl)

    @staticmethod
    def _ps4_event(event):
        """
        Helper method: checks if pygame.event is one of the supported joystick event / ps4 controller event
        """
        return event.type in [pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYAXISMOTION]

    @staticmethod
    def _event_for_this_controller(ctrl, event):
        return ctrl.id == event.joy

    def _handle_ps4_event(self, event):
        """
        Helper method: handles pygame ps4 event to be handled by the correct ps4 device
        """
        for ctrl in self._controllers:
            if self._event_for_this_controller(ctrl, event):
                ctrl.handle_event(event)

    def _run_event_loop(self):
        """
        Helper method: runs the event loop than listens for incoming events
        """
        self._listen = True
        while self._listen:
            for event in pygame.event.get():
                if self._ps4_event(event):
                    self._handle_ps4_event(event)
            time.sleep(1.0 / 50.0)


# EXAMPLE CODE

if __name__ == "__main__":
    # EXAMPLE CODE FOR PS4 MANAGER

    # EXAMPLE CB's
    def button_square_cb():
        print ("Square")

    def button_x_cb():
        print ("X")

    def button_circle_cb():
        print ("Circle")
        
    def button_triangle_cb():
        print ("Triangle")

    def axis_cb(value):
        print( "axis:", value)
        pass

    # INIT MANAGER
    manager = PS4manager()

    # SETUP CALLBACKS FOR EACH CONTROLLER
    for controller in manager.controllers():
        # EXAMPLE SET SINGLE CB EVENT
        controller.set_button_press_event(constants.BUTTON_CIRCLE, button_circle_cb)
        controller.set_button_release_event(constants.BUTTON_SQUARE, button_square_cb)
        controller.set_button_release_event(constants.BUTTON_TRIANGLE, button_triangle_cb)
        controller.set_button_release_event(constants.BUTTON_CROSS, button_x_cb)
        controller.set_axis_change_event(constants.AXIS_JOYSTICK_R_VER, axis_cb)

        # EXAMPLE SET MULTIPLE CB SAME EVENT TYPE
        # controller.set_axis_change_events({
        #     constants.AXIS_JOY_PAD_LEFT: axis_cb,
        #     constants.AXIS_JOY_PAD_UP: axis_cb,
        #     constants.AXIS_JOY_PAD_DOWN: axis_cb,
        #     constants.AXIS_JOY_PAD_RIGHT: axis_cb
        # })

        # EXAMPLE SET MULTIPLE EVENTS ALL TYPES
        # controller.set_events(
        #     button_press={
        #         constants.BUTTON_SQUARE: button_square_cb
        #     },
        #     button_release={
        #         constants.BUTTON_JOY_PAD_DOWN: button_up_cb
        #     },
        #     axis={
        #         constants.AXIS_JOY_PAD_RIGHT: axis_cb
        #     }
        # )

    manager.start()
    time.sleep(1000)

    # manager.controllers()[0].disabled = True

    # manager.stop()
    # time.sleep(10)

    # manager.start()
    # time.sleep(10)

    # manager.stop()
