#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module to load and save app options.

@author: albertowd
"""

import configparser
import os


class Config(object):
    """ Singleton to handle configuration methods. """

    __configs = configparser.ConfigParser()

    def __init__(self):
        self.load_config()

    def load_config(self):
        """ Loads or creates the app configuration file. """
        if os.path.isfile("apps/python/LiveTelemetry/cfg.ini"):
            Config.__configs.read("apps/python/LiveTelemetry/cfg.ini")
        else:
            Config.__configs["Windows"] = { "Engine": "False", "FL": "False", "FR": "False", "RL": "False", "RR": "False", "SIZE": "HD"}
            Config.__configs["Positions"] = { "Engine_x": "384", "Engine_y": "104", "FL_x": "100", "FL_y": "100", "FR_x": "668", "FR_y": "100", "RL_x": "100", "RL_y": "364", "RR_x": "668", "RR_y": "364"}

    def get_engine_x(self):
        """ Returns the x position of the engine window. """
        return float(self.get_str("Positions", "Engine_x"))

    def get_engine_y(self):
        """ Returns the y position of the engine window. """
        return float(self.get_str("Positions", "Engine_y"))

    def get_resolution(self):
        """ Returns the windows resolution. """
        return self.get_str("Windows", "SIZE")

    def get_str(self, section, option):
        """ Returns an option. """
        return Config.__configs.get(section, option)

    def get_x(self, wheel_id):
        """ Returns the x position of window. """
        return float(self.get_str("Positions", "{}_x".format(wheel_id)))

    def get_y(self, wheel_id):
        """ Returns the y position of window. """
        return float(self.get_str("Positions", "{}_y".format(wheel_id)))

    def is_active(self, wheel_id):
        """ Returns if window is active. """
        return bool(self.get_str("Windows", wheel_id))
    
    def is_engine_active(self):
        """ Returns if engine window is active. """
        return bool(self.get_str("Windows", "Engine"))

    def save_config(self):
        """ Writes the actual options on the configuration file. """
        cfg_file = open("apps/python/LiveTelemetry/cfg.ini", 'w')
        Config.__configs.write(cfg_file)
        cfg_file.close()

    def set_active(self, wheel_id, active):
        """ Updates if window is active. """
        self.set_str("Windows", wheel_id, str(active))
    
    def set_engine_active(self, active):
        """ Updates if engine window is active. """
        self.set_str("Windows", "Engine", str(active))

    def set_engine_position(self, pos_x, pos_y):
        """ Updates engine window position. """
        self.set_str("Positions", "Engine_x", str(pos_x))
        self.set_str("Positions", "Engine_y", str(pos_y))

    def set_position(self, wheel_id, pos_x, pos_y):
        """ Updates window position. """
        self.set_str("Positions", "{}_x".format(wheel_id), str(pos_x))
        self.set_str("Positions", "{}_y".format(wheel_id), str(pos_y))

    def set_str(self, section, option, value):
        """ Updates an option. """
        Config.__configs.set(section, option, value)
