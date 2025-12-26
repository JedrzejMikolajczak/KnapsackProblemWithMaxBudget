import json
 
def wczytaj_dane(nazwa_pliku):
    try:
        with open(nazwa_pliku, 'r') as plik:
            dane = json.load(plik)
        return dane['przedmioty'], dane['max_waga'], dane['max_budzet']
    except FileNotFoundError:
        print("nie znaleziono pliku")
        return [], 0, 0
    except json.JSONDecodeError:
        print("blad odczytu pliku")
        return [], 0, 0
 
 
def plecak_z_budzetem(przedmioty, max_waga, max_budzet):
    for p in przedmioty:
        wartosc = p['wartosc']
        waga = p['waga']
        p['oplacalnosc'] = wartosc / waga
 
    przedmioty_posortowane = sorted(przedmioty, key=lambda x: x['oplacalnosc'], reverse=True)
 
    plecak = []
    waga_obecna = 0
    koszt_obecny = 0
    wartosc_calkowita = 0
 
    for p in przedmioty_posortowane:
        nazwa = p['nazwa']
        waga = p['waga']
        wartosc = p['wartosc']
        koszt = p['koszt']
 
        czy_miesci_sie_waga = (waga_obecna + waga <= max_waga)
        czy_miesci_sie_budzet = (koszt_obecny + koszt <= max_budzet)
 
        if czy_miesci_sie_waga and czy_miesci_sie_budzet:
            plecak.append(p)
            waga_obecna += waga
            koszt_obecny += koszt
            wartosc_calkowita += wartosc
 
        else:
            print(f"Pominięto: {nazwa}")
            if not czy_miesci_sie_waga:
                print("Za duża waga")
            elif not czy_miesci_sie_budzet:
                print("Brak budżetu")
 
    return plecak, wartosc_calkowita, waga_obecna, koszt_obecny
 
 
def uruchom(nazwapliku):
    lista_przedmiotow, limit_wagi, limit_budzetu = wczytaj_dane(nazwapliku)
 
    if not lista_przedmiotow:
        return
 
    plecak, wartosc, waga, koszt = plecak_z_budzetem(lista_przedmiotow, limit_wagi, limit_budzetu)
 
    print("WYNIK:")
    print(f"Calkowita wartosc: {wartosc}")
    print(f"Wykorzystana waga: {waga} / {limit_wagi}")
    print(f"Wykorzystany budzet: {koszt} / {limit_budzetu}")
    print("Wybrane przedmioty:")
 
    for p in plecak:
        print(f" {p['nazwa']} (Wartosc: {p['wartosc']}, Waga: {p['waga']}, Koszt: {p['koszt']})")
 
if __name__ == "__main__":
    uruchom('dane.json')
