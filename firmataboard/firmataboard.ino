#include <Boards.h>
#include <Firmata.h>

byte previous_port[TOTAL_PORTS];
void digital_write(byte port,int value){
    byte i;
    byte curr_pinval, prev_pinval;
    if (port < TOTAL_PORTS && value != previous_port[port]) {
        for (i = 0; i < 8; i++) {
            curr_pinval = (byte) value & (1 << i);
            prev_pinval = previous_port[port] & (1 << i);
            if (curr_pinval != prev_pinval) {
                digitalWrite(i + (port * 8), curr_pinval);
            }
        }
        previous_port[port] = value;
    }    
}

void set_pin_mode_cb(byte pin, int mode) {
    if (IS_PIN_DIGITAL(pin)) {
        pinMode(PIN_TO_DIGITAL(pin), mode);
    }
}

void setup() {
    // Setup Firmata module
    Firmata.setFirmwareNameAndVersion("firmata_arduino_101_v_0_1",FIRMATA_MAJOR_VERSION,FIRMATA_MINOR_VERSION);
    Firmata.attach(DIGITAL_MESSAGE,digital_write);
    Firmata.attach(SET_PIN_MODE, set_pin_mode_cb);    
    // Begin the firmata module
    Firmata.begin(57600);
    while (!Serial);
}

void loop() {
    while(Firmata.available()){
        Firmata.processInput();
    }

}
