# napište funkci filtruj_cisla(typ, cisla), která přijme dva parametry:
# typ – řetězec, který může nabývat hodnot "kladna", "zaporna", "suda", "licha"
# cisla – seznam čísel
# Funkce vrátí nový seznam obsahující pouze ta čísla z parametru cisla, která odpovídají zadanému typu.

def filtruj_cisla(typ, cisla):
    vysledek = []
    if typ=="kladna":
            for cislo in cisla:
                try:
                    if cislo>0:
                        vysledek.append(cislo)
                except TypeError:
                    print(f"{cislo} není číslo")
    elif typ=="suda":
            for cislo in cisla:
                try:
                        if cislo%2==0:
                            vysledek.append(cislo)
                except TypeError:
                    print(f"{cislo} není číslo")
    elif typ=="zaporna":
            for cislo in cisla:
                try:
                    if cislo<0:
                        vysledek.append(cislo)
                except TypeError:
                    print(f"{cislo} není číslo")
    elif typ=="licha":
            for cislo in cisla:
                try:
                    if cislo%2!=0:
                        vysledek.append(cislo)
                except TypeError:
                    print(f"{cislo} není číslo")
    
    # Vaše řešení zde
 
    return vysledek


if __name__ == "__main__":
    print(filtruj_cisla("kladna", [1, -2, 0, 5, -3]))   # [1, 5]
    print(filtruj_cisla("suda", [1, 2, 3, 4, 5]))       # [2, 4]
    print(filtruj_cisla("zaporna", [1, -2, 0, 5, -3]))   # [-2, -3]
    print(filtruj_cisla("licha", [1, 2, 3, 4, 5]))       # [1, 3, 5]
    # neexistující typ
    print(filtruj_cisla("xxx", [1, 2, 3]))              # []