#include <Arduino.h>

// Asignación de los 10 pines 
const int BTN1_PIN  = 12; // Botón 1
const int BTN2_PIN  = 13; // Botón 2
const int BTN3_PIN  = 14; // Botón 3
const int BTN4_PIN  = 27; // Botón 4
const int BTN5_PIN  = 26; // Botón 5
const int BTN6_PIN  = 25; // Botón 6
const int BTN7_PIN  = 33; // Botón 7
const int BTN8_PIN  = 32; // Botón 8
const int BTN9_PIN  = 15; // Botón 9 
const int BTN10_PIN = 2;  // Botón 10 

void setup() {
  Serial.begin(115200);

  // Activamos resistencias Pull-Up internas para TODOS los pines
  pinMode(BTN1_PIN, INPUT_PULLUP);
  pinMode(BTN2_PIN, INPUT_PULLUP);
  pinMode(BTN3_PIN, INPUT_PULLUP);
  pinMode(BTN4_PIN, INPUT_PULLUP);
  pinMode(BTN5_PIN, INPUT_PULLUP);
  pinMode(BTN6_PIN, INPUT_PULLUP);
  pinMode(BTN7_PIN, INPUT_PULLUP);
  pinMode(BTN8_PIN, INPUT_PULLUP);
  pinMode(BTN9_PIN, INPUT_PULLUP);
  pinMode(BTN10_PIN, INPUT_PULLUP);
}

void loop() {
  if (digitalRead(BTN1_PIN) == LOW)  { Serial.println("BUTTON1");  delay(300); }
  if (digitalRead(BTN2_PIN) == LOW)  { Serial.println("BUTTON2");  delay(300); }
  if (digitalRead(BTN3_PIN) == LOW)  { Serial.println("BUTTON3");  delay(300); }
  if (digitalRead(BTN4_PIN) == LOW)  { Serial.println("BUTTON4");  delay(300); }
  if (digitalRead(BTN5_PIN) == LOW)  { Serial.println("BUTTON5");  delay(300); }
  if (digitalRead(BTN6_PIN) == LOW)  { Serial.println("BUTTON6");  delay(300); }
  if (digitalRead(BTN7_PIN) == LOW)  { Serial.println("BUTTON7");  delay(300); }
  if (digitalRead(BTN8_PIN) == LOW)  { Serial.println("BUTTON8");  delay(300); }
  if (digitalRead(BTN9_PIN) == LOW)  { Serial.println("BUTTON9");  delay(300); }
  if (digitalRead(BTN10_PIN) == LOW) { Serial.println("BUTTON10"); delay(300); }
}