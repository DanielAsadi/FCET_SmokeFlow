//Daniel Asadi
//Eng Sci 2T3
//FCET Lab, UTIAS
//From code created by Jason Kelly at CUI Inc.

/* MANUAL CONTROL FOR MEGA
   Set the baud rate to 115200 to view the serial stream the position from the AMT22.

   Arduino Pin Connections
   SPI Chip Select Enc 0:   Pin  2
   SPI Chip Select Enc 1:   Pin  3
   SPI MOSI                 Pin 11
   SPI MISO                 Pin 12
   SPI SCLK:                Pin 13

   AMT22 Pin Connections
   Vdd (5V):                Pin  1 RED
   SPI SCLK:                Pin  2 BROWN
   SPI MOSI:                Pin  3 ORANGE
   GND:                     Pin  4 BLACK
   SPI MISO:                Pin  5 GREEN
   SPI Chip Select:         Pin  6 YELLOW
*/

/* Include the SPI library for the arduino boards */
#include <SPI.h>

/* Serial rates for UART */
#define BAUDRATE 115200

/* SPI commands */
#define AMT22_NOP 0x00
#define AMT22_RESET 0x60
#define AMT22_ZERO 0x70

/* Define special ascii characters */
#define NEWLINE 0x0A
#define TAB 0x09

/* We will use these define macros so we can write code once compatible with 12 or 14 bit encoders */
#define RES12 12
#define RES14 14

/* SPI pins */
#define ENC_0 32    //YELLOW CABLE
#define ENC_1 1     //ALT ENCODER, NOT USED RN
#define SPI_MOSI 51 //ORANGE CABLE
#define SPI_MISO 50 //GREEN CABLE
#define SPI_SCLK 52 //BROWN CABLE
#define LEDY 22     //VALVE STATUS
#define LEDR 23     //CAM STATUS
#define LEDG 24     //WIRE STATUS
#define LEDB 25     //CAP STATUS
#define VALVE 13    //PWM
#define CAM 12      //PWM
#define WIRE 11     //PWM
#define CAP 10      //PWM
#define CAMOUT A0 //CAM RECORDING OUTPUT

//create a 16 bit variable to hold the encoders position
uint16_t encoderPosition;
//let's also create a variable where we can count how many times we've tried to obtain the position in case there are errors
uint8_t attempts;

int incomingByte; // a variable to read incoming serial data into

void setup()
{
  digitalWrite(WIRE, HIGH); //Set wire off by default
  digitalWrite(VALVE, LOW); //Set valve off by default
  //Set the modes for the SPI IO
  pinMode(SPI_SCLK, OUTPUT);
  pinMode(SPI_MOSI, OUTPUT);
  pinMode(SPI_MISO, INPUT);
  pinMode(ENC_0, OUTPUT);
  pinMode(ENC_1, OUTPUT);
  pinMode(LEDY, OUTPUT);
  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);
  pinMode(VALVE, OUTPUT);
  pinMode(CAM, OUTPUT);
  pinMode(WIRE, OUTPUT);
  pinMode(CAP, OUTPUT);

  //Initialize the UART serial connection for debugging
  Serial.begin(BAUDRATE);
  Serial.setTimeout(50);

  //Get the CS line high which is the default inactive state
  digitalWrite(ENC_0, HIGH);
  digitalWrite(ENC_1, HIGH);

  //set the clockrate. Uno clock rate is 16Mhz, divider of 32 gives 500 kHz.
  //500 kHz is a good speed for our test environment
  //SPI.setClockDivider(SPI_CLOCK_DIV2);   // 8 MHz
  SPI.setClockDivider(SPI_CLOCK_DIV4); // 4 MHz
  //SPI.setClockDivider(SPI_CLOCK_DIV8);   // 2 MHz
  //SPI.setClockDivider(SPI_CLOCK_DIV16);  // 1 MHz
  //SPI.setClockDivider(SPI_CLOCK_DIV32);  // 500 kHz
  //SPI.setClockDivider(SPI_CLOCK_DIV64);  // 250 kHz
  //SPI.setClockDivider(SPI_CLOCK_DIV128); // 125 kHz

  //start SPI bus
  SPI.begin();
}

