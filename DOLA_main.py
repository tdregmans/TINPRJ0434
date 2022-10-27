### main DOLA GUI code ###
# gemaakt op 08-06-2022
# versie 9.0
# lib voor DOLA bank automaat

# team:
#   Neelesh
#   Bartholomeus
#   Hidde-Jan
#   Thijs

# Libaries voor GUI
from tkinter import * 
# from tkinter.ttk import *
# from tkinter.font import *
import tkinter as tk

# Libaries voor tijd functies
import time

# Libaries voor afhandeling gegevens
# wanneer de GUI gekoppeld wordt moet de volgende regel geactiveerd worden:
import DOLA

# set IBAN global
global IBAN, rekeningNummer, pasNummer, PIN, hoeveelheid

import threading

lettertype = "Poppins"
backgroundColor = "#1B1B1E"
forgroundColor = "#FBFFFE"

root = Tk()
root.title("DOLLAS BANK")
root.state("iconic")

root.config(bg=backgroundColor)

win = Frame(root)
win.config(bg=backgroundColor)
win.pack(fill=BOTH, expand=True, padx=50, pady=50)

# Activate fullscreen mode
#root.attributes("-fullscreen", True)

global objecten
objecten = []

# taal regelen
import DOLA_talen as text
global taal
taal = 0

global invoerVeldText
invoerVeldText = ""        

def taalMenu():
    global objecten
    for obj in objecten:
        obj.destroy()
        
    global taal
        
    # objecten
    titel = tk.Label(win, text=text.getText(0,taal), font=(lettertype,45,'bold'))
    onderTitel = tk.Label(win, text=text.getText(1,taal), font=(lettertype,30))
    knopA = tk.Label(win, text="A Nederlands", font=(lettertype,30), relief="sunken")
    knopB = tk.Label(win, text="B English", font=(lettertype,30), relief="sunken")
    knopC = tk.Label(win, text="C Español", font=(lettertype,30), relief="sunken")
    knopD = tk.Label(win, text="D _", font=(lettertype,30), relief="sunken")
    
    objecten = [titel, onderTitel, knopA, knopB, knopC, knopD]
    
    for obj in objecten:
        obj.config(fg=forgroundColor, bg=backgroundColor)
        obj.pack()
    
    def leesKeypad():
        invoer = ""
        global taal
        while len(invoer) < 1:
            invoer = DOLA.knoppenKeypad()
        if invoer == "A":
            taal = 0
            scanMenu()
        elif invoer == "B":
            taal = 1
            scanMenu()
        elif invoer == "C":
            taal = 2
            scanMenu()
        else:
            taalMenu()

    knoppen = threading.Thread(target=leesKeypad)
    knoppen.start()
    
def scanMenu():
    global IBAN
    done = False
    IBAN = ""
    
    global objecten
    for obj in objecten:
        obj.destroy()
    
    titel = tk.Label(win, text=text.getText(0,taal), font=(lettertype,45,'bold'))
    onderTitel = tk.Label(win, text=text.getText(2,taal), font=(lettertype,30))
    melding = tk.Label(win, text="", font=(lettertype,15))
    knopA = tk.Label(win, text="A _", font=(lettertype,30), relief='sunken')
    knopB = tk.Label(win, text="B _", font=(lettertype,30), relief='sunken')
    knopC = tk.Label(win, text="C _", font=(lettertype,30), relief='sunken')
    knopD = tk.Label(win, text=("D "+text.getText(3,taal)), font=(lettertype,30), relief='sunken')
    
    objecten = [titel, onderTitel, melding, knopA, knopB, knopC, knopD]
    
    for obj in objecten:
        obj.config(fg=forgroundColor, bg=backgroundColor)
        obj.pack()
    
    # er is hier nog een error! LET OP! deze leesKeypad heeft geen while loop.
    # wellicht ligt hier de oplossing!
    def leesKeypad():
        invoer = ""
        while len(invoer) < 1:
            invoer = DOLA.knoppenKeypad()
        if invoer == "A":
            scanMenu()
        elif invoer == "B":
            scanMenu()
        elif invoer == "C":
            scanMenu()
        elif invoer == "D":
            uitMenu()
        else:
            scanMenu()

    knoppen = threading.Thread(target=leesKeypad)
    knoppen.start()
            
            
    def scannen():
        while True:
            global IBAN
            global rekeningNummer
            global pasNummer
            IBAN = DOLA.readCard_old()
            rekeningNummer = IBAN[10:14]
            pasNummer = IBAN[15:16]
            if DOLA.valideerIBAN(IBAN):
                # IBAN heeft het juiste format
                print("IBAN: "+ IBAN)
                codeMenu()
                break
            else:
                melding.config(text="pas is ongeldig")

    scanner = threading.Thread(target=scannen)
    scanner.start()
        
        
