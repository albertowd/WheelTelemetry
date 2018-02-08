
"""
Module to update one wheel infos from car and draw on screen.
"""
from wconfig import Config
from wcomponents import BoxComponent, Brake, Camber, Dirt, Height, Load, Temps, Suspension, TyreAndPsi, Wear
from wsim_info import info
import ac
import acsys


class Data(object):

    def __init__(self):
        self.brake_t = 0.0
        self.camber = 0.0
        self.height = 0.0
        self.susp_t = 0.0
        self.tyre_d = 0.0
        self.tyre_l = 0.0
        self.tyre_p = 0.0
        self.tyre_t_i = 0.0
        self.tyre_t_m = 0.0
        self.tyre_t_o = 0.0
        self.tyre_w = 0.0

    def update(self, index, info):
        self.brake_t = info.physics.brakeTemp[index]
        self.camber = info.physics.camberRAD[index]

        # um to mm
        self.height = info.physics.rideHeight[int(index / 2)] * 1000.0

        max_travel = info.static.suspensionMaxTravel[index]
        max_travel = max_travel if max_travel > 0.0 else 1.0
        self.susp_t = info.physics.suspensionTravel[index] / max_travel
        self.tyre_d = info.physics.tyreDirtyLevel[index] * 4.0

        # N to (5*kgf)
        self.tyre_l = info.physics.wheelLoad[index] / (5.0 * 9.80665)
        self.tyre_p = info.physics.wheelsPressure[index]
        self.tyre_t_i = info.physics.tyreTempI[index]
        self.tyre_t_m = info.physics.tyreTempM[index]
        self.tyre_t_o = info.physics.tyreTempO[index]

        # Normal to percent
        self.tyre_w = info.physics.tyreWear[index] / 100.0


class Info(object):
    """ Wheel info to draw and update each tyre. """

    indexes = {0: "FL", 1: "FR", 2: "RL", 3: "RR"}
    names = {"FL": 0, "FR": 1, "RL": 2, "RR": 3}

    def __init__(self, wheel_index):
        """ Default constructor receive the index of the wheel it will draw info. """
        configs = Config()

        self.__id = Info.indexes[wheel_index]
        self.__active = False
        self.__data = Data()
        self.__index = wheel_index
        self.__info = info
        self.__is_left = wheel_index is 0 or wheel_index is 2
        self.__window_id = ac.newApp("Wheel Telemetry {}".format(self.__id))
        ac.drawBorder(self.__window_id, 0)
        ac.drawBackground(self.__window_id, 0)
        ac.setIconPosition(self.__window_id, 0, -10000)
        ac.setTitle(self.__window_id, "")

        pos_x = configs.get_x(self.__id)
        pos_y = configs.get_y(self.__id)
        ac.setPosition(self.__window_id, pos_x, pos_y)

        resolution = configs.get_resolution()
        mult = BoxComponent.resolution_map[resolution]
        ac.setSize(self.__window_id, 512 * mult, 256 * mult)

        self.__bt_resolution = ac.addButton(self.__window_id, resolution)
        ac.setSize(self.__bt_resolution, 50, 30)
        ac.setFontAlignment(self.__bt_resolution, "center")

        self.__components = []
        self.__components.append(
            Temps(resolution, self.__id, self.__window_id))
        self.__components.append(Dirt(resolution))
        self.__components.append(TyreAndPsi(resolution, self.__window_id))

        self.__components.append(
            Brake(resolution, self.__id, self.__window_id))
        self.__components.append(Camber(resolution, self.__id))
        self.__components.append(Suspension(resolution, self.__id))
        self.__components.append(
            Height(resolution, self.__id, self.__window_id))
        self.__components.append(Wear(resolution, self.__id))
        self.__components.append(Load(resolution))

        self.set_active(configs.is_active(self.__id))

    def get_id(self):
        """ Returns the whhel id. """
        return self.__id

    def get_position(self):
        """ Returns the window position. """
        return ac.getPosition(self.__window_id)

    def get_button_id(self):
        """ Returns the resolution button id. """
        return self.__bt_resolution

    def get_window_id(self):
        """ Returns the window id. """
        return self.__window_id

    def is_active(self):
        """ Returns window status. """
        return self.__active

    def draw(self):
        """ Draws all info on screen. """
        ac.setBackgroundOpacity(self.__window_id, 0)
        for component in self.__components:
            component.draw(self.__data)

    def resize(self, resolution):
        """ Resizes the window. """
        ac.setText(self.__bt_resolution, resolution)
        for component in self.__components:
            component.resize(resolution)

    def set_active(self, active):
        """ Toggles the window status. """
        self.__active = active

    def update(self):
        """ Updates the wheel infos. """
        self.__data.update(self.__index, self.__info)
