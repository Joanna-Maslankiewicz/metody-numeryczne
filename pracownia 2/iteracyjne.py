"""Klasa zawierajac trzy metody:
    - badaj_zbieznosc - bada zbieznosc wybranej metody
    - wartosc_wlasna - wyznacza dominujaca wartosc wlasna metoda potegowa
    - page_rank_iteracja - zastsowanie met. Seidela do wyznaczenia rankingu"""

import uklad, wykresy
import iteracjaprosta, iteracjaseidela, potegowa, pagerank

class Iteracyjne:

    def __init__(self, nn):
        """Konstruktor okreslajacy problem"""
        self.n = nn                  # maksymalny wymiar macierzy
        
    
    def badaj_zbieznosc(self):
        """Badam zbieznosc wybranej metody"""
        norma0 = 0
        u1 = uklad.Uklad(wymiar = self.n)
        # losujemy uklad z parametrem alfa z przedzialu (0, 1) -
        # - im wieksza alfa, tym mniejsza norma macierzy
        u1.losuj_uklad_symetryczny_dodatnio_okreslony(alfa = 0.2)
        # rozwiazuje uklad z wykorzystaniem metody iteracji prostej
        test1 = iteracjaprosta.IteracjaProsta(ukl = u1)
        # wyznaczam macierz D i wektor C
        test1.przygotuj()
        # wyswietlam norma macierzy D
        norma_D = u1.norma_macierzy(typ = norma0, macierz = test1.D)
        print(f"Norma macierzy D: {norma_D}")
        # wykonuje iteracje do momentu, gdy norma roznicy kolejnych
        # przyblizen jest mniejsza niz eps = 0.0000001
        test1.iteruj_roznica(eps = 1e-7, norma = norma0)
        test1.wypisz_normy()
        # tworze wykres obrazujacy zbieznosc - rysuje normy wektorow
        wykres1 = wykresy.Wykresy()
        wykres1.badaj_zbieznosc(
            tytul = "Zbieznosc ciagu norm",
            opis_OY = "Norma przyblizenia",
            dane1 = test1.normy,
            opis1 = "Iteracja prosta"
        )
        
    def wartosc_wlasna(self):
        # zadaje uklad
        u2 = uklad.Uklad(wymiar = self.n)
        u2.losuj_uklad()
        test2 = potegowa.Potegowa(u2)
        # wykonuje iteracje do momentu, gdy kolejne dwa przyblizenia
        # wartosci wlasnej roznia się o mniej niz 1e-10
        # zapisuje liczbe iteracji do zmiennej iteracje
        iteracje = test2.iteruj_roznica(eps = 1e-15, wyswietlaj = 1)
        wykres2 = wykresy.Wykresy()
        wykres2.badaj_zbieznosc(
            tytul = "Metoda potegowa",
            opis_OY = "Przyblizenia wartosci wlasnej",
            dane1 = test2.lambdy,
            opis1 = "Przyblizenia wartosci wlasnej"
        )
        test2.wypisz_rozwiazanie(iter = iteracje, normalizacja = 1)
        
    def page_rank_iteracja(self):
        # ustalam norme
        norma1 = 1
        # okreslam liczbe iteracji
        iter = 50
        # zadaje uklad o rozmiarze n
        P = pagerank.PageRank(self.n)
        # losuje macierz przejscia podajac parametr gamma
        P.losuj(0.4)
        # wyswietlam srednia liczbe linkow
        print(f"Srednia liczba linkow: {P.srednia_liczba_linkow()}")
        # rozwiazuje problem metoda iteracji Seidela
        P.przygotuj_do_iteracji()
        # tworze obiekt klasy IteracjaSeidela i przekazuje tam
        # zmodyfikowany uklad - v
        test3 = iteracjaseidela.IteracjaSeidela(P.v)
        test3.przygotuj()
        # wykonuje zadana liczbe iteracji
        test3.iteruj(iteracje = iter, norma = norma1)
        # wypisuje rozwiazanie - wektor wlasny bez ostatniej wspolrzednej
        test3.wypisz_rozwiazanie(iter)
        # sprwadzam jego niedokladnosc
        test3.sprawdz_rozwiazanie(norma = norma1)
        # wyswietlam ranking stron
        P.ranking_po_iteracji(test3.X)