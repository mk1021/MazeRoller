// Uses A4988 stepper motor driver and Arduino without a library. More info: https://www.makerguides.com

// Define stepper motor connections and steps per revolution:
#define stepPinR 23  // D2
#define dirPinR  22  // D3
#define stepPinL 21  // D4
#define dirPinL  19  // D5

#define stepsPerRevolution 200

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <math.h>

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
long double prev_yaw_ang;

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

void sensor_update(){
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

  // prev_pitch_ang = pitch_ang;

  if (accel_y != 0 || accel_z != 0){
    pitch_ang = (pitch_ang + pitch_vel*time_diff) * P_CompCoeff;
    pitch_ang -= (1.0f - P_CompCoeff) * atan(accel_x / sqrt((long)accel_y*accel_y + (long)accel_z*accel_z));
  }
  else pitch_ang += pitch_vel*time_diff;

  if(pitch_ang != pitch_ang) pitch_ang = 0;

  prev_yaw_ang = yaw_ang;
  yaw_ang += yaw_vel*time_diff;
}


long double prev_ang_err, curr_ang_err, total_ang_err;
const long double K_p = 1, K_i = 1, K_d = 1; // TODO: change this to make it do the balance
const double control_to_mvmnt = 3.1415; // TODO: change this to make output fit desired movement change
// a higher value means more movement to achieve a desired pitch, lower value means less movement

// Maybe think about acceleration during movement, how much does that affect the correction?

int pitch_control(long double desired_pitch_ang){
  long double pitch_control_output = 0;
  curr_ang_err = pitch_ang - desired_pitch_ang;
  
  pitch_control_output +=  K_p*curr_ang_err;
  pitch_control_output +=  K_i*(total_ang_err += curr_ang_err*time_diff);
  pitch_control_output +=  K_d*(curr_ang_err - prev_ang_err)/time_diff;
  // pitch_control_output += K_x*x_position(or x_theta);  //  TODO: decide if this is even necessary
  //  ^^ was supposed to reduce speed the closer you got to your desired position, but idk

  prev_ang_err = curr_ang_err;
  return (int)(pitch_control_output*control_to_mvmnt);
}

int x_position = 0;
int x_theta = 0;
int x_moved = 0;
int z_to_rotate = 0; // positive is clockwise, negative is anti-clockwise
int movement_input = 0; // from exploration, will be used to adjust x_position
bool rotation = false;
const double yaw_to_rotation = 60; // TODO: tune to get yaw to rotation amount
const double pos_to_ang = 5; // TODO: tune to give better value for desired pitch angle
// i.e. if it's tilting too much and falling over when moving, this needs to be higher,
//      if it's not tilting enough and falling backwards when moving, this needs to be lower, etc.

// outputs the desired pitch angle, to set the rover up for motion
long double position_control(){
  return atan((x_position + x_theta)/pos_to_ang); // should return 0 for x_position == 0
}

// sign of x_theta and x_position should give the direction of acceleration,
// with ==0 describing whether the motors were even on or not
short sign_of(int *operand, bool approximate_zero=false){
    if(approximate_zero){
      if(abs(*operand) < 3) return 0;
    }
    else{
      if(*operand == 0) return 0;
    }

    if(*operand < 0) return -1;
    else return 1;
}

bool dynamic = false;   // variable holding current state
double linear_velocity = 0;
/*const*/ double approx_acceleration_magnitude = 2; // TODO: find value for rough rate of motors accelerating the rover

// should just be used in below functions, only sign changes
inline double approx_accel(){
    return approx_acceleration_magnitude * (dynamic ? sign_of(x_position) : sign_of(x_theta));
}

// must be called before update_velocity() in loop()
inline int distance_moved(){
    return (int)(linear_velocity*time_diff + 0.5*approx_accel()*sq(time_diff));
}

// v = u + at
double update_velocity(){
   linear_velocity += approx_accel()*time_diff;
}

// ------------------ simple movement functions -----------------------

void move_forward(){
  digitalWrite(dirPinL, HIGH);
  digitalWrite(dirPinR, HIGH);

  digitalWrite(stepPinL, HIGH);
  digitalWrite(stepPinR, HIGH);
}

void move_backward(){
  digitalWrite(dirPinL, LOW);
  digitalWrite(dirPinR, LOW);

  digitalWrite(stepPinL, HIGH);
  digitalWrite(stepPinR, HIGH);
}

void move_clockwise(){
  digitalWrite(dirPinL, HIGH);
  digitalWrite(dirPinR, LOW);

  digitalWrite(stepPinL, HIGH);
  digitalWrite(stepPinR, HIGH);
}

void move_anticlockwise(){
  digitalWrite(dirPinL, LOW);
  digitalWrite(dirPinR, HIGH);

  digitalWrite(stepPinL, HIGH);
  digitalWrite(stepPinR, HIGH);
}

void move_stationary(){
  digitalWrite(stepPinL, LOW);
  digitalWrite(stepPinR, LOW);
}


// ------------------ main loop -----------------------

void loop() {
  comm = Serial.readString();
  
  /*else */if (comm == "C10") calibrate_sensors(10);
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

  sensor_update();

  // ------------------------------------    Control System     ---------------------------------------------

  x_moved = distance_moved(); // I'm assuming the x values are measured in steps or sth, so they'll be in the hundreds?
  update_velocity();
  
  if(dynamic){  // shouldn't be interrupted while in dynamic mode, since it's supposed to be tipping
    x_position -= x_moved;
    switch (sign_of(x_position, approximate_zero=true){
      case 1:
        move_forward();
        break;
      case -1:
        move_backward();
        break;
      default:
        x_position = 0;
        dynamic = false;
        move_stationary();
        break;
    }

    // TODO: tune these three values, which as killswitches for dynamic mode
    if((abs(pitch_ang) < 0.01)  // not sure about this condition, I feel if it's upright before reaching it's target,
                                // it's probably gonna fall back, but I'm not sure
    || (abs(pitch_vel) > 5)     // if it's falling too quickly, probably want to stop?
    || (abs(linear_velocity) > 100))  // if it's moving too quickly, that's also probably not good
        dynamic = false; // turn off dynamic mode
  }
  else{ // for the static case
    x_theta -= x_moved; // x_theta is used in position_control()
    x_theta = pitch_control(position_control());

    if (abs(x_theta) < 2){ // is balanced
      if(x_position == 0){ // has nowhere left to travel to
        z_to_rotate -= (yaw_ang - prev_yaw_ang) * yaw_to_rotation;
        if(z_to_rotate == 0){ // has nowhere left to rotate to
          // deal with exploration inputs
          if(movement_input != 0){
            if(rotation) z_to_rotate += movement_input;
            else x_position += movement_input;
            movement_input = 0;
          }
          move_stationary();
        }
        else{ // has yet to rotate, rotation isn't the same as dynamic, can only take place when tilt is correct
          switch (sign_of(z_to_rotate, approximate_zero=true){
            case 1:
              move_clockwise();
              break;
            case -1:
              move_anticlockwise();
              break;
            default:
              z_to_rotate = 0;
              move_stationary();
              break;
          }
        }
      }
      else dynamic = true;
    }
    else{ 
      if(x_theta > 0) move_forward();
      else move_backward();
    }
  }
}
