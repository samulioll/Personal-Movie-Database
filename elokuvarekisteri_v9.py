from imdb import Cinemagoer
from datetime import datetime, timedelta
ia = Cinemagoer()




class Ohjaaja:
    def __init__(self, nimi: str):
        self._nimi = nimi
        self._elokuvat = []
    
    def lisaa_elokuva(self, elokuva: tuple):
        self._elokuvat.append(elokuva)
    
    #Palauttaa ohjaajan elokuvan, jolla on korkein käyttäjäarvio
    def paras_elokuva(self):
        try:
            paras = ""
            parhaan_arvo = 0
            for elokuva in self._elokuvat:
                if elokuva[1] > parhaan_arvo:
                    paras = elokuva[0]
                    parhaan_arvo = elokuva[1]
            return (paras, parhaan_arvo)
        except:
            pass

    #Palauttaa ohjaajan elokuvien käyttäjäarvioiden keskiarvion
    def elokuvien_keskiarvo(self):
        try:
            arvot = []
            for elokuva in self._elokuvat:
                arvot.append(elokuva[1])
            keskiarvo = sum(arvot) / len(arvot)
            return keskiarvo
        except:
            pass




class Genre:
    def __init__(self, nimi: str):
        self._nimi = nimi
        self._elokuvat = []

    def lisaa_elokuva(self, elokuva: tuple):
        self._elokuvat.append(elokuva)
    
    #Palauttaa genren elokuvan, jolla on korkein käyttäjäarvio   
    def paras_elokuva(self):
        try:
            paras = ""
            parhaan_arvo = 0
            for elokuva in self._elokuvat:
                if elokuva[1] > parhaan_arvo:
                    paras = elokuva[0]
                    parhaan_arvo = elokuva[1]
            return (paras, parhaan_arvo)
        except:
            pass

    #Palauttaa genren elokuvien käyttäjäarvioiden keskiarvion
    def elokuvien_keskiarvo(self):
        try:
            arvot = []
            for elokuva in self._elokuvat:
                arvot.append(elokuva[1])
            keskiarvo = sum(arvot) / len(arvot)
            return keskiarvo
        except:
            pass




class Elokuva:
    def __init__(self, id: str, nimi: str, arvosana: float, imdb: float, vuosi: int, pituus: int, ohjaajat: list, genret: list, arvioitu: str):
        self._tunnus = id
        self._nimi = nimi
        self._oma_arvosana = round(arvosana, 2)
        self._imdb_arvosana = round(imdb, 2)
        self._julkaisuvuosi = vuosi
        self._pituus = pituus
        self._ohjaajat = ohjaajat
        self._genret = genret
        self._arvio_pvm = arvioitu


    #Apufunktio
    def pituus(self):
        tunnit = int(self._pituus) // 60
        minuutit = int(self._pituus) % 60
        return f"{tunnit}h {minuutit:02d}min"


    #Apufunktio
    def pisin_nimi_pituus(self):
        pisin = ""
        for elokuva in self._elokuvat:
            if len(elokuva._nimi) > pisin:
                pisin = elokuva._nimi
        return len(pisin)
    

    #Tulostetaan elokuvan tiedot halutussa muodossa.
    def __str__(self):
        palautus = []
        palautus.append(f"Oma: {self._oma_arvosana:>4} IMDb: {self._imdb_arvosana:>4} Arvioitu {self._arvio_pvm:10}  || ")
        palautus.append(f"{self._nimi:45} ({self._julkaisuvuosi}), {self.pituus():10}|| ")
        if len(self._ohjaajat) == 1:
            palautus.append(f"Ohjaaja:  {self._ohjaajat[0]:30}")
        else:
            palautus.append(f"Ohjaajat: {', '.join(self._ohjaajat):30}")
        if len(self._genret) == 1:
            palautus.append(f"Genre: {self._genret:45}")
        else:
            palautus.append(f"Genret: {', '.join(self._genret):55}")
        palautus.append(f"(id: {self._tunnus})")
        return " ".join(palautus)




