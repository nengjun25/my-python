
# Filename: pad.py

class Pad:
    def __init__(self, interface, name):
        self._name = name
        self.XC = None
        self.XI = None
        self.IE = None
        self.OEN = None
        self.PU = None
        self.PD = None
        self.ST = None
        self.DS0 = None
        self.DS1 = None
        self.DS2 = None
        self._interface = interface

    def get_name(self):
        return self._name

    def get_interface(self):
        return self._interface


class TestMode:
    def __init__(self, name):
        self.pad_list = []
        self.name = name
        self.var_name = None
