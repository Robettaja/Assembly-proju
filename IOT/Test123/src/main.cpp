#include <WiFi.h>
#include <WiFiUdp.h>

WiFiUDP Udp;

const char *ssid = "Roope";
const char *pass = "12345678";

unsigned int port = 420;
char packetBuffer[255];

void setup() {
  Serial.begin(250000);
  while (!Serial)
    ;

  analogWrite(LED_BUILTIN, 255);
  bool isConnected = false;

  while (!isConnected) {

    WiFi.begin(ssid, pass); // Start connecting to WiFi
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
    }
    if (WiFi.localIP() != "0.0.0.0")
      isConnected = true;
  }

  analogWrite(LED_BUILTIN, 0);

  Serial.println("WiFi connected!");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  Udp.begin(port);
}
void loop() {
  char buf[8];
  float i0;
  float i1;
  int packetSize = Udp.parsePacket();
  if (packetSize == 8) {
    Udp.read(buf, 8);
    memcpy(&i0, buf, 4);
    memcpy(&i1, buf + 4, 4);
    int hForce = i1 * 255;
    int vForce = i0 * 255;
    if (i0 > 0.05) {
      analogWrite(LED_BUILTIN, vForce);
    } else if (i0 < -0.05) {

    } else {

      analogWrite(LED_BUILTIN, 0);
    }
    if (i1 > 0.05) {
    } else if (i1 < -0.05) {
    } else {
    }
  }
}