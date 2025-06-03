#include <WiFi.h>
#include <WiFiUdp.h>

WiFiUDP Udp;

const char *ssid = "Roope";
const char *pass = "12345678";

unsigned int port = 420;
char packetBuffer[255];

void setup() {
  Serial.begin(9600);
  while (!Serial)
    ;
  WiFi.begin(ssid, pass); // Start connecting to WiFi
  Serial.println("WiFi connected!");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  Udp.begin(port);
}
void loop() {
  float i0;
  float i1;
  int packetSize = Udp.parsePacket();
  if (packetSize == 8) {
    Udp.read((char *)&i0, 4);
    Udp.read((char *)&i1, 4);
    int hForce = i0 * 255;
    int vForce = i1 * 255;
    if (hForce > 0 ) {
      analogWrite(LED_BUILTIN, 255);
    } else if(hForce < 0) {
      analogWrite(LED_BUILTIN, 0);
    }
    if (vForce > 0) {
      analogWrite(LED_BUILTIN, 255);
    } else if(vForce < 0) {
      analogWrite(LED_BUILTIN, 0);
    }
  }
}