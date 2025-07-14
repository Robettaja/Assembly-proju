#include <Arduino.h>
#include <ArduinoBLE.h>

BLEService customService("180C");
BLECharacteristic rxChar("2A56", BLEWrite | BLERead | BLENotify, 3);  // 3-byte writable

void setup() {
  Serial.begin(9600);
  while (!Serial);  // wait for Serial connection (on native USB)

  if (!BLE.begin()) {
    Serial.println("BLE init failed!");
    while (1);
  }

  BLE.setLocalName("BLE_Test");
  BLE.setAdvertisedService(customService);
  customService.addCharacteristic(rxChar);
  BLE.addService(customService);

  BLE.advertise();
  Serial.println("BLE peripheral ready");
}

void loop() {
  BLEDevice central = BLE.central();

  if (central) {
    Serial.print("Connected to: ");
    Serial.println(central.address());

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

        // Serial.print("Received: ");
        // Serial.print(payload[0]); Serial.print(", ");
        // Serial.print(payload[1]); Serial.print(", ");
        // Serial.print(payload[2]);

        if (elapsed > 0) {
          // Serial.print(" | Time since last: ");
          // Serial.print(elapsed);
          // Serial.println(" ms");

          // Accumulate for average calculation
          sumElapsed += elapsed;
          count++;
        } else {
          Serial.println(" | First message");
        }

        // Every 1 second, print average elapsed time
        if (millis() - lastPrintTime >= 1000 && count > 0) {
          unsigned long averageElapsed = sumElapsed / count;
          Serial.print("Average elapsed time per message (last 1s): ");
          Serial.print(averageElapsed);
          Serial.println(" ms");
          // Reset counters for next second
          sumElapsed = 0;
          count = 0;
          lastPrintTime = millis();
        }
      }
    }

    Serial.println("Disconnected.");
  }
}