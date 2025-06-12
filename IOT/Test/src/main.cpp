#include <Arduino.h>
#include <Servo.h>

Servo servo;

void setup()
{

  Serial.begin(9600);
  servo.attach(9);
}

void loop()
{

  // int rotation = 45;
  // servo.write(0);
  // for(int i = 0; i < 4; i++) {
  //   rotation *= rotation * (i +1);
  //   servo.write(rotation);
  //   delay(500);
    

 
}
