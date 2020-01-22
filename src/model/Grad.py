# Author: Marko Njegomir sw-38-2018
import numpy as np


class Grad:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def udaljenost(self, grad):
        xUdaljenost = abs(self.x - grad.x)
        yUdaljenost = abs(self.y - grad.y)
        return np.sqrt((xUdaljenost ** 2) + (yUdaljenost ** 2))

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
