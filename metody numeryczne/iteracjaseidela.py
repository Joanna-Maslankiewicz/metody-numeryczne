"""Klasa realizujaca metode iteracji Seidela"""

import uklad
import math
import numpy as np
from typing import List

class IteracjaSeidela:
  
    def __init__(self, ukl):
        """Konstruktor okreslajacy problem"""
        self.n = ukl.A.shape[0]                   # wymiar macierzy
        self.u = uklad.Uklad(self.n)              # uklad do rozwiazania
        self.u.zadaj_uklad(ukl.A, ukl.B)          # zadaje uklad
        self.X = np.zeros([self.n, 1])            # biezace przyblizenie
        self.Xp = np.zeros([self.n, 1])           # poprzednie przyblizenie
        self.D = np.zeros([self.n, self.n])       # macierz D
        self.C = np.zeros([self.n, 1])            # wektor C
        self.normy: List = []                     # lista norm
        self.kmax = 100000                        # maskymalna liczba iteracji
    
    def przygotuj(self):
        """Metoda wyznaczajaca macierze D oraz wektor C
            na wyjsciu zwracane jest:
            1 - jeżeli mozna zastoswac metode
            0 - jezeli nie mozna zastosowac metody"""
        for i in range(self.n):
            if self.u.A[i, i] == 0:
                # jezeli jest 0, szukam ponizej wiersza z niezerowym elementem
                k = 1
                while (k < self.n):
                    if self.u.A[k, i] == 0:
                        k += 1
                    else:
                        break
                else:
                    # jezeli nie zanaleziono odpowiedniego wiersza
                    # wyswietlany jest komunikat i program zwraca 0
                    print("Dla danego ukladu nie mozna zastosowac iteracji.")
                    return 0
                # jezeli znaleziono odpowiedni wiersz - zamieniamy go z i-tym
                self.u.A[[i, k], :] = self.u.A[[k, i], :]
                self.u.B[[i, k], 0] = self.u.B[[k, i], 0]
            for j in range(self.n):
                self.D[i, j] = -self.u.A[i, j] / self.u.A[i, i]
            self.D[i, i] = 0.0;
            self.C[i, 0] = self.u.B[i, 0] / self.u.A[i, i]
        return 1
        
    def iteruj(self, iteracje, norma, wyswietlaj = 0, X0 = None):
        """Wykonuje zadana liczbe iteracji zaczynajac od wektora X0
            lub jezeli nie jest on podany od wektora C.
            Parametr norma opisany jest w klasie Uklad
            Dodatkowy parametr:
            - wyswietlaj - pozwala wyswietlac poszczegolne iteracje"""
        if X0 is None:
            X0 = self.C.copy()
        self.X = X0.copy()
        self.Xp = X0.copy()
        self.normy.append(self.u.norma_wektora(norma, X0))
        k = 0
        while k < iteracje:
            for i in range(self.n):
                self.X[i] = self.D[i, :]@self.X + self.C[i]
            k += 1
            self.normy.append(self.u.norma_wektora(norma, self.X))
            self.Xp = self.X.copy()
            if wyswietlaj == 1:
                self.wypisz_rozwiazanie(k)               
    
    def iteruj_roznica(self, eps, norma, wyswietlaj = 0, X0 = None):
        """Wykonuje iteracje do momentu, gdy norma roznicy kolejnych
            przyblizen nie jest mniejsza niz eps, zaczynajac od wektora X0
            lub jezeli nie jest on podany od wektora C.
            Metoda zwraca na wyjsciu liczbe wykonanych iteracji lub
            0, jezeli dla podanego ukladu nie mozna zastosowac tej metody
            tzn. gdy liczba iteracji przekroczy ustalona liczbe.
            Parametr norma opisany jest w klasie Uklad
            Dodatkowy parametr:
            - wyswietlaj - pozwala wyswietlac poszczegolne iteracje"""
        if X0 is None:
            X0 = self.C.copy()
        self.X = X0.copy()
        self.Xp = X0.copy()
        self.normy.append(self.u.norma_wektora(norma, X0))
        roznica = 1000.0
        k = 0
        while roznica > eps:
            k += 1
            for i in range(self.n):
                self.X[i] = self.D[i, :]@self.X + self.C[i]
            self.normy.append(self.u.norma_wektora(norma, self.X))
            roznica = self.u.norma_roznicy_wektorow(norma, self.Xp, self.X)
            self.Xp = self.X.copy()
            if wyswietlaj == 1:
                self.wypisz_rozwiazanie(k)
            if k > self.kmax:
                print("Liczba iteracji przekroczyla ustalony limit")
                return 0
        return k
    
    def iteruj_twierdzenie(self, eps, norma, wyswietlaj = 0, X0 = None):
        """Wykonuje liczbe iteracji zgodnie z twierdzeniem,
            zaczynajac od wektora X0 lub jezeli nie jest podany od wektora C.
            Parametr norma opisany jest w klasie Uklad
            Dodatkowy parametr:
            - wyswietlaj - pozwala wyswietlac poszczegolne iteracje
            Metoda zwraca na wyjsciu liczbe wykonanych iteracji lub
            0, jezeli dla podanego ukladu nie mozna zastosowac tej metody"""
        if X0 is None:
            X0 = self.C.copy()
        norma_D = self.u.norma_macierzy(norma, self.D)
        if norma_D < 1:
            self.X = X0.copy()
            self.Xp = X0.copy()
            self.normy.append(self.u.norma_wektora(norma, X0))
            k = 1
            for i in range(self.n):
                self.X[i] = self.D[i, :]@self.X + self.C[i]
            if wyswietlaj == 1:
                self.wypisz_rozwiazanie(k)
            self.normy.append(self.u.norma_wektora(norma, X0))
            norma_dX = self.u.norma_roznicy_wektorow(norma, self.X, self.Xp)
            iteracje = math.log(eps*(1-norma_D)/norma_dX)/math.log(norma_D)-1
            while k < iteracje:
                k += 1
                for i in range(self.n):
                    self.X[i] = self.D[i, :]@self.X + self.C[i]
                self.normy.append(self.u.norma_wektora(norma, self.X))
                self.Xp = self.X.copy()
                if wyswietlaj == 1:
                    self.wypisz_rozwiazanie(k)
            return k
        else:
            print("Nie mozna zastosowac tej metody.")
            return 0
    
    def wypisz_uklad(self):
        """Metoda wyswietlajaca uklad"""
        self.u.wypisz_uklad()
    
    def wypisz_macierze_iteracji(self):
        """Metoda wyswietlajaca macierze D i C"""
        self.u.wypisz_macierze(self.D, self.C)
    
    def wypisz_rozwiazanie(self, iteracja):
        """Metoda wyswietlajaca wektor rozwiazania"""
        print(f"X({iteracja}) = {self.X[:, 0]}")
    
    def wypisz_normy(self):
        """Metoda wypisujaca liste norm"""
        for i in range(len(self.normy)):
            print(f"||X({i})|| = {self.normy[i]}")
            
    def sprawdz_rozwiazanie(self, norma):
        """Metoda sprwadzajaca niedokladnosc rozwiazania"""
        self.u.sprawdz_rozwiazanie(norma, self.X)