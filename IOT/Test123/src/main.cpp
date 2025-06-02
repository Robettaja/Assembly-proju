#include <WiFi.h>
#include <WiFiUdp.h>

WiFiUDP Udp;

const char *ssid = "WIFI_NAME";
const char *pass = "WIFI_PASS";

unsigned int port = 420;
char packetBuffer[255];

void setup() {
  Serial.begin(9600);
  while (!Serial)
    ;
  WiFi.begin(ssid, pass); // Start connecting to WiFi
  Serial.println("");
  Serial.println("WiFi connected!");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  Udp.begin(port);
}
void loop() {
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    Serial.println(1);
    int len = Udp.read(packetBuffer, 255);
    if (len > 0)
      packetBuffer[len] = 0;
    char cmd = packetBuffer[0];
    switch (cmd) {
    case 'L':
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println("IP address: ");
      break;
    case 'R':
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println("address: ");
      break;
    case 'U':;
      break;
    case 'D':;
      break;
    }
  }
}