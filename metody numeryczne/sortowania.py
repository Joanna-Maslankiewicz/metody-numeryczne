import random as rand
import time
import wykresy
from typing import List

class Sortowania:
  
    def __init__(self, n=200, lprob=5, ldlugosci=10, najkrotsza=100):
        """Konstruktor okreslajacy parametry eksperymentu"""
        self.dlugosc = n                    # maksymalna dlugosc listy
        self.lista = []                     # lista nieposortowana
        self.lista1 = []                    # lista do sort. przez wstawianie
        self.lista2 = []                    # lista do sort. przez wybieranie
        self.rozmiary = []                  # lista rozmiarow list
        self.czasy: List[List] = [[], []]   # lista czasow sortowania
        self.liczba_dlugosci = ldlugosci    # liczba roznych dlugosci list
        self.liczba_prob = lprob            # liczba eksper. dla jednej dlugosci
        self.min_dlugosc = najkrotsza       # dlugosc najkrotszej listy
        
    def __str__(self):
        """Wyswietlanie listy nieposortowanej"""
        return self.lista.__str__()
    
    def losuj(self, k=None):
        """Losowanie k elementow listy"""
        if k is None:
            k = self.dlugosc
        self.lista = []
        for _ in range(k):
            self.lista.append(rand.randint(0, self.dlugosc*10))
        self.lista1 = self.lista[:]
        self.lista2 = self.lista[:]
    
    def wyswietl_liste1(self):
        """Wyswietlanie listy1"""
        return f"{self.lista1}"
    
    def wyswietl_liste2(self):
        """Wyswietlanie listy2"""
        return f"{self.lista2}"
    
    def sortuj_przez_wstawianie(self, k=None):
        """Sortowanie przez wstawianie k pierwszych elementow"""
        if k is None:
            k = self.dlugosc
        self.lista = []
        for i in range(1, k):
            # wybieram element listy
            elem = self.lista1[i] 
            indeks = 0
            # szukam miejsca gdzie wstawic wybrany element
            while self.lista1[indeks] < elem:
                indeks = indeks + 1
            # wstawiam wybrany element w odpowiednie miejsce
            if indeks < i:
                self.lista1.pop(i)
                self.lista1.insert(indeks, elem)
    
    def sortuj_przez_wybieranie(self, k=None):
        if k is None:
            k = self.dlugosc
        self.lista = []
        """Sortowanie przez wybieranie k pierwszych elementow"""
        for i in range(k):
            x_min = self.lista2[i]
            indeks_min = i
            # wybieram najmniejszy element nieposortowanej czesci listy
            for j in range(i+1, k):
                if self.lista2[j] < x_min:
                    x_min = self.lista2[j]
                    indeks_min = j
            # zamieniam miejscacmi i-ty element z najmniejszym elementem
            # nieposortowanej jeszcze czesci listy
            self.lista2[indeks_min] = self.lista2[i]
            self.lista2[i] = x_min
            
    def nazwa_metody(self, metoda):
        """Metoda zwracajaca nazwe algorytmu
            1 - sortowanie przez wstawianie
            2 - sortowanie przez wybieranie"""
        if metoda == 1:
            return "Sortowanie przez wstawianie"
        return "Sortowanie przez wybieranie"
        
    def mierz_czas(self, metoda, k=None):
        """Metoda mierzaca czas sortowan losowych list o dlugosci k"""
        if k is None:
            k = self.dlugosc
        self.lista = []
        czas = 0.0
        for _ in range(self.liczba_prob):
            self.losuj(k)
            if metoda == 1:
                stoper = time.time()
                self.sortuj_przez_wstawianie(k)
                stoper = time.time() - stoper
            else:
                stoper = time.time()
                self.sortuj_przez_wybieranie(k)
                stoper = time.time() - stoper
            czas = czas + stoper
        return czas/self.liczba_prob

    def badaj_zlozonosc(self, metoda):
        """Metoda badajaca zlozonosc wybranej metody sortowania"""
        if self.liczba_dlugosci < 2:
            print("Zbyt mala liczba dlugosci list.")
            return
        # wyznaczam krok zmiany dlugosci listy
        krok = (self.dlugosc-self.min_dlugosc) / (self.liczba_dlugosci-1);
        self.rozmiary = []
        self.czasy[metoda-1] = []
        for i in range(self.liczba_dlugosci):
            self.rozmiary.append(int(self.min_dlugosc + i*krok))   
            self.czasy[metoda-1].append(
                self.mierz_czas(metoda, self.rozmiary[i])
            )
            print(self.rozmiary[i], self.czasy[metoda-1][i])
        wykres = wykresy.Wykresy(self.dlugosc)
        wykres.badaj_zlozonosc(
            self.rozmiary,
            self.czasy[metoda-1],
            self.nazwa_metody(metoda)
        )

    def porownaj_metody(self):
        """Metoda porownujaca metody sortowania"""
        # wyznaczam krok zmiany dlugosci listy
        krok = self.dlugosc / self.liczba_dlugosci;
        self.rozmiary = []
        self.czasy = [[], []]
        for i in range(self.liczba_dlugosci):
            k = int((i+1)*krok)
            self.rozmiary.append(k)   
            self.czasy[0].append(self.mierz_czas(1, k))
            self.czasy[1].append(self.mierz_czas(2, k))
            print(f"{k} \t {self.czasy[0][i]} \t {self.czasy[1][i]}")
        wykres = wykresy.Wykresy(self.dlugosc)
        wykres.porownaj_algorytmy(
            self.rozmiary,
            self.czasy,
            self.nazwa_metody(1),
            self.nazwa_metody(2)
        )