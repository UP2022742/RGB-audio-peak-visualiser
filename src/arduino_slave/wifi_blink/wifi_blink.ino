// Henry's Bench
//Checking to ensure you can connect ESP-12E to a router
     
#include <ESP8266WiFi.h>
 
const char* ssid     = "BTHub6-TCMG";
const char* password = "RobinsonHouse3";     

int wifiStatus;
 
void setup() {
  Serial.begin(115200);\
  delay(200);
  Serial.print("Your are connecting to;");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
  }
}   
     
void loop() {
  wifiStatus = WiFi.status();
  if(wifiStatus == WL_CONNECTED){
     Serial.println(WiFi.localIP());  
  }
  else{
    Serial.println("WiFi not connected");
  }
  delay(200); // check for connection every once a second
}
