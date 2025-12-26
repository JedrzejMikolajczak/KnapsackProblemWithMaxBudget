import json
import random
 
 
def generuj_dane_losowe(nazwa_pliku="dane.json", liczba_przedmiotow=10):
    przedmioty = []
    for i in range(liczba_przedmiotow):
        item = {
            "nazwa": f"Przedmiot_{i + 1}",
            "waga": random.randint(1, 20),
            "wartosc": random.randint(10, 200),
            "koszt": random.randint(1, 20)
        }
        przedmioty.append(item)
 
    suma_wag = sum(p['waga'] for p in przedmioty)
    suma_kosztow = sum(p['koszt'] for p in przedmioty)
 
    max_waga = int(suma_wag * 0.5)
    max_budzet = int(suma_kosztow * 0.5)
 
    dane = {
        "max_waga": max_waga,
        "max_budzet": max_budzet,
        "przedmioty": przedmioty
    }
 
    try:
        with open(nazwa_pliku, 'w') as f:
            json.dump(dane, f, indent=4)
        print(f"Sukces! Wygenerowano {liczba_przedmiotow} przedmiotów do pliku '{nazwa_pliku}'.")
        print(f"Limity: Waga={max_waga}, Budżet={max_budzet}")
    except IOError:
        print("Błąd zapisu do pliku.")
 
 
if __name__ == "__main__":
    n = input("Podaj liczbę przedmiotów do wygenerowania (domyślnie 10): ")
    if not n.strip():
        n = 10
    else:
        n = int(n)
    generuj_dane_losowe(liczba_przedmiotow=n)