void loop()
{
  //if you want to set the zero position before beggining uncomment the following function call
  //setZeroSPI(ENC_0);
  //setZeroSPI(ENC_1);
  /*int camOutput = analogRead(CAMOUT);
  float voltage = camOutput * (5.0 / 1023.0);
  if(voltage > 4){
    digitalWrite(LEDB, HIGH);    
  }
  else{
    digitalWrite(LEDB, LOW);
  }
  Serial.println(voltage);*/
  /* TEMPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
  attempts = 0; //set attemps counter at 0 so we can try again if we get bad position

  //this function gets the encoder position and returns it as a uint16_t
  //send the function either res12 or res14 for your encoders resolution
  encoderPosition = getPositionSPI(ENC_0, RES14);

  //if the position returned was 0xFFFF we know that there was an error calculating the checksum
  //make 3 attempts for position. we will pre-increment attempts because we'll use the number later and want an accurate count
  while (encoderPosition == 0xFFFF && ++attempts < 3){
    encoderPosition = getPositionSPI(ENC_0, RES14);} //try again
  
  if (encoderPosition == 0xFFFF){ //position is bad, let the user know how many times we tried
    Serial.print("Encoder 0 error. Attempts: ");
    Serial.print(attempts, DEC); //print out the number in decimal format. attempts - 1 is used since we post incremented the loop
    Serial.write("\r\n");}
  
  else { //position was good, print to serial stream
    Serial.println(encoderPosition, DEC);} //print the position in decimal format
  */
  if (Serial.available() > 0)
  {
    incomingByte = Serial.read(); // read the oldest byte in the serial buffer:

    if (incomingByte == 'A')
    {
      digitalWrite(VALVE, HIGH);
      digitalWrite(LEDY, HIGH);
    }
    else if (incomingByte == 'B')
    {
      digitalWrite(VALVE, LOW);
      digitalWrite(LEDY, LOW);
    }

    if (incomingByte == 'C')
    {
      digitalWrite(CAM, HIGH);
      digitalWrite(LEDR, HIGH);
    }
    else if (incomingByte == 'D')
    {
      digitalWrite(CAM, LOW);
      digitalWrite(LEDR, LOW);
    }

    if (incomingByte == 'E')
    {
      digitalWrite(WIRE, LOW);
      digitalWrite(LEDG, HIGH);
    }
    else if (incomingByte == 'F')
    {
      digitalWrite(WIRE, HIGH);
      digitalWrite(LEDG, LOW);
    }

    if (incomingByte == 'G')
    {
      digitalWrite(CAP, HIGH);
      digitalWrite(LEDB, HIGH);
    }
    else if (incomingByte == 'H')
    {
      digitalWrite(CAP, LOW);
      digitalWrite(LEDB, LOW);
    }
  }

  //For the purpose of this demo we don't need the position returned that quickly so let's wait a half second between reads
  //delay(250);   //delay() is in milliseconds
}

