import pygame
from .constants import *


class PS4C(object):
    EVENT_AXIS_CHANGE = pygame.JOYAXISMOTION
    EVENT_BUTTON_PRESS = pygame.JOYBUTTONDOWN
    EVENT_BUTTON_RELEASE = pygame.JOYBUTTONUP

    def __init__(self, pygame_joystick_obj):
        self._button_press_callbacks = {}
        self._button_release_callbacks = {}
        self._axis_callbacks = {}

        self.joystick_obj = pygame_joystick_obj

        # Disable callbacks
        self.disabled = False

        self.in_use = False

    def clear_all_callbacks(self):
        self._button_press_callbacks = {}
        self._button_release_callbacks = {}
        self._axis_callbacks = {}

    def free(self):
        self.in_use = False
        self.disabled = False
        self.clear_all_callbacks()

    @property
    def controller_name(self):
        """
        Get controller name

        :return: The name of the controller
        :rtype: str
        """
        return self.joystick_obj.get_name()

    @property
    def id(self):
        """
        Get the pygame controller id

        :return: The id of the controller
        :rtype: int
        """
        return self.joystick_obj.get_id()

    @staticmethod
    def is_ps4_controller(ctrl_name):
        """
        Check if controller name is a PSP controller

        :param ctrl_name: The name of the joystick device
        :return: True if this is a PSP controller
        :rtype: bool
        """
        print("Controller Name: " + ctrl_name)
        return True

    def set_events(self, button_press=None, button_release=None, axis=None):
        """
        Set multiple callbacks for each even type

        :param button_press: Event callbacks that should be triggered on button press: {button_id: cb, . . .}
        :type button_press: dict
        :param button_release: Event callbacks that should be triggered on button release: : {button_id: cb, . . .}
        :type button_release: dict
        :param axis: Event callbacks that should be triggered on axis events: : {axis_id: cb, . . .}
        :type axis: dict
        """
        for event_type in [button_press, button_release, axis]:
            if event_type is None:
                button_press = {}

        self.set_button_press_events(button_press)
        self.set_button_release_events(button_release)
        self.set_axis_change_events(axis)

    def set_button_press_events(self, event_dict):
        """
        Set multiple callbacks for button press events
        :param event_dict: Event callbacks that should be triggered on button press: {button_id: cb, . . .}
        :type event_dict: dict
        """
        for button_id, cb in event_dict.items():
            self.set_button_press_event(button_id, cb)

    def set_button_press_event(self, button_id, cb):
        """
        Set single cb for button press event
        :param button_id: The button id. Example PS3C.BUTTON_SQUARE
        :type button_id: int
        :param cb: The callback that should be triggered on a button press event for the given button id
        :type cb: Callback method or function example: def foo(*args)
        """
        self._add_event_cb(self._button_press_callbacks, button_id, cb)

    def set_button_release_events(self, event_dict):
        """
        Set multiple callbacks for button release events
        :param event_dict: Event callbacks that should be triggered on button release: : {button_id: cb, . . .}
        :type event_dict: dict
        """
        for button_id, cb in event_dict.items():
            self.set_button_release_event(button_id, cb)

    def set_button_release_event(self, button_id, cb):
        """
        Set single cb for button release event
        :param button_id: The button id. Example PS3C.BUTTON_SQUARE
        :type button_id: int
        :param cb: The callback that should be triggered on a button release event for the given button id
        :type cb: Callback method or function example: def foo(*args)
        """
        self._add_event_cb(self._button_release_callbacks, button_id, cb)

    def set_axis_change_events(self, event_dict):
        """
        Set multiple callbacks for axis events
        :param event_dict: Event callbacks that should be triggered on axis events: : {axis_id: cb, . . .}
        :type event_dict: dict
        """
        for axis_id, cb in event_dict.items():
            self.set_axis_change_event(axis_id, cb)

    def set_axis_change_event(self, axis_id, cb):
        """
        Set single cb for axis events
        :param axis_id: The axis id. Example PS3C.AXIS_SQUARE
        :type axis_id: int
        :param cb: The callback that should be triggered on a axis event for the given axis id
        :type cb: Callback method or function example: def foo(*args)
        """
        self._add_event_cb(self._axis_callbacks, axis_id, cb)

    def handle_event(self, e):
        """
        Method used to handle a given event and trigger the correct callback
        :param e: The event that should be handled
        :type e: pygame.event
        """
        if e.type == PS4C.EVENT_BUTTON_PRESS:
            self._handle_button_release(e)
        elif e.type == PS4C.EVENT_BUTTON_RELEASE:
            self._handle_button_press(e)
        elif e.type == PS4C.EVENT_AXIS_CHANGE:
            self._handle_axis_event(e)

    @staticmethod
    def _add_event_cb(event_dict, button_id, cb):
        """
        Helper method: adds a new event cb to the given event dict
        """
        event_dict[button_id] = cb

    def _handle_button_press(self, e):
        """
        Helper method: Triggers a on button press cb for the given button down event
        :param e: Pygame.event
        """
        print("Handle button press")
        self._trigger_cb(self._button_release_callbacks, e.button)

    def _handle_button_release(self, e):
        """
        Helper method: Triggers a on button release cb for the given button down event
        :param e: Pygame.event
        """
        self._trigger_cb(self._button_press_callbacks, e.button)

    def _handle_axis_event(self, e):
        """
        Helper method: Triggers a on button release cb for the given button down event
        :param e: Pygame.event
        """
        self._trigger_cb(self._axis_callbacks, e.axis, e.value)

    def _trigger_cb(self, cb_dict, event_id, *args):
        """
        Helper method: Triggers a cb in the given event_cb dictionary if that cb exists
        """
        if not self.disabled:
            try:
                cb_dict[event_id](*args)
            except KeyError:
                pass  # NO Callback registered for this event_id

