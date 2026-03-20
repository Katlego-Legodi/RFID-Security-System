#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "secrets.h" // This pulls in my WiFi name and password safely

// Pins for the RFID reader
#define SS_PIN 5
#define RST_PIN 22
MFRC522 rfid(SS_PIN, RST_PIN);

// Pulling the hidden WiFi details from secrets.h
const char* ssid = SECRET_SSID;
const char* password = SECRET_PASS;

// Using the IP Alias we set on my Linux Mint laptop (10.112.185.239)
String serverUrl = "http://10.112.185.239:5000/scan?tag_id=";

void setup() {
  Serial.begin(115200);
  SPI.begin();
  rfid.PCD_Init();

  // Connecting to the home network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print("."); 
  }
  Serial.println("\nWiFi connected! System is live.");
}

void loop() {
  // Checking for a card tap
  if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
    return;
  }

  // Formatting the Tag ID so Python can read it easily
  String tagId = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    tagId += String(rfid.uid.uidByte[i], HEX);
  }
  tagId.toUpperCase();

  Serial.println("Scanned Tag: " + tagId);

  // Sending the ID to the Flask server on my laptop
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String fullUrl = serverUrl + tagId;
    
    http.begin(fullUrl);
    int httpResponseCode = http.GET(); 

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Server Response: " + response);
      // If server says 'DENIED', the alarm logic we wrote in Python kicks in
    } else {
      Serial.print("Connection Error: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  }

  delay(2000); // Wait 2 seconds so it doesn't spam the database
}
