"""Klasa, w ktorej mozna zrealizowac rozwiazanie Zadania 2"""

import uklad, wykresy
import iteracjaprosta, iteracjaseidela, pagerank, potegowa
import numpy as np

class Zadanie2:

    def __init__(self):
        """Konstruktor"""
        self.k = 5            # liczba pomiarow dla jednej wartosci parametru
        self.liczba_iteracji = 10
        self.n = 10         # rozmiar macierzy i liczba stron
        self.norma = 1
        
    def testy(self):
        """Testy wstepne"""
        # miejsce na rozwiazanie pierwszej czesci zadania 2
        norma1 = 1
        P = pagerank.PageRank(self.n)
        P.losuj(gamma=0.1)
        print(f"Średnia liczba linków: {P.srednia_liczba_linkow()}")
        P.przygotuj_do_iteracji()
        
        print("Iteracja prosta: ")
        test3 = iteracjaprosta.IteracjaProsta(P.v)
        test3.przygotuj()
        test3.iteruj(iteracje = self.liczba_iteracji, norma = norma1)
        test3.wypisz_rozwiazanie(self.liczba_iteracji)
        niedokl3 = test3.sprawdz_rozwiazanie(norma = norma1)
        
        P.ranking_po_iteracji(test3.X)
        print("Niedokładność: ", niedokl3)
        
        print("Metoda potęgowa: ")
        test2 = potegowa.Potegowa(P.u)
        test2.iteruj(self.liczba_iteracji)
        test2.wypisz_rozwiazanie(self.liczba_iteracji)
        niedokl2 = test2.sprawdz_rozwiazanie(norma = norma1)
        P.ranking(test2.y)
        print("Niedokładność: ", niedokl2)
        
        return 0
        
    def badaj_zbieznosc(self):
        """Badam zbieznosc metody iteracyjnej"""
        # miejsce na realizacje eksperymentu - drugiej czesci zadania 2
        gamma = [0.1, 0.16, 0.22, 0.28, 0.34, 0.4, 0.46, 0.52, 0.58, 0.64, 0.7, 0.76, 0.82]
        
        u1 = uklad.Uklad(wymiar = self.n)
        liczba_iteracji = 10
        sr_niedokladnosc_iteracji = []
        sr_niedokladnosc_metody = []
        
        for g in gamma:
            niedokladnosc_iteracji = 0.0
            niedokladnosc_metody = 0.0
            count = 0
            while count < self.k:
                
                #Page Rank
                pagerank1 = pagerank.PageRank(self.n)
                pagerank1.losuj(g)
                pagerank1.przygotuj_do_iteracji()
                
                #iteracja prosta
                iteracja = iteracjaprosta.IteracjaProsta(pagerank1.v)
                iteracja.przygotuj()
                iteracja.iteruj(liczba_iteracji, self.norma)
                
                niedokl_iter = iteracja.sprawdz_rozwiazanie(self.norma)
                pagerank1.ranking_po_iteracji(iteracja.X)
                
                #metoda potęgowa
                poteg = potegowa.Potegowa(pagerank1.u)
                poteg.iteruj(liczba_iteracji, self.norma)
                
                niedokl_poteg = poteg.sprawdz_rozwiazanie(self.norma)
                pagerank1.ranking(poteg.y)
                
                niedokladnosc_iteracji += niedokl_iter
                niedokladnosc_metody += niedokl_poteg
                count += 1
            
            #średnie
            sr_niedokladnosc_iteracji.append(niedokladnosc_iteracji/self.k)
            sr_niedokladnosc_metody.append(niedokladnosc_metody/self.k)
        
        print("Gamma    Niedokładność")
        print("------"*6)
        for i in range(len(gamma)):
            wyniki_iteracji = f"{gamma[i]} \t"
            wyniki_iteracji += f"{sr_niedokladnosc_iteracji[i]:.6e} \n"
            print(wyniki_iteracji)
            
        print("Gamma    Niedokładność")
        print("------"*6)
        for i in range(len(gamma)):
            wyniki_potegowej = f"{gamma[i]} \t"
            wyniki_potegowej += f"{sr_niedokladnosc_metody[i]:.6e} \n"
            print(wyniki_potegowej)

        return 0

z2 = Zadanie2()
z2.badaj_zbieznosc()