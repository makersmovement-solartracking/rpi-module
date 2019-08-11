#include <Wire.h>

#define SlaveAddress 0x8

void sendData();

void setup() {
  // Start the connections as a slave
  Wire.begin(SlaveAddress);
  // When the R_Pi requests data from the arduino, call the sendData function.
  Wire.onRequest(sendData);
}

void loop() {
  delay(1);
}

void ldrIntToByte (int ldrValues[], byte ldrByteValues[], int ldrLength) {
  /*
    / Transform the integers into bytes, in order to send them
    / through I²C with precision.
  */
  for (int i = 0, j = 0; i < ldrLength; i++, j += 2) {
    // Iterate through the int values array, transforming each one into byte values to append to the ldrByteValues Array
    ldrByteValues[j] = (ldrValues[i] >> 8) & 0xFF;
    ldrByteValues[j + 1] = ldrValues[i] & 0xFF;
  }
}

void sendData() {
  // Collects the data from the LDRs, storing it within the ldrIntValues array
  int ldrIntValues[] = {analogRead(A1), analogRead(A0)}; // The left LDR must always come before the right LDR

  // Length of the LDR's value array and length of LDR's byte value array
  int ldrLength = (sizeof(ldrIntValues) / sizeof(ldrIntValues[0]));
  int ldrByteLength = ldrLength * 2;

  // Declares an array which will store the byte values
  byte ldrArray[ldrByteLength];

  // Transforms the integers into bytes
  ldrIntToByte(ldrIntValues, ldrArray, ldrLength);

  // Sends the data individually via I²C to the Raspberry Pi
  for (int i = 0; i < ldrByteLength; i += 2) {
      byte submissionValuesArray[] = {ldrArray[i], ldrArray[i+1]};
      Wire.write(submissionValuesArray, 2);
  }
}
