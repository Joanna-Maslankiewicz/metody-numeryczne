"""Klasa realizujaca metode Banchiewicz"""

import uklad
import numpy as np

class Banachiewicz:
  
    def __init__(self, ukl):
        """Konstruktor okreslajacy problem"""
        self.n = ukl.A.shape[0]                      # wymiar macierzy
        self.u = uklad.Uklad(self.n)                 # uklad do rozwiazania
        self.u.zadaj_uklad(ukl.A, ukl.B)             # zadaje uklad
        self.X = np.zeros([self.n, 1])               # wektor rozwiazania
        self.Y = np.zeros([self.n, 1])               # wektor Y
        self.U = np.zeros([self.n, self.n])          # zadaje macierz U
    
    def rozklad(self, wyswietl = 0):
        """Wykonuje rozklad U^TU i zwraca na wyjsciu:
            1 - jezeli uklad mozna rozwiazac metoda Banachiewicza
            0 - jezeli ukladu nie mozna rozwiazac metoda Banachiewicza
            Metoda nie sprawdza, czy uklad jest symetryczny
            Dodatkowy parametr:
            - wyswietl - pozwala wyswietlic rozklad U^TU na koncu"""
        # jezeli w pozycji (0,0) wystepuje 0 konczy program
        if self.u.A[0, 0] == 0:
            print("Ukladu nie mozna rozwiazac metoda Banachiewicza.")
            return 0
        # wpisuje pierwszy wiersz macierzy U
        wsp = pow(self.u.A[0, 0], 0.5)
        self.U[0] = self.u.A[0] / wsp
        # obliczamy kolejne elementy wierszami
        for i in range(1, self.n):
            wsp = self.u.A[i, i]
            for j in range(i):
                wsp -= pow(self.U[j, i], 2)
            if wsp < 0:
                print("Ukladu nie mozna rozwiazac metoda Banachiewicza.")
                return 0
            self.U[i, i] = pow(wsp, 0.5)
            for j in range(i + 1, self.n):
                wsp = self.u.A[i, j]
                for k in range(j):
                    wsp -= self.U[k, i] * self.U[k, j]
                self.U[i, j] = wsp / self.U[i, i]
        # wyswietlamy rozklad
        if wyswietl:
            self.wypisz_rozklad()
        return 1
    
    def rozwiaz_trojkatny_dolny(self):
        """Metoda rozwiazujaca uklad trojkatny dolny"""
        for i in range(self.n):
            suma = self.u.B[i, 0]
            for j in range(i):
                suma = suma - self.U[j, i]*self.Y[j, 0]
            self.Y[i, 0] = suma / self.U[i, i]
    
    def rozwiaz_trojkatny_gorny(self):
        """Metoda rozwiazujaca uklad trojkatny gorny"""
        for i in range(self.n - 1, -1, -1):
            suma = self.Y[i, 0]
            for j in range(i + 1, self.n):
                suma -= self.U[i, j] * self.X[j, 0]
            self.X[i, 0] = suma / self.U[i, i]
    
    def wypisz_uklad(self):
        """Metoda wyswietlajaca uklad"""
        self.u.wypisz_uklad()
    
    def wypisz_rozklad(self):
        """Metoda wyswietlajaca rozklad na L i U"""
        self.u.wypisz_macierze(self.U.transpose(), self.U)

    def wypisz_trojkatny_dolny(self):
        """Metoda wyswietlajaca uklad trojkatny dolny"""
        gorny = uklad.Uklad(self.n)
        gorny.zadaj_uklad(self.U.transpose(), self.u.B)
        gorny.wypisz_uklad()
    
    def wypisz_trojkatny_gorny(self):
        """Metoda wyswietlajaca uklad trojkatny gorny"""
        gorny = uklad.Uklad(self.n)
        gorny.zadaj_uklad(self.U, self.Y)
        gorny.wypisz_uklad()
    
    def wypisz_rozwiazanie(self):
        """Metoda wyswietlajaca wektor rozwiazania"""
        print(f"Wektor rozwiazania: {self.X[:, 0]}")
        
    def sprawdz_rozwiazanie(self, norma):
        """Metoda wyznaczajaca niedokladnosc rozwiazania"""
        self.u.sprawdz_rozwiazanie(norma, self.X)