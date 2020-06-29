// Henry's Bench
//Checking to ensure you can connect ESP-12E to a router
#include <ESP8266WiFi.h>
 
const char* ssid     = "BTHub6-TCMG";
const char* password = "RobinsonHouse3";
byte server[] = { 192, 168, 1, 106 }; 
int wifiStatus;
WiFiClient client;
 
void setup() {
  
  Serial.begin(115200);\

  // We start by connecting to a WiFi network
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
}   
     
void loop() {
  wifiStatus = WiFi.status();

  String dataString = "sensor1,";
  dataString += " sensor2,";

  if(wifiStatus == WL_CONNECTED){
     sendData(dataString);
  }
  else{
    Serial.println("");
    Serial.println("WiFi not connected");
  }
  delay(1000); // check for connection every once a second
}

// this method makes a HTTP connection to the server:
void sendData(String thisData) {
  client.flush();
  if (client.connect(server, 7000)) {
    client.write((uint8_t)1);
    client.write((uint8_t)0);
    client.write((uint8_t)(thisData.length() + 1));
    client.write((uint8_t)0);

    // here's the actual content of the PUT request:
    client.print(thisData);
    client.flush();
    client.stop();
  } 
  else {
    // if you couldn't make a connection:
    Serial.println("connection failed");
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();
  }
}
