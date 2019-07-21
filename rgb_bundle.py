from myhdl import *

class rgb_bundle:
    def __init__(self):
        self.red=Signal(bool(0))
        self.green=Signal(bool(0))
        self.blue=Signal(bool(0))
