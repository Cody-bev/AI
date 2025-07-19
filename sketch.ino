#include <LiquidCrystal.h>

// LCD pin configuration: RS=12, Enable=11, D4=5, D5=4, D6=3, D7=2
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {
  Serial.begin(9600);
  Serial.println("Arduino LCD Bridge Ready");
  
  // Initialize the LCD
  lcd.begin(16, 2);
  
  // Clear the display and show ready message
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Arduino Ready");
  lcd.setCursor(0, 1);
  lcd.print("Waiting...");
  
  delay(2000);
  lcd.clear();
}

void loop() {
  // Check if there's incoming serial data
  if (Serial.available() > 0) {
    // Read the incoming message
    String message = Serial.readStringUntil('\n');
    
    // Remove any whitespace/newlines
    message.trim();
    
    // Clear the LCD
    lcd.clear();
    
    // Display the message
    displayMessage(message);
    
    // Send confirmation back to Python
    Serial.println("Message displayed: " + message);
  }
}

void displayMessage(String message) {
  // If message is short enough for one line
  if (message.length() <= 16) {
    lcd.setCursor(0, 0);
    lcd.print(message);
  } 
  // If message is longer, split across two lines
  else {
    // First line (first 16 characters)
    lcd.setCursor(0, 0);
    lcd.print(message.substring(0, 16));
    
    // Second line (remaining characters, up to 16 more)
    if (message.length() > 16) {
      lcd.setCursor(0, 1);
      lcd.print(message.substring(16, min(32, (int)message.length())));
    }
  }
}
