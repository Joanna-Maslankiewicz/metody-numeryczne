"""Klasa realizujaca metode CholeskY'ego"""

import uklad
import numpy as np

class Cholesky:
  
    def __init__(self, ukl):
        """Konstruktor okreslajacy problem"""
        self.n = ukl.A.shape[0]                      # wymiar macierzy
        self.u = uklad.Uklad(self.n)                 # uklad do rozwiazania
        self.u.zadaj_uklad(ukl.A, ukl.B)             # zadaje uklad
        self.X = np.zeros([self.n, 1])               # wektor rozwiazania
        self.Y = np.zeros([self.n, 1])               # wektor Y
        self.L = np.zeros([self.n, self.n])          # zadaje macierz L
        self.U = np.zeros([self.n, self.n])          # zadaje macierz U
    
    def rozklad(self, wyswietl = 0):
        """Wykonuje rozklad LU (z jedynkami w macierzy U) i zwraca na wyjsciu:
            0 - jezeli uklad mozna rozwiazac metoda Cholesky'ego
            1 - jezeli ukladu nie mozna rozwiazac metoda Cholesky'ego
            Dodatkowy parametr:
            - wyswietl - pozwala wyswietlic rozklad LU na koncu"""
        # sprawdzam, czy w pozycji (0,0) nie wystepuje 0
        if self.u.A[0, 0] == 0:
            # jezeli jest 0, szukam ponizej wiersza z niezerowym elementem
            k = 1
            while (k < self.n):
                if self.u.A[k, 0] == 0:
                    k = k + 1
                else:
                    break;
            else:
                # jezeli nie zanaleziono odpowiedniego wiersza
                # wyswietlany jest komunikat i program zwraca 0
                print("Uklad nie jest oznaczony!")
                return 0
            # jezeli znaleziono odpowiedni wiersz - zamieniamy go z zerowym
            self.u.A[[0, k], :] = self.u.A[[k, 0], :]
            self.u.B[[0, k], 0] = self.u.B[[k, 0], 0]
        # wpisuje pierwszy wiersz macierzy U, element (0,0) macierzy L
        # oraz jedynki w macierzy U
        self.U[0] = self.u.A[0] / self.u.A[0, 0]
        self.L[0, 0] = self.u.A[0, 0]
        for i in range(self.n):
            self.U[i, i] = 1.0
        # obliczamy kolejne elementy wierszami
        for i in range(1, self.n):
            for j in range(i + 1):
                wsp = self.u.A[i, j]
                for k in range(j):
                    wsp -= self.L[i, k] * self.U[k, j]
                self.L[i, j] = wsp
            # jezeli L[i, i] jest zerem, przerywamy algorytm
            # mozna tez probowac przestawic wiersz i-ty z ktoryms z ponizszych
            if self.L[i, i] == 0:
                print("Rozklad nie jest wykonalny.")
                return 0
            for j in range(i + 1, self.n):
                wsp = self.u.A[i, j]
                for k in range(i):
                    wsp -= self.L[i, k] * self.U[k, j]
                self.U[i, j] = wsp / self.L[i, i]
        # wyswietlamy rozklad
        if wyswietl:
            self.wypisz_rozklad()
        return 1
    
    def rozwiaz_trojkatny_dolny(self):
        """Metoda rozwiazujaca uklad trojkatny dolny"""
        for i in range(self.n):
            suma = self.u.B[i, 0]
            for j in range(i):
                suma = suma - self.L[i, j]*self.Y[j, 0]
            self.Y[i, 0] = suma / self.L[i, i]
    
    def rozwiaz_trojkatny_gorny(self):
        """Metoda rozwiazujaca uklad trojkatny gorny"""
        for i in range(self.n - 1, -1, -1):
            suma = self.Y[i, 0]
            for j in range(i + 1, self.n):
                suma -= self.U[i, j] * self.X[j, 0]
            self.X[i, 0] = suma
    
    def wypisz_uklad(self):
        """Metoda wyswietlajaca uklad"""
        self.u.wypisz_uklad()
    
    def wypisz_rozklad(self):
        """Metoda wyswietlajaca rozklad na L i U"""
        self.u.wypisz_macierze(self.L, self.U)

    def wypisz_trojkatny_dolny(self):
        """Metoda wyswietlajaca uklad trojkatny dolny"""
        gorny = uklad.Uklad(self.n)
        gorny.zadaj_uklad(self.L, self.u.B)
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
        """Metoda wyznaczajaca niedkoladnosc rozwiazania"""
        self.u.sprawdz_rozwiazanie(norma, self.X)