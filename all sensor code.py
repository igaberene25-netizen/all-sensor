import sys
import time

# ==============================================================================
# ULTIMATE ARDUINO HARDWARE & SENSOR CODE HUB (SAFE TEXT + STREAMING EFFECT)
# ==============================================================================

sensor_data = {
    "1": {
        "name": "Temperature Sensor (LM35)",
        "code": """// Type: Analog sensor | Pin: A0
int tempPin = A0;
float temperature;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int value = analogRead(tempPin);
  temperature = value * (5.0 * 100.0 / 1024.0); // LM35 formula

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" C");

  delay(1000);
}"""
    },
    "2": {
        "name": "Humidity + Temperature (DHT11 / DHT22)",
        "code": """// Library needed: DHT sensor library | Pin: D2
#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.print("%  Temperature: ");
  Serial.print(t);
  Serial.println("C");

  delay(2000);
}"""
    },
    "3": {
        "name": "Distance / Proximity (HC-SR04 Ultrasonic)",
        "code": """#define trigPin 9
#define echoPin 10

long duration;
int distance;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  delay(500);
}"""
    },
    "4": {
        "name": "Motion Sensor (PIR Sensor)",
        "code": """// Pin: D3
int pirPin = 3;
int ledPin = 13;
int state = 0;

void setup() {
  pinMode(pirPin, INPUT);
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  state = digitalRead(pirPin);

  if (state == HIGH) {
    digitalWrite(ledPin, HIGH);
    Serial.println("Motion detected!");
  } else {
    digitalWrite(ledPin, LOW);
    Serial.println("No motion");
  }

  delay(500);
}"""
    },
    "5": {
        "name": "Ultrasonic Sensor (Basic Distance Alert)",
        "code": """// Same as HC-SR04 but with LED warning
#define trig 9
#define echo 10
#define led 13

void setup() {
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  pinMode(led, OUTPUT);
}

void loop() {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);

  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);

  long duration = pulseIn(echo, HIGH);
  int distance = duration * 0.034 / 2;

  if (distance < 20) {
    digitalWrite(led, HIGH);
  } else {
    digitalWrite(led, LOW);
  }

  delay(300);
}"""
    },
    "6": {
        "name": "LDR Light Sensor",
        "code": """// Pin: A0
int ldrPin = A0;
int ledPin = 13;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int lightValue = analogRead(ldrPin);

  Serial.println(lightValue);

  if (lightValue < 300) {
    digitalWrite(ledPin, HIGH); // dark -> LED ON
  } else {
    digitalWrite(ledPin, LOW);
  }

  delay(500);
}"""
    },
    "7": {
        "name": "Servo Motor Control",
        "code": """#include <Servo.h>

Servo myServo;

void setup() {
  myServo.attach(9);
}

void loop() {
  myServo.write(0);
  delay(1000);

  myServo.write(90);
  delay(1000);

  myServo.write(180);
  delay(1000);
}"""
    },
    "8": {
        "name": "Relay Module Control",
        "code": """int relayPin = 7;

void setup() {
  pinMode(relayPin, OUTPUT);
}

void loop() {
  digitalWrite(relayPin, HIGH); // ON
  delay(2000);

  digitalWrite(relayPin, LOW);  // OFF
  delay(2000);
}"""
    },
    "9": {
        "name": "Servo + Ultrasonic (Automatic Door System)",
        "code": """// Door opens when object is close
#include <Servo.h>

Servo doorServo;

#define trigPin 9
#define echoPin 10

void setup() {
  doorServo.attach(6);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  int distance = duration * 0.034 / 2;

  if (distance < 20) {
    doorServo.write(90); // open door
  } else {
    doorServo.write(0);  // close door
  }

  delay(300);
}"""
    },
    "10": {
        "name": "Standard LED Control (Blink)",
        "code": """int ledPin = 13;

void setup() {
  pinMode(ledPin, OUTPUT);
}

void loop() {
  digitalWrite(ledPin, HIGH); // Turn LED ON
  delay(1000);                // Wait 1 second
  digitalWrite(ledPin, LOW);  // Turn LED OFF
  delay(1000);                // Wait 1 second
}"""
    },
    "11": {
        "name": "RGB LED (Color Cycle Control)",
        "code": """// Pins must support PWM (~ symbols on Arduino)
int redPin = 9;
int greenPin = 10;
int bluePin = 11;

void setup() {
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
}

void loop() {
  setColor(255, 0, 0);   // Red
  delay(1000);
  setColor(0, 255, 0);   // Green
  delay(1000);
  setColor(0, 0, 255);   // Blue
  delay(1000);
  setColor(255, 255, 0); // Yellow
  delay(1000);
}

void setColor(int redValue, int greenValue, int blueValue) {
  analogWrite(redPin, redValue);
  analogWrite(greenPin, greenValue);
  analogWrite(bluePin, blueValue);
}"""
    },
    "12": {
        "name": "Piezo Buzzer (Tone and Alarms)",
        "code": """int buzzerPin = 8;

void setup() {
  pinMode(buzzerPin, OUTPUT);
}

void loop() {
  // Play a 1000Hz tone for 500 milliseconds
  tone(buzzerPin, 1000); 
  delay(500);
  
  // Stop the tone for 500 milliseconds
  noTone(buzzerPin);     
  delay(500);
  
  // Quick alarm pulse sequence
  for (int i = 0; i < 3; i++) {
    tone(buzzerPin, 2000);
    delay(100);
    noTone(buzzerPin);
    delay(100);
  }
  delay(2000); // Wait before next cycle
}"""
    },
    "13": {
        "name": "16x2 LCD Display (I2C Module)",
        "code": """// Library needed: LiquidCrystal I2C
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

// Set the LCD address to 0x27 for a 16 chars and 2 line display
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  lcd.init();          // Initialize the LCD
  lcd.backlight();     // Turn on backlight
  
  lcd.setCursor(0, 0); // Top Row
  lcd.print("Arduino Project");
  
  lcd.setCursor(0, 1); // Bottom Row
  lcd.print("Status: Active");
}

void loop() {
  // Static screen context, loop empty
}"""
    },
    "14": {
        "name": "OLED Display (SSD1306 I2C 128x64)",
        "code": """// Libraries needed: Adafruit_GFX and Adafruit_SSD1306
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void setup() {
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { 
    for(;;); // Loop forever if display failed
  }
  
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  
  display.setCursor(10, 10);
  display.println("OLED INITIALIZED");
  
  display.setTextSize(2);
  display.setCursor(10, 30);
  display.println("HELLO!");
  
  display.display(); // Push layout to screen hardware
}

void loop() {
}"""
    },
    "15": {
        "name": "TFT Display (ST7735 SPI Color screen)",
        "code": """// Libraries needed: Adafruit_GFX and Adafruit_ST7735
#include <Adafruit_GFX.h>    
#include <Adafruit_ST7735.h> 
#include <SPI.h>

#define TFT_CS     10
#define TFT_RST    9  
#define TFT_DC     8

Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS,  TFT_DC, TFT_RST);

void setup() {
  tft.initR(INITR_BLACKTAB); // Initialize chip variant
  tft.fillScreen(ST7735_BLACK);
  
  tft.setCursor(15, 30);
  tft.setTextColor(ST7735_RED);
  tft.setTextSize(2);
  tft.println("TFT COLOR");
  
  tft.setCursor(15, 60);
  tft.setTextColor(ST7735_GREEN);
  tft.setTextSize(1);
  tft.println("Systems Operational.");
}

void loop() {
}"""
    },
    "16": {
        "name": "Seven-Segment Display (1-Digit Direct)",
        "code": """// Pins assigned to segments A, B, C, D, E, F, G
int segA = 2; int segB = 3; int segC = 4; int segD = 5;
int segE = 6; int segF = 7; int segG = 8;

void setup() {
  for(int i = 2; i <= 8; i++){
    pinMode(i, OUTPUT);
  }
}

void loop() {
  displayZero();
  delay(1000);
  displayOne();
  delay(1000);
}

void displayZero() {
  digitalWrite(segA, HIGH); digitalWrite(segB, HIGH);
  digitalWrite(segC, HIGH); digitalWrite(segD, HIGH);
  digitalWrite(segE, HIGH); digitalWrite(segF, HIGH);
  digitalWrite(segG, LOW);
}

void displayOne() {
  digitalWrite(segA, LOW);  digitalWrite(segB, HIGH);
  digitalWrite(segC, HIGH); digitalWrite(segD, LOW);
  digitalWrite(segE, LOW);  digitalWrite(segF, LOW);
  digitalWrite(segG, LOW);
}"""
    }
}

