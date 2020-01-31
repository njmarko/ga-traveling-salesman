# Author: Marko Njegomir sw-38-2018


class Fitness:
    def __init__(self, putanja):
        self.putanja = putanja
        self.udaljenost = 0
        self.fitness = 0.0

    def duzinaPutanje(self):
        if self.udaljenost == 0:
            duzina_puta = 0
            for i in range(0, len(self.putanja)):
                od_grada = self.putanja[i]
                if i + 1 < len(self.putanja):
                    do_grada = self.putanja[i + 1]
                else:
                    do_grada = self.putanja[0]
                duzina_puta += od_grada.udaljenost(do_grada)
            self.udaljenost = duzina_puta
        return self.udaljenost

    def fitnessPutanje(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.duzinaPutanje())
        return self.fitness
