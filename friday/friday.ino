// This file is for ARDUINO TO for the friday project
// Using Arduino I planning to use it to 3 main baic things
// INFORAMTION ABOUT THE ROOM LIKE TEMP, HUMIDITY, IR INFO
// TO CONTROL THINGS INCLUDING LIGHT,
// FOR ROOM SECURITY CONFIRMATIONS INCLUDING PASSWORDS, OR FACE RECOGNITIONS,
#include <SimpleDHT.h>
int light = 8;
int DHT11 = 2;

//for dht11 sensor
SimpleDHT11 dht11(DHT11);


char command[20];
void setup(){
    Serial.begin(9600);
    //Serial.setTimeout(1);
    pinMode(light, OUTPUT);
}

void loop(){
  //read
  String state= "";
  state.reserve(15);
  if (Serial.available() > 0)
  {
      state = Serial.readString();
      state.toCharArray(command, 15);
      checkCommands(command);
  }
}

String temp_humdi(){
  byte temperature = 0;
  byte humidity = 0;
  int err = SimpleDHTErrSuccess;
  if ((err = dht11.read(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Read DHT11 failed, err="); Serial.print(SimpleDHTErrCode(err));
    Serial.print(","); Serial.println(SimpleDHTErrDuration(err)); delay(1000);
    return "ERROR";
  }
  String temp = String((float)temperature) + " *C, ";
  String humdi = String((float)humidity) + " H";
  Serial.print(temp + humdi);
  return (temp + humdi);
}

void checkCommands(char inStr[]){
    if(!strcmp(inStr, "light_on")){
      //hereGoes the command to turnOn the light
      digitalWrite(light, HIGH);
    }
    if(!strcmp(inStr, "light_off")){
      //command to turnOff the light
      digitalWrite(light, LOW);
    }
    if(!strcmp(inStr, "room_info")){
      //command to get info from DHT11
      Serial.print(temp_humdi());
    }
}
