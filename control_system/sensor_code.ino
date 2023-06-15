// Uses A4988 stepper motor driver and Arduino without a library. More info: https://www.makerguides.com

// Define stepper motor connections and steps per revolution:
#define dirPinL 2
#define stepPinL 15
#define stepsPerRevolution 200

#define dirPinR 4
#define stepPinR 0

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <math.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

struct a_offsets{
  float x_off = 0;
  float y_off = 0;
  float z_off = 0;
};
struct g_offsets{
  float roll_off = 0;
  float pitch_off = 0;
  float yaw_off = 0;
};
struct sensor_offsets{
  a_offsets accel;
  g_offsets gyro;
  float temp_off = 0;
} stat_vals{};

sensors_event_t a, g, temp;
unsigned int prevTime, curTime;
long double time_diff = 0;
void updateTimeDiff(){
  curTime = micros();
  time_diff = (curTime - prevTime)/1000000.0f;
  prevTime = curTime;
}


long double roll_ang, pitch_ang, yaw_ang;

void calibrate_sensors(int offset_loops){
  Serial.print("Calibrating sensors (");
  Serial.print(offset_loops);
  Serial.print(" rounds): ");

  for(int i = 0; i < offset_loops; i++){
    mpu.getEvent(&a, &g, &temp);
    stat_vals.accel.x_off += a.acceleration.x;
    stat_vals.accel.y_off += a.acceleration.y;
    stat_vals.accel.z_off += a.acceleration.z - 9.81;

    stat_vals.gyro.roll_off += g.gyro.x;
    stat_vals.gyro.pitch_off += g.gyro.y;
    stat_vals.gyro.yaw_off += g.gyro.z;

    stat_vals.temp_off += temp.temperature;
  
    Serial.print(i);
    Serial.print(" ");
    delay(1000); // to seperate the readings from each other
  }
  stat_vals.accel.x_off /= offset_loops;
  stat_vals.accel.y_off /= offset_loops;
  stat_vals.accel.z_off /= offset_loops;

  stat_vals.gyro.roll_off /= offset_loops;
  stat_vals.gyro.pitch_off /= offset_loops;
  stat_vals.gyro.yaw_off /= offset_loops;

  roll_ang = pitch_ang = yaw_ang = 0;
  
  Serial.println("done :)");
}


void setup() {
  // Declare pins as output:
  pinMode(stepPinL, OUTPUT);
  pinMode(dirPinL, OUTPUT);
  pinMode(stepPinR, OUTPUT);
  pinMode(dirPinR, OUTPUT);

  // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  Serial.begin(1000000);
  while (!Serial)
    delay(10);  // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("Adafruit MPU6050 test!");

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10000);
      Serial.println("aaaaaaaah");
    }
  }
  Serial.println("MPU6050 Found!");

  mpu.setAccelerometerRange(MPU6050_RANGE_4_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ); // maybe 44Hz LP, dk

  calibrate_sensors(10);

  // Set the spinning direction counterclockwise:
  digitalWrite(dirPinL, LOW);
  digitalWrite(dirPinR, HIGH);

  Serial.setTimeout(1); // make it spend around 1 microsecond on input reading

  prevTime = curTime = micros();
}


unsigned int reading_count = 0;
String comm = "";

long double accel_x, accel_y, accel_z;
long double roll_vel, pitch_vel, yaw_vel;
float P_CompCoeff = 0.95; // complementary filter coefficient
unsigned short prev_roll_ang = 0, roll_err_counter = 0; // counts static roll angle error

long double K_p, K_i, K_d; // TODO: actually implement these things for PID
long double err_curr, err_total, err_rate;