def slow_print(text, delay=0.003):
    """Prints text character by character for a smooth streaming look."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def display_menu():
    print("\n=============================================")
    print("ARDUINO CODE HUB TERMINAL")
    print("=============================================")
    for key, value in sensor_data.items():
        # Clean columns structure for clear scannability
        print(f" [{key.zfill(2)}] {value['name']}")
    print(" [exit] Quit program")
    print("=============================================\n")

def main():
    while True:
        display_menu()
        choice = input("Select a hardware number (1-16) to stream code: ").strip()

        if choice.lower() == 'exit' or choice == '0':
            print("\nExiting Code Hub... Goodbye!")
            break
        elif choice in sensor_data or choice.lstrip('0') in sensor_data:
            # Clean normalized index keys (e.g. handling "1" or "01")
            clean_choice = choice.lstrip('0') if choice.lstrip('0') in sensor_data else choice
            print(f"\n--- ARDUINO CODE FOR: {sensor_data[clean_choice]['name']} ---")
            
            # Streams the code character by character smoothly
            slow_print(sensor_data[clean_choice]['code'])
            
            print("-" * 55)
            input("\nPress Enter to return to the menu...")
        else:
            print("\nInvalid choice! Please enter a valid index number (1 to 16) or 'exit'.")

if __name__ == "__main__":
    main()