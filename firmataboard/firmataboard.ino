#include <Boards.h>
#include <Firmata.h>

void digital_write(byte pin,int value){
    pinMode(pin,OUTPUT);
    digitalWrite(pin,value);    
}


void setup() {
    // Setup Firmata module
    Firmata.setFirmwareNameAndVersion("arduino_101",FIRMATA_MAJOR_VERSION,FIRMATA_MINOR_VERSION);
    Firmata.attach(DIGITAL_MESSAGE,digital_write);
    // Begin the firmata module
    Firmata.begin(57600);
}

void loop() {
    while(Firmata.available()){
        Firmata.processInput();
    }

}
