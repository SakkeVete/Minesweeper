#Sakari Veteläinen 2555304 Ohjelmoinnin alkeet. 6.5.2019
#
#Pelissä pystyy pelaamaan miinaharavaa haluamallaan miinamäärällä ja kentän koolla.
#
#Parannuksia ja puutteita:
#
#
#
#
#

import haravasto
import random
import time



tila = {
    "miinat": None,
    "kentta": None,
    "luukut": None,
    "liput": None,
    "alku": None,
    "vapaat_ruudut": None,
    "loppu": False,
}

def asetukset():
    """Valikko joka asettaa halutun kentän leveyden, korkeuden sekä miinojen määrän."""
    print("Valitse kentän koko ja miinojen määrä")
    while True:
        try:
            print("1. Helppo\n2. Keskitaso\n3. Vaikea\n4. Custom")
            valinta = int(input("Syötä valintasi: "))
            if valinta == 1:
                leveys = 8
                korkeus = 8
                maara = 10
                return leveys, korkeus, maara
            elif valinta == 2:
                leveys = 16
                korkeus = 16
                maara = 40
                return leveys, korkeus, maara
            elif valinta == 3:
                leveys = 24
                korkeus = 24
                maara = 99
                return leveys, korkeus, maara
            elif valinta == 4:
                leveys = int(input("Syötä kentän leveys kokonaislukuna: "))
                korkeus = int(input("Syötä kentän korkeus kokonaislukuna: "))
                maara = int(input("Syötä miinojen lukumäärä: "))
                if leveys < 1 or korkeus < 1 or maara > leveys*korkeus:
                    print("Kenttä on liian pieni tai miinoja on enemmän kuin ruutuja.\n")
                else:
                    return leveys, korkeus, maara
            else:
                print("Virheellinen valinta.\n")
        except ValueError:
            print("Syötä arvot kokonaislukuina.\n")

def alkuvalikko():
    """Alkuvalikko josta käynnistetään uusi peli tai tarkastellaan tilastoja."""
    print("Tervetuloa pelaamaan Miinaharavaa!")
    print("1. Uusi peli\n2. Tilastot\nQ. Poistu Miinaharavasta")
    syote = input("Syötä valintasi: ")
    if syote == "1":
        luo_kentta()
    elif syote == "2":
        tilasto()
    elif syote == "q" or syote == "Q":
        raise SystemExit
    else:
        print("Virheellinen valinta.\n")
        alkuvalikko()

def tilasto():
    """Valikko jossa valitaan mitä tilastoja halutaan tarkastella."""
    print("1. Huipputulokset\n2. 10 viimeisinta \n3. Alkuvalikko \nQ. Poistu Miinaharavasta")
    syote = input("Syötä valintasi: ")
    if syote == "1":
        print("1. Helpot\n2. Keskitaso \n3. Vaikea \nQ. Poistu Miinaharavasta")
        syote = input("Syötä valintasi: ")
        if syote == "1":
            nayta_top("Helppo", 5)
        if syote == "2":
            nayta_top("Keskitaso", 5)
        if syote == "3":
            nayta_top("Vaikea", 5)
        tilasto()
    elif syote == "2":
        nayta_top("Kaikki", 10)
        tilasto()
    elif  syote == "3":
        alkuvalikko()
    elif syote == "q" or syote == "Q":
        raise SystemExit
    else:
        print("Virheellinen valinta.\n")
        tilasto()
    
def tulvataytto(x_koord, y_koord):
    """Käy läpi viereiset ruudut ja aukaisee ne mikäli ne ovat tyhjiä(ei miinoja tai numeroita)"""
    kentta = tila["kentta"]
    uusi_lista = [(x_koord, y_koord)]
    leveys = len(kentta[0])
    korkeus = len(kentta)
    if kentta[y_koord][x_koord] != "x":
        while uusi_lista:
            tila["luukut"][y_koord][x_koord] = tila["kentta"][y_koord][x_koord]
            if tila["kentta"][y_koord][x_koord] == "0":
                kentta[y_koord][x_koord] = "jj"
            x_koord, y_koord = uusi_lista.pop()

            for ny in range(y_koord - 1, y_koord + 2):
                for nx in range(x_koord - 1, x_koord + 2):
                    if 0 <= nx < leveys and 0 <= ny < korkeus:
                        if kentta[ny][nx] == "0" and uusi_lista.count((nx, ny)) == 0:
                            uusi_lista.append((nx, ny))
                        elif kentta[ny][nx] == "x":
                            continue
                        else:
                            tila["luukut"][ny][nx] = tila["kentta"][ny][nx]
                            continue

