// #include<Servo.h>
#include<ESP8266WiFi.h>
#include "FirebaseESP8266.h"
// Provide the RTDB payload printing info and other helper functions.
#include <addons/RTDBHelper.h>

#include<ArduinoJson.h>
#define WIFI_SSID "LQHOMES-155NVT-203"
#define WIFI_PASSWORD "62778763"
#define DATABASE_URL "iot-ptit-61e0e-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "A0oQYNoqbaPuw8hx5BGWor0eDuN6synXyALS9jap"

FirebaseData firebaseData;
// WiFiClient client;
/* 4, Define the FirebaseAuth data for authentication data */
FirebaseAuth auth;
/* Define the FirebaseConfig data for config data */
FirebaseConfig config;

String path = "/";
FirebaseJson json;

// dong co moter
// Servo myServo;

unsigned long t1 = 0;
// Biến để lưu giá trị từ Firebase
String action;
byte x = 0;
void setup(){
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while(WiFi.status() != WL_CONNECTED){
    delay(5000);
    Serial.print(".");
    Serial.println();
  }
  Serial.print("Connect with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  /* Assign the database URL(required) */
    config.database_url = DATABASE_URL;

    config.signer.test_mode = true;
    // Comment or pass false value when WiFi reconnection will control by your code or third party library e.g. WiFiManager
    Firebase.reconnectNetwork(true);
    /* Initialize the library with the Firebase authen and config */
    Firebase.begin(&config, &auth);

}

void loop(){
  Firebase.setString(firebaseData, path+"test", "Damocua");
  
  if(millis()-t1 > 1000){
    if(Firebase.getString(firebaseData, path + "test")){
      action = firebaseData.stringData();
      Serial.println(action);
    }
    t1 = millis();

  }

}