class Leffa_arkisto:
    versio = 9

    print("")
    print("")
    print("¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤")
    print("Elokuva-arkisto - versio " + str(versio))
    print("¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤")
    print("")
    print("")
    kayttaja = input("Käyttäjänimi: ")

    pvm = datetime.today()
    pvm_str = pvm.strftime("%Y-%m-%d_%H:%M:%S")
    tallennusosoite = "/home/samollik/Documents/Personal python projects/Elokuvarekisteri/"
    varmuuskopionimi = tallennusosoite + "elokuvarekisteri_v" + str(versio) + "_" + kayttaja + "_varmuuskopio_" + pvm_str + ".csv"
    vanha_tiedostonimi = tallennusosoite + "elokuvarekisteri_v" + str((versio - 1)) + "_" + kayttaja + ".csv"
    tiedostonimi = tallennusosoite + "elokuvarekisteri_v" + str(versio) + "_" + kayttaja + ".csv"


    def __init__(self):
        self._elokuvat = []
        self._ohjaajat = []
        self._genret = []


    # 0.1 - Lataa elokuvat tiedostolta.
    def lataa_tiedosto(self):
        #Kokeile ladata nykyisen version tiedostoa oikealta käyttäjältä
        try:
            with open(Leffa_arkisto.tiedostonimi, "r") as tiedosto:
                for rivi in tiedosto:
                    rivi = rivi.strip()
                    tiedot = rivi.split(";")
                    tunnus = tiedot[0]
                    nimi = tiedot[1]
                    oma_arvio = float(tiedot[2])
                    imdb_arvio = float(tiedot[3])
                    vuosi = tiedot[4]
                    pituus = tiedot[5]
                    ohjaajat = self.palauta_listana(tiedot[6])
                    genret = self.palauta_listana(tiedot[7])
                    pvm = tiedot[8]

                    leffa = Elokuva(tunnus, nimi, oma_arvio, imdb_arvio, vuosi, pituus, ohjaajat, genret, pvm)
                    self._elokuvat.append(leffa)
                print("")
                if len(self._elokuvat) > 1:
                    print(f"(Ladattiin {len(self._elokuvat)} elokuvaa.)")
                else:
                    print(f"(Ladattiin {len(self._elokuvat)} elokuva.)")
        except:
            #Jos nykyisen version tiedostoa ei ole, kokeile ladata edellisen version tiedosto oikealta käyttäjältä
            try:
                with open(Leffa_arkisto.vanha_tiedostonimi, "r") as tiedosto:
                    for rivi in tiedosto:
                        rivi = rivi.strip()
                        tiedot = rivi.split(";")
                        tunnus = tiedot[0]
                        nimi = tiedot[1]
                        oma_arvio = float(tiedot[2])
                        imdb_arvio = float(tiedot[3])
                        vuosi = tiedot[4]
                        pituus = tiedot[5]
                        ohjaajat = self.palauta_listana(tiedot[6])
                        genret = self.palauta_listana(tiedot[7])
                        pvm = tiedot[8]

                        leffa = Elokuva(tunnus, nimi, oma_arvio, imdb_arvio, vuosi, pituus, ohjaajat, genret, pvm)
                        self._elokuvat.append(leffa)
                    if len(self._elokuvat) > 1:
                        print(f"(Ladattiin {len(self._elokuvat)} elokuvaa.)")
                    else:
                        print(f"(Ladattiin {len(self._elokuvat)} elokuva.)")
            except:
                #Jos aiemmat eivät toimi, niin silloin annetulla käyttäjänimellä ei ole olemassa arkistoa
                print("")
                print("")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("! Ei löytynyt arkistoa hakemallasi käyttäjänimellä !")
                print("")
                print("          * Luotiin uusi arkisto. *")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("")  


    # 0.2 - Lataa tiedot ohjaajista ohjaaja-olioihin
    def lataa_ohjaajat(self):
        lista_ohjaajista = []
        for elokuva in self._elokuvat:
            for ohjaaja in elokuva._ohjaajat:
                lista_ohjaajista.append(ohjaaja)
        for ohjaaja in set(lista_ohjaajista):
            self._ohjaajat.append(Ohjaaja(ohjaaja))
        for ohjaaja in self._ohjaajat:
            for elokuva in self._elokuvat:
                if ohjaaja._nimi in elokuva._ohjaajat:
                    ohjaaja.lisaa_elokuva((elokuva._nimi, elokuva._oma_arvosana))


    # 0.3 - Lataa tiedot genreistä genre-olioihin
    def lataa_genret(self):
        lista_genreista = []
        for elokuva in self._elokuvat:
            for genre in elokuva._genret:
                lista_genreista.append(genre)
        for genre in set(lista_genreista):
            self._genret.append(Genre(genre))
        for genre in self._genret:
            for elokuva in self._elokuvat:
                if genre._nimi in elokuva._genret:
                    genre.lisaa_elokuva((elokuva._nimi, elokuva._oma_arvosana))


    # 0.4 - Sovellukset komento-ohjeet.
    def ohje(self):
        montako = len(f"Käyttäjän {Leffa_arkisto.kayttaja} Elokuva-arkisto - versio {str(Leffa_arkisto.versio)}")
        apu2 = len(f"Elokuvia arkistossa: {len(self._elokuvat)}")
        sisennys = (montako - apu2) // 2   
        print("")
        print("")
        print(montako * "¤")
        print(f"Käyttäjän {Leffa_arkisto.kayttaja} Elokuva-arkisto - versio {str(Leffa_arkisto.versio)}")
        print(montako * "¤")
        print(f"{sisennys * ' '}Elokuvia arkistossa: {len(self._elokuvat)}")
        print("")
        print("Komennot:")
        print("---------------------")
        print("1 - (Lisää arvostelu)")
        print("2 - (Etsi elokuva)")
        print("3 - (Listaa elokuvat)")
        print("4 - (Tilastot)")
        print("5 - (Haku parametreilla)")
        print("")
        print("v - (Varmuuskopioi)")
        print("d - (Tyhjennä tiedosto)")
        print("x - (Lopeta)")
        print("- - - - - - - - - - -")
        print("")


    # 1.0 - Arkiston pääsovellusrakenne
    def sovellus(self):
        self.lataa_tiedosto()
        self.lataa_ohjaajat()
        self.lataa_genret()
        while True:
            self.ohje()
            #print("")
            #print("To Do: Lisää haku pituuden mukaan")
            #print("")
            syote = input("Komento: ")
            if syote == "x":
                self.tallenna_tiedosto()
                self.tulosta_korostettu("Tiedosto tallennettu ja ohjelma suljetaan.")
                exit()
            elif syote == "1":
                print("")
                self.lisaa_arvostelu()
            elif syote == "2":
                print("")
                self.etsi_elokuva()
            elif syote == "3":
                print("")
                self.listaa_elokuvat()
            elif syote == "4":
                self.tilastot()
            elif syote == "5":
                self.haku_parametreilla()
            elif syote == "v":
                self.varmuuskopioi()
            elif syote == "d":
                self.tyhjenna_tiedosto()
            #Testauskomento
            elif syote == "t":
                self.testi_haku_parametreilla()


    # 1.1 - Lisää arkistoon arvostelun
    def lisaa_arvostelu(self):
        self.tulosta_otsikko("Lisää arvostelu:")
        haku = input("Elokuvan nimi: ")
        print("Hakee...")
        print("")
        while True:
            try:
                tulokset = ia.search_movie(haku)
            except:
                continue
            #Jos tulokset ei ole totta, tarkoittaa se että dataa ei saatu haettua IMDb-palvelimelta. Yritetään uudestaan kunnes tulokset saadaan.
            if not tulokset:
                continue
            for elokuva in tulokset:
                print("")
                print(f"Tarkoititko {elokuva['title']} ({elokuva['year']})")
                print(len(f"Tarkoititko {elokuva['title']} ({elokuva['year']})")*"~")
                syote = input("Kyllä (y)     Ei (n)     Peruuta (c)")
                if syote == "y":
                    print("")
                    arvosana = self.anna_arvosana()
                    loytyy = False
                    #Jos elokuva on jo tietokannassa:
                    for raina in self._elokuvat:
                        if raina._tunnus == elokuva.movieID:
                            loytyy = True
                            vanha = raina._oma_arvosana
                            raina._oma_arvosana = arvosana
                            print("")
                            print(len(f"Elokuvan {raina._nimi} arvosana muutettu {vanha} -> {arvosana}.") * "~")
                            print(f"Elokuvan {raina._nimi} arvosana muutettu {vanha} -> {arvosana}.")
                            print(len(f"Elokuvan {raina._nimi} arvosana muutettu {vanha} -> {arvosana}.") * "~")
                            break
                    #Jos elokuva ei vielä ole tietokannassa:
                    if loytyy == False:
                        print("Odota...")
                        while True:
                            leffa = ia.get_movie(elokuva.movieID)
                            if not leffa:
                                continue
                            else:
                                try:
                                    ohjaajat = []
                                    for director in leffa['directors']:
                                        ohjaajat.append(director['name'])
                                    genret = []
                                    for genre in leffa['genres']:
                                        genret.append(genre)
                                    pvm = datetime.today()
                                    pvm_str = pvm.strftime("%d/%m/%Y")
                                    self._elokuvat.append(Elokuva(leffa.movieID, str(leffa['title']), arvosana, float(leffa['rating']), leffa['year'], leffa['runtime'][0], ohjaajat, genret, pvm_str))
                                    print("")
                                    print(len(f"{leffa} lisätty arkistoon!") * "~")
                                    print(f"{leffa} lisätty arkistoon!")
                                    print(len(f"{leffa} lisätty arkistoon!") * "~")
                                    break
                                except:
                                    print("Tapahtui virhe")
                                    break
                        break
                    break
                if syote == "c":
                    break
            break


    # 1.2 - Etsii tietokannasta käyttäjän hakeman elokuvan tiedot, jos se on arvosteltu.
    def etsi_elokuva(self):
        if len(self._elokuvat) == 0:
            print("")
            print("Et ole vielä arvostellut yhtään elokuvaa.")
        else:
            self.tulosta_otsikko("Etsi elokuva:")
            haku = input("Elokuvan nimi: ")
            print("Hakee...")
            print("")
            while True:
                tulokset = ia.search_movie(haku)
                #Jos tulokset ei ole totta, tarkoittaa se että dataa ei saatu haettua iMDB-palvelimelta. Yritetään uudestaan kunnes tulokset saadaan.
                if not tulokset:
                    continue
                for leffa in tulokset:
                    elokuvan_id = leffa.movieID
                    print(f"Tarkoititko {leffa['title']} ({leffa['year']})")
                    print(len(f"Tarkoititko {leffa['title']} ({leffa['year']})")*"~")
                    syote = input("Kyllä (y)     Ei (n)     Peruuta (c)")
                    if syote == "y":
                        print("")
                        print("")
                        loytyi = False
                        for elokuva in self._elokuvat:
                            if elokuva._tunnus == elokuvan_id:
                                self.tulosta_korostettu("Elokuvan tiedot:")
                                print(elokuva)
                                loytyi = True
                                break
                        if loytyi == False:
                            print("Et ole vielä arvostellut tätä elokuvaa.")
                        break
                    if syote == "c":
                        break
                break


    # 1.3 - Listataan tietokannassa olevat arvostellut elokuvat järjestettynä annetun parametrin mukaan.
    def listaa_elokuvat(self):
        def arvosanajarjestys(leffa: Elokuva):
            return leffa._oma_arvosana     
        def imdb_jarjestys(leffa: Elokuva):
            return leffa._imdb_arvosana 
        def nimijarjestys(leffa: Elokuva):
            return leffa._nimi
        def pvm_jarjestys(leffa: Elokuva):
            return leffa._arvio_pvm
        def vuosijarjestys(leffa: Elokuva):
            return leffa._julkaisuvuosi
        def pituusjarjestys(leffa: Elokuva):
            return int(leffa._pituus)
        if len(self._elokuvat) == 0:
            self.tulosta_korostettu("Et ole vielä arvotellut yhtään elokuvaa")
        else:
            self.tulosta_otsikko("Arvostellut elokuvat:")
            while True:
                print("")
                print("---------------------------------")
                print("Järjestä elokuvat: ")
                print("")
                print("1 - Oman arvosanan mukaan")
                print("2 - iMDb arvosanan mukaan")
                print("3 - Aakkosjärjestyksessä")
                print("4 - Arvostelun päivämäärän mukaan")
                print("5 - Julkaisuvuoden mukaan")
                print("6 - Pituuden mukaan")
                print("")
                print("c - Palaa päävalikkoon")
                print("- - - - - - - - - - - - - - - - -")
                print("")
                peruste = input("Komento: ")
                if peruste == "1":
                    self.tulosta_otsikko("Arvostellut elokuvat:")
                    print("      ~¤~")
                    for elokuva in sorted(self._elokuvat, key=arvosanajarjestys, reverse=True):
                        print(elokuva)
                elif peruste == "2":
                    self.tulosta_otsikko("Arvostellut elokuvat:")
                    print("                 ~¤~")
                    for elokuva in sorted(self._elokuvat, key=imdb_jarjestys, reverse=True):
                        print(elokuva)
                elif peruste == "3":
                    self.tulosta_otsikko("Arvostellut elokuvat:")
                    print("                                                ~¤~")
                    for elokuva in sorted(self._elokuvat, key=nimijarjestys):
                        print(elokuva)
                elif peruste == "4":
                    self.tulosta_otsikko("Arvostellut elokuvat:")
                    print("                                   ~¤~")
                    for elokuva in sorted(self._elokuvat, key=pvm_jarjestys, reverse=True):
                        print(elokuva)
                elif peruste == "5":
                    self.tulosta_otsikko("Arvostellut elokuvat:")
                    print("                                                                                    ~¤~")
                    for elokuva in sorted(self._elokuvat, key=vuosijarjestys, reverse=True):
                        print(elokuva)
                elif peruste == "6":
                    self.tulosta_otsikko("Arvostellut elokuvat:")
                    print("                                                                                                   ~¤~")
                    for elokuva in sorted(self._elokuvat, key=pituusjarjestys, reverse=True):
                        print(elokuva)
                elif peruste == "c":
                    break


    # 1.4 - Tilastojen alisovellus
    def tilastot(self):
        if len(self._elokuvat) == 0:
            self.tulosta_korostettu("Et ole vielä arvostellut yhtään elokuvaa")
            pass
        self.tulosta_otsikko("Arkiston tilastot")
        #Silmukka jonka sisällä valitaan mitkä tilastot halutaan tulostaa.
        while True:
            print("")
            print("-----------------------")
            print("1 - Yleiset tilastot ")
            print("2 - Ohjaajat")
            print("3 - Genret")
            print("")
            print("c - Palaa päävalikkoon")
            print("- - - - - - - - - - - -")
            print("")
            syote = input("Komento: ")
            if syote == "c":
                break
            elif syote == "1":
                self.yleis_tilastot()
            elif syote == "2":
                self.ohjaaja_tilastot()
            elif syote == "3":
                self.genre_tilastot()


    # 1.4.1 - Tulostetaan yleiset tilastot arvostelluista elokuvista.
    def yleis_tilastot(self):  
        arvosteluja = 0
        omat_arvosanat = 0
        imdb_arvosanat = 0
        kaikki_genret = []
        kaikki_ohjaajat = []

        for elokuva in self._elokuvat:
            arvosteluja += 1
            omat_arvosanat += elokuva._oma_arvosana
            imdb_arvosanat += elokuva._imdb_arvosana
            for genre in elokuva._genret:
                kaikki_genret.append(genre)
            for ohjaaja in elokuva._ohjaajat:
                kaikki_ohjaajat.append(ohjaaja)
        
        yleisin_genre = self.yleisin_genre(kaikki_genret)
        yleisin_ohjaaja = self.yleisin_ohjaaja(kaikki_ohjaajat)
        paras_genre = self.paras_huonoin_genre("paras")
        paras_ohjaaja = self.paras_huonoin_ohjaaja("paras")
        paras_elokuva = self.paras_huonoin_elokuva("paras")
        huonoin_elokuva = self.paras_huonoin_elokuva("huonoin")
        suurin_ero = self.arvio_erot("suurin")
        pienin_ero = self.arvio_erot("pienin")
        combo = self.palauta_combot()
        paras_combo = combo[0]
        paras_combo_tekstina = f"{paras_combo[0]}"
        huonoin_combo = combo[-1]
        huonoin_combo_tekstina = f"{huonoin_combo[0]}"
        isoin_ero = round(suurin_ero[1],2)
        pikku_ero = round(pienin_ero[1], 2)
        self.tulosta_otsikko("Yleiset tilastot:")
        print(f"Elokuvia arvioitu: {arvosteluja}")
        print(f"Omien arvosanojen keskiarvo: {omat_arvosanat / arvosteluja: .2f}               || Paras elokuva:   {paras_elokuva[0]:35} {paras_elokuva[1]:.2f}  ||", end="")
        print(f"   Suurin ero vrt. IMDb: {suurin_ero[0]:35} {isoin_ero:5}")
        print(f"iMDb arvosanojen keskiarvo:  {imdb_arvosanat / arvosteluja: .2f}               || Huonoin elokuva: {huonoin_elokuva[0]:35} {huonoin_elokuva[1]:.2f}   ||", end="")
        print(f"   Pienin ero vrt. IMDb: {pienin_ero[0]:35} {pikku_ero:5}")
        print("")
        yleisin_genre_pituus = len(f"Yleisin genre: {yleisin_genre[0]}, {yleisin_genre[1]} elokuvaa.")
        paras_genre_pituus = len(f"Paras genre: {paras_genre[0]} {paras_genre[1]}")
        print(f"Yleisin genre:   {yleisin_genre[0]}, {yleisin_genre[1]} elokuvaa. {(46 - yleisin_genre_pituus) * ' '}|| Paras genre:     {paras_genre[0]:35} {paras_genre[1]:.2f}   ||", end="")
        print(f"   Paras yhdistelmä:     {paras_combo_tekstina:35} {paras_combo[1]:>5}")
        yleisin_ohjaaja_pituus = len(f"Yleisin ohjaaja: {yleisin_ohjaaja[0]}, {yleisin_ohjaaja[1]} elokuvaa.")
        paras_ohjaaja_pituus = len(f"Paras ohjaaja: {paras_ohjaaja[0]} {paras_ohjaaja[1]}")
        print(f"Yleisin ohjaaja: {yleisin_ohjaaja[0]}, {yleisin_ohjaaja[1]} elokuvaa. {(48 - yleisin_ohjaaja_pituus) * ' '}|| Paras ohjaaja:   {paras_ohjaaja[0]:35} {paras_ohjaaja[1]:.2f}   ||", end="")
        print(f"   Huonoin yhdistelmä:   {huonoin_combo_tekstina:35} {huonoin_combo[1]:>5}")
        print("")


    # 1.4.2 - Tulostaa kaikki arkistossa olevat ohjaajat arvosanakeskiarvon mukaan järjestettynä.
    def ohjaaja_tilastot(self):
        def keskiarvon_mukaan(ohjaaja: Ohjaaja):
            return ohjaaja.elokuvien_keskiarvo()
        indeksi = 1
        self.tulosta_otsikko("Tilastoja ohjaajista:")
        print("#  Nimi                       Ka.    Elokuvia")
        print("¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨")
        for ohjaaja in sorted(self._ohjaajat, key=keskiarvon_mukaan, reverse=True):
            print(f"{indeksi:<2} {ohjaaja._nimi:25} {ohjaaja.elokuvien_keskiarvo():.2f}       {len(ohjaaja._elokuvat):2}")
            indeksi += 1


    # 1.4.3 - Tulostaa kaikki arkistossa olevat genret arvosanakeskiarvon mukaan järjestettynä.
    def genre_tilastot(self):
        def keskiarvon_mukaan(genre: Genre):
            return genre.elokuvien_keskiarvo()
        indeksi = 1
        self.tulosta_otsikko("Tilastoja genreistä:")
        print("#  Genre            Ka.    Elokuvia")
        print("¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨")
        for genre in sorted(self._genret, key=keskiarvon_mukaan, reverse=True):
            print(f"{indeksi:<2} {genre._nimi:15} {genre.elokuvien_keskiarvo():.2f}       {len(genre._elokuvat):2}")
            indeksi += 1


    # 1.5 - Haku parametreilla
    def haku_parametreilla(self):
        def arvosananmukaan(leffa: Elokuva):
            return leffa._oma_arvosana
        if len(self._elokuvat) == 0:
            self.tulosta_korostettu("Et ole vielä arvostellut yhtään elokuvaa")
            pass
        lopeta = False
        while True:
            self.tulosta_otsikko("Hae parametreilla")
            #alkuparametrit jotka täyttyvät kaikilla elokuvilla. Täten alkutilanteessa tulostetaan kaikki elokuvat.
            oma_arvosana_yli = -1
            oma_arvosana_alle = 11
            imdb_arvosana_yli = -1
            imdb_arvosana_alle = 11
            arvosteltu_myohemmin = datetime(1, 1, 1)
            arvosteltu_aiemmin = datetime(3000, 1, 1)
            julkaistu_myohemmin = 1
            julkaistu_aiemmin = 3000
            nimi_sisaltaa = ""
            ohjaajan_nimi_sisaltaa = ""
            genret = []
            elokuvan_pituus_yli = 0
            elokuvan_pituus_alle = 1000
            #Silmukka jonka sisällä hakutulokset tulostetaan ja hakuparametreja voi muokata.
            while True:
                print("")
                print("Valitse parametrit")
                print("")
                print("-------------------------")
                print("1 - Oma arvosana ")
                print("2 - IMDb arvosana")
                print("3 - Arvostelun päivämäärä")
                print("4 - Elokuvan nimi")
                print("5 - Julkaisuvuosi")
                print("6 - Ohjaajan nimi")
                print("7 - Genre")
                print("8 - Elokuvan pituus")
                print("")
                print("0 - Nollaa parametrit")
                print("c - Palaa päävalikkoon")
                print("- - - - - - - - - - - - -")
                print("")
                print("")
                syote = input("Komento: ")
                #Lisää hakuehto omalle arvosanalle
                if syote == "1":
                    print("Anna parametri muodossa >|< arvosana")
                    print("")
                    syote = input("Parametri: ")
                    print("")
                    try:
                        osat = syote.split(" ")
                        if osat[0] == ">":
                            oma_arvosana_yli = float(osat[1])
                        elif osat[0] == "<":
                            oma_arvosana_alle = float(osat[1])
                        else:
                            self.tulosta_korostettu("Virheellinen parametri")
                    except:
                        self.tulosta_korostettu("Virheellinen parametri")
                        pass
                #Lisää hakuehto IMDb-arvosanalle
                elif syote == "2":
                    print("Anna parametri muodossa >|< arvosana")
                    print("")
                    syote = input("Parametri: ")
                    print("")
                    try:
                        osat = syote.split(" ")
                        if osat[0] == ">":
                            imdb_arvosana_yli = float(osat[1])
                        elif osat[0] == "<":
                            imdb_arvosana_alle = float(osat[1])
                        else:
                            self.tulosta_korostettu("Virheellinen parametri")
                    except:
                        self.tulosta_korostettu("Virheellinen parametri")
                        pass
                #Lisää päivämäärä hakuehdoksi
                elif syote == "3":
                    print("Anna parametri muodossa >|< dd/mm/yyyy")
                    print("")
                    syote = input("Parametri: ")
                    print("")
                    try:
                        osat = syote.split(" ")
                        if osat[0] == ">":
                            arvosteltu_myohemmin = datetime.strptime(osat[1], "%d/%m/%Y")
                        elif osat[0] == "<":
                            arvosteltu_aiemmin = datetime.strptime(osat[1], "%d/%m/%Y")
                        else: 
                            self.tulosta_korostettu("Virheellinen parametri")
                    except:
                        self.tulosta_korostettu("Virheellinen parametri")
                        pass
                #Lisää hakuehto elokuvan nimelle
                elif syote == "4":
                    print("Anna merkkijono jota haet elokuvien nimistä")
                    print("")
                    nimi_sisaltaa = input("Merkkijono: ")
                elif syote == "5":
                    print("Anna parametri muodossa >|< yyyy")
                    print("")
                    syote = input("Parametri: ")
                    try:
                        osat = syote.split(" ")
                        if osat[0] == ">":
                            julkaistu_myohemmin = int(osat[1])
                        elif osat[0] == "<":
                            julkaistu_aiemmin = int(osat[1])
                        else:
                            self.tulosta_korostettu("Virheellinen parametri")
                    except:
                        self.tulosta_korostettu("Virheellinen parametri")
                #Lisää hakuehto ohjaajan nimelle
                elif syote == "6":
                    print("Anna merkkijono jota haet ohjaajien nimistä")
                    print("")
                    ohjaajan_nimi_sisaltaa = input("Merkkijono: ")
                #Lisää haluttu genre parametreihin
                elif syote == "7":
                    print("Anna genre jonka haluat löytyvän elokuvasta")
                    print("")
                    syote = input("Genre: ")
                    genret.append(syote.lower())
                #Lisää haluttu elokuvan pituus parametreihin
                elif syote == "8":
                    print("Anna parametri muodossa >|< minuutit")
                    print("")
                    syote = input("Parametri: ")
                    print("")
                    try:
                        osat = syote.split(" ")
                        if osat[0] == ">":
                            elokuvan_pituus_yli = float(osat[1])
                        elif osat[0] == "<":
                            elokuvan_pituus_alle = float(osat[1])
                        else:
                            self.tulosta_korostettu("Virheellinen parametri")
                    except:
                        self.tulosta_korostettu("Virheellinen parametri")
                        pass

                #Tyhjentää hakuehdot
                elif syote == "0":
                    self.tulosta_korostettu("Parametrit nollattu")
                    break
                elif syote == "c":
                    lopeta = True
                    break
                #Elokuvien tulostus annetuilla parametreillä
                alku_arvio = ""
                loppu_arvio = ""
                alku_imdb = ""
                loppu_imdb = ""
                alku_pvm = ""
                loppu_pvm = ""
                nimihaku = ""
                alku_vuosi = ""
                loppu_vuosi = ""
                ohjaajahaku = ""
                genrehaku = []
                alku_pituus = ""
                loppu_pituus = ""
                #Jos parametreille on annettu käyttäjäarvot niin vaihdetaan tulostettavien arvojen paikalle
                if oma_arvosana_yli > -1:
                    alku_arvio = str(oma_arvosana_yli)
                if oma_arvosana_alle < 11:
                    loppu_arvio = str(oma_arvosana_alle)
                if imdb_arvosana_yli > -1:
                    alku_imdb = str(imdb_arvosana_yli)
                if imdb_arvosana_alle < 11:
                    loppu_imdb = str(imdb_arvosana_alle)
                if arvosteltu_myohemmin > datetime(1, 1, 1):
                    alku_pvm = datetime.strftime(arvosteltu_myohemmin, "%d/%m/%Y")
                if arvosteltu_aiemmin < datetime(3000, 1, 1):
                    loppu_pvm = datetime.strftime(arvosteltu_aiemmin, "%d/%m/%Y")
                if len(nimi_sisaltaa) > 0:
                    nimihaku = nimi_sisaltaa
                if julkaistu_myohemmin > 1:
                    alku_vuosi = julkaistu_myohemmin
                if julkaistu_aiemmin < 3000:
                    loppu_vuosi = julkaistu_aiemmin
                if len(ohjaajan_nimi_sisaltaa) > 0:
                    ohjaajahaku = ohjaajan_nimi_sisaltaa
                if len(genret) > 0:
                    genrehaku = genret
                if elokuvan_pituus_yli > 0:
                    alku_pituus = (f"{str(elokuvan_pituus_yli)} min")
                if elokuvan_pituus_alle < 1000:
                    loppu_pituus = (f"{str(elokuvan_pituus_alle)} min")
                #Hakuparametrien tulostusmuodon luominen
                if len(alku_arvio) > 0 or len(loppu_arvio) > 0:
                    tulostus_oma_arvosana = f"{alku_arvio} < Oma arvosana < {loppu_arvio}"
                if len(alku_imdb) > 0 or len(loppu_imdb) > 0:
                    tulostus_imdb_arvosana = f"{alku_imdb} < IMDb-arvosana < {loppu_imdb}"
                if len(alku_pvm) > 0 or len(loppu_pvm) > 0:
                    tulostus_pvm = f"{alku_pvm} < Arvostelun pvm < {loppu_pvm}"
                if len(nimihaku) > 0:
                    tulostus_nimihaku = f"Nimihaku: {nimihaku}"
                try:
                    if alku_vuosi > 0 or loppu_vuosi > 0:
                        tulostus_julkaisuvuosi = f"{alku_vuosi} < Julkaisuvuosi < {loppu_vuosi}"
                except:
                    pass
                if len(ohjaajahaku) > 0:
                    tulostus_ohjaajahaku = f"Ohjaajahaku: {ohjaajahaku}"
                if len(genrehaku) > 0:
                    tulostus_genrehaku = f"Genret: {', '.join(genrehaku)}"
                if len(alku_pituus) > 0 or len(loppu_pituus) > 0:
                    tulostus_pituus = f"{alku_pituus} < Pituus < {loppu_pituus}"
                #Hakuparametrien tulostus
                self.tulosta_otsikko("Hae parametreilla")
                print("Hakuparametrit: ")
                print("¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨")
                if len(alku_arvio) > 0 or len(loppu_arvio) > 0:
                    print(f"{tulostus_oma_arvosana:30} ||  ", end="")
                if len(alku_imdb) > 0 or len(loppu_imdb) > 0:
                    print(f"{tulostus_imdb_arvosana:30} ||  ", end="")
                if len(alku_pvm) > 0 or len(loppu_pvm) > 0:
                    print(f"{tulostus_pvm:30} ||  ", end="")
                if len(nimihaku) > 0:
                    print(f"{tulostus_nimihaku:30} ||  ", end="")
                try:
                    if alku_vuosi > 0 or loppu_vuosi > 0:
                        print(f"{tulostus_julkaisuvuosi:30} ||  ", end="")
                except:
                    pass
                if len(ohjaajahaku) > 0:
                    print(f"{tulostus_ohjaajahaku:30} ||  ", end="")
                if len(genrehaku) > 0:
                    print(f"{tulostus_genrehaku:30} ||  ", end="")
                if len(alku_pituus) > 0 or len(loppu_pituus) > 0:
                    print(f"{tulostus_pituus:30} ||  ", end="")
                print("")
                print("")
                print("")
                #Jos kaikki parametrit täyttyvät, niin tulosta elokuva
                for elokuva in sorted(self._elokuvat, key=arvosananmukaan, reverse=True):
                    if oma_arvosana_yli < elokuva._oma_arvosana < oma_arvosana_alle:
                        if imdb_arvosana_yli < elokuva._imdb_arvosana < imdb_arvosana_alle:
                            arvioinnin_pvm = elokuva._arvio_pvm
                            pvm_datetime = datetime.strptime(arvioinnin_pvm, "%d/%m/%Y")
                            if arvosteltu_myohemmin < pvm_datetime < arvosteltu_aiemmin:
                                if nimi_sisaltaa.lower() in elokuva._nimi.lower():
                                    elokuvan_ohjaajat = ""
                                    for ohjaaja in elokuva._ohjaajat:
                                        elokuvan_ohjaajat += str(ohjaaja.lower())
                                    if int(julkaistu_myohemmin) < int(elokuva._julkaisuvuosi) < int(julkaistu_aiemmin):
                                        if ohjaajan_nimi_sisaltaa.lower() in elokuvan_ohjaajat:
                                            if len(genret) == 0:
                                                if elokuvan_pituus_yli < int(elokuva._pituus) < elokuvan_pituus_alle:
                                                    print(elokuva)
                                            else:
                                                elokuvan_genret = ""
                                                for genre in elokuva._genret:
                                                    elokuvan_genret += genre.lower()
                                                genret_loytyy = 0
                                                for genre in genret:
                                                    if genre not in elokuvan_genret:
                                                        genret_loytyy += 1
                                                if genret_loytyy == 0:
                                                    if elokuvan_pituus_yli < int(elokuva._pituus) < elokuvan_pituus_alle:
                                                        print(elokuva)         
            if lopeta:
                break


    # 1.V Tallentaa tiedot varmuuskopioon
    def varmuuskopioi(self):
        with open(Leffa_arkisto.varmuuskopionimi, "w") as tiedosto:
            for elokuva in self._elokuvat:
                tunnus = elokuva._tunnus
                nimi = elokuva._nimi
                oma_arvosana = elokuva._oma_arvosana
                imdb_arvosana = elokuva._imdb_arvosana
                vuosi = elokuva._julkaisuvuosi
                pituus = elokuva._pituus
                ohjaajat = "/".join(elokuva._ohjaajat)
                genret = "/".join(elokuva._genret)
                pvm = elokuva._arvio_pvm
                tiedosto.write(f"{tunnus};{nimi};{oma_arvosana};{imdb_arvosana};{vuosi};{pituus};{ohjaajat};{genret};{pvm}\n")
            self.tulosta_korostettu("Varmuuskopio luotu!")


    # 1.D - Tyhjentää tiedoston datasta ja tallentaa ne varmuuskopiona toiseen tiedostoon
    def tyhjenna_tiedosto(self):
        print("")
        print("Haluatko varmasti tyhjentää tiedoston?")
        print("")
        syote1 = input("Kyllä (y):")
        if syote1 == "y":
            print("")
            print("Oletko täysin varma?")
            syote2 = input("Kyllä (k)")
            if syote2 == "k":
                self.varmuuskopioi()
                with open(Leffa_arkisto.tiedostonimi, "w") as tiedosto:
                    pass
                self._elokuvat = []
                self._ohjaajat = []
                self._genret = []
                self.tulosta_korostettu("!Elokuvarekisteri on nyt tyhjä!")


    # 1.X - Kirjoittaa elokuvat .csv tiedostoon.
    def tallenna_tiedosto(self):
        with open(Leffa_arkisto.tiedostonimi, "w") as tiedosto:
            for elokuva in self._elokuvat:
                tunnus = elokuva._tunnus
                nimi = elokuva._nimi
                oma_arvosana = elokuva._oma_arvosana
                imdb_arvosana = elokuva._imdb_arvosana
                vuosi = elokuva._julkaisuvuosi
                pituus = elokuva._pituus
                ohjaajat = "/".join(elokuva._ohjaajat)
                genret = "/".join(elokuva._genret)
                pvm = elokuva._arvio_pvm

                tiedosto.write(f"{tunnus};{nimi};{oma_arvosana};{imdb_arvosana};{vuosi};{pituus};{ohjaajat};{genret};{pvm}\n")




    #Apufunktiot -------------------------------------------------------------------------------------------------------------------------------------------------------------------




    # Apufunktio - Muuttaa merkkijonossa olevat objektit listaksi
    def palauta_listana(self, teksti: str):
        ohjaajat = []
        if "/" in teksti:
            osat = teksti.split("/")
            for osa in osat:
                ohjaajat.append(osa)
        else:
            ohjaajat.append(teksti)
        return ohjaajat

    
    #Apufunktio - Tulostaa alisovelluksen yläotsikon (Annetaan parametrina).
    def tulosta_otsikko(self, otsikko: str):
        print("")
        print("")
        print(len(otsikko) * "¤")
        print(otsikko)
        print(len(otsikko) * "¤")
        print("")

    
    #Apufunktio - Tulostaa korostetun tuloksen
    def tulosta_korostettu(self, teksti: str):
        print("")
        print(len(teksti) * "~")
        print(teksti)
        print(len(teksti) * "~")
        print("")
        print("")
    

    #Apufunktio - Kysyy arvosanaa niin kauan kunnes se on oikeassa muodossa.
    def anna_arvosana(self):
        while True:
            try:
                arvosana = float(input("Anna oma arvosana elokuvalle: "))
                if 0 <= arvosana <= 10:
                    return arvosana
            except:
                print("Anna arvosana numerona välillä 0-10 (desimaalimerkki on .)")           


    #Apufunktio - Palauttaa ohjaajan ja hänen elokuvien lukumäärän, jota on arkistossa eniten
    def yleisin_ohjaaja(self, ohjaajat: list):
        suosituin = ""
        suosituinta = 0
        for ohjaaja in ohjaajat:
            maara = ohjaajat.count(ohjaaja)
            if maara > suosituinta:
                suosituinta = maara
                suosituin = ohjaaja
        return (suosituin, suosituinta)


    #Apufunktio - Palauttaa genren ja sen elokuvien lukumäärän, jota on arkistossa eniten
    def yleisin_genre(self, genret: list):
        suosituin = ""
        suosituinta = 0
        for genre in genret:
            maara = genret.count(genre)
            if maara > suosituinta:
                suosituinta = maara
                suosituin = genre
        return (suosituin, suosituinta)
    

    #Apufunktio - Palauttaa parhaan/huonoimman (riippuen annetusta parametrista) ohjaajan ja hänen elokuvien keskiarvon
    def paras_huonoin_ohjaaja(self, parametri: str):
        nimi = ""
        if parametri == "paras":
            keskiarvo = -1
            for ohjaaja in self._ohjaajat:
                if ohjaaja.elokuvien_keskiarvo() > keskiarvo:
                    nimi = ohjaaja._nimi 
                    keskiarvo = ohjaaja.elokuvien_keskiarvo()
        if parametri == "huonoin":
            keskiarvo = 11
            for ohjaaja in self._ohjaajat:
                if ohjaaja.elokuvien_keskiarvo() < keskiarvo:
                    nimi = ohjaaja._nimi 
                    keskiarvo = ohjaaja.elokuvien_keskiarvo()
        return (nimi, keskiarvo)


    #Apufunktio - Palauttaa parhaan/huonoimman (riippuen annetusta parametrista) genren ja sen elokuvien keskiarvon
    def paras_huonoin_genre(self, parametri: str):
        nimi = ""
        if parametri == "paras":
            keskiarvo = -1
            for genre in self._genret:
                if genre.elokuvien_keskiarvo() > keskiarvo:
                    nimi = genre._nimi 
                    keskiarvo = genre.elokuvien_keskiarvo()
        elif parametri == "huonoin":
            keskiarvo = 11
            for genre in self._genret:
                if genre.elokuvien_keskiarvo() < keskiarvo:
                    nimi = genre._nimi
                    keskiarvo = genre._elokuvien_keskiarvo()
        return (nimi, keskiarvo)

    
    #Apufunktio - Palauttaa arkistossa olevan elokuvan ja sen arvosanan, jonka oma arvosana on paras/huonoin (riippuen annetusta parametrista)
    def paras_huonoin_elokuva(self, parametri: str):
        nimi = ""
        if parametri == "paras":
            arvosana = -1
            for elokuva in self._elokuvat:
                if elokuva._oma_arvosana > arvosana:
                    nimi = elokuva._nimi
                    arvosana = elokuva._oma_arvosana
        elif parametri == "huonoin":
            arvosana = 11
            for elokuva in self._elokuvat:
                if elokuva._oma_arvosana < arvosana:
                    nimi = elokuva._nimi
                    arvosana = elokuva._oma_arvosana
        return (nimi, arvosana)


    #Apufunktio - Palauttaa elokuvan jonka kohdalla oman arvosanan ja IMDb-arvosanan ero on suurin/pienin (riippuen funktiolle annetusta parametrista), ja sen kuinka suuri ero on.
    def arvio_erot(self, kumpi: str):
        if kumpi == "suurin":
            suurin_ero = 0
            leffa = ""
            for elokuva in self._elokuvat:
                ero = elokuva._oma_arvosana - elokuva._imdb_arvosana
                if abs(ero) > abs(suurin_ero):
                    suurin_ero = ero
                    leffa = elokuva._nimi
            return (leffa, suurin_ero)
        elif kumpi =="pienin":
            pienin_ero = 10
            leffa = ""
            for elokuva in self._elokuvat:
                ero = elokuva._oma_arvosana - elokuva._imdb_arvosana
                if abs(ero) < abs(pienin_ero):
                    pienin_ero = ero
                    leffa = elokuva._nimi
            return (leffa, pienin_ero)
        else: 
            pass

    
    #Apufunktio - Palauttaa kaikki arkistossa olevat kahden genren yhdistelmät ja niiden arvosanakeskiarvon järjestettynä listaan arvosanakeskiarvon mukaan.
    def palauta_combot(self):
        def arvosanan_mukaan(genrepari: tuple):
            return genrepari[1]
        kayty_lapi = []
        parit = []
        for genre1 in self._genret:
            for genre2 in self._genret:
                if genre2 != genre1 and genre2 not in kayty_lapi:
                    parit.append((genre1._nimi, genre2._nimi))
            kayty_lapi.append(genre1)
        parien_arvot = []
        for pari in parit:
            for elokuva in self._elokuvat:
                if pari[0] in elokuva._genret and pari[1] in elokuva._genret:
                    parien_arvot.append((pari, (elokuva._oma_arvosana)))
        kaikki_combot = sorted(parien_arvot, key=arvosanan_mukaan, reverse=True)
        yksittaiset_combot = {}
        for combo in kaikki_combot:
            combon_nimi = str(combo[0])
            yksittaiset_combot[combon_nimi] = []
        for combo in kaikki_combot:
            combon_nimi = str(combo[0])
            yksittaiset_combot[combon_nimi].append(combo[1])
        palautettava_lista = []
        for combo, arvosanat in yksittaiset_combot.items():
            keskiarvo = sum(arvosanat) / len(arvosanat)
            palautettava_lista.append((combo, keskiarvo))
        return sorted(palautettava_lista, key=arvosanan_mukaan, reverse=True)

    

                


#############################################################################################################################################################################################
if __name__ == "__main__":
    arkisto = Leffa_arkisto()
    arkisto.sovellus()
