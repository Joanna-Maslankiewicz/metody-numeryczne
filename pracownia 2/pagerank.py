"""Klasa realizujaca uproszczony algorytm Google PageRank"""

import uklad
import numpy as np
from typing import List

class PageRank:
    
    def __init__(self, nn):
        """Konstruktor okreslajacy liczbe stron"""
        self.n = nn                      # liczba stron
        self.y = np.ones([nn, 1])        # przybl. wektora wlasnego 
        self.u = uklad.Uklad(nn)         # uklad z macierza P
        self.lambdy: List = []           # przybl. dom. wart. wlasnej
        self.srednia = 0.0               # srednia liczba linkow
       
    def losuj(self, gamma = 0.5):
        """Metoda losujaca macierz o zadanym prawdopodobienstwie
            wystapienia linku - gamma - z przedzialu (0, 1)"""
        liczba_linkow = 0.0
        for i in range(self.n):
            # wstawiam jedynki tam, gdzie wystepuje link
            for j in range(self.n):
                los = np.random.random()
                if los < gamma:
                    self.u.A[j, i] = 1.0
                else:
                    self.u.A[j, i] = 0.0
            # zliczam jedynki w kolumnie
            linki = sum(self.u.A[:, i])
            liczba_linkow += linki
            if linki == 0:
                self.u.A[:, i] = 1.0/self.n
            else:
                self.u.A[:, i] *= 1.0/linki
            self.u.B[i] = 1.0
        self.srednia = liczba_linkow/self.n
            
    def przygotuj_do_iteracji(self):
        """Metoda, przeksztalcajaca macierz do macierzy,
            dla ktorej bedzie mozna zastosowac metode iteracyjna
            - odejmuje jedynki na przekatnej
            - usuwam jedno rownanie (domyslnie ostatnie)
            - ustalam jedna ze wspolrzednych (domyslnie ostatnia) na 1.0
            Zwraca na wyjsciu 0, jezeli uklad po powyzszyh operacjach
            nie bedzie sie dalo rozwiazac"""
        blad = 1
        for i in range(self.n):
            if self.u.A[i, i] == 1:
                blad = 0
        self.v = uklad.Uklad(self.n - 1)
        for i in range(self.n - 1):
            self.v.A[i, 1:self.n-1] = self.u.A[i, 1:self.n-1]
            self.v.A[i, i] -= 1.0;
            self.v.B[i] = -self.u.A[i, self.n-1]
        return blad

    def ranking(self, wektor):
        """Tworzenie rankingu stron dla podanego wektora wag"""
        m = len(wektor)
        # tworze tablice indeksow
        ind = np.arange(1,m+1)
        # sortuje przez wybieranie - malejaco
        for i in range(m-1):
            w_max = wektor[i]
            k = i
            for j in range(i+1, m):
                if wektor[j] > w_max:
                    k = j
                    w_max = wektor[j]
            wektor[k], wektor[i] = wektor[i], wektor[k]
            ind[k], ind[i] = ind[i], ind[k]
        print(ind)
        
    def ranking_po_iteracji(self, wektor):
        """Tworzenie rankingu stron dla podanego wektora wag
            uzyskanego metoda iteracji prostej lub Seidela"""
        m = len(wektor)
        wektor1 = []
        for i in range(m):
            wektor1.append(wektor[i])
        wektor1.append(1.0)
        self.ranking(wektor1)

    def wypisz_macierz(self):
        """Metoda wyswietlajaca macierz P"""
        self.u.wypisz_macierz_ukladu()
        
    def srednia_liczba_linkow(self):
        """Metoda wyznaczajaca srednia liczbe linkow"""
        return self.srednia