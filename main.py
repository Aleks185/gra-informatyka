from random import randint, choice
from choroby import choroby 
from badania import badania as lista_badan


# Pozwala na kolorki
import ctypes
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)



up = "\033[A"
colors = {
    "GREEN":"\033[32m",
    "RED":"\033[31m",
    "YELLOW":"\033[33m",
    "UNDERLINE":"\033[4m",
    "BOLD":"\033[1m",
    "RESET":"\033[0m"
}




print("\033[5;10H")
class pacjent:
    def __init__(self):
        self.nazwy_chorob = list(choroby.keys())
        self.pacjent_choroba = choice(self.nazwy_chorob)
        self.dane_choroby = choroby[self.pacjent_choroba]
        self.objawyWyjawnione = losowanie_objawow(choroby[self.pacjent_choroba]['objawy'])
        self.objawyStr = "\n".join(self.objawyWyjawnione)
        self.ostatnie = 0
        print("Przychodzi pacjent...")
        print(f"Skarży się na:\n{self.objawyStr}\n"+"-"*10)

    def wykonaj_badanie(self):
        badania = list(lista_badan.keys())
        i=1
        badaniaDict = {}
        for badanie in badania:
            if len(lista_badan[badanie]) == 1:
                print(f"[{i}]{badanie}")
                badaniaDict[str(i)] = badanie
                i+=1
            else:
                print(f"{colors['BOLD']}{badanie}{colors['RESET']}")
                if len(lista_badan[badanie]) > 1:
                    for podbadanie in lista_badan[badanie]:
                        if podbadanie != lista_badan[badanie][-1]:
                            pre = "├─"
                        else:
                            pre = "└─"
                        print(f"{pre}[{i}]{podbadanie}")
                        badaniaDict[str(i)] = podbadanie
                        i+=1

        wybor = wyborFunc("",i)
        # print(badaniaDict)
        if badaniaDict[wybor] in self.dane_choroby['wyniki_badan']:
            print(f"{colors['YELLOW']}Wynik badania: {self.dane_choroby['wyniki_badan'][badaniaDict[wybor]]}{colors['RESET']}")
        else:
            print(f"{colors['GREEN']}{badaniaDict[wybor]} jest w normie{colors['RESET']}")
    
    def leczenie(self):
        lista_lekow = [item["leczenie"] for item in choroby.values()]
        i = 1
        lekiDict = {}
        for lek in lista_lekow:
            if lek in lekiDict.values():
                continue
            print(f"[{i}]{lek}")
            lekiDict[str(i)] = lek
            i+=1
        wybor = wyborFunc("",i)
        wybrany_lek = lekiDict[wybor]
        if wybrany_lek == self.dane_choroby['leczenie']:
            self.wygrana()
        else:
            self.przegrana()

    def daj_objaw(self):
        if choice([1,2]) == 1:
            dostepne = [item for item in self.dane_choroby['objawy'] if item not in self.objawyWyjawnione]
            self.dlugosc_dostepnosci = len(dostepne)
            if self.dlugosc_dostepnosci == 0:
                print("UWAGA: OSTATNIA RUNDA!")
                self.ostatnia_tura()
            else:
                objaw = choice(dostepne)
                self.objawyWyjawnione.append(objaw)

                print(f"Nowe objawy: {objaw}")
        

    def ostatnia_tura(self):
        
        while True:
            print("Dostępne objawy:")
            for objaw in self.objawyWyjawnione:
                print(f"{objaw}")
            wybor = wyborFunc("[1] Leczenie \t [2] Podręcznik",2)
            if wybor == "1":
                self.leczenie()
            else:
                podrecznik()
            

    def skip(self):
        self.daj_objaw()
    def przegrana(self):

        print(f"{colors['RED']}PRZEGRAŁEŚ, chorobą było {self.pacjent_choroba.replace('_',' ').capitalize()}, a leczenie {self.dane_choroby['leczenie']}{colors['RESET']}")
        exit()
    def wygrana(self):
        print(f"{colors['GREEN']}WYGRAŁEŚ, chorobą było {self.pacjent_choroba.replace('_',' ').capitalize()}{colors['RESET']}")
        exit()
        