def codeMenu():
    global objecten
    for obj in objecten:
        obj.destroy()
    
    titel = tk.Label(win, text=text.getText(0,taal), font=(lettertype,45,'bold'))
    onderTitel = tk.Label(win, text=text.getText(4,taal), font=(lettertype,30))
    melding = tk.Label(win, text="", font=(lettertype,15))
    invoerVeld = tk.Label(win, text="", font=(lettertype,40))
    knopA = tk.Label(win, text=("A "+text.getText(5,taal)), font=(lettertype,30), relief='sunken')
    knopB = tk.Label(win, text="B _", font=(lettertype,30), relief='sunken')
    knopC = tk.Label(win, text=("C "+text.getText(6,taal)), font=(lettertype,30), relief='sunken')
    knopD = tk.Label(win, text=("D "+text.getText(3,taal)), font=(lettertype,30), relief='sunken')
        
    objecten = [titel, onderTitel, melding, invoerVeld, knopA, knopB, knopC, knopD]
    
    for obj in objecten:
        obj.config(fg=forgroundColor, bg=backgroundColor)
        obj.pack()
    
    def leesKeypadCode():
        global PIN
        invoerVeld.config(text="")
        invoer = ""
        global invoerVeldText
        ingevoerdePincode = ""
        while True:
            invoer = invoer + DOLA.knoppenKeypad()
            getallen = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
            if invoer[-1] in getallen:
                if len(invoerVeldText) < 4:
                    invoerVeldText = invoerVeldText + "*"
                    ingevoerdePincode = ingevoerdePincode + invoer[-1]
                    invoerVeld.config(text=invoerVeldText)
            if invoer[-1] == "A":
                melding.config(text=text.getText(20, taal))
                PIN = ingevoerdePincode
                print(ingevoerdePincode)
                if DOLA.balance(IBAN, ingevoerdePincode)[0]:
                    # IBAN bestaat!
                    Menu()
                    break
                else:
                    melding.config(text=text.getText(22, taal))
                    invoerVeldText = ""
                    ingevoerdePincode = ""
                    invoerVeld.config(text=invoerVeldText)
                    if not(DOLA.balance(IBAN, ingevoerdePincode)[0]):
                        melding.config(text=("Pincode incorrect."))
                    else:
                        # geen kansen meer
                        melding.config(text=("Pincode incorrect. Pas geblokeerd!"))
                        
                    
            elif invoer[-1] == "C":
                invoerVeldText = invoerVeldText[:-1]
                ingevoerdePincode = ingevoerdePincode[:-1]
                invoerVeld.config(text=invoerVeldText)
            elif invoer[-1] == "D":
                uitMenu()
                break
            else:
                print("ERROR:" + invoer)
    
    keypad = threading.Thread(target=leesKeypadCode)
    keypad.start()
    

def Menu():
    global objecten
    for obj in objecten:
        obj.destroy()
    
    titel = tk.Label(win, text=text.getText(0,taal), font=(lettertype,45,'bold'))
    onderTitel = tk.Label(win, text=text.getText(9,taal), font=(lettertype,30))
    knopA = tk.Label(win, text=("A "+text.getText(10,taal)), font=(lettertype,30), relief='sunken')
    knopB = tk.Label(win, text=("B "+text.getText(11,taal)), font=(lettertype,30), relief='sunken')
    knopC = tk.Label(win, text=("C "+text.getText(12,taal)), font=(lettertype,30), relief='sunken')
    knopD = tk.Label(win, text=("D "+text.getText(3,taal)), font=(lettertype,30), relief='sunken')
    
    objecten = [titel, onderTitel, knopA, knopB, knopC, knopD]

    for obj in objecten:
        obj.config(fg=forgroundColor, bg=backgroundColor)
        obj.pack()
    
    def leesKeypad():
        invoer = ""
        while len(invoer) < 1:
            invoer = DOLA.knoppenKeypad()
        if invoer == "A":
            saldoMenu()
        elif invoer == "B":
            pinMenu()
        elif invoer == "C":
            DOLA.dispensGeld(70)
            global hoeveelheid
            hoeveelheid = 70
            bonMenu()
        elif invoer == "D":
            uitMenu()
        else:
            print("ERROR:" + invoer)
    
    knoppen = threading.Thread(target=leesKeypad)
    knoppen.start()

def saldoMenu():
    global IBAN, PIN
    saldo = DOLA.balance(IBAN, PIN)
    
    global objecten
    for obj in objecten:
        obj.destroy()
    
    titel = tk.Label(win, text=text.getText(0,taal), font=(lettertype,45,'bold'))
    onderTitel = tk.Label(win, text=text.getText(10,taal), font=(lettertype,30))
    saldoLabel = tk.Label(win, text=saldo, font=(lettertype,40))
    knopA = tk.Label(win, text=("A "+text.getText(13,taal)), font=(lettertype,30), relief='sunken')
    knopB = tk.Label(win, text="B _", font=(lettertype,30), relief='sunken')
    knopC = tk.Label(win, text="C _", font=(lettertype,30), relief='sunken')
    knopD = tk.Label(win, text=("D "+text.getText(3,taal)), font=(lettertype,30), relief='sunken')
    
    objecten = [titel, onderTitel, saldoLabel, knopA, knopB, knopC, knopD]

    for obj in objecten:
        obj.config(fg=forgroundColor, bg=backgroundColor)
        obj.pack()
        
    def leesKeypad():
        invoer = ""
        while len(invoer) < 1:
            invoer = DOLA.knoppenKeypad()
        if invoer == "A":
            Menu()
        elif invoer == "B":
            saldoMenu()
        elif invoer == "C":
            saldoMenu()
        elif invoer == "D":
            uitMenu()
        else:
            print("ERROR:" + invoer)
    
    knoppen = threading.Thread(target=leesKeypad)
    knoppen.start()


