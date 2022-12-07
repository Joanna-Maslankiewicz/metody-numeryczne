from matplotlib import pyplot as plt
import scipy.optimize as sco
import numpy as np

class Wykresy:

    def __init__(self, n = None):
        """Konstruktor"""
        self.n = n              # liczba danych

    def funkcja_potegowa(self, x, a, b):
        return a*np.power(x, b)

    def badaj_zbieznosc(
        self, tytul, opis_OY, dane1, opis1,
        dane2 = None, opis2 = None, dane3 = None, opis3 = None
    ):
        """Wykres jednej, dwóch lub trzech serii danych
            - pierwsza seria - czerwona, druga - niebieska, trzecia - zielona
            - nazwa - opis na osi OY"""
        # tworzymy wykres
        plt.figure(facecolor = "white")
        seria1 = plt.plot(dane1, "ro")
        plt.title(tytul)
        dane_max = max(dane1)
        dane_min = min(dane1)
        if dane2 is not None:
            dane_max = max(dane_max, max(dane2))
            dane_min = min(dane_min, min(dane2))
            seria2 = plt.plot(dane2, "bo")
        if dane3 is not None:
            dane_max = max(dane_max, max(dane3))
            dane_min = min(dane_min, min(dane3))
            seria3 = plt.plot(dane3, "go")
        delta = 0.05*(dane_max-dane_min)
        y_min = dane_min - delta
        y_max = dane_max + delta
        plt.ylim(y_min, y_max)
        plt.xlabel("Numer iteracji")
        plt.ylabel(opis_OY)
        plt.margins(0.1)
        local = "upper right"
        if dane3 is None:
            if dane2 is None:
                plt.legend(seria1, [opis1], loc = local)
            else:
                plt.legend(seria1 + seria2, [opis1, opis2], loc = local)
        else:
            plt.legend(seria1 + seria2 + seria3, [opis1, opis2, opis3], loc = local)
        plt.grid(True)
        plt.show()

    def badaj_zlozonosc(self, rozmiary, czasy, nazwa):
        """Wykres jednej serii danych i dopasowanej krzywej potegowej"""
        # dopasowujemy krzywa potegowa do danych eksperymentalnych
        pars = sco.curve_fit(
            f = self.funkcja_potegowa,
            xdata = rozmiary,
            ydata = czasy,
            p0 = [0, 0]
        )[0]
        # tworzymy tablice argumentow, by dopasowana krzywa byla gladka
        x = np.arange(rozmiary[-1])
        # wyznaczamy wartosci funkcji uzyskanej w regresji
        czasy_teoretyczne = self.funkcja_potegowa(x, *pars)
        # tworzymy wykres
        opis_linii = "Krzywa regresji"
        plt.figure(facecolor = "white")
        seria1 = plt.plot(rozmiary, czasy, "ro")
        seria2 = plt.plot(x, czasy_teoretyczne, "b-") 
        plt.title("Zlozonosc obliczeniowa algorytmu")
        plt.xlim(0, 1.05*max(rozmiary))
        plt.ylim(0, 1.05*max(max(czasy[0]), max(czasy[1])))
        plt.xlabel("Rozmiar problemu")
        plt.ylabel("Sredni czas")
        plt.margins(0.1)
        plt.legend(seria1 + seria2, [nazwa, opis_linii], loc = "upper left")
        plt.grid(True)
        plt.show()
        zlozonosc = pars[1]
        print(f"Zlozonosc obliczeniowa algorytmu: {zlozonosc}")

    def porownaj_algorytmy(self, rozmiary, czasy, nazwa1, nazwa2):
        """Wykres dwoch serii danych
           nazwa1, nazwa2 - nazwy algorytmow
           pierwsza seria danych - kolor czerwony
           druga seria danych - kolor niebieski"""
        plt.figure(facecolor = "white")
        seria1 = plt.plot(rozmiary, czasy[0], "ro")
        seria2 = plt.plot(rozmiary, czasy[1], "bo")
        plt.title("Porownanie dzialania algorytmow")
        plt.xlim(0, 1.05*max(rozmiary))
        plt.ylim(0, 1.05*max(max(czasy)))
        plt.xlabel("Rozmiar problemu")
        plt.ylabel("Sredni czas")
        plt.margins(0.1)
        plt.legend(seria1 + seria2, [nazwa1, nazwa2], loc = "upper left")
        plt.grid(True)
        plt.show()