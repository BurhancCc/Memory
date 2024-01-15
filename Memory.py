from tkinter import *
from tkinter import messagebox
import random

root = Tk()
root.title('Burhan en Osman - Kwartetten memory met kaartspel')
root.geometry("1000x600")

kaarten = []
AANTAL_CIJFERKAARTEN_PER_KAARTSOORT = 10
GELETTERDE_KAARTEN = ["K", "Q", "J"]
KAARTSOORTEN = ["H", "K", "S", "R"]

AANTAL_RIJEN = 13
AANTAL_KOLOMMEN = 4
frame = Frame(root)
frame.pack(pady=10)
knoppen = {}

tel = 0
score = 0
antwoordenLijst = []
antwoordenDict = {}

label = Label(root, text='')
label.pack(pady=20)

aantalGoedeAntwoorden = 0
MAXIMAAL_GOED_ANTWOORDENAANTAL_VOOR_EINDE = 12
PUNTEN_GOED_ANTWOORD = 20
AFTREK_FOUT_ANTWOORD = 1

#Start het script.
def start():
    global kaarten
    kaartenMaker()
    kaartenSchudder()
    bordMaker()
    menu()
    root.mainloop()

#Maakt een stapel speelkaarten.
def kaartenMaker():
    global kaarten
    for cijfer in range(1, AANTAL_CIJFERKAARTEN_PER_KAARTSOORT + 1):
        for kaartsoort in KAARTSOORTEN:
            kaarten.append(kaartsoort + str(cijfer))

    for letterkaart in GELETTERDE_KAARTEN:
        for kaartsoort in KAARTSOORTEN:
            kaarten.append(kaartsoort + letterkaart)

#Schud de globale stapel kaarten.
def kaartenSchudder():
    global kaarten
    random.shuffle(kaarten)

#Creëert een bord om het spel op te spelen.
def bordMaker():
    global knoppen, score
    commands = []
    #Hier worden de knoppen, welk als kaarten dienen, gecreëerd.
    for i in range(len(kaarten)):
            knoppen[str(i)] = Button(frame, text='', font=("Helvetica", 12), heigh=3, width=6, command=lambda i=i: checkAntwoord(i), relief="sunken")
    #Hier worden de knoppen op het spelbord gesorteerd.
    coordinaten = []
    for rij in range(AANTAL_RIJEN):
        for kolom in range(AANTAL_KOLOMMEN):
            coordinaten.append([rij, kolom])
    for i in range(len(knoppen)):
        knoppen[str(i)].grid(row=coordinaten[i][1], column=coordinaten[i][0])
    #Dit is een accurate placeholder tekst.
    label.config(text=("Score: " + str(score)))

#Controleert of de geflipte kaarten tot een kwartet behoren.
def checkAntwoord(nummer):
    global tel, antwoordenLijst, antwoordenDict, kaarten, knoppen, aantalGoedeAntwoorden, MAXIMAAL_GOED_ANTWOORDENAANTAL_VOOR_EINDE
    knop = knoppen[str(nummer)]
    #Registreert de gespeelde zetten.
    if  knop["text"] == '' and tel < 4:
        knop["text"] = kaarten[nummer]
        antwoordenLijst.append(nummer)
        antwoordenDict[knop] = kaarten[nummer]
        tel+=1
    
    #Controleert of de eerste zet correct is.
    if len(antwoordenLijst) == 2:
        if kaarten[antwoordenLijst[0]][-1] == kaarten[antwoordenLijst[1]][-1]:
            pass
        else:
            foutAntwoord()
    #Controleert of de tweede zet correct is.
    elif len(antwoordenLijst) == 3:
        if kaarten[antwoordenLijst[0]][-1] == kaarten[antwoordenLijst[2]][-1]:
            pass
        else:
            foutAntwoord()
    #Controleert of de derde zet correct is.
    elif len(antwoordenLijst) == 4:
        if kaarten[antwoordenLijst[0]][-1] == kaarten[antwoordenLijst[3]][-1]:
            goedAntwoord()
        else:
            foutAntwoord()

#Functie welk wordt gestart indien er een kwartet is ontdekt.
def goedAntwoord():
    global antwoordenDict, antwoordenLijst, tel, score, aantalGoedeAntwoorden
    #Controleert of het spel is uitgespeeld.
    score += PUNTEN_GOED_ANTWOORD
    if aantalGoedeAntwoorden == MAXIMAAL_GOED_ANTWOORDENAANTAL_VOOR_EINDE:
        spelEinde()
    label.config(text="Je hebt een kwartet gevonden! Score: " + str(score))
    #Verwijderd de kaarten welk behoren tot een al ontdekt kwartet.
    for key in antwoordenDict:
        key["state"] = "disabled"
        tel = 0
        antwoordenLijst = []
        antwoordenDict = {}
    aantalGoedeAntwoorden += 1

#Functie welk wordt gestart indien er een foute combinatie wordt gespeeld.
def foutAntwoord():
    global tel, score, antwoordenDict, antwoordenLijst
    #Controleert of de score wel verminderd mag worden, aangezien er niet lager dan 0 kan worden gescoord.
    if score > 0:
        score -= AFTREK_FOUT_ANTWOORD
    messagebox.showinfo("Geen kwartet!", "Die kaarten waren helaas geen kwartet!")
    #Flipt alle kaarten terug.
    for antwoord in antwoordenDict:
        antwoord["text"] = ''
    antwoordenLijst = []
    antwoordenDict = {}
    label.config(text="Die kaarten waren helaas geen kwartet! Score: " + str(score))
    tel = 0

#Functie welk wordt gestart indien er een foute combinatie wordt uitgespeeld.
def spelEinde():
    global label, knoppen, score
    #Markeert het bord met een visueel esthetische kleur om een successvol einde van het spel te markeren.
    for knop in knoppen.values():
        knop.config(bg="yellow")
    messagebox.showinfo("Gefeliciteerd!", "Gefeliciteerd! Je hebt het spel uitgespeeld en gewonnen! Score: " + str(score))

#Functie welk het menu beheert.
def menu():
    menu = Menu(root)
    root.config(menu=menu)
    optieMenu = Menu(menu, tearoff=False)
    menu.add_cascade(label="Opties", menu=optieMenu)
    optieMenu.add_command(label="Spel opnieuw beginnen", command=reset)
    optieMenu.add_separator()
    optieMenu.add_command(label="Spel afsluiten", command=root.quit)

#Functie welk de optie beheert dat het spel opnieuw opstart.
def reset():
    global kaarten, aantalGoedeAntwoorden, knoppen, tel, score
    kaarten = []
    kaartenMaker()
    kaartenSchudder()
    label.config(text='')
    #Reset alle knoppen.
    for knop in knoppen.values():
        knop.config(text='', bg="SystemButtonFace", state="normal")
    tel = 0
    score = 0
    aantalGoedeAntwoorden = 0

start()