#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <env.h>
#include <ArduinoJson.h>

#define led 2
int getWaterLevel();
int water = 0;
int sensorinputpin = 5;


void setup() {
  Serial.begin(115200);
  pinMode(led,OUTPUT);

  WiFi.begin(SSID,PASS);
  while (WiFi.status()!= WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
  
}

void loop() {
  water = getWaterLevel();
  if (water>=80 && water<=100){
    digitalWrite(led,HIGH);
  }else{
    digitalWrite(led, LOW);
  }

  HTTPClient http;
  http.begin("http://192.168.0.10:3000/tank");
  http.addHeader("Content-Type", "application/json"); // Send POST request


  char output[128];
  const size_t CAPACITY = JSON_OBJECT_SIZE(4);
  StaticJsonDocument<CAPACITY> doc;

  doc["tank_id"].set(WiFi.macAddress());
  doc["water_level"].set(water);
  
  serializeJson(doc,output);
  int httpResponseCode = http.POST(String(output));
  String payload = "{}"; 
  if (httpResponseCode>0) {
    payload = http.getString();
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
    }
  // Free resources
  Serial.println(payload);
  delay(5000);
  http.end();
}

int getWaterLevel(){
  //using LM35 which does 10mV/1 deg. C
  int water_value = ((analogRead(sensorinputpin)/4095)*5)/0.01;//4095 because 2^12 = 4096 since 12 bit ADC
  return water_value;
}