def luo_kentta():
    """Luo kentän aikaisemmin määriteltyjen asetusten mukaan."""
    leveys, korkeus, maara = asetukset()
    kentta = []
    luukut = []
    for rivi in range(korkeus):
        kentta.append([])
        luukut.append([])
        for sarake in range(leveys):
            kentta[-1].append(" ")
            luukut[-1].append(" ")
    vapaat_ruudut = []
    for x in range(leveys):
        for y in range(korkeus):
            vapaat_ruudut.append((x, y))
    tila["kentta"] = kentta
    tila["luukut"] = luukut
    tila["vapaat_ruudut"] = vapaat_ruudut
    tila["liput"] = []
    tila["vuorot"] = []
    miinoita(kentta, vapaat_ruudut, maara)
    aseta_numerot(kentta)

def miinoita(kentta, vapaat_ruudut, maara):
    """Asettaa tietyn määrän miinoja sattumanvaraisesti pelikentälle."""
    miinat = []
    for ruutu in range(maara):
        x, y = random.choice(vapaat_ruudut)
        kentta[y][x] = "x"
        miinat.append((x, y))
        vapaat_ruudut.remove((x, y))
    tila["kentta"] = kentta
    tila["miinat"] = miinat
    tila["vapaat_ruudut"] = vapaat_ruudut


def laske_ninjat(x, y):
    """Laskee annetun ruudun ympärillä olevien miinojen määrän."""
    korkeus = len(tila["kentta"][0])
    leveys = len(tila["kentta"])
    ninjat = []
    for nx in range(min(max(x-1, 0), leveys), min(max(x+2, 0), leveys)):
        for ny in range(min(max(y-1, 0), korkeus), min(max(y+2, 0), korkeus)):
            ninjat.append((nx, ny))
    return ninjat

def aseta_numerot(kentta):
    """Asettaa ruudulle arvon riippuen vieresten miinojen määrästä."""
    for rivinro, rivi in enumerate(kentta):
        for sarakenro, sarake in enumerate(rivi):
            if sarake != "x":
                arvot = [kentta[r][s] for r, s in laske_ninjat(rivinro, sarakenro)]
                if arvot.count("x") > 0:
                    kentta[rivinro][sarakenro] = str(arvot.count("x"))
                else:
                    kentta[rivinro][sarakenro] = "0"
    tila["kentta"] = kentta

def piirra_kentta():
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for x in range(len(tila["luukut"][0])):
        for y in range(len(tila["luukut"])):
            haravasto.lisaa_piirrettava_ruutu(tila["luukut"][y][x], x * 40, y * 40)
    haravasto.piirra_ruudut()

def avaa_ruutu(x, y):
    tila["vuorot"].append((x, y))
    if tila["luukut"][y][x] == " ":
        tila["luukut"][y][x] = tila["kentta"][y][x]
        if not tarkista_havio(x, y):
            tarkista_voitto()
        
    if tila["kentta"][y][x] == "0":
        tulvataytto(x, y)
        piirra_kentta()
        if not tarkista_havio(x, y):
            tarkista_voitto()

def aseta_lippu(x, y):
    if tila["luukut"][y][x] == " ":
        tila["luukut"][y][x] = "f"
        tila["liput"].append((x, y))
    elif tila["luukut"][y][x] == "f":
        tila["luukut"][y][x] = " "
        tila["liput"].remove((x, y))
    piirra_kentta()

def hiiri_kasittelija(x, y, nappi, muokkausnapit):
    """Käsittelee hiiren oikean ja vasemman painikkeen napautukset"""
    x = int(x / 40)
    y = int(y / 40)
    if nappi == haravasto.HIIRI_VASEN:
        avaa_ruutu(x, y)
    elif nappi == haravasto.HIIRI_OIKEA:
        aseta_lippu(x, y)

