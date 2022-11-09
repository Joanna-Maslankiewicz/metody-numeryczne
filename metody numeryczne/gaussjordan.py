"""Klasa realizujaca metode Gaussa-Jordana"""

import uklad
import numpy as np

class GaussJordan:
  
    def __init__(self, ukl):
        """Konstruktor okreslajacy problem"""
        self.n = ukl.A.shape[0]                      # wymiar macierzy
        self.u = uklad.Uklad(self.n)                 # uklad do rozwiazania
        self.u.zadaj_uklad(ukl.A, ukl.B)             # zadaje uklad
        self.X = np.zeros([self.n, 1])               # wektor rozwiazania
    
    def eliminacja(self, wyswietlaj = 0):
        """Wykonuje eliminacje Gaussa-Jordana i zwraca na wyjsciu:
            1 - jezeli uklad jest oznaczony
            0 - jezeli uklad nie jest oznaczony
            Dodatkowy parametr:
            - wyswietlaj - pozwala wyswietlac poszczegolne etapy"""
        for i in range(self.n):
            # sprawdzam, czy na przekatnej nie ma zera
            if self.u.A[i, i] == 0:
                # jezeli jest 0, szukam ponizej wiersza z niezerowym elementem
                k = i + 1
                while (k < self.n):
                    if self.u.A[k, i] == 0:
                        k = k + 1
                    else:
                        break
                else:
                    # jezeli nie zanaleziono odpowiedniego wiersza
                    # wyswietlany jest komunikat i program zwraca 0
                    print("Uklad nie jest oznaczony!")
                    return 0
                # jezeli znaleziono odpowiedni wiersz - zamieniamy go z i-tym
                self.u.A[[i, k], :] = self.u.A[[k, i], :]
                self.u.B[[i, k], 0] = self.u.B[[k, i], 0]
            # dzielimy i-ty wiersz przez element przekatnej
            wsp = self.u.A[i, i]
            for j in range(i + 1, self.n):
                self.u.A[i, j] /= wsp
            self.u.B[i, 0] /= wsp
            self.u.A[i, i] = 1.0
            # wykonuje eliminacje elementow w i-tej kolumnie
            for j in range(self.n):
                if j != i:
                    wsp = self.u.A[j, i]
                else:
                    wsp = 0.0
                if wsp != 0:                        
                    for k in range(i, self.n):
                        self.u.A[j, k] -= wsp*self.u.A[i, k]
                    self.u.B[j, 0] -= wsp*self.u.B[i, 0]
            # wyswietlamy kolejne fazy procesu eliminacji
            if wyswietlaj:
                self.u.wypisz_uklad()    
        self.X = self.u.B
        return 1
            
    def wypisz_uklad(self):
        """Metoda wyswietlajaca uklad"""
        self.u.wypisz_uklad()
    
    def wypisz_rozwiazanie(self):
        """Metoda wyswietlajaca wektor rozwiazania"""
        print(f"Wektor rozwiazania: {self.X[:, 0]}")
        
    def sprawdz_rozwiazanie(self, norma):
        """Metoda wyznaczajaca niedkoladnosc rozwiazania"""
        self.u.sprawdz_rozwiazanie(norma, self.X)
