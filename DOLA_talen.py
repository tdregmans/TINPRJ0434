### DOLA_TALEN lijst ###
# gemaakt op 01-06-2022
# versie 2.1
# list voor alle tekst in de GUI

# team:
#   Neelesh
#   Bartholomeus
#   Hidde-Jan
#   Thijs









lijst = [["DOLLAS BANK", "DOLLAS BANK", "DOLLAS BANCO"],
         ["Welkom", "Welcome", "Bienvenidos"],
         ["Plaats uw kaart voor de scanner.", "Place your card for the cardreader, please.", "Por favor coloque su tarjeta para el lector."],
         ["Afbreken", "Abort", "Abortar"],
         ["Voer uw pincode in.", "Enter your pincode, please.", "Introduzca su código PIN."],
         ["Akkoord", "Enter", "Entrar"],
         ["Backspace", "Backspace", "Retroceso"],
         ["Incorrecte pincode.", "Wrong pincode.", "código PIN incorrecto."],
         ["Incorrecte pincode. Pas geblokeerd.", "Wrong pincode. Card blocked.", "código PIN incorrecto. Paso bloqueado."],
         ["Menu", "Menu", "Menú"],
         ["Saldo", "Balance", "Balance"],
         ["Bedrag kiezen", "Choose amount", "Elegir la cantidad"],
         ["Snelpinnen (70 EUR)", "Quick pin (70 EUR)", "Pines rápidos (70 EUR)"],
         ["Terug", "Back", "Atrás"],
         ["Typ de hoeveelheid in.", "Enter the desired amount.", "Escriba la cantidad."],
         ["Er ontstond een fout.", "An error occured.", "Ocurrió un error."],
         ["Wilt u een bon?", "Do you want a receipt?", "Quieres un recibo?"],
         ["Ja", "Yes", "Sí"],
         ["Nee", "No", "No"],
         ["Vergeet uw bankpas en geld niet.", "Don't forget your card and money.", "No olvides tu tarjeta y dinero."],
         ["Een ogenblik geduld aub...", "One moment please...", "Un momento por favor..."],
         ["Account niet gevonden!", "Account not found!", "Cuenta no encontrada!"],
         ["Combinatie pinpas en pincode bestaat niet!", "Combination debitcard and pincode does not exist!", "La combinación de tarjeta de débito y código pin no existe!"],]


# nr. 8 niet langer in gebruik
def getText(id, taal):
    return lijst[id][taal]

    
