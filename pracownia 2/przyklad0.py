"""Przyklady sluzace porownaniu metod iteracyjnych"""

import uklad, wykresy
import iteracjaprosta, iteracjaseidela
import numpy as np

class Przyklad0:

    def __init__(self, wymiar = 100):
        """Konstruktor"""
        self.n = wymiar       # wymiar macierzy
        self.norma = 0        # bede wykorzystywal norme wierszowa
        
    def porownaj(self, typ):
        if typ == 1:
            # porownuje metode iteruj_roznica i iteruj_twierdzenie
            u1 = uklad.Uklad(wymiar = self.n)
            # losujemy uklad
            u1.losuj_uklad_symetryczny_dodatnio_okreslony()
            # rozwiazuje uklad z wykorzystaniem metody iteracji prostej
            test1 = iteracjaprosta.IteracjaProsta(ukl = u1)
            test2 = iteracjaprosta.IteracjaProsta(ukl = u1)
            # wyznaczam macierz D i wektor C
            test1.przygotuj()
            test2.przygotuj()
            # wyswietlam normy macierzy D
            u1.wypisz_normy_macierzy(macierz = test1.D)
            # wykonuje iteracje do momentu, gdy norma roznicy kolejnych
            # przyblizen jest mniejsza niz eps = 0.0000001
            iter1 = test1.iteruj_roznica(
                eps = 1e-7,
                norma = self.norma)
            test1.wypisz_normy()
            niedokl1 = test1.sprawdz_rozwiazanie(self.norma)
            # wykorzystuje twierdzenie do obliczenia liczby iteracji
            iter2 = test2.iteruj_twierdzenie(
                eps = 1e-7,
                norma = self.norma)
            test2.wypisz_normy()
            niedokl2 = test2.sprawdz_rozwiazanie(self.norma)
            print(f"Liczba iteracji - iteruj_roznica: {iter1}")
            print(f"Niedokladnosc rozwiazania: {niedokl1}")
            print(f"Liczba iteracji - iteruj_twierdzenie: {iter2}")
            print(f"Niedokladnosc rozwiazania: {niedokl2}")
        elif typ == 2:
            # porownuje metode iteracji prostej i Seidela
            u1 = uklad.Uklad(wymiar = self.n)
            # losujemy uklad
            u1.losuj_uklad_symetryczny_dodatnio_okreslony()
            # rozwiazuje uklad z wykorzystaniem metody iteracyjnych
            test1 = iteracjaprosta.IteracjaProsta(ukl = u1)
            test3 = iteracjaseidela.IteracjaSeidela(ukl = u1)
            # wyznaczam macierz D i wektor C
            test1.przygotuj()
            test3.przygotuj()
            # wyswietlam normy macierzy D
            u1.wypisz_normy_macierzy(macierz = test1.D)
            # iteracja prosta
            iter1 = test1.iteruj_roznica(
                eps = 1e-16,
                norma = self.norma)
            seria1 = test1.normy.copy()
            test1.wypisz_normy()
            niedokl1 = test1.sprawdz_rozwiazanie(self.norma)
            print(f"Liczba iteracji - iteracja prosta: {iter1}")
            print(f"Niedokladnosc rozwiazania: {niedokl1}")
            # iteracja Seidela
            iter3 = test3.iteruj_roznica(
                eps = 1e-16,
                norma = self.norma)
            seria3 = test3.normy.copy()
            test3.wypisz_normy()
            niedokl3 = test3.sprawdz_rozwiazanie(self.norma)
            print(f"Liczba iteracji - iteracja Seidela: {iter3}")
            print(f"Niedokladnosc rozwiazania: {niedokl3}")
            # rysuje obie serie na wykresie
            wykres_test = wykresy.Wykresy()
            wykres_test.badaj_zbieznosc(
                tytul = "Zbieznosc metod iteracyjnych",
                opis_OY = "Normy przyblizen",
                dane1 = seria1,
                opis1 = "Iteracja prosta",
                dane2 = seria3,
                opis2 = "Iteracja Seidela"
            )
        
    def badaj_zbieznosc(self, typ, iteracje):
        """Zbieznosc/rozbieznosc metod iteracyjnych dla roznych macierzy"""
        u1 = uklad.Uklad(wymiar = self.n)
        # zadaje macierze z zadania 3.1
        if typ == 1:
            # macierz A1 - przekątniowo dominująca
            A1 = np.array([
                [0.7, 0.3, 0.2],
                [0.4, 0.9, 0.3],
                [0.0, 0.5, 0.7]])
        elif typ == 2:
            # macierz A2 - symteryczna, dodatnio określona
            A1 = np.array([
                [3.0, 0.0, -5.0],
                [0.0, 8.0, 2.0],
                [-5.0, 2.0, 9.0]])               
        elif typ == 3:
            # macierz A3 - dla ktorej zaden z WW nie byl spelniony
            A1 = np.array([
                [0.1, 1.0, 0.0],
                [0.0, 0.9, 1.0],
                [0.0, 0.0, 0.3]])
        elif typ == 4:
            # macierz slabo przekatniowo dominujaca
            A1 = np.array([
                [10.0, 5.0, 5.0],
                [1.0, 2.001, 1.0],
                [5.0, 5.0, 10.0]])
        elif typ == 5:
            # macierz z zadania 3.4
            A1 = np.array([
                [3.0, 2.0, 7.0],
                [1.0, -1.0, 1.0],
                [7.0, 1.0, -4.0]])
        # zadaje wektor B1
        B1 = np.array([[1.0, 1.0, 1.0]]).transpose()
        # zadaje uklad o macierzy A1 i wektorze B1
        u1.zadaj_uklad(macierz = A1, wektor = B1)
        u1.wypisz_uklad()
        # rozwiazuje uklad z wykorzystaniem metody iteracji prostej
        test1 = iteracjaprosta.IteracjaProsta(ukl = u1)
        test2 = iteracjaseidela.IteracjaSeidela(ukl = u1)
        # wyznaczam macierz D i wektor C
        test1.przygotuj()
        test2.przygotuj()
        # wyswietlam normy macierzy D
        u1.wypisz_normy_macierzy(macierz = test1.D)
        # iteracja prosta
        test1.iteruj(
            iteracje = iteracje,
            norma = self.norma)
        seria1 = test1.normy.copy()
        niedokl1 = test1.sprawdz_rozwiazanie(self.norma)
        print(f"Niedokladnosc rozwiazania - iteracja prosta: {niedokl1}")
        # iteracja Seidela
        test2.iteruj(
            iteracje = iteracje,
            norma = self.norma)
        seria2 = test2.normy.copy()
        niedokl2 = test2.sprawdz_rozwiazanie(self.norma)
        print(f"Niedokladnosc rozwiazania - iteracja Seidela: {niedokl2}")
        # rysuje obie serie na wykresie
        wykres_test = wykresy.Wykresy()
        wykres_test.badaj_zbieznosc(
            tytul = "Zbieznosc metod iteracyjnych",
            opis_OY = "Normy przyblizen",
            dane1 = seria1,
            opis1 = "Iteracja prosta",
            dane2 = seria2,
            opis2 = "Iteracja Seidela"
        )