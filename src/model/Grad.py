# Author: Marko Njegomir sw-38-2018
import numpy as np


class Grad:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def udaljenost(self, grad):
        x_udaljenost = abs(self.x - grad.x)
        y_udaljenost = abs(self.y - grad.y)
        return np.sqrt((x_udaljenost ** 2) + (y_udaljenost ** 2))

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
