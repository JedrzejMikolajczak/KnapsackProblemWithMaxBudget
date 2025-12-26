import json
import random
 
def wczytaj_dane(nazwa_pliku):
    try:
        with open(nazwa_pliku, 'r') as plik:
            dane = json.load(plik)
        return dane['przedmioty'], dane['max_waga'], dane['max_budzet']
    except FileNotFoundError:
        print("Nie znaleziono pliku")
        return [], 0, 0
 
 
# alg parameters
ants = 20
iterations = 100
alpha = 1.0
beta = 2.0
evaporation_rate = 0.5
pheromone_to_give = 30
 
# dane
wartosci = []
wagi = []
oplacalnosc = []
koszty = []
 
lista_przedmiotow, limit_wagi, limit_budzetu = wczytaj_dane("dane.json")
 
if not lista_przedmiotow:
    print("Brak danych do przetworzenia.")
    exit()
 
for p in lista_przedmiotow:
    wartosc = p['wartosc']
    waga = p['waga']
    koszt = p['koszt']
 
    wartosci.append(wartosc)
    wagi.append(waga)
    koszty.append(koszt)
 
    if waga > 0:
        oplacalnosc.append(wartosc / waga)
    else:
        oplacalnosc.append(0)
 
ilosc_przemiotow = len(wartosci)
pheromone = [1.0] * ilosc_przemiotow
 
 
def obliczenie_prawdopodobienstwa(aktualne_koszta, aktualna_waga, dostepne_przedmioty):
    prawdopodobienstwa = []
    suma_szans = 0
 
    for i in dostepne_przedmioty:
        fits_weight = (aktualna_waga + wagi[i] <= limit_wagi)
        fits_budget = (aktualne_koszta + koszty[i] <= limit_budzetu)
 
        if fits_weight and fits_budget:
            szansa = (pheromone[i] ** alpha) * (oplacalnosc[i] ** beta)
            prawdopodobienstwa.append((i, szansa))
            suma_szans += szansa
 
    if suma_szans <= 0:
        return []
 
    wynik = []
    for przedmiot, szansa in prawdopodobienstwa:
        wynik.append((przedmiot, szansa / suma_szans))
 
    return wynik
 
 
def budowanie_rozwiazania():
    solution = []
    aktualna_waga = 0
    aktualne_wydane = 0
    dostepne_przedmioty = list(range(ilosc_przemiotow))
 
    while dostepne_przedmioty:
        probs = obliczenie_prawdopodobienstwa(aktualne_wydane, aktualna_waga, dostepne_przedmioty)
        if not probs:
            break
 
        r = random.random()
        suma = 0
        for przedmiot, szansa in probs:
            suma += szansa
            if r <= suma:
                solution.append(przedmiot)
 
                aktualna_waga += wagi[przedmiot]
                aktualne_wydane += koszty[przedmiot]
 
                dostepne_przedmioty.remove(przedmiot)
                break
    return solution
 
 
def wartosc_plecaka(solution):
    return sum(wartosci[i] for i in solution)
 
 
def pheromone_update(best_sol, best_val):
    global pheromone
    for i in range(ilosc_przemiotow):
        pheromone[i] *= (1 - evaporation_rate)
 
    if best_val > 0:
        for i in best_sol:
            pheromone[i] += pheromone_to_give
 
 
best_sol = []
best_val = 0
 
 
for i in range(iterations):
    for ant in range(ants):
        solution = budowanie_rozwiazania()
        value = wartosc_plecaka(solution)
 
        if value > best_val:
            best_sol = solution
            best_val = value
 
    pheromone_update(best_sol, best_val)
 
print("Najlepsze znalezione rozwiązanie:")
print(f"Łączna wartość: {best_val}")
 
koncowa_waga = sum(wagi[i] for i in best_sol)
koncowy_koszt = sum(koszty[i] for i in best_sol)
 
print(f"Waga:   {koncowa_waga} / {limit_wagi}")
print(f"Budżet: {koncowy_koszt} / {limit_budzetu}")
 
if koncowa_waga <= limit_wagi and koncowy_koszt <= limit_budzetu:
    print("STATUS: Wynik poprawny.")
else:
    print("STATUS: BŁĄD! Przekroczono limity.")
