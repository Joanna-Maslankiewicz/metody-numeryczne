"""Klasa przechowujaca uklad rownan i udostepniajaca uzyteczne metody"""

import numpy as np

class Uklad:
  
    def __init__(self, wymiar=10):
        """Konstruktor okreslajacy uklad"""
        self.n = wymiar            # maksymalny wymiar macierzy ukladu
    
    def losuj_uklad(self):
        """Losowanie ukladu"""
        self.A = np.random.random([self.n, self.n])
        self.B = np.random.random([self.n, 1])
        
    def losuj_uklad_symetryczny_dodatnio_okreslony(self):
        """Losowanie ukladu symetrycznego, dodatnio okreslonego
            z przekatniowa dominacja w kazdym wierszu"""
        C = (np.random.random([self.n, self.n])*2-1)
        D = np.random.random([self.n, 1])      
        self.A = (0.5*(C + C.transpose())).copy()
        for i in range(self.n):
            self.A[i, i] = np.sum(abs(self.A[i, :]))
        self.B = D.copy()
        # Do sprawdzania dodatniej okreslonosci
        # for i in range(self.n):
        #     print(np.linalg.det(self.A[0:(i+1), 0:(i+1)]))
        
    def zadaj_uklad(self, macierz, wektor):
        self.A = macierz.copy()
        self.B = wektor.copy()

    def wypisz_macierz(self, macierz):
        """Wyswietlanie danej macierzy kwadratowej"""
        m = macierz.shape[0]
        print("  ", end=" ")
        print("----------"*(m))
        for i in range(m):
            for j in macierz[i]:
                print(f"{j:10.5f}", end = " ")
            print(" ")

    def wypisz_macierz_ukladu(self):
        """Wyswietlanie macierzy ukladu"""
        self.wypisz_macierz(self.A)
    
    def wypisz_macierze(self, mac1, mac2):
        """Wyswietlanie zadanych macierzy kwadratowych
            macierze musza miec taka sama liczbe wierszy"""
        m = mac1.shape[0]
        k1 = mac1.shape[1]      # liczba kolumn pierwszej macierzy
        k2 = mac2.shape[1]      # liczba kolumn drugiej macierzy
        print(" ", end=" ")
        print("-----------"*(k1 + k2))
        for i in range(m):
            for j in mac1[i]:
                print(f"{j:10.5f}", end = " ")
            print("|", end=" ")
            for j in mac2[i]:
                print(f"{j:10.5f}", end = " ")
            print(" ")
            
    def wypisz_uklad(self):
        """Wyswietlanie ukladu"""
        self.wypisz_macierze(self.A, self.B)
    
    def norma_macierzy(self, typ, macierz=None):
        """Oblicza norme podanej macierzy kwadratowej, przyjmuje parametr typ:
            0 - norma nieskonczonosc (wierszowa)
            1 - norma kolumnowa
            2 - norma Frobeniusa"""
        if macierz is None:
            macierz = self.A.copy()
        norma = 0.0
        n = macierz.shape[0]
        if typ == 0:
            for i in range(n):
                suma = 0.0
                for j in range(n):
                    suma += abs(macierz[i, j])
                    if suma > norma:
                        norma = suma
        elif typ == 1:
            for i in range(n):
                suma = 0.0
                for j in range(n):
                    suma += abs(macierz[j, i])
                    if suma > norma:
                        norma = suma
        elif typ == 2:
            for i in range(n):
                suma = 0.0
                for j in range(n):
                    suma += pow(macierz[i,j],2)
                    if suma > norma:
                        norma = suma
        return norma
    
    def wypisz_normy_macierzy(self, macierz=None):
        """Wyswietla trzy normy macierzy"""
        if macierz is None:
            macierz = self.A.copy()
        print(f"Norma wierszowa: {self.norma_macierzy(0, macierz)}.")
        print(f"Norma kolumnowa: {self.norma_macierzy(1, macierz)}.")
        print(f"Norma Frobeniusa: {self.norma_macierzy(2, macierz)}.")
    
    
    def norma_wektora(self, typ, wektor=None):
        """Oblicza norme podanego wektora, przyjmuje parametr typ:
            0 - norma nieskonczonosc (wierszowa)
            1 - norma kolumnowa
            2 - norma euklidesowa"""
        if wektor is None:
            wektor = self.B.copy()
        norma = 0.0
        n = wektor.shape[0]
        if typ == 0:
            for i in range(n):
                abs_xi = abs(wektor[i, 0])
                if abs_xi > norma:
                    norma = abs_xi
        elif typ == 1:
            for i in range(n):
                norma += abs(wektor[i, 0])
        elif typ == 2:
            suma = 0.0
            for i in range(n):
                suma += pow(wektor[i,0],2)
            norma = pow(suma, 0.5)
        return norma
    
    def wypisz_normy_wektora(self, wektor=None):
        """Wyswietla trzy normy wektora"""
        if wektor is None:
            wektor = self.B.copy()
        print(f"Norma wierszowa: {self.norma_wektora(0, wektor)}.")
        print(f"Norma kolumnowa: {self.norma_wektora(1, wektor)}.")
        print(f"Norma euklidesowa: {self.norma_wektora(2, wektor)}.")
    
    def norma_roznicy_wektorow(self, typ, wektor1, wektor2):
        """Oblicza norme roznicy dwoch wektorow"""
        return self.norma_wektora(typ, wektor1 - wektor2)
        
    def sprawdz_rozwiazanie(self, norma, wektor):
        """Oblicza norme roznicy iloczynu macierzy A i danego wektora
            oraz wektora B"""
        odchyl = self.norma_roznicy_wektorow(norma, self.A@wektor, self.B)
        print(f"Niedokladnosc rozwiazania: {odchyl}")
        return odchyl