/*
   This function gets the absolute position from the AMT22 encoder using the SPI bus. The AMT22 position includes 2 checkbits to use
   for position verification. Both 12-bit and 14-bit encoders transfer position via two bytes, giving 16-bits regardless of resolution.
   For 12-bit encoders the position is left-shifted two bits, leaving the right two bits as zeros. This gives the impression that the encoder
   is actually sending 14-bits, when it is actually sending 12-bit values, where every number is multiplied by 4.
   This function takes the pin number of the desired device as an input
   This funciton expects res12 or res14 to properly format position responses.
   Error values are returned as 0xFFFF
*/
uint16_t getPositionSPI(uint8_t encoder, uint8_t resolution)
{
  uint16_t currentPosition; //16-bit response from encoder
  bool binaryArray[16];     //after receiving the position we will populate this array and use it for calculating the checksum

  //get first byte which is the high byte, shift it 8 bits. don't release line for the first byte
  currentPosition = spiWriteRead(AMT22_NOP, encoder, false) << 8;

  //this is the time required between bytes as specified in the datasheet.
  //We will implement that time delay here, however the arduino is not the fastest device so the delay
  //is likely inherantly there already
  delayMicroseconds(3);

  //OR the low byte with the currentPosition variable. release line after second byte
  currentPosition |= spiWriteRead(AMT22_NOP, encoder, true);

  //run through the 16 bits of position and put each bit into a slot in the array so we can do the checksum calculation
  for (int i = 0; i < 16; i++)
    binaryArray[i] = (0x01) & (currentPosition >> (i));

  //using the equation on the datasheet we can calculate the checksums and then make sure they match what the encoder sent
  if ((binaryArray[15] == !(binaryArray[13] ^ binaryArray[11] ^ binaryArray[9] ^ binaryArray[7] ^ binaryArray[5] ^ binaryArray[3] ^ binaryArray[1])) && (binaryArray[14] == !(binaryArray[12] ^ binaryArray[10] ^ binaryArray[8] ^ binaryArray[6] ^ binaryArray[4] ^ binaryArray[2] ^ binaryArray[0])))
  {
    //we got back a good position, so just mask away the checkbits
    currentPosition &= 0x3FFF;
  }
  else
  {
    currentPosition = 0xFFFF; //bad position
  }

  //If the resolution is 12-bits, and wasn't 0xFFFF, then shift position, otherwise do nothing
  if ((resolution == RES12) && (currentPosition != 0xFFFF))
    currentPosition = currentPosition >> 2;

  return currentPosition;
}

/*
   This function does the SPI transfer. sendByte is the byte to transmit.
   Use releaseLine to let the spiWriteRead function know if it should release
   the chip select line after transfer.
   This function takes the pin number of the desired device as an input
   The received data is returned.
*/
uint8_t spiWriteRead(uint8_t sendByte, uint8_t encoder, uint8_t releaseLine)
{
  //holder for the received over SPI
  uint8_t data;

  //set cs low, cs may already be low but there's no issue calling it again except for extra time
  setCSLine(encoder, LOW);

  //There is a minimum time requirement after CS goes low before data can be clocked out of the encoder.
  //We will implement that time delay here, however the arduino is not the fastest device so the delay
  //is likely inherantly there already
  delayMicroseconds(3);

  //send the command
  data = SPI.transfer(sendByte);
  delayMicroseconds(3);            //There is also a minimum time after clocking that CS should remain asserted before we release it
  setCSLine(encoder, releaseLine); //if releaseLine is high set it high else it stays low

  return data;
}

/*
   This function sets the state of the SPI line. It isn't necessary but makes the code more readable than having digitalWrite everywhere
   This function takes the pin number of the desired device as an input
*/
void setCSLine(uint8_t encoder, uint8_t csLine)
{
  digitalWrite(encoder, csLine);
}

/*
   The AMT22 bus allows for extended commands. The first byte is 0x00 like a normal position transfer, but the
   second byte is the command.
   This function takes the pin number of the desired device as an input
*/
void setZeroSPI(uint8_t encoder)
{
  spiWriteRead(AMT22_NOP, encoder, false);

  //this is the time required between bytes as specified in the datasheet.
  //We will implement that time delay here, however the arduino is not the fastest device so the delay
  //is likely inherantly there already
  delayMicroseconds(3);

  spiWriteRead(AMT22_ZERO, encoder, true);
  delay(250); //250 second delay to allow the encoder to reset
}

/*
   The AMT22 bus allows for extended commands. The first byte is 0x00 like a normal position transfer, but the
   second byte is the command.
   This function takes the pin number of the desired device as an input
*/
void resetAMT22(uint8_t encoder)
{
  spiWriteRead(AMT22_NOP, encoder, false);

  //this is the time required between bytes as specified in the datasheet.
  //We will implement that time delay here, however the arduino is not the fastest device so the delay
  //is likely inherantly there already
  delayMicroseconds(3);

  spiWriteRead(AMT22_RESET, encoder, true);

  delay(250); //250 second delay to allow the encoder to start back up
}
