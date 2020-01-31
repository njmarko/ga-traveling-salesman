# Author: Marko Njegomir

from math import floor

import matplotlib.pyplot as plt
import numpy as np
import operator
import pandas as pd
import random

from src.model.Fitness import Fitness
from src.model.Grad import Grad


def napraviPutanju(lista_gradova):
    return random.sample(lista_gradova, len(lista_gradova))


def inicijalnaPopulacija(velicina_populacije, lista_gradova):
    pop = []
    for i in range(velicina_populacije):
        pop.append(napraviPutanju(lista_gradova))
    return pop


def rankPutanja(pop):
    fitness_rezultati = {}
    for i in range(len(pop)):
        fitness_rezultati[i] = Fitness(pop[i]).fitnessPutanje()
    return sorted(fitness_rezultati.items(), key=operator.itemgetter(1), reverse=True)


def selection(pop_rangirana, broj_elitnih):
    rezultat_selekcije = []
    df = pd.DataFrame(np.array(pop_rangirana), columns=["Index", "Fitness"])
    df['cumulative_sum'] = df.Fitness.cumsum()
    df['cumulative_perc'] = 100 * df.cumulative_sum / df.Fitness.sum()

    for i in range(0, broj_elitnih):
        rezultat_selekcije.append(pop_rangirana[i][0])
    for i in range(len(pop_rangirana) - broj_elitnih):
        odabrani = 100 * random.random()
        for i in range(len(pop_rangirana)):
            if odabrani <= df.iat[i, 3]:
                rezultat_selekcije.append(pop_rangirana[i][0])
                break
    return rezultat_selekcije


def odabirZaUkrstanje(pop, rezultat_selekcije):
    odabrani = []
    for i in range(len(rezultat_selekcije)):
        odabrani.append(pop[rezultat_selekcije[i]])
    return odabrani


def ukrstanje(roditelj1, roditelj2):
    prvi_deo = []

    gen_a = int(random.random() * len(roditelj1))
    gen_b = int(random.random() * len(roditelj2))

    pocetni_gen = min(gen_a, gen_b)
    krajnji_gen = max(gen_a, gen_b)

    for i in range(pocetni_gen, krajnji_gen):
        prvi_deo.append(roditelj1[i])

    drugi_deo = [gen for gen in roditelj2 if gen not in prvi_deo]
    child = drugi_deo[:pocetni_gen] + prvi_deo + drugi_deo[pocetni_gen:]
    # return prvi_deo + drugi_deo
    return child


def parenjePopulacije(odabrani_za_parenje, broj_elitnih):
    deca = []
    duzina = len(odabrani_za_parenje) - broj_elitnih
    odabir = random.sample(odabrani_za_parenje, len(odabrani_za_parenje))

    for i in range(0, broj_elitnih):
        deca.append(odabrani_za_parenje[i])

    for i in range(duzina):
        deca.append(ukrstanje(odabir[i], odabir[len(odabrani_za_parenje) - 1 - i]))
    return deca


def mutate(putanja, sansa_mutacije):
    for zamenjen in range(len(putanja)):
        if random.random() < sansa_mutacije:
            zameni_sa = int(random.random() * len(putanja))

            putanja[zamenjen], putanja[zameni_sa] = putanja[zameni_sa], putanja[zamenjen]
    return putanja


def mutirajPopulaciju(pop, sansa_mutacije):
    mutirana_pop = []

    for i in range(len(pop)):
        mutirana_pop.append(mutate(pop[i], sansa_mutacije))
    return mutirana_pop


def sledecaGeneracija(trenutna_gen, broj_elitnih, sansa_mutacije):
    rangirana_pop = rankPutanja(trenutna_gen)
    rezultat_selekcije = selection(rangirana_pop, broj_elitnih)
    odabrani_za_ukrstanje = odabirZaUkrstanje(trenutna_gen, rezultat_selekcije)
    deca = parenjePopulacije(odabrani_za_ukrstanje, broj_elitnih)
    sledeca_gen = mutirajPopulaciju(deca, sansa_mutacije)
    return sledeca_gen


def prikaziMapu(lista_gradova, iteracija=None):
    plt.clf()
    # print(lista_gradova)
    prev = Grad(0, 0)
    # plt.suptitle("Problem putujuceg trgovca")
    if iteracija:
        plt.title("Iteracija: " + str(iteracija))
    for i in lista_gradova:
        plt.plot(i.x, i.y, 'ro')
        plt.plot(prev.x, prev.y, 'k-')
        if prev.x == 0 and prev.y == 0:
            prev = i
            plt.plot([prev.x, lista_gradova[-1].x], [prev.y, lista_gradova[-1].y], 'k-')
            continue
        else:
            plt.plot([prev.x, i.x], [prev.y, i.y], 'k-')
            prev = i

    plt.pause(0.0000001)


def genetskiAlgoritam(populacija, velicina_populacije, broj_elitnih, sansa_mutacije, generacije):
    pop = inicijalnaPopulacija(velicina_populacije, populacija)
    print("Inicijalna udaljenost: " + str(1 / rankPutanja(pop)[0][1]))
    interval = floor(generacije * 0.05)  # %generacija koji se prikazuje
    treshold = 50  # prikazi prvih n generacija gde ima mnogo promena a onda idi po intervalima
    for i in range(generacije):
        pop = sledecaGeneracija(pop, broj_elitnih, sansa_mutacije)
        indeks_najbolje_putanje = rankPutanja(pop)[0][0]
        najbolja_putanja = pop[indeks_najbolje_putanje]
        if i < treshold:
            print("ITERACIJA " + str(i))
            prikaziMapu(najbolja_putanja, i)
        elif i < 2 * treshold:
            if i % interval == 0:
                print("ITERACIJA " + str(i))
                prikaziMapu(najbolja_putanja, i)

        elif i % (interval * 2) == 0:
            print("ITERACIJA " + str(i))
            prikaziMapu(najbolja_putanja, i)
    konacna_udaljenost = 1 / rankPutanja(pop)[0][1]
    print("Konacna udaljenost: " + str(konacna_udaljenost))
    indeks_najbolje_putanje = rankPutanja(pop)[0][0]
    najbolja_putanja = pop[indeks_najbolje_putanje]
    prikaziMapu(najbolja_putanja, str(generacije) + "\nDuzina putanje: " + str(konacna_udaljenost))
    # return najbolja_putanja
    return konacna_udaljenost
