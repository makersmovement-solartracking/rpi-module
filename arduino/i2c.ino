#include <Wire.h>

byte *ldrArray;

void sendData();

void setup() {
  Serial.begin(9600);
  // Start the connections as a slave
  Wire.begin(0x8);
  // When the R_Pi requests data from the arduino, call the sendData function.
  Wire.onRequest(sendData);
}

void loop();

void sendData() {
  // Collects the data from the LDRs, storing it within the ldrIntValues array
  int ldrIntValues[] = {analogRead(A0), analogRead(A1)};
  // Length of the LDR's value array
  int ldrLength = (sizeof(ldrArray)/sizeof(ldrArray[0]));
  // Transforms the integers into bytes
  *ldrArray = ldrIntToByte(ldrIntValues, ldrLength);
  // Sends the data via I²C to the Raspberry Pi
  Wire.write(ldrArray, ldrLength);
}

byte ldrIntToByte (int ldrValues[], int ldrLength) {
  /* 
  / Transform the integers into bytes, in order to send them
  / through I²C with precision.
  */
  byte byteLdrValues[ldrLength];
  for (int i = 0, j = i + 1; i < ldrLength; i+= 2) {
    /*
    / Iterates through the integer array storing the bytes of each number,
    / separated into two, in the byteLdrValues array.
    */
    byteLdrValues[i] = (ldrValues[i] >> 8) & 0xFF;
    byteLdrValues[j] = ldrValues[i] & 0xFF;
    }
  // Returns the memory address of the byte array
  return byteLdrValues;
}

