"""Klasa, w ktorej mozna zrealizowac rozwiazanie Zadania 1"""

import uklad, wykresy
import iteracjaprosta
import numpy as np

class Zadanie1:

    def __init__(self):
        """Konstruktor"""
        self.k = 10            # liczba pomiarow dla jednej wartosci parametru
        self.norma=1           # norma kolumnowa
        self.eps=1e-05          #parametr stopu
        
    def testy(self):
        
        u1 = uklad.Uklad(wymiar = 100)
        u2 = uklad.Uklad(wymiar = 100)
        # losujemy uklad
        u1.losuj_uklad_symetryczny_dodatnio_okreslony(0.1)
        u2.losuj_uklad_symetryczny_dodatnio_okreslony(0.7)
        # rozwiazuje uklad z wykorzystaniem metody iteracji prostej
        test1 = iteracjaprosta.IteracjaProsta(ukl = u1)
        test2 = iteracjaprosta.IteracjaProsta(ukl = u2)
        # wyznaczam macierz D i wektor C
        test1.przygotuj()
        test2.przygotuj()
        # wyswietlam normy macierzy D
        u1.wypisz_normy_macierzy(macierz = test1.D)
        u2.wypisz_normy_macierzy(macierz = test2.D)
        # wykonuje iteracje do momentu, gdy norma roznicy kolejnych
        # przyblizen jest mniejsza niz eps = 0.0000001
        iter1 = test1.iteruj_roznica(
            eps = self.eps,
            norma = self.norma)
        
        niedokl1 = test1.sprawdz_rozwiazanie(self.norma)
        seria1 = test1.normy.copy()
        test1.wypisz_normy()

        print(f"Liczba iteracji przy alfa = 0.1 - iteruj_roznica: {iter1}")
        print(f"Niedokladnosc rozwiazania: {niedokl1}")

        iter2 = test2.iteruj_roznica(
            eps = self.eps,
            norma = self.norma)
        
        niedokl2 = test2.sprawdz_rozwiazanie(self.norma)
        test2.wypisz_normy()
        seria2 = test2.normy.copy()
        
        
        print(f"Liczba iteracji przy alfa = 0.7 - iteruj_roznica: {iter2}")
        print(f"Niedokladnosc rozwiazania: {niedokl2}")


        # rysuje obie serie na wykresie
        wykres_test = wykresy.Wykresy()
        wykres_test.badaj_zbieznosc(
            tytul = "Zbieznosc metod iteracyjnych",
            opis_OY = "Normy przyblizen",
            dane1 = seria1,
            opis1 = "Iteracja prosta dla alfa = 0.1",
            dane2 = seria2,
            opis2 = "Iteracja prosta dla alfa = 0.7"
        )
        
    def badaj_zbieznosc(self):
        """Badam zbieznosc metody iteracji prostej"""
        # miejsce na realizacje eksperymentu - drugiej czesci zadania 1
        alfa = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]
        sr_liczba_iteracji = []
        sr_norma_macierzy = []
        sr_niedokladnosc = []
        
        for a in alfa:
            norma_macierzy = 0.0
            liczba_iteracji = 0
            niedokladnosc = 0.0
            iteracje = 0
            
            while iteracje < self.k:
                
                u1 = uklad.Uklad(100)
                u1.losuj_uklad_symetryczny_dodatnio_okreslony(a)
                i1 = iteracjaprosta.IteracjaProsta(u1)
                i1.przygotuj()
                norma_D = u1.norma_macierzy(typ = 1, macierz = i1.D)
                iter = i1.iteruj_roznica(eps = 1.0E-5, norma = 1)
                niedokl = i1.sprawdz_rozwiazanie(norma = 1)
                
                if iter == 0:
                    continue
                else:
                    norma_macierzy += norma_D
                    niedokladnosc += niedokl
                    liczba_iteracji += iter
                    iteracje += 1
            
            sr_norma_macierzy.append(norma_macierzy/self.k)
            sr_liczba_iteracji.append(liczba_iteracji/self.k)
            sr_niedokladnosc.append(niedokladnosc/self.k)
            
        print("Alfa \t ||D|| \t     Iteracje   Niedokladnosc")
        print("------"*9)
        for i in range(len(alfa)):
            wyniki = f"{alfa[i]} \t"
            wyniki += f"{sr_norma_macierzy[i]:.6f} \t"
            wyniki += f"{np.ceil(sr_liczba_iteracji[i])} \t"
            wyniki += f"{sr_niedokladnosc[i]:.6e} \n"
            print(wyniki)

        return 0
    
# if __name__ == '__main__':
#     c1 = Zadanie1()
#     c1.testy()

z1 = Zadanie1()
z1.badaj_zbieznosc()