def tarkista_vaikeus():
    if len(tila["kentta"]) == 8:
        taso = "Helppo"
        return taso
    elif len(tila["kentta"]) == 16:
        taso = "Keskitaso"
        return taso
    elif len(tila["kentta"]) == 24:
        taso = "Vaikea"
        return taso
    else:
        taso = "Custom"
        return taso

def tallenna_tulos(temp):
    """Tallentaa tulokset tilastoihin."""
    vuorot = len(tila["vuorot"])
    aika = round(lopeta_aika(), 1)
    t = time.localtime()
    pvm = f"{t[2]}.{t[1]}.{t[0]} {t[3]}:{t[4]}"
    loppu = temp
    taso = tarkista_vaikeus()
    tulos = "{}, {}, Aika: {}s, Vuorot: {}, {}".format(pvm, taso, aika, vuorot, loppu)
    with open("tulokset.txt", "a") as kohde:
        kohde.write("{}\n".format(tulos))

def nayta_top(vaikeustaso, lkm):
    tulokset = []
    tiedosto = "tulokset.txt"
    with open(tiedosto) as lahde:
        x = lkm
        for rivi in lahde:
            if vaikeustaso in rivi:
                if rivi.strip().endswith("Voitto"):
                    tulokset.append(rivi.strip().split(","))
            if vaikeustaso == "Kaikki":
                tulokset.append(rivi.strip().split(","))
    if lkm >= len(tulokset):
        lkm = len(tulokset)
    if vaikeustaso == "Kaikki":
        print(f"Viimeisimmat {lkm} tulosta:")
        tulokset.reverse()
        for i in range(lkm):
            pvm, taso, aika, vuorot, loppu = tulokset[i]
            print("{:<17} {:<15} {:<14} {:<13} {:<14}".format(pvm, taso, aika, vuorot, loppu))
        return
    if len(tulokset) != 0:
        print(f"Top 5 tulokset vaikeustasolla: {vaikeustaso}.")
    else:
        print(f"Ei tuloksia vaikeustasolla: {vaikeustaso}.")
    for i in sorted(tulokset, key=lambda temp:
            float(temp[2].replace(" Aika: ", "").replace("s", ""))):
        if x <= 0:
            break
        x -= 1
        pvm, taso, aika, vuorot, loppu = i
        print("{:<17} {:<15} {:<14} {:<13} {:<14}".format(pvm, taso, aika, vuorot, loppu))
                
                
def tarkista_voitto():
    if tila["loppu"] is False:
        l = []
        k = []
        for y, lista in enumerate(tila["luukut"]):
            for x, alkio in enumerate(lista):
                if alkio in {"jj", "1", "2", "3"}:
                    l.append((x, y))
        for y, lista in enumerate(tila["kentta"]):
            for x, alkio in enumerate(lista):
                if alkio in {"jj", "1", "2", "3"}:
                    k.append((x, y))
        if set(l) == set(k) == set(tila["vapaat_ruudut"]):
            vuorot = len(tila["vuorot"])
            print("Voitit pelin!")
            print("Aikasi oli {:.1f} sekuntia! Vuoroja kului: {}".format(lopeta_aika(), vuorot))
            piirra_kentta()
            tallenna_tulos("Voitto")
            tila["loppu"] = True
            return True             
        else:
            return False
    
def tarkista_havio(x, y):
    if tila["loppu"] is False:
        if tila["kentta"][y][x] == "x":
            print("Hävisit pelin :(")
            tila["luukut"] = tila["kentta"]
            piirra_kentta()
            tallenna_tulos("Havio")
            return True
        else:
            return False
    
def aloita_aika():
    tila["alku"] = time.time()

def lopeta_aika():
    lopetus_aika = time.time()
    kulunut_aika = lopetus_aika - tila["alku"]
    return kulunut_aika
    
def main():
    alkuvalikko()
    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna(len(tila["luukut"][0] * 40), len(tila["luukut"] * 40))
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aseta_hiiri_kasittelija(hiiri_kasittelija)
    aloita_aika()
    haravasto.aloita()

if __name__ == "__main__":
    main()
