#include<Servo.h>
int Servopin=3;
Servo Servo1;
int triggerpin=11;
int echopin=12;
int time;
int distance;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(triggerpin,OUTPUT);
  pinMode(echopin,INPUT);
  pinMode(13,OUTPUT);
  pinMode(10,OUTPUT);
  Servo1.attach(Servopin);
}

void loop() {
  digitalWrite(triggerpin,HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerpin,LOW);
  time=pulseIn(echopin,HIGH);
  distance=(time*0.034);
  if(distance<=50)
  {Serial.println("Door Open");
  Serial.print("distance=");
  Serial.println(distance);
  digitalWrite(13,HIGH);
  delay(500);
   Servo1.write(90);
  delay(1000);
  }
  else
  {Serial.println("Door Open");
  Serial.print("distance=");
  Serial.println(distance);
  digitalWrite(10,HIGH);
  delay(500);
  Servo1.write(0);
  delay(1000);
  }

}
