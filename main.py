# Author: Marko Njegomir

import matplotlib.pyplot as plt
import random

from src import ga
from src.model.Grad import Grad


def main():
    lista_gradova = []

    for i in range(0, 20):
        lista_gradova.append(Grad(x=int(random.random() * 200), y=int(random.random() * 200)))
    najbolji = []
    for i in range(3):
        plt.figure()
        najbolji.append(ga.genetskiAlgoritam(populacija=lista_gradova, velicina_populacije=100, broj_elitnih=10,
                                             sansa_mutacije=0.02,
                                             generacije=400))

    print("\n\n\n\nNajkrace putanje kroz iteracije:")
    for i in range(len(najbolji)):
        print(str(i + 1) + ". Konacna udaljenost: " + str(najbolji[i]))
    plt.show()


if __name__ == '__main__':
    main()