def start():
    print("\033[2J\033[H")
    print("""
██████╗  ██████╗ ██╗  ██╗████████╗ ██████╗ ██████╗     ██████╗  ██████╗ ███╗   ███╗
██╔══██╗██╔═══██╗██║ ██╔╝╚══██╔══╝██╔═══██╗██╔══██╗    ██╔══██╗██╔═══██╗████╗ ████║
██║  ██║██║   ██║█████╔╝    ██║   ██║   ██║██████╔╝    ██║  ██║██║   ██║██╔████╔██║
██║  ██║██║   ██║██╔═██╗    ██║   ██║   ██║██╔══██╗    ██║  ██║██║   ██║██║╚██╔╝██║
██████╔╝╚██████╔╝██║  ██╗   ██║   ╚██████╔╝██║  ██║    ██████╔╝╚██████╔╝██║ ╚═╝ ██║
╚═════╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝
                                                                                   
""")
    print("Witamy w grze Doktor Dom")
    wybor = wyborFunc("[1]Rozpocznij grę \t [2]Ustawienia",2)
    if wybor == "1":
        gra()
    else:
        ustawienia()
    print("\033[2J\033[H") # Oczyszcza ekran
def ustawienia():
    global colors
    stan_kolorow = "ON"
    print("Ustawienia:")
    while True:
        wybor = wyborFunc(f"[1] Kolory: {stan_kolorow}\n[2] Wyjdź",2)
        if wybor == "1":
            if stan_kolorow == "ON":
                colors={
                    "RED":"",
                    "GREEN":"",
                    "YELLOW":"",
                    "BOLD":"",
                    "UNDERLINE":"",
                    "RESET":"",
                }
                stan_kolorow = "OFF"
            else:
                colors = {
                    "GREEN":"\033[32m",
                    "RED":"\033[31m",
                    "YELLOW":"\033[33m",
                    "UNDERLINE":"\033[4m",
                    "BOLD":"\033[1m",
                    "RESET":"\033[0m"
                }
                stan_kolorow = "ON"
            
        elif wybor == "2":
            start()
def losowanie_objawow(objawy:list):
    iloscWylosowanych = randint(1,2)
    wroc = []
    i=0
    while i < iloscWylosowanych:
        objaw = choice(objawy)
        if objaw in wroc:
            continue
        wroc.append(objaw)
        i+=1
    return wroc



def wyborFunc(message,dlugosc):
    ok = False
    print(message)
    print("Opcja: ")
    while not ok:
        opcja = int(input())
        if opcja not in list(range(1,dlugosc+1)):
            print("Zła opcja")
            print(up+up, end="")
        else:
            ok=True
            break
    return str(opcja)

def podrecznik():
    lista_chorob = list(choroby.keys())
    
    for choroba in lista_chorob:
        print(f"Choroba: {colors['UNDERLINE']}{colors['BOLD']}{choroba}{colors['RESET']}")
        print(f"{colors['BOLD']}Objawy: {colors['RESET']}")
        for objaw in choroby[choroba]['objawy']:
            if objaw != choroby[choroba]['objawy'][-1]:
                print(f"├─{objaw}")
            else:
                print(f"└─{objaw}")
        print("\n")
        print(f"Wyniki badań: ")
        for badanie in choroby[choroba]['wyniki_badan']:
            badanieNazwa = badanie.capitalize() if not badanie.isupper() else badanie
            if badanie != list(choroby[choroba]['wyniki_badan'])[-1]:
                pre = "├─"
            else:
                pre = "└─"
            print(f"{pre}{badanieNazwa.replace('_', ' '):.<25}{choroby[choroba]['wyniki_badan'][badanie]:<15}")
        print("\n")
        print(f"Leczenie: {choroby[choroba]['leczenie']}")
        if choroba != lista_chorob[-1]:
            print("\n")
            print("═"*10+"╗")
            print("═"*10+"╝")

            print("\n")


def gra():
    pacjent1 = pacjent()
    zdrowy = False
    tury = 0
    while not zdrowy:
        print("Dostępne objawy:")
        for objaw in pacjent1.objawyWyjawnione:
            print(f"{objaw}")
        print("")
        wybor = wyborFunc("[1] Wykonaj badanie \t [2] Leczenie \t [3] Skip tury \t [4] Podręcznik do medecyny",4)
        if wybor == "1":
            pacjent1.wykonaj_badanie()
        elif wybor == "2":
            pacjent1.leczenie()
        elif wybor == "3":
            pacjent1.skip()
        elif wybor == "4":
            podrecznik()
            

if __name__ == "__main__":
    start()