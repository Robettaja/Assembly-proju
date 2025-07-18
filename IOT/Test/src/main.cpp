#include <ArduinoBLE.h>
#include <Servo.h>

float moveTowardsTarget(float current, float target, float speed, float dt);

BLEService customService("12345678-1234-5678-1234-56789abcdef0");
BLECharacteristic rxChar("abcdefab-cdef-1234-5678-abcdefabcdef", BLEWriteWithoutResponse | BLERead | BLENotify, 8);

Servo servo;

const char *carName = "CAR2";

const int ROTATION_AMOUNT = 30;
const int DEFAULT_ROTATION = 93;

const int MIN_POWER = 20;
const int MAX_POWER = 32;

const int SERVO_PIN = 10;
const int MOTOR_DIR_PIN = 11;
const int MOTOR_POWER_PIN = 12;

void setup()
{
  Serial.begin(9600);
  while (!Serial)
    ;

  servo.attach(SERVO_PIN);
  pinMode(MOTOR_DIR_PIN, OUTPUT);
  pinMode(MOTOR_POWER_PIN, OUTPUT);
  servo.write(DEFAULT_ROTATION);
  delay(1000);

  if (!BLE.begin())
  {
    Serial.println("BLE init failed!");
    while (1)
      ;
  }

  BLE.setLocalName(carName);
  BLE.setAdvertisedService(customService);
  customService.addCharacteristic(rxChar);
  BLE.addService(customService);
  rxChar.setValue(0);
  BLE.advertise();
  Serial.println("BLE peripheral ready");
}
unsigned long lastUpdate = millis();

float currentX = 0;
float currentY = 0;

void loop()
{

  BLEDevice central = BLE.central();

  if (central)
  {
    Serial.print("Connected to: ");
    Serial.println(central.address());

    while (central.connected())
    {

      unsigned long currentTime = millis();
      float deltaTime = (currentTime - lastUpdate) / 1000.0;
      lastUpdate = currentTime;
      if (rxChar.written())
      {
        if (rxChar.valueLength() == 8)
        {

          uint8_t payload[8];
          rxChar.readValue(payload, sizeof(payload));

          float x, y;
          memcpy(&x, &payload[0], 4);
          memcpy(&y, &payload[4], 4);

          currentX = x;
          currentY = moveTowardsTarget(currentY, y, 0.01, deltaTime);

          if (currentX > 0.05)
          {
            int rotationAmount = DEFAULT_ROTATION - (fabs(currentX) * ROTATION_AMOUNT);

            servo.write(rotationAmount);
          }
          else if (currentX < -0.05)
          {
            int rotationAmount = DEFAULT_ROTATION + (fabs(currentX) * ROTATION_AMOUNT);
            servo.write(rotationAmount);
          }
          else
          {
            servo.write(DEFAULT_ROTATION);
          }
          if (currentY > 0.05)
          {
            Serial.println("moving...");
            analogWrite(MOTOR_POWER_PIN, (int)(((fabs(currentY) - 0.05) / (1.0 - 0.05)) * (MAX_POWER - MIN_POWER) + MIN_POWER));
            digitalWrite(MOTOR_DIR_PIN, LOW);
          }
          else if (currentY < -0.05)
          {

            analogWrite(MOTOR_POWER_PIN, (int)(((fabs(currentY) - 0.05) / (1.0 - 0.05)) * (MAX_POWER - MIN_POWER) + MIN_POWER));
            digitalWrite(MOTOR_DIR_PIN, HIGH);
          }
          else
          {
            analogWrite(MOTOR_POWER_PIN, 0);
          }
        }
      }
    }

    Serial.println("Disconnected.");
  }
}
float moveTowardsTarget(float current, float target, float speed, float dt)
{
  float maxStep = dt / speed;

  float delta = target - current;

  if (fabs(delta) <= maxStep)
    return target;

  return current + (delta > 0 ? maxStep : -maxStep);
}