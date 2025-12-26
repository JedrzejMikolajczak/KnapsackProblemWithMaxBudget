import json
 
def wczytaj_dane(nazwa_pliku):
    try:
        with open(nazwa_pliku, 'r') as plik:
            dane = json.load(plik)
        return dane['przedmioty'], dane['max_waga'], dane['max_budzet']
    except FileNotFoundError:
        print("Nie znaleziono pliku")
        return [], 0, 0
 
def algorytm_silowy_z_budzetem(przedmioty, max_waga, max_budzet):
    n = len(przedmioty)
    max_wartosc = 0
    najlepszy_zbior = []
 
    # Przegląd wszystkich możliwych podzbiorów (od 0 do 2^n - 1)
    # Każdy podzbiór reprezentowany jest przez liczbę binarną o n bitach
    for i in range(1, 2 ** n):
        wybor = []
        suma_wagi = 0
        suma_kosztu = 0
        suma_wartosci = 0
 
        for j in range(n):
            if (i >> j) & 1:
                # Jeśli j-ty bit jest 1, bierzemy j-ty przedmiot
                p = przedmioty[j]
                wybor.append(p)
                suma_wagi += p['waga']
                suma_kosztu += p['koszt']
                suma_wartosci += p['wartosc']
 
        if suma_wagi <= max_waga and suma_kosztu <= max_budzet:
            if suma_wartosci > max_wartosc:
                max_wartosc = suma_wartosci
                najlepszy_zbior = wybor[:]
 
    koncowa_waga = sum(p['waga'] for p in najlepszy_zbior)
    koncowy_koszt = sum(p['koszt'] for p in najlepszy_zbior)
 
    return najlepszy_zbior, max_wartosc, koncowa_waga, koncowy_koszt
 
 
def uruchom(nazwapliku):
    lista_przedmiotow, limit_wagi, limit_budzetu = wczytaj_dane(nazwapliku)
 
    if not lista_przedmiotow:
        print("Brak danych.")
        return
 
    plecak, wartosc, waga, koszt = algorytm_silowy_z_budzetem(lista_przedmiotow, limit_wagi, limit_budzetu)
 
    print(f"Calkowita wartosc: {wartosc}")
    print(f"Wykorzystana waga: {waga} / {limit_wagi}")
    print(f"Wykorzystany budzet: {koszt} / {limit_budzetu}\n")
    print("Wybrane przedmioty:")
    for p in plecak:
        print(f"{p['nazwa']} (Wartosc: {p['wartosc']}, Waga: {p['waga']}, Koszt: {p['koszt']})")
 
 
if __name__ == "__main__":
    uruchom('dane.json')
