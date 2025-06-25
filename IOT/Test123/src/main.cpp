#include <Servo.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <MsgPack.h>

WiFiUDP Udp;
Servo servo;

const char *ssid = "-Tomi-";
const char *pass = "Tomi1104!";

unsigned int port = 420;
char packetBuffer[255];

void setup() {
  Serial.begin(9600);
  while (!Serial)
    ;

  servo.attach(4);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);

  analogWrite(LED_BUILTIN, 255);
  bool isConnected = false;

  while (!isConnected) {

    WiFi.begin(ssid, pass); // Start connecting to WiFi
    while (WiFi.status() != WL_CONNECTED) {
      delay(10);
    }
    if (WiFi.localIP() != "0.0.0.0")
      isConnected = true;
  }

  analogWrite(LED_BUILTIN, 0);

  Serial.println("WiFi connected!");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  if (!Udp.begin(port)) {
    Serial.println("UDP port 420 start failed");
    while (1)
      ;
  }
}
void loop() {
  int packetSize = Udp.parsePacket();
  if (packetSize > 0) {
    char buf[32];
    Udp.read(buf, 32);
    buf[packetSize] = '\0';

    if (strcmp(buf, "DISCOVER_ARDUINO") == 0) {
      Serial.println(Udp.remoteIP());
      IPAddress ip = WiFi.localIP();
      Udp.beginPacket(Udp.remoteIP(), 1420);
      Udp.print("CAR1_IP:");
      Udp.print(ip);
      Udp.endPacket();
    }
  }

  // char buf[8];
  // float i0;
  // float i1;
  // packetSize = Udp.parsePacket();
  // if (packetSize == 8) {
  //   Udp.read(buf, 8);
  //   memcpy(&i0, buf, 4);
  //   memcpy(&i1, buf + 4, 4);
  //   int hForce = i1 * 255;
  //   if (i0 > 0.05) {
  //     int rotationAmount = 98 - (i0 * 45);
  //     servo.write(rotationAmount);
  //   } else if (i0 < -0.05) {
  //     int rotationAmount = 98 + (i0 * 45 * -1);
  //     servo.write(rotationAmount);
  //   } else {
  //     servo.write(98);
  //   }
  //   if (i1 > 0.05) {

  //     analogWrite(9, hForce);
  //     digitalWrite(7, HIGH);
  //     digitalWrite(8, LOW);
  //   } else if (i1 < -0.05) {

  //     analogWrite(9, hForce * -1);
  //     digitalWrite(7, LOW);
  //     digitalWrite(8, HIGH);
  //   } else {
  //     analogWrite(9, 0);
  //     digitalWrite(7, LOW);
  //     digitalWrite(8, LOW);
  //   }
  // }
}