import json
import random
 
 
def wczytaj_dane(nazwa_pliku):
    try:
        with open(nazwa_pliku, 'r') as plik:
            dane = json.load(plik)
        return dane['przedmioty'], dane['max_waga'], dane['max_budzet']
    except FileNotFoundError:
        print(f"Blad: Nie znaleziono pliku {nazwa_pliku}")
        return [], 0, 0
    except json.JSONDecodeError:
        print(f"Blad: Problem z formatem pliku {nazwa_pliku}")
        return [], 0, 0
 
 
def algorytm_zachlanny_z_prawdopodobienstwem(przedmioty, max_waga, max_budzet):
    items = przedmioty.copy()
    for p in items:
        p['oplacalnosc'] = p['wartosc'] / p['waga']
 
    items.sort(key=lambda x: x['oplacalnosc'], reverse=True)
 
    plecak = []
    waga_obecna = 0
    koszt_obecny = 0
    wartosc_calkowita = 0
 
    for p in items:
        if random.random() < 0.6:
 
            if (waga_obecna + p['waga'] <= max_waga) and (koszt_obecny + p['koszt'] <= max_budzet):
                plecak.append(p)
                waga_obecna += p['waga']
                koszt_obecny += p['koszt']
                wartosc_calkowita += p['wartosc']
 
    return plecak, wartosc_calkowita, waga_obecna, koszt_obecny
 
 
def uruchom(nazwa_pliku):
    lista_przedmiotow, limit_wagi, limit_budzetu = wczytaj_dane(nazwa_pliku)
 
    if not lista_przedmiotow:
        return
 
    plecak, wartosc, waga, koszt = algorytm_zachlanny_z_prawdopodobienstwem(lista_przedmiotow, limit_wagi, limit_budzetu)
 
    print("WYNIK:")
    print(f"Calkowita wartosc: {wartosc}")
    print(f"Wykorzystana waga: {waga} / {limit_wagi}")
    print(f"Wykorzystany budzet: {koszt} / {limit_budzetu}")
    print("Wybrane przedmioty:")
 
    for p in plecak:
        print(f" {p['nazwa']} (Wartosc: {p['wartosc']}, Waga: {p['waga']}, Koszt: {p['koszt']})")
 
 
if __name__ == "__main__":
    uruchom('dane.json')