def pinMenu():
    global objecten
    for obj in objecten:
        obj.destroy()
    
    titel = tk.Label(win, text=text.getText(0,taal), font=(lettertype,45,'bold'))
    onderTitel = tk.Label(win, text=text.getText(14,taal), font=(lettertype,30))
    melding = tk.Label(win, text="", font=(lettertype,15))
    invoerVeld = tk.Label(win, text="", font=(lettertype,40))
    knopA = tk.Label(win, text=("A _"+text.getText(5,taal)), font=(lettertype,30), relief='sunken')
    knopB = tk.Label(win, text="B _", font=(lettertype,30), relief='sunken')
    knopC = tk.Label(win, text=("C "+text.getText(6,taal)), font=(lettertype,30), relief='sunken')
    knopD = tk.Label(win, text=("D "+text.getText(3,taal)), font=(lettertype,30), relief='sunken')
    
    objecten = [titel, onderTitel, melding, invoerVeld, knopA, knopB, knopC, knopD]

    for obj in objecten:
        obj.config(fg=forgroundColor, bg=backgroundColor)
        obj.pack()
        
    def leesKeypadHoeveelheid():
        invoer = ""
        global invoerVeldText
        global IBAN
        invoerVeldText = ""
        while True:
            invoer = invoer + DOLA.knoppenKeypad()
            getallen = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
            if invoer[-1] in getallen:
                if len(invoerVeldText) < 4:
                    invoerVeldText = invoerVeldText + invoer[-1]
                    invoerVeld.config(text=invoerVeldText)
            if invoer[-1] == "A":
                print("Hoeveelheid ingevoerd. Een ogenblik geduld a.u.b.")
                global PIN, hoeveelheid
                hoeveelheid = invoerVeldText
                if(DOLA.doTransaction(IBAN, PIN, hoeveelheid)):
                    DOLA.dispensGeld(hoeveelheid)
                    bonMenu()
                    break
                else:
                    # error! transactie niet gelukt
                    melding.config(text=(text.getText(15,taal)))
                    
            elif invoer[-1] == "C":
                invoerVeldText = invoerVeldText[:-1]
                invoerVeld.config(text=invoerVeldText)
            elif invoer[-1] == "D":
                uitMenu()
                break
            else:
                print("ERROR:" + invoer)
    
    keypad = threading.Thread(target=leesKeypadHoeveelheid)
    keypad.start()
    
    
def bonMenu():
    global objecten
    for obj in objecten:
        obj.destroy()
    
    titel = tk.Label(win, text=text.getText(0,taal), font=(lettertype,45,'bold'))
    onderTitel = tk.Label(win, text=text.getText(16,taal), font=(lettertype,30))
    knopA = tk.Label(win, text=("A "+text.getText(17,taal)), font=(lettertype,30), relief='sunken')
    knopB = tk.Label(win, text="B _", font=(lettertype,30), relief='sunken')
    knopC = tk.Label(win, text="C _", font=(lettertype,30), relief='sunken')
    knopD = tk.Label(win, text=("D "+text.getText(18,taal)), font=(lettertype,30), relief='sunken')
    
    objecten = [titel, onderTitel, knopA, knopB, knopC, knopD]

    for obj in objecten:
        obj.config(fg=forgroundColor, bg=backgroundColor)
        obj.pack()
        
    def leesKeypadBon():
        global IBAN
        global hoeveelheid
        invoer = ""
        while len(invoer) < 1:
            invoer = DOLA.knoppenKeypad()
        if invoer == "A":
            DOLA.printBon(IBAN, hoeveelheid)
            print("Bon wordt geprint!")
            uitMenu()
        elif invoer == "B":
            bonMenu()
        elif invoer == "C":
            bonMenu()
        elif invoer == "D":
            uitMenu()
        else:
            print("ERROR:" + invoer)
            bonMenu()
    
    knoppen = threading.Thread(target=leesKeypadBon)
    knoppen.start()
    
    
def uitMenu():
    global objecten
    for obj in objecten:
        obj.destroy()
    
    titel = tk.Label(win, text=text.getText(0,taal), font=(lettertype,45,'bold'))
    onderTitel = tk.Label(win, text=text.getText(19,taal), font=(lettertype,30))
    
    objecten = [titel, onderTitel]

    for obj in objecten:
        obj.config(fg=forgroundColor, bg=backgroundColor)
        obj.pack()
        
    def eind():
        global IBAN
        global rekeningNummer
        time.sleep(5)
        
        IBAN = ""
        rekeningNummer = ""
        taalMenu()
        
    eindFunctie = threading.Thread(target=eind)
    eindFunctie.start()
    
    
def scherm():
    taalMenu()

scherm = threading.Thread(target=scherm)
scherm.start()

root.mainloop()