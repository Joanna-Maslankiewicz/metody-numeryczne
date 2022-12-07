"""Zbieznosc metod iteracyjnych"""

import przyklad0, zadanie, iteracyjne

def testy(typ):
    if typ == 1:    
        # porownanie metod iteruj_roznica oraz iteruj_twierdzenie
        test1 = przyklad0.Przyklad0(wymiar = 100)
        test1.porownaj(1)
    elif typ == 2:
        # porownanie metod iteracji prostej i Seidela
        test2 = przyklad0.Przyklad0(wymiar = 100)
        test2.porownaj(2)
    elif typ == 3:
        # zbieznosc/rozbieznosc metod iteracyjnych
        test3 = przyklad0.Przyklad0(wymiar = 3)
        test3.badaj_zbieznosc(typ = 1, iteracje = 100)
    elif typ == 4:
        # realizacja przykladowego zadania - sprawdzamy wplyw skali wektora
        # poczatkowego na zbieznosc metody iteracji prostej
        # wykonujemy najpierw test - wybieramy 2 przykladowe wart. parametru
        test4 = zadanie.Zadanie()
        test4.testy()
    elif typ == 5:
        # realizacja przykladowego zadania - sprawdzamy wplyw skali wektora
        # poczatkowego na zbieznosc metody iteracji prostej
        # przeprowadzamy eksperyment
        test5 = zadanie.Zadanie()
        test5.badaj_zbieznosc(epsilon = 1e-10)
    elif typ == 6:
        # przyklad zastosowania metody potegowej
        test6 = iteracyjne.Iteracyjne(50)
        test6.wartosc_wlasna()
    elif typ == 7:
        # przyklad zastosowania iteracji Seidela do znalezienia rankingu
        test7 = iteracyjne.Iteracyjne(10)
        test7.page_rank_iteracja()
    elif typ == 8:
        # tutaj mozna zrealizowac zadania
        pass
    
if __name__ == '__main__':
    testy(1)