void loop() {
  comm = Serial.readString();

  if (comm == "LF") digitalWrite(dirPinL, HIGH);
  else if (comm == "LB") digitalWrite(dirPinL, LOW);
  else if (comm == "RF") digitalWrite(dirPinR, HIGH);
  else if (comm == "RB") digitalWrite(dirPinR, LOW);
  
  else if (comm == "C10") calibrate_sensors(10);
  else if (comm == "C50") calibrate_sensors(50);
  
  else if (comm == ""){}
  else if (comm == "P"){
    Serial.println("Pause, short break (10 seconds)");
    delay(10000);
  }
  else{
    Serial.print("invalid command: ");
    Serial.println(comm);
  }

  // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  /*//Spin the stepper motor 5 (before the loop, so 25 now?) revolutions fast:
  // These four lines result in 1 step:
  for(int i = 0; i < 5; i++){
    digitalWrite(stepPinL, HIGH);
    digitalWrite(stepPinR, HIGH);
    delayMicroseconds(2000);

    digitalWrite(stepPinL, LOW);
    digitalWrite(stepPinR, LOW);
    delayMicroseconds(2000);
  }*/

  // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  /* Get new sensor events with the readings */
  mpu.getEvent(&a, &g, &temp);

  updateTimeDiff();

  accel_x = a.acceleration.x - stat_vals.accel.x_off;
  accel_x *= abs(accel_x) > 0.08; // basic HP filters for sensor values
  accel_y = a.acceleration.y - stat_vals.accel.y_off;
  accel_y *= abs(accel_y) > 0.05;
  accel_z = a.acceleration.z - stat_vals.accel.z_off;
  if(abs(accel_z - 9.81) < 0.08) accel_z = 9.81;

  roll_vel = g.gyro.x - stat_vals.gyro.roll_off;
  roll_vel *= abs(roll_vel) > 0.02;
  pitch_vel = g.gyro.y - stat_vals.gyro.pitch_off;
  pitch_vel *= abs(pitch_vel) > 0.05;
  yaw_vel = g.gyro.z - stat_vals.gyro.yaw_off;
  yaw_vel *= abs(yaw_vel) > 0.02;

  
  // complementary filter: https://forum.arduino.cc/t/complementary-filter-with-the-mpu6050/210303/10
  roll_ang += roll_vel*time_diff;

  if (prev_roll_ang == (unsigned short)(roll_ang*256)) 
    roll_err_counter++;
  else roll_err_counter = 0;

  if(roll_err_counter > 100) // if it stays on a roll value for too long, it's zeroed (assumed to be drift)
    roll_ang = 0;
  prev_roll_ang = (unsigned short)(roll_ang*256);

  if (accel_y != 0 || accel_z != 0){
    pitch_ang = (pitch_ang + pitch_vel*time_diff) * P_CompCoeff; //-gy or +ve???
    pitch_ang -= (1.0f - P_CompCoeff) * atan(accel_x / sqrt((long)accel_y*accel_y + (long)accel_z*accel_z));
  }
  else pitch_ang += pitch_vel*time_diff;

  if(pitch_ang != pitch_ang) pitch_ang = 0;

  yaw_ang += yaw_vel*time_diff;

  
  /* // PID Controller
  
  */
  
  
  /* // Print out the values
  Serial.print("reading number ");
  Serial.println(reading_count);
  Serial.print("Acceleration Forwards(x): ");
  Serial.print((double)accel_x);
  Serial.print(", Left(y): ");
  Serial.print((double)accel_y);
  Serial.print(", Down(z): ");
  Serial.print((double)accel_z);
  Serial.println(" m s^-2");

  Serial.print("Rotational vel. Roll(x): ");
  Serial.print((double)roll_vel);
  Serial.print(", Pitch(y): ");
  Serial.print((double)pitch_vel);
  Serial.print(", Yaw(z): ");
  Serial.print((double)yaw_vel);
  Serial.println(" rad s^-1");

  Serial.print("Angle Roll(x): ");
  Serial.print((double)roll_ang);
  Serial.print(", Pitch(y): ");
  Serial.print((double)pitch_ang);
  Serial.print(", Yaw(z): ");
  Serial.print((double)yaw_ang);
  Serial.println(" rad");

  reading_count++;
  Serial.println("");*/
}

// --------------------------------------
// i2c_scanner
//
// Version 1
//    This program (or code that looks like it)
//    can be found in many places.
//    For example on the Arduino.cc forum.
//    The original author is not know.
// Version 2, Juni 2012, Using Arduino 1.0.1
//     Adapted to be as simple as possible by Arduino.cc user Krodal
// Version 3, Feb 26  2013
//    V3 by louarnold
// Version 4, March 3, 2013, Using Arduino 1.0.3
//    by Arduino.cc user Krodal.
//    Changes by louarnold removed.
//    Scanning addresses changed from 0...127 to 1...119,
//    according to the i2c scanner by Nick Gammon
//    https://www.gammon.com.au/forum/?id=10896
// Version 5, March 28, 2013
//    As version 4, but address scans now to 127.
//    A sensor seems to use address 120.
// Version 6, November 27, 2015.
//    Added waiting for the Leonardo serial communication.
//
//
// This sketch tests the standard 7-bit addresses
// Devices with higher bit address might not be seen properly.
//
/*
#include <Wire.h>
 
 
void setup()
{
  Wire.begin();
 
  Serial.begin(9600);
  while (!Serial);             // Leonardo: wait for serial monitor
  Serial.println("\nI2C Scanner");
}
 
 
void loop()
{
  byte error, address;
  int nDevices;
 
  Serial.println("Scanning...");
 
  nDevices = 0;
  for(address = 1; address < 127; address++ )
  {
    // The i2c_scanner uses the return value of
    // the Write.endTransmisstion to see if
    // a device did acknowledge to the address.
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
 
    if (error == 0)
    {
      Serial.print("I2C device found at address 0x");
      if (address<16)
        Serial.print("0");
      Serial.print(address,HEX);
      Serial.println("  !");
 
      nDevices++;
    }
    else if (error==4)
    {
      Serial.print("Unknown error at address 0x");
      if (address<16)
        Serial.print("0");
      Serial.println(address,HEX);
    }    
  }
  if (nDevices == 0)
    Serial.println("No I2C devices found\n");
  else
    Serial.println("done\n");
 
  delay(5000);           // wait 5 seconds for next scan
}
*/