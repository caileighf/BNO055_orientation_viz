// BNO055 (I2C)
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
using BNO055 = Adafruit_BNO055;

// Initialize sensors
Adafruit_BNO055 ahrs = Adafruit_BNO055(55, 0x28);

imu::Vector<3> euler;
imu::Quaternion quat;
unsigned long time = millis();
unsigned int blink_rate_per_millis = 1000;
String out_str = "";

#define qBlink() (digitalWriteFast(LED_BUILTIN, !digitalReadFast(LED_BUILTIN) ))  // Pin13 on T3.x & LC
int BNO_RST_PIN = 15;

// set this to the hardware serial port you wish to use
#define HWSERIAL Serial1

void displayCalStatus(void);

void setup() {
  Serial.begin(921600);
//  HWSERIAL.begin(921600);
  HWSERIAL.begin(115200); // 115200 is the fastest baud that works well with UART
  delay(1000);

  pinMode(BNO_RST_PIN, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);   // On Teensy must set to OUTPUT before setting value
  qBlink();
  delay(200);
  qBlink();
  delay(500);

  while(!ahrs.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.println("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    HWSERIAL.println("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(true);
  }
  Serial.print("Connected to BNO055!\n\n");
  HWSERIAL.print("Connected to BNO055!\n\n");
  //
  // Display if system is ready and cal status of gyro, accel, mag
  displayCalStatus();
}

char incomingByte = 0;
String cmd = "";
void loop() {
  if (millis() - time > blink_rate_per_millis){
      time = millis();
      qBlink();
  }

  
  //
  //  EULER Vector build output string
  //    Euler angles ------> Z,Y,X
  //    roll, pitch, yaw --> X,Y,Z
  //    
  // euler.z() --> X = ROLL
  // euler.y() --> Y = PITCH
  // euler.x() --> Z = YAW
  euler = ahrs.getVector(BNO055::VECTOR_EULER);
  out_str = "$EULV,x_yaw," + String(euler.x(), 4) + 
               ",y_pitch," + String(euler.y(), 4) + 
               ",z_roll," +  String(euler.z(), 4) + "\r\n";
  // Write to USB
  Serial.print(out_str);
  // Write to HW Serial
  HWSERIAL.print(out_str);

  //
  //  QUATURNION build output string
  //
  quat = ahrs.getQuat();
  out_str = "$QUAT,w," + String(quat.w(), 4) + 
                 ",x," + String(quat.x(), 4) + 
                 ",y," + String(quat.y(), 4) + 
                 ",z," + String(quat.z(), 4) + "\r\n";
  // Write to USB
  Serial.print(out_str);
  // Write to HW Serial
  HWSERIAL.print(out_str);
  
  // check if we should reset BNO
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();
    if (incomingByte == '\n'){
      // do something depending on cmd
      cmd = "";
    }
    if (incomingByte == 'c' || incomingByte == 'C')
        displayCalStatus();
    else
      cmd += incomingByte;
  }
}

void displayCalStatus(void)
{
  /* Get the four calibration values (0..3) */
  /* Any sensor data reporting 0 should be ignored, */
  /* 3 means 'fully calibrated" */
  uint8_t system, gyro, accel, mag;
  system = gyro = accel = mag = 0;
  ahrs.getCalibration(&system, &gyro, &accel, &mag);

  Serial.println("\n\n========================================");
  /* The data should be ignored until the system calibration is > 0 */
  if (!system)
  {
    Serial.print("!");
  }
 
  /* Display the individual values */
  Serial.print("$CALIBRATION,sys,");
  Serial.print(system, DEC);
  Serial.print(",gyro,");
  Serial.print(gyro, DEC);
  Serial.print(",accel,");
  Serial.print(accel, DEC);
  Serial.print(",mag,");
  Serial.println(mag, DEC);

  if (system) 
    Serial.print(" System Calibration O.K.");
  else
    Serial.print("! NEEDS System Calibration !");

   Serial.println("\n========================================\n");
   Serial.print("\r\n");
   delay(1000);
}
