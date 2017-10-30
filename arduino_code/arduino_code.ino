/*
 * Sketch to control the pins of Arduino via serial interface
 *
 * Commands implemented with examples:
 *
 * - RD13 -> Reads the Digital input at pin 13
 * - RA4 - > Reads the Analog input at pin 4
 * - WD13:1 -> Writes 1 (HIGH) to digital output pin 13
 * - WA6:125 -> Writes 125 to analog output pin 6 (PWM)
 * - WS3:95 -> Sets servo on pin 3 to 95 deg
 */

#include <Servo.h>

char operation; // Holds operation (R, W, ...)
char mode; // Holds the mode (D, A)
int pin_number; // Holds the pin number
int digital_value; // Holds the digital value
int analog_value; // Holds the analog value
int value_to_write; // Holds the value that we want to write
int wait_for_transmission = 5; // Delay in ms in order to receive the serial data

// create servo object to control a servo
// a maximum of eight servo objects can be created
Servo SERVO1; 
Servo SERVO2;
Servo SERVO3;
Servo SERVO4;
Servo SERVO5;

int SERVO1_PIN = 11;
int SERVO2_PIN = 10;
int SERVO3_PIN = 9;
int SERVO4_PIN = 6; 
int SERVO5_PIN = 5;

void setup() {
    Serial.begin(9600); // Serial Port at 9600 baud
    Serial.setTimeout(500); // Instead of the default 1000ms, in order
                            // to speed up the Serial.parseInt() 

    SERVO1.attach(SERVO1_PIN);
    SERVO1.write(100); // reset to original position
    
    SERVO2.attach(SERVO2_PIN);
    SERVO2.write(150); // reset to original position

    SERVO3.attach(SERVO3_PIN);
    SERVO3.write(60); // reset to original position
    // servo3 limit 0-85

    SERVO4.attach(SERVO4_PIN);
    SERVO4.write(90); // reset to original position

    SERVO5.attach(SERVO5_PIN);
    SERVO5.write(100); // reset to original position 
}

void servo_write(int pin_number, int servo_value){
    /*
     * Performs a servo write on pin_number with the servo_value
     * The value must be 0 to 180 (might change depending on servo)
     */
     
    switch (pin_number) {
      case 5:
        {
          SERVO5.write(servo_value);
          delay(10);
          break;
        }
      case 6:
        {
          SERVO4.write(servo_value);
          delay(10);
          break;
        }
      case 9:
        {
          SERVO3.write(servo_value);
          delay(10);
          break;
        }
      case 10:
        {
          SERVO2.write(servo_value);
          delay(10);
          break;
        }
      case 11:
        {
          SERVO1.write(servo_value);
          delay(10);
          break;
        }
      default:
        break;
    }

    
          //bolje case, break na kraju svakog
}

void loop() {
    // Check if characters available in the buffer
    if (Serial.available() > 0) 
    {
        // parse information
        // courtesy of lekum 
        operation = Serial.read();
        delay(wait_for_transmission); // If not delayed, second character is not correctly read
        mode = Serial.read();
        pin_number = Serial.parseInt(); // Waits for an int to be transmitted
        
        if (Serial.read()==':')
        {
            value_to_write = Serial.parseInt(); // Collects the value to be written
        }

        // if we recieve proper input write servo
        if (operation == 'W')
        {
            if (mode == 'S')
            {
                servo_write(pin_number, value_to_write);
            }
        }
        
    }
}
