#include <Arduino.h>
#include <ArduinoBLE.h>

BLEService customService("180C");
BLECharacteristic rxChar("2A56", BLEWrite | BLERead | BLENotify, 3);

void setup() {
  Serial.begin(115200); // Higher baud rate
  while (!Serial);
  
  if (!BLE.begin()) {
    Serial.println("BLE init failed!");
    while (1);
  }
  
  BLE.setLocalName("BLE_Test");
  BLE.setAdvertisedService(customService);
  customService.addCharacteristic(rxChar);
  BLE.addService(customService);
  
  // Set connection parameters for faster communication
  BLE.setConnectionInterval(6, 12); // 7.5ms to 15ms intervals
  BLE.setConnectable(true);
  
  BLE.advertise();
  Serial.println("BLE peripheral ready with optimized settings");
}

void loop() {
  BLEDevice central = BLE.central();
  
  if (central) {
    Serial.print("Connected to: ");
    Serial.println(central.address());
    
    // Request faster connection parameters after connection
    central.setConnectionInterval(6, 12); // Min 7.5ms, Max 15ms
    
    unsigned long lastTime = 0;
    unsigned long sumElapsed = 0;
    unsigned int count = 0;
    unsigned long lastPrintTime = millis();
    
    while (central.connected()) {
      if (rxChar.written()) {
        unsigned long now = millis();
        unsigned long elapsed = lastTime ? now - lastTime : 0;
        lastTime = now;
        
        uint8_t payload[3];
        rxChar.readValue(payload, 3);
        
        if (elapsed > 0) {
          sumElapsed += elapsed;
          count++;
        } else {
          Serial.println(" | First message");
        }
        
        // Print stats every 1 second
        if (millis() - lastPrintTime >= 1000 && count > 0) {
          unsigned long averageElapsed = sumElapsed / count;
          Serial.print("Average: ");
          Serial.print(averageElapsed);
          Serial.print(" ms | Count: ");
          Serial.print(count);
          Serial.print(" | Rate: ");
          Serial.print(1000.0 / averageElapsed);
          Serial.println(" Hz");
          
          sumElapsed = 0;
          count = 0;
          lastPrintTime = millis();
        }
      }
    }
    Serial.println("Disconnected.");
  }
}