// This #include statement was automatically added by the Spark IDE.
#include "HttpClient/HttpClient.h"

HttpClient http;
http_header_t headers[] = {
     { "Content-Type", "application/json" },
     { NULL, NULL } // NOTE: Always terminate headers with NULL
};
http_request_t request;
http_response_t response;

int relay_status = 0;
int relay_set = D1;
int relay_reset = D0;
String code = "";

void setup() {
    pinMode(relay_set, OUTPUT);
    pinMode(relay_reset, OUTPUT);
    
    //Serial.begin(9600);
    Serial1.begin(9600);

    Spark.function("relay",relay);
    Spark.function("blink",blink);
    
    digitalWrite(relay_set, LOW);
    digitalWrite(relay_reset, LOW);

    request.hostname = "vast-oasis-4934.herokuapp.com";
    request.port = 80;
}

void loop() {
    if (Serial1.available()) {
        char inChar = Serial1.read();
        Serial.write(inChar);
        code += inChar;
/*

        Serial.print("[");
        Serial.print(code.length());
        Serial.print("]");
*/
        if (code.length()==16) {
          //Serial.println(code);
          /*
          response.body = "";
          response.status = 0;
          request.path = "/tables/96/deactivate?id="+code;
          http.get(request, response, headers);
          */
          if (relay_status==1) {
              relayOff();
          } else {
              relayOn();
          }
          code = "";
        }
    }
}

void relayOn() {
    digitalWrite(relay_set, HIGH);
    relay_status = 1;
    delay(100);
    digitalWrite(relay_set, LOW);
}

void relayOff() {
    digitalWrite(relay_reset, HIGH);
    relay_status = 0;
    delay(100);
    digitalWrite(relay_reset, LOW);
}


int blink(String command) {
    relayOn();
    delay(500);
    relayOff();
    delay(500);
    relayOn();
    delay(500);
    relayOff();
    delay(500);
    relayOn();
    delay(500);
    relayOff();
    return 0;
}

int relay(String command) {
    if (command=="on") {
        relayOn();
        return 1;
    } else {
        relayOff();
        return 0;
    }
}