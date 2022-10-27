// Arduino Slave code Thermal Printer
// DOLLAS-bank

// gemaakt op 22-04-2022

// team:
  // Neelesh
  // Bartholomeus
  // Hidde-Jan
  // Thijs

// Libs
#include "Adafruit_Thermal.h"
#include "SoftwareSerial.h"
#include <Wire.h>

String currentDate;
String currentTime;
String amount;
String IBAN;
String RekeningNummer;
String cardID;
const String bankNaam = "Dollas bank";
bool aan =false;

// Wiring
#define TX_PIN 6 // Arduino transmit  YELLOW WIRE  labeled RX on printer
#define RX_PIN 5 // Arduino receive   GREEN WIRE   labeled TX on printer

SoftwareSerial mySerial(RX_PIN, TX_PIN); // Declare SoftwareSerial obj first
Adafruit_Thermal printer(&mySerial);     // Pass addr to printer constructor

void setup() {
  // I2C comms with RPi 3
  Wire.begin(9);                // join I2C bus with address #8
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);           // start serial for output
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  
  String data;
  while (0 < Wire.available()) { // loop through all but the last
    char c = Wire.read(); // receive byte as a character
    Serial.print(c);         // print the character
    data += c;
  }
  Serial.println();
  

  // separate data from string recieved from Master RPi
  currentDate = data.substring(1,3) + "-" + data.substring(3,5) + "-" + data.substring(5,7);
  currentTime = data.substring(7,9) + ":" + data.substring(9,11) + ":" + data.substring(11,13);
  
  IBAN = data.substring(13,29);
  RekeningNummer = data.substring(25,27);
  cardID = data.substring(27,29);
  amount = data.substring(29,32);

  //printBon();
  aan = true;
  
}


void printBon() {
  // This line is for compatibility with the Adafruit IotP project pack,
  // which uses pin 7 as a spare grounding point.  You only need this if
  // wired up the same way (w/3-pin header into pins 5/6/7):
  pinMode(7, OUTPUT); 
  digitalWrite(7, LOW);
  mySerial.begin(9600);  // Initialize SoftwareSerial
  printer.begin();        // Init printer (same regardless of serial type)

  // The following calls are in setup(), but don't *need* to be.  Use them
  // anywhere!  They're just here so they run one time and are not printed
  // over and over (which would happen if they were in loop() instead).
  // Some functions will feed a line when called, this is normal.

  // Font options
  printer.justify('C');
  printer.setSize('L');
  printer.boldOn();
  printer.println(F("DOLLAS BANK"));
  printer.boldOff();
  printer.setSize('S');
  printer.justify('L');

  printer.justify('C');
  printer.setFont('A');
  printer.println(F("CASH RECEIPT"));
  printer.justify('R');
  printer.println("Date: "+currentDate);
  printer.println("Time: "+currentTime);


  printer.justify('L');
  printer.inverseOn();
  printer.println(F("Amount withdrawn:               "));
  printer.inverseOff();
  printer.justify('R');
  printer.setSize('L');
  printer.println(amount+",- Bolivar");
  printer.setSize('S');
  printer.justify('L');

  printer.inverseOn();
  printer.println(F("Info:                           "));
  printer.inverseOff();
  
  printer.boldOn();
  printer.println(F("Account number:"));
  printer.boldOff();
  printer.justify('R');
  printer.println("**** **"+RekeningNummer);
  printer.justify('L');
  
  printer.boldOn();
  printer.println(F("Card ID:"));
  printer.boldOff();
  printer.justify('R');
  printer.println(cardID);
  printer.justify('L');
  
  printer.boldOn();
  printer.println(F("Location:"));
  printer.boldOff();
  printer.justify('R');
  printer.println(bankNaam);
  printer.justify('L');

  printer.feed(2);
  
  printer.inverseOn();
  printer.justify('C');
  printer.setSize('L');
  printer.println(F("   THANK YOU   "));
  printer.setSize('S');
  printer.inverseOff();
  printer.println(F("www.dollas.com"));
  
  printer.feed(2);

  printer.sleep();      // Tell printer to sleep
  delay(3000);         // Sleep for 3 seconds
  printer.wake();       // MUST wake() before printing again, even if reset
  printer.setDefault(); // Restore printer to defaults
}

void loop() {
  switch (aan){
    case true:
         printer.wake(); 
        // This line is for compatibility with the Adafruit IotP project pack,
        // which uses pin 7 as a spare grounding point.  You only need this if
        // wired up the same way (w/3-pin header into pins 5/6/7):
        pinMode(7, OUTPUT); 
        digitalWrite(7, LOW);
        mySerial.begin(9600);  // Initialize SoftwareSerial
        printer.begin();        // Init printer (same regardless of serial type)
      
        // The following calls are in setup(), but don't *need* to be.  Use them
        // anywhere!  They're just here so they run one time and are not printed
        // over and over (which would happen if they were in loop() instead).
        // Some functions will feed a line when called, this is normal.
      
        // Font options
        printer.justify('C');
        printer.setSize('L');
        printer.boldOn();
        printer.println(F("DOLLAS BANK"));
        printer.boldOff();
        printer.setSize('S');
        printer.justify('L');
      
        printer.justify('C');
        printer.setFont('A');
        printer.println(F("CASH RECEIPT"));
        printer.justify('R');
        printer.println("Date: "+currentDate);
        printer.println("Time: "+currentTime);
      
      
        printer.justify('L');
        printer.inverseOn();
        printer.println(F("Amount withdrawn:               "));
        printer.inverseOff();
        printer.justify('R');
        printer.setSize('L');
        printer.println(amount+",- Bolivar");
        printer.setSize('S');
        printer.justify('L');
      
        printer.inverseOn();
        printer.println(F("Info:                           "));
        printer.inverseOff();
        
        printer.boldOn();
        printer.println(F("Account number:"));
        printer.boldOff();
        printer.justify('R');
        printer.println("**** **"+RekeningNummer);
        printer.justify('L');
        
        printer.boldOn();
        printer.println(F("Card ID:"));
        printer.boldOff();
        printer.justify('R');
        printer.println(cardID);
        printer.justify('L');
        
        printer.boldOn();
        printer.println(F("Location:"));
        printer.boldOff();
        printer.justify('R');
        printer.println(bankNaam);
        printer.justify('L');
      
        printer.feed(2);
        
        printer.inverseOn();
        printer.justify('C');
        printer.setSize('L');
        printer.println(F("   THANK YOU   "));
        printer.setSize('S');
        printer.inverseOff();
        printer.println(F("www.dollas.com"));
        
        printer.feed(10);
        printer.setDefault(); // Restore printer to defaults
        aan = false;
        break;
  }
}
