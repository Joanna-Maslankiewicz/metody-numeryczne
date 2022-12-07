"""Klasa realizujaca metode potegowa"""

import uklad
import numpy as np
from typing import List

class Potegowa:
  
    def __init__(self, ukl):
        """Konstruktor okreslajacy problem"""
        self.n = ukl.A.shape[0]                  # wymiar macierzy
        self.u = uklad.Uklad(self.n)             # uklad z macierza A
        self.u.zadaj_uklad(ukl.A, ukl.B)         # zadaje uklad
        self.y = np.ones([self.n, 1])            # przybl. wektora wlasnego 
        self.y1 = np.ones([self.n, 1])           # nast. przybl. w. wlasnego
        self.lambdy: List = []                   # przybl. dom. wart. wlasnej
        self.kmax = 100000                       # maskymalna liczba iteracji

    def iteruj(self, iteracje, wyswietlaj = 0, y0 = None):
        """Wykonuje zadana liczbe iteracji zaczynajac od wektora y0
            lub jezeli nie jest on podany od wektora jedynek.
            Metoda zwraca na wyjsciu liczbe wykonanych iteracji lub
            0, jezeli dla macierzy nie mozna zastosowac tej metody
            tzn. wystapi dzielenie przez 0.
            Dodatkowy parametr:
            - wyswietlaj - pozwala wyswietlac poszczegolne iteracje"""
        if y0 is not None:
            self.y1 = y0.copy()
        # resetujemy liste norm
        self.lambdy = []
        k = 0      
        while (k < iteracje):
            self.y = self.y1.copy()
            k += 1
            self.y1 = self.u.A @ self.y
            lam = 0.0
            for i in range(self.n):
                mian = self.y[i]
                if mian == 0:
                    print("Blad dzielenia przez 0")
                    print("Sprobuj podac inny wektor poczatkowy")
                    return 0
                lam += self.y1[i]/mian
            lam /= self.n
            self.lambdy.append(lam)
            if wyswietlaj:
                self.wypisz_rozwiazanie(k)
        return k

    def iteruj_roznica(self, eps, wyswietlaj = 0, normalizacja = 0, y0 = None):
        """Wykonuje iteracje do momentu, gdy norma roznicy kolejnych
            przyblizen nie jest mniejsza niz eps, zaczynajac od wektora y0
            lub jezeli nie jest on podany od wektora jedynek.
            Metoda zwraca na wyjsciu liczbe wykonanych iteracji lub
            0, jezeli dla macierzy nie mozna zastosowac tej metody
            tzn. gdy liczba iteracji przekroczy ustalona liczbe lub
            wystapi dzielenie przez 0.
            Dodatkowy parametr:
            - wyswietlaj - pozwala wyswietlac poszczegolne iteracje
            - normalizacja - pozwala uniknąć rozbieżności metody"""
        if y0 is not None:
            self.y1 = y0.copy()
        # resetujemy liste norm
        self.lambdy = []
        k = 0
        roznica = 1000.0
        while (roznica > eps):
            self.y = self.y1.copy()
            self.y1 = self.u.A @ self.y
            if normalizacja == 1:
                skala = pow(self.y.transpose() @ self.y, 0.5)
                self.y /= skala
                self.y1 = self.u.A @ self.y
                lam = self.y1.transpose() @ self.y
            else:
                self.y1 = self.u.A @ self.y
                lam = 0.0
                for i in range(self.n):
                    mian = self.y[i]
                    if mian == 0:
                        print("Blad dzielenia przez 0")
                        print("Sprobuj podac inny wektor poczatkowy")
                        return 0
                    lam += self.y1[i]/mian
                lam /= self.n
            self.lambdy.append(lam)
            if k > 0:
                roznica = abs(self.lambdy[k]-self.lambdy[k-1])
            k += 1
            if wyswietlaj:
                print(k, lam)
                # self.wypisz_rozwiazanie(k)
            if k > self.kmax:
                print("Liczba iteracji przekroczyla ustalony limit")
                return 0
        return k
        
    def wypisz_macierz(self):
        """Metoda wyswietlajaca macierz A"""
        self.u.wypisz_macierz_ukladu()
            
    def wypisz_rozwiazanie(self, iter, normalizacja = 0, norma = 2):
        """Metoda wyswietlajaca aktualna iteracje
            - normalizacja - parametr pozwalajacy wyswietlic
            unormowany wektor wlasny (domyslnie norma 2)"""
        lam = self.lambdy[iter-1]
        if normalizacja == 1:
            skala = self.u.norma_wektora(typ = norma, wektor = self.y)
            y_norm = self.y / skala
            print(f"l({iter}) = {lam}, \t y({iter}) = {y_norm[:, 0]}")
        else:
            print(f"l({iter}) = {lam}, \t y({iter}) = {self.y[:, 0]}")
    
    def sprawdz_rozwiazanie(self, norma):
        """Metoda sprwadzajaca wzgledna niedokladnosc rozwiazania"""
        odchyl = self.u.norma_roznicy_wektorow(
            norma,
            self.u.A@self.y,
            self.y*self.lambdy[-1]
        )
        odchyl /= self.u.norma_wektora(norma, self.y)
        print(f"Wzgledna niedokladnosc rozwiazania: {odchyl}")
        return odchyl
