import time
from .controllable import ControllableSphero
from ps4_controller import manager
#import tracker
from sphero_mini import sphero_mini
from tracker import trackerbase
from ps4_controller import constants


class SpheroMiniPS4Controls(object):
    def __init__(self):
        super(SpheroMiniPS4Controls, self).__init__()
        self._ps4_manager = manager.PS4manager()

        # self._tracker = trackerbase.ColorTracker()

        self._controllable_devices = []

    #     self._init_sphero_manager()

    # def _init_sphero_manager(self):
    #     self._sphero_manager.set_sphero_found_cb(self.on_new_sphero)

    def run(self, hwaddr):
        
        # connect to peripheral
        sphero = sphero_mini.sphero_mini(hwaddr, verbosity = 1)
        self.on_new_sphero(sphero)
        while True:
            pass
        # while True:
        #     pass
        # while True:
        #     traceable_objects = []
        #     for controllable in self._controllable_devices:
        #         traceable_objects.append(controllable)

        #     if len(traceable_objects) > 1:
        #         if traceable_objects[0].pos:
        #             traceable_objects[1].dot_pos = traceable_objects[0].pos

        #     self._tracker.track_objects(traceable_objects)
        #     time.sleep(1.0 / 25.0)

    @staticmethod
    def set_tracking_filter(controllable_sphero, device):
        if device.bt_name == "Sphero-YGY":
            controllable_sphero.filter = tracker.FilterSpheroBlueCover()
            print ("SAME SPHERO")

        elif device.bt_name == "Sphero-ORB":
            controllable_sphero.filter = tracker.FilterGlow()

        elif device.bt_name == "Sphero-RWO":
            controllable_sphero.filter = tracker.FilterSpheroYellowCover()

        else:
            print (device.bt_name)

    def on_new_sphero(self, device):
        """
        Callback when new spheros are found
        :param device:
        :type device: sphero_mini
        """
        print ("NEW Sphero")

        # if device.connect():
        controllable_sphero = ControllableSphero(device)
        controllable_sphero.set_sphero_disconnected_cb(self.clean_up_sphero_dev)

        ps4_ctrl = self._ps4_manager.get_available_controller()

        if ps4_ctrl:
            controllable_sphero.set_ps4_controller(ps4_ctrl)

        else:
            print ("No free PS4 controller available")

        # self.set_tracking_filter(controllable_sphero, device)

        self._controllable_devices.append(controllable_sphero)
        self._ps4_manager.start()
        return

        # self.clean_up_sphero_dev(device)

    def clean_up_sphero_dev(self, device):
        #device.disconnect()
        try:
            print (device, self._controllable_devices)
            for controllable in self._controllable_devices:
                if controllable.device == device:
                    self._controllable_devices.remove(controllable)
                    break

            else:
                print( "NOT FOUND")
        except ValueError:
            print ("could not remove sphero")
            pass
        #self._sphero_manager.remove_sphero(device)


# if __name__ == "__main__":
#     sphero_ps4 = SpheroPS4Controls()
#     sphero_ps4.run()
