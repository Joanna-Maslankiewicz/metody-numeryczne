"""Klasa, w ktorej mozna zrealizowac rozwiazanie Zadania 1"""

import uklad, wykresy
import iteracjaprosta, iteracjaseidela
import numpy as np

class Zadanie1:

    def __init__(self):
        """Konstruktor"""
        self.k = 5          # liczba pomiarow dla jednej wartosci parametru
        
    def testy(self):
        """Testy wstepne"""
        # miejsce na rozwiazanie pierwszej czesci zadania 1
        # alfa = [0.3, 0.9]
        # alfa = [0.3, 0.6, 0.9]
        alfa = [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9]
        eps = 1.0E-5
        norma = 1

        for a in alfa:
            u1 = uklad.Uklad(100)
            u1.losuj_uklad_symetryczny_dodatnio_okreslony(a)

            i1 = iteracjaprosta.IteracjaProsta(u1)
            i1.przygotuj()
            i1.iteruj_twierdzenie(eps, norma, 1)
        
        return 0
        
    def badaj_zbieznosc(self):
        """Badam zbieznosc metody iteracyjnej"""
        # miejsce na realizacje eksperymentu - drugiej czesci zadania 1
        u1 = uklad.Uklad(wymiar = self.n)
        

        return 0

z1 = Zadanie1()
z1.testy()