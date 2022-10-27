### DOLLAS lib ###
# gemaakt op 08-06-2022
# versie 9.0
# lib voor DOLA bank automaat

# team:
#   Neelesh
#   Bartholomeus
#   Hidde-Jan
#   Thijs

# libaries voor communiceren met Arduino Uno voor bonnenprinter
import smbus2
import time
from datetime import date
from datetime import datetime

# libaries voor communiceren met RFID scanner voor het scannen van de pas
import RPi.GPIO as gpio
from mfrc522 import SimpleMFRC522

gpio.setmode(gpio.BCM)

# libaries voor communiceren met MYSQL server
import pymysql

# libaries voor communiceren met Keypad
from pad4pi import rpi_gpio

 # disable warnings about GPIO
gpio.setwarnings(False)

# constanten
LAND = "VE"
BANK = "DOLA"

def printBon(IBAN, hoeveelheid):
    # IBAN moet een STRING van 16 tekens zijn
    # hoeveelheid moet een STRING van 3 tekens zijn. Als hoeveelheid < 100: voeg '0' toe
    if(len(IBAN) != 16 or len(hoeveelheid) != 3):
        print("IBAN en/of hoeveelheid heeft niet het juiste format")
        return False
    else:
        # kies andere busId voor andere versie van smbus2
        # opties: 0, 1
        busId = 1
        bus = smbus2.SMBus(busId)
        # adres verandert telkens
        address = 0x08

        # haal datum op
        today = date.today()
        todayString = today.strftime("%d%m%y")

        now = datetime.now()
        nowString = now.strftime("%H%M%S")
        dataString = todayString + nowString + IBAN + str(hoeveelheid)
        print(dataString)

        # zet gegevens in een array
        dataBytes = []
        for char in dataString:
            dataBytes.append(ord(char))
        # uncomment om bytes te zien
        #print(dataBytes)

        # wacht 2 sec zodat zeker is dat Arduino klaar is met printen van vorige bon
        time.sleep(2)

        # stuur data
        try:
            # stuur data via I2C
            bus.write_i2c_block_data(address, 99, dataBytes)
            print("SUCCES! Bon geprint!")
            return True
        except:
            print("ERROR! Bon niet geprint!")
            return False
        bus.close()

def dispensGeld(hoeveelheid):
    if(hoeveelheid < 1 or hoeveelheid > 300):
        print("De gevraagde hoeveelheid zorgt voor een error!")
        return False
    else:
        # kies andere busId voor andere versie van smbus2
        # opties: 0, 1
        busId = 1
        bus = smbus2.SMBus(busId)
        # adres verandert telkens
        
        address = 0x06
        
        dataString = str(hoeveelheid)
        print(dataString)

        # zet gegevens in een array
        dataBytes = []
        for char in dataString:
            dataBytes.append(ord(char))
        # uncomment om bytes te zien
        print(dataBytes)

        # stuur data
        try:
            # stuur data via I2C
            bus.write_i2c_block_data(address, 99, dataBytes)
            print("SUCCES!")
            return True
        except:
            print("ERROR!")
            return False
        bus.close()

def readCard_old():
    # maak CardReader object
    CardReader = SimpleMFRC522()
    try:
        id, text = CardReader.read()
        # 'id' is kaartId
        # 'text' is tekst opgeslagen op de kaart
        return text[:16]
    finally:
        gpio.cleanup()
        
    
def printKeyKnop(key):
    global keys
    print(key[-1], end='')
    keys.append(key)
        
def knoppenKeypad():
    KEYPAD = [
        ["1","2","3","A"],
        ["4","5","6","B"],
        ["7","8","9","C"],
        ["*","0","#","D"]
    ]
    
    ROW_PINS = [26,19,13,6]
    COL_PINS = [5,21,20,16]
    
    global keys
    keys = []

    # stel keypad in
    factory = rpi_gpio.KeypadFactory()
    keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
    
    keypad.registerKeyPressHandler(printKeyKnop)

    try:
        while(len(keys) < 1):
            # hou de loop levend zolang er er nog geen volledige pincode is ingevoerd
            time.sleep(0.1)
        # als genoeg tekens zijn ingevoerd, geeft deze terug
        keypad.cleanup()
        return keys[-1]
            
    except:
        # ruim op aan het einde
        keypad.cleanup()  

def valideerIBAN(IBAN):
    # een IBAN is 16 tekens lang
    if len(IBAN) != 16:
        return False
    else:
        # een IBAN bestaat uit 6 letters en 10 cijfers
        bankCode = IBAN[:6]
        rekeningNummer = IBAN[6:16]
        for char in bankCode:
            if not(char.isalpha()):
                return False
        for number in rekeningNummer:
            if number.isalpha():
                return False
        return True

def balance(IBAN, pincode):
    if not(valideerIBAN(IBAN)):
        print("r")
        return False, 0
    # IBAN heeft correct vorm
    object = {
    'head' :
        {
            "fromCtry": LAND,
            "fromBank": BANK,
            "toCtry":  IBAN[0:2],
            "toBank": IBAN[2:6]
        },
    "body":
        {
            "acctNo": IBAN,
            "pin": pincode
        }
    }
    print(object)
    try:
        ### maak verbinding met bankserver en vraag om saldo ###
        JSON_object = json.dumps(object)
        req = requests.post("http://145.24.222.63:8443/balance", json=object)
        res = req.text
        print(res)
        try:
            saldo = str(json.loads(res)["body"]["balance"])
            print(saldo)
        except:
            return True, saldo
    except:
        return False, 0

def doTransaction(IBAN, PIN, mutatie):
    # functie kan alleen aangeroepen worden als transactie valide is
    # mutatie is positief wanneer er geld wordt gepind!
    if not(valideerIBAN(IBAN)):
        return False
    object = {
    'head' :
        {
            "fromCtry": LAND,
            "fromBank": BANK,
            "toCtry":  IBAN[0:2],
            "toBank": IBAN[2:6]
        },
    "body":
        {
            "acctNo": IBAN,
            "pin": PIN,
            "amount": mutatie
        }
    }
    try:
        # maak verbinding met bankserver en probeer transactie uit te voeren
        JSON_object = json.dumps(object)
        req = requests.post("http://145.24.222.63:8443/withdraw", json=object)
        res = req.text
        resultaat = str(json.loads(res)["body"]["succes"])
        return resultaat == 200
    except:
        return False