if __name__ == "__main__":
    # EXAMPLE CODE TO USE THE PS4 JOYSTICK CLASS

    # INIT PYGAME
    pygame.init()
    from pygame import joystick
    pygame.init()
    #if not joystick.get_init():
    joystick.init()
    print("Joystick init()")

    # EXAMPLE CALLBACKS
    def button_down_cb():
        print ("Button down")

    def button_up_cb():
        print ("Button up")

    def axis_cb(value):
        print ("axis:", value)

    # SETUP PS# CONTROLLERS
    ps4_controllers = []
    for joy_id in range(joystick.get_count()):
        js = joystick.Joystick(joy_id)
        print(js.get_name())
        if PS4C.is_ps4_controller(js.get_name()):
            print ("gets here")
            js.init()
            ps4ctrl = PS4C(js)

            # EXAMPLE SET SINGLE CB EVENT
            ps4ctrl.set_button_press_event(BUTTON_CIRCLE, button_down_cb)
            ps4ctrl.set_button_release_event(BUTTON_CIRCLE, button_up_cb)
            ps4ctrl.set_axis_change_event(AXIS_JOYSTICK_R_VER, axis_cb)

            # EXAMPLE SET MULTIPLE CB SAME EVENT TYPE
            ps4ctrl.set_axis_change_events({
                AXIS_JOY_PAD_LEFT: axis_cb,
                AXIS_JOY_PAD_UP: axis_cb,
                AXIS_JOY_PAD_DOWN: axis_cb,
                AXIS_JOY_PAD_RIGHT: axis_cb
            })

            # EXAMPLE SET MULTIPLE EVENTS ALL TYPES
            ps4ctrl.set_events(
                button_press={
                    BUTTON_SQUARE: button_down_cb
                },
                button_release={
                    BUTTON_JOY_PAD_DOWN: button_up_cb
                },
                axis={
                    AXIS_JOY_PAD_RIGHT: axis_cb
                }
            )

            ps4_controllers.append(ps4ctrl)

    # RUN EVENT LOOP
    run = True
    while run:
        for event in pygame.event.get():
            if event.type in [pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYAXISMOTION]:
                for controller in ps4_controllers:
                    if controller.id == event.joy:
                        controller.handle_event(event)