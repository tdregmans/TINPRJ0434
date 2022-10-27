// DOLLAS BANK
// gemaakt op 02-06-2022
// versie 1.1
// code voor arduino 2 die verantwoordelijk is voor de gelddispenser

// team:
  // Neelesh
  // Bartholomeus
  // Hidde-Jan
  // Thijs

// includes voor communicatie met Master (RPi)
#include <Wire.h>
//#include <string>
const int ADDRESS = 6;

// includes voor munt dispenser
#include <Servo.h>

// includes en defintie biljet dispensers
const int aantalStappenIn360Graden = 20;
#include <Stepper.h>
const int stepsPerRevolution = 200;
Stepper biljectDispenser1(stepsPerRevolution, 2, 3, 4, 5);
Stepper biljectDispenser2(stepsPerRevolution, 6, 7, 8, 9);
int stepCount = 0;

// Muntdispenser 1
int muntDispenserPin1 = 10;
Servo muntDispenser1;

// Muntdispenser 2
int muntDispenserPin2 = 11;
Servo muntDispenser2;


// waardes van muntdispensers & biljetdispensers
// LET OP! De hoogste waarde MOET al eerst gedefinieerd worden:
  // WAARDEBILJECTDISPENSER1 MOET groter zijn dan WAARDEBILJECTDISPENSER2
  // WAARDEMUNTDISPENSER1 MOET groter zijn dan WAARDEMUNTDISPENSER2
const int WAARDEBILJECTDISPENSER1 = 50;
const int WAARDEBILJECTDISPENSER2 = 10;
const int WAARDEMUNTDISPENSER1 = 2;
const int WAARDEMUNTDISPENSER2 = 1;
// LET OP! Voorbeeld waarden zijn gekozen! Deze kunnen veranderen!

void setup() {
  // Setup I2C address and receive event
  Wire.begin(ADDRESS);
  Wire.onReceive(receiveEvent);
  Serial.begin(9600);

  // biljet dispensers
  biljectDispenser1.setSpeed(60);
  biljectDispenser2.setSpeed(60);

  // koppel Servo-objecten en pinnen
  muntDispenser1.attach(muntDispenserPin1); 
  muntDispenser2.attach(muntDispenserPin2); 

}


void receiveEvent(int howMany) {
  // called wanneer Master bericht stuurt
  String data;
  while (0 < Wire.available()) {
    char c = Wire.read();
    Serial.print(c);
    data += c;
  }
  data = data.substring(1);
  Serial.println();

  // definitie van hoeveelheid misschien nog aanpassen !!!
  int hoeveelheid = data.toInt();
  dispenseGeld(hoeveelheid);
  
}


void dispenseGeld(int hoeveelheid) {
  int nogTeDispensenHoeveelheid = hoeveelheid;
  Serial.println(nogTeDispensenHoeveelheid);
  // Bilject Dispenser 1
    //Serial.println("Dispense biljet:" + WAARDEBILJECTDISPENSER1);
  while (nogTeDispensenHoeveelheid >= WAARDEBILJECTDISPENSER1) {
    Serial.println("1 omwenteling biljet type 1");
    Serial.print("nogTeDispensenHoeveelheid: ");
    Serial.println(nogTeDispensenHoeveelheid);
    for(int x=0; x<aantalStappenIn360Graden; x++){
      biljectDispenser1.step(105);
    }
    nogTeDispensenHoeveelheid -= WAARDEBILJECTDISPENSER1;
  }
  
  Serial.println(nogTeDispensenHoeveelheid);
  // Bilject Dispenser 2
    //Serial.println("Dispense biljet:"+WAARDEBILJECTDISPENSER2);
  while (nogTeDispensenHoeveelheid >= WAARDEBILJECTDISPENSER2) {
    Serial.println("1 omwenteling biljet type 2");
    Serial.print("nogTeDispensenHoeveelheid: ");
    Serial.println(nogTeDispensenHoeveelheid);
    for(int x=0; x<aantalStappenIn360Graden; x++){
      biljectDispenser2.step(105);
    }
    nogTeDispensenHoeveelheid -= WAARDEBILJECTDISPENSER2;
  }

  // Munt Dispenser 1
  while (nogTeDispensenHoeveelheid >= WAARDEMUNTDISPENSER1) {
    muntDispenser1.write(90);
    delay(500);
    muntDispenser1.write(0);
    delay(500);
    muntDispenser1.write(90);
    nogTeDispensenHoeveelheid -= WAARDEMUNTDISPENSER1;
  }

  // Munt Dispenser 2
  while (nogTeDispensenHoeveelheid >= WAARDEMUNTDISPENSER2) {
    muntDispenser2.write(90);
    delay(500);
    muntDispenser2.write(0);
    delay(500);
    muntDispenser2.write(90);
    nogTeDispensenHoeveelheid -= WAARDEMUNTDISPENSER2;
 }
  
}

void loop() {
  // empty 
  // DO NOT DELETE!
}
