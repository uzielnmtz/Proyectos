#include<OneWire.h>
#include<DallasTemperature.h>
#define Pin 2

OneWire ourWire(Pin);
DallasTemperature sensors(&ourWire);



const int analogInPin2 = A1;
const int analogInPin3 = A2;
const int sensorPin = A3;
int sensorValue1 = 0;
int sensorValue2 = 0;
int sensorValue3 = 0;
int readingTemp = 0;
float voltage = 0;
float voltage1 = 0;
float voltage2 = 0;
float voltage3 = 0;
float res1 = 10000;
float res2 = 15000;
float res3 = 10000;
float therm1 = 0;
float therm2 = 0;
float therm3 = 0;
float buff1;
float buff2;
float buff3;
float temp = 0;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  sensors.begin();

}

void loop() {
  // put your main code here, to run repeatedly:
  // termometro
  sensors.requestTemperatures();
  Serial.print(sensors.getTempCByIndex(0));
  Serial.print("\t");

  // Segundo termistor
  sensorValue2 = analogRead(analogInPin2);
  voltage2= sensorValue2 * (5.0/1023.0);
  buff2 = (5.0/voltage2) - 1;
  therm2 = res2/buff2;
  //Serial.print("\t");
  //Serial.print(therm2);

  // Tercer termistor
  sensorValue3 = analogRead(analogInPin3);
  voltage3 = sensorValue3 * (5.0/1023.0);
  buff3 = (5.0/voltage3) - 1;
  therm3 = res3/buff3;
  Serial.print("\t");
  Serial.print(therm3);
  Serial.print('\t');
  Serial.println(millis());
  delay(1000);
} 


