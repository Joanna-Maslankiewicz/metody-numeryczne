"""Przyklad badania zbieznosci metody iteracji prostej w zaleznosci
    w zaleznosci od wybranego wektora poczatkowego"""

import uklad, wykresy
import iteracjaprosta
import numpy as np

class Zadanie:

    def __init__(self, sk = 1):
        """Konstruktor okreslajacy skale wektora poczatkowego"""
        self.skala = sk       # parametr skali
        self.n = 100          # wymiar macierzy
        self.norma = 1        # bede wykorzystywal norme kolumnowa
        self.k = 5            # liczba pomiarow dla jednej wartosci parametru
        
    def testy(self):
        """Testy wstepne"""
        # przeprowadzam dwa testowe eksperymenty dla wektorow o roznych normach
        # okreslam uklad rownan
        u1 = uklad.Uklad(wymiar = self.n)
        # losujemy uklad
        u1.losuj_uklad_symetryczny_dodatnio_okreslony()
        # rozwiazuje uklad z wykorzystaniem metody iteracji prostej
        test1 = iteracjaprosta.IteracjaProsta(ukl = u1)
        # wyznaczam macierz D i wektor C
        test1.przygotuj()
        # wyswietlam normy macierzy D
        u1.wypisz_normy_macierzy(macierz = test1.D)
        # losuje wektor poczatkowy
        wek = np.random.random([self.n, 1])
        # obliczam norme tego wektora
        norma_wek = u1.norma_wektora(typ = self.norma, wektor = wek)
        # skaluje wylosowany wektor i tworze 2 wektory o roznych normach
        sk1 = pow(10, 3)/norma_wek
        wek1 = wek.copy()*sk1
        norma_wek1 = u1.norma_wektora(typ = self.norma, wektor = wek1)
        sk2 = pow(10, -3)/norma_wek
        wek2 = wek.copy()*sk2
        norma_wek2 = u1.norma_wektora(typ = self.norma, wektor = wek2)
        # wykonuje iteracje do momentu, gdy norma roznicy kolejnych
        # przyblizen jest mniejsza niz eps = 0.0000001
        iter1 = test1.iteruj_roznica(
            eps = 1e-10,
            norma = self.norma,
            wyswietlaj = 0,
            X0 = wek1)
        seria1 = test1.normy.copy()
        niedokl1 = test1.sprawdz_rozwiazanie(self.norma)
        iter2 = test1.iteruj_roznica(
            eps = 1e-10,
            norma = self.norma,
            wyswietlaj = 0,
            X0 = wek2)
        seria2 = test1.normy.copy()
        niedokl2 = test1.sprawdz_rozwiazanie(self.norma)
        print(f"Liczba iteracji dla wektora o normie {norma_wek1}: {iter1}")
        print(f"Niedokladnosc rozwiazania: {niedokl1}")
        print(f"Liczba iteracji dla wektora o normie {norma_wek2}: {iter2}")
        print(f"Niedokladnosc rozwiazania: {niedokl2}")
        wykres_test = wykresy.Wykresy()
        wykres_test.badaj_zbieznosc(
            tytul = "Zbieznosc norm dla wektorow poczatkowych o roznej skali",
            opis_OY = "Normy przyblizen",
            dane1 = seria1,
            opis1 = "||X0|| = 1000",
            dane2 = seria2,
            opis2 = "||X0|| = 0.001"
        )
        
    def badaj_zbieznosc(self, epsilon = 1e-7):
        """Badam zbieznosc metody iteracji prostej"""
        # ustalam zbior parametrow
        # zmieniam je w skali logarytmicznej
        param = [1e-9, 1e-7, 1e-5, 1e-3, 0.1, 10, 1e3, 1e5, 1e7, 1e9]
        # okreslam uklad rownan
        u1 = uklad.Uklad(wymiar = self.n)
        # dla kazdej wartosci parametru przeprowadzam po k testow
        # i wyswietlam wartosci wybranych charakterystyk eksperymentu
        sr_liczba_iteracji = []
        sr_norma_macierzy = []
        sr_norma_X0 = []
        sr_niedokladnosc = []
        for sk in param:
            norma_macierzy = 0.0
            liczba_iteracji = 0.0
            norma_X0 = 0.0
            niedokladnosc = 0.0
            iteracje = 0
            while iteracje < self.k:
                # losujemy uklad
                u1.losuj_uklad_symetryczny_dodatnio_okreslony()
                # rozwiazuje uklad z wykorzystaniem metody iteracji prostej
                test1 = iteracjaprosta.IteracjaProsta(ukl = u1)
                # wyznaczam macierz D i wektor C
                test1.przygotuj()
                # obliczam norma macierzy D
                norma_D = u1.norma_macierzy(
                        typ = self.norma,
                        macierz = test1.D
                    )
                # losuje wektor poczatkowy
                wek = np.random.random([self.n, 1])
                # obliczam norme tego wektora
                norma_wek = u1.norma_wektora(typ = self.norma, wektor = wek)
                # skaluje wylosowany wektor
                wek *= sk/norma_wek
                norma_wek = u1.norma_wektora(typ = self.norma, wektor = wek)
                # wykonuje iteracje do momentu, gdy norma roznicy kolejnych
                # przyblizen jest mniejsza niz zadany eps
                iter = test1.iteruj_roznica(
                    eps = epsilon,
                    norma = self.norma,
                    wyswietlaj = 0,
                    X0 = wek)
                niedokl = test1.sprawdz_rozwiazanie(norma = self.norma)
                if iter == 0:
                    # jezeli nie mozna bylo wykonac iteracji
                    # nalezy powtorzyc pomiar
                    continue
                else:
                    # jezeli eksperyment udalo sie przeprowadzic
                    # agregujemy charakterystyki
                    norma_macierzy += norma_D
                    norma_X0 += norma_wek
                    niedokladnosc += niedokl
                    liczba_iteracji += iter
                    iteracje += 1
            # obliczam srednie wartosci charakterystyk
            sr_norma_macierzy.append(norma_macierzy/self.k)
            sr_norma_X0.append(norma_X0/self.k)
            sr_liczba_iteracji.append(liczba_iteracji/self.k)
            sr_niedokladnosc.append(niedokladnosc/self.k)
        # wypisujemy srednie charakterystyki
        print("||X0|| \t \t ||D|| \t     Iteracje   Niedkoladnosc")
        print("------"*9)
        for i in range(len(param)):
            wyniki = f"{sr_norma_X0[i]:.2e} \t"
            wyniki += f"{sr_norma_macierzy[i]:.6f} \t"
            wyniki += f"{sr_liczba_iteracji[i]:.2f} \t"
            wyniki += f"{sr_niedokladnosc[i]:.6e} \n"
            print(wyniki)
            