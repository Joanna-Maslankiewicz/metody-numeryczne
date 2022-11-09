from matplotlib import pyplot as plt
import scipy.optimize as sco
import numpy as np

class Wykresy:

    def __init__(self, n):
        """Konstruktor"""
        self.n = n              # liczba danych

    def funkcja_potegowa(self, x, a, b):
        return a*np.power(x, b)

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
        x = np.array(rozmiary[:])
        # wyznaczamy wartosci funkcji uzyskanej w regresji
        czasy_teoretyczne = self.funkcja_potegowa(x, *pars)
        # tworzymy wykres
        opis_linii = "Krzywa regresji"
        plt.figure(facecolor = "white")
        seria1 = plt.plot(rozmiary, czasy, "ro")
        seria2 = plt.plot(x, czasy_teoretyczne, "b-") 
        plt.title("Zlozonosc obliczeniowa algorytmu")
        plt.xlim(0, 1.1*max(rozmiary))
        plt.ylim(0, 1.1*max(czasy))
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
        plt.xlim(0, 1.1*max(rozmiary))
        plt.ylim(0, 1.1*max(max(czasy[0]), max(czasy[1])))
        plt.xlabel("Rozmiar problemu")
        plt.ylabel("Sredni czas")
        plt.margins(0.1)
        plt.legend(seria1 + seria2, [nazwa1, nazwa2], loc = "upper left")
        plt.grid(True)
        plt.show()