  #include <HardwareSerial.h>
#include <WiFi.h>
#include <WiFiMulti.h>
#include <Arduino.h>

#define dirPin 18       // pin 5
#define stepPin 19      // pin 6
#define dirPin2 4       // pin 7
#define stepPin2 5      // pin 11

HardwareSerial SerialPort(2);
WiFiMulti WiFiMulti;
WiFiClient client;

uint32_t message = 0;
int dist_max = 200;     
int dist_min = 75;     
int timer = 0;
int localisationcount = 1;
int message_id;
const uint16_t port = 5555;
const char * host = "192.168.0.33";
bool found_red = false;
bool found_blue = false;
bool found_yellow = false;

unsigned long curtime;
unsigned long red_time;
unsigned long blue_time;
unsigned long yellow_time;
unsigned long yr_time;
unsigned long rbj_time;

void setup() {
  //open UART connections
  Serial.begin(115200);
  SerialPort.begin(115200, SERIAL_8N1, 17, 16);

  //assign pins as output
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(stepPin2, OUTPUT);
  pinMode(dirPin2, OUTPUT);


  //connect to wifi and establish connection to server
  WiFiMulti.addAP("SSID", "PASSWORD");

  while (WiFiMulti.run() != WL_CONNECTED) {
    Serial.println("Waiting for WiFi connection...");
    delay(500);
  }

  Serial.println("WiFi connected");

  while (!client.connect(host, port)) {
    Serial.println("Connection to Server failed.");
    Serial.println("Waiting 3 seconds before retrying...");
    delay(3000);
  }

}



void loop() {

  //if at least one message is available in the buffer
  if (SerialPort.available() >= 4) { 
     //read all 4 bytes of message into buffer                            
    SerialPort.readBytes((uint8_t*)&message, 4);
    message_id = message >> 27;
  
    //if message containing x_min coordinate
    if (message_id == 0) {                                       
      message = message & 0b00000111111111110000000000000000;
      int x_min = message >> 16;
      Serial.println(x_min);
  
      //if wall getting too far from rover
      if (x_min > dist_far) {                                     
        Serial.println("Turning right");
        digitalWrite(dirPin, HIGH);
        digitalWrite(dirPin2, HIGH);
        // SPIN 1 REVOLUTION MEDIUM SPEED
        for (int i = 0; i < 200; i++) {
          digitalWrite(stepPin, HIGH);
          digitalWrite(stepPin2, HIGH);
          delayMicroseconds(2000);
          digitalWrite(stepPin, LOW);
          digitalWrite(stepPin2, LOW);
          delayMicroseconds(2000);
        }
        client.print("MR");
      }
      
      // if wall getting too close to rover
      else if (x_max < dist_close) {                               
        Serial.println("Turning left");
        digitalWrite(dirPin, LOW);
        digitalWrite(dirPin2, LOW);
        // SPIN 1 REVOLUTION MEDIUM SPEED
        for (int i = 0; i < 200; i++) {
          digitalWrite(stepPin, HIGH);
          digitalWrite(stepPin2, HIGH);
          delayMicroseconds(2000);
          digitalWrite(stepPin, LOW);
          digitalWrite(stepPin2, LOW);
          delayMicroseconds(2000);
        }
        client.print("ML");
      }
  
      // if wall appropriate distance from Rover
      else {
        Serial.println("Going forward");                           
        digitalWrite(dirPin, HIGH);
        digitalWrite(dirPin2, LOW);
        // SPIN 1 REVOLUTION MEDIUM SPEEDk
        for (int i = 0; i < 200; i++) {
          digitalWrite(stepPin, HIGH);
          digitalWrite(stepPin2, HIGH);
          delayMicroseconds(2000);
          digitalWrite(stepPin, LOW);
          digitalWrite(stepPin2, LOW);
          delayMicroseconds(2000);
        }
        client.print("MF");
      }
      delay(1000);
    }
  
    curtime=millis();
    if (curtime == 30000*localisationcount) {
      Localise();
      localisationcount += 1;
    }
  }
}




void Localise(){
  while(1){
    //start spinning on the spot clockwise slowly
    digitalWrite(dirPin, HIGH);
    digitalWrite(dirPin2, HIGH);
    digitalWrite(stepPin, HIGH);
    digitalWrite(stepPin2, HIGH);
    delayMicroseconds(2000);
    digitalWrite(stepPin, LOW);
    digitalWrite(stepPin2, LOW);
    delayMicroseconds(2000);
    
    
    if(found_yellow == false){
      if (SerialPort.available() >= 4) { 
        //read all 4 bytes of message into buffer                            
        SerialPort.readBytes((uint8_t*)&message, 4);
        message_id = message >> 27;
        if(message_id == 7){
          int y_min_y = (message & 0b00000111111111110000000000000000) >>  16;
          int y_max_y = (message & 0b00000000000000000000011111111111);
          int yellow_height = y_min_y - y_max_y;
          yellow_time = millis();
          found_yellow = true;
        }
      }
    }

    if(found_yellow == true and found_red == false){
      if (SerialPort.available() >= 4) { 
        //read all 4 bytes of message into buffer                            
        SerialPort.readBytes((uint8_t*)&message, 4);
        message_id = message >> 27;
        if(message_id == 3){
          int y_min_r = (message & 0b00000111111111110000000000000000) >>  16;
          int y_max_r = (message & 0b00000000000000000000011111111111);
          int red_height = y_min_r - y_max_r;
          blue_time = millis();
          found_red = true;
        }
      }
    }

    if(found_yellow == true and found_red == true and found_blue == false){
      if (SerialPort.available() >= 4) { 
        //read all 4 bytes of message into buffer                            
        SerialPort.readBytes((uint8_t*)&message, 4);
        message_id = message >> 27;
        if(message_id == 5){
          int y_min_b = (message & 0b00000111111111110000000000000000) >>  16;
          int y_max_b = (message & 0b00000000000000000000011111111111);
          int blue_height = y_min_b - y_max_b;
          blue_time = millis();
          found_blue = true;
        }
      }
    }


    if(found_yellow == true and found_red == true and found_blue == true){
      yr_time = yellow_time - red_time;
      rb_time = red_time - blue_time;
      client.print("L", yellow_height, "|", red_height, "|", blue_height, "|", yr_time, "|", rb_time); // raw variables to keep esp processing to a minimum and distribute some load to EC2 server instance
      found_yellow = false;
      found_red = false;
      found_blue = false;
    }
    break;
  }
}
