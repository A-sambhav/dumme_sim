/*
 * Dumm-E arm firmware (ESP32 + 5x MG995 servos)
 *
 * 4 logical ROS joints, driven by 5 physical servos:
 *   shoulder_rotation_plate_joint -> 1 servo  ('p')
 *   shoulder_joint                -> 2 servos, mirrored ('s')
 *   elbow_joint                   -> 1 servo  ('e')
 *   wrist_joint                   -> 1 servo  ('w')
 *
 * Serial protocol (matches dumme_controller's DummeInterface):
 *   "p090,s045,e120,w030,\n"  -- angle in whole degrees, 0-180, per joint
 *
 * IMPORTANT - CALIBRATE BEFORE USE:
 *   - SHOULDER_MIRROR_INVERT: whether the second shoulder servo needs
 *     (180 - angle) instead of the same angle, depends on which way it's
 *     physically mounted relative to the first. Verify on the real arm
 *     before trusting this value.
 *   - SERVO_MIN_DEG / SERVO_MAX_DEG: MG995 servos only travel ~180 degrees
 *     mechanically. These bounds are a hard safety clamp applied in
 *     software regardless of what's requested over serial, so a bad
 *     command from ROS can't strip a servo's gears. Narrow these further
 *     once you've measured each joint's actual safe range on hardware.
 */

#include <Arduino.h>
#include <ESP32Servo.h>

// ---- Pin assignment: update to match your actual wiring ----
#define SERVO_PLATE_PIN        13
#define SERVO_SHOULDER_L_PIN   12
#define SERVO_SHOULDER_R_PIN   14
#define SERVO_ELBOW_PIN        27
#define SERVO_WRIST_PIN        26

// ---- Starting pose (degrees) ----
#define PLATE_START      90
#define SHOULDER_START    90
#define ELBOW_START        90
#define WRIST_START        90

// ---- Safety clamp: MG995 mechanical range is ~180 deg. Verify/tighten these. ----
#define SERVO_MIN_DEG        0
#define SERVO_MAX_DEG      180

// ---- TODO: verify on hardware. If the mirrored shoulder servo moves the
//      wrong direction relative to the first, flip this to true/false. ----
#define SHOULDER_MIRROR_INVERT true

Servo plate;
Servo shoulder_l;
Servo shoulder_r;
Servo elbow;
Servo wrist;

uint8_t idx = 0;
uint8_t val_idx = 0;
char value[4] = "000";


int clamp_deg(int deg)
{
  if (deg < SERVO_MIN_DEG) return SERVO_MIN_DEG;
  if (deg > SERVO_MAX_DEG) return SERVO_MAX_DEG;
  return deg;
}

/*
 * Moves a given servo smoothly from its current position to a goal position.
 */
void reach_goal(Servo& motor, int goal)
{
  goal = clamp_deg(goal);
  if (goal >= motor.read())
  {
    for (int pos = motor.read(); pos <= goal; pos += 1)
    {
      motor.write(pos);
      delay(5);
    }
  }
  else
  {
    for (int pos = motor.read(); pos >= goal; pos -= 1)
    {
      motor.write(pos);
      delay(5);
    }
  }
}

void reach_shoulder_goal(int goal)
{
  goal = clamp_deg(goal);
  int start_l = shoulder_l.read();
  int steps = abs(goal - start_l);

  for (int i = 0; i <= steps; i++)
  {
    int pos_l = start_l + (goal >= start_l ? i : -i);
    int pos_r = SHOULDER_MIRROR_INVERT ? (180 - pos_l) : pos_l;
    shoulder_l.write(pos_l);
    shoulder_r.write(pos_r);
    delay(5);
  }
}

void setup()
{
  plate.attach(SERVO_PLATE_PIN);
  shoulder_l.attach(SERVO_SHOULDER_L_PIN);
  shoulder_r.attach(SERVO_SHOULDER_R_PIN);
  elbow.attach(SERVO_ELBOW_PIN);
  wrist.attach(SERVO_WRIST_PIN);

  plate.write(PLATE_START);
  shoulder_l.write(SHOULDER_START);
  shoulder_r.write(SHOULDER_MIRROR_INVERT ? (180 - SHOULDER_START) : SHOULDER_START);
  elbow.write(ELBOW_START);
  wrist.write(WRIST_START);

  Serial.begin(115200);
  Serial.setTimeout(1);
}

void loop()
{
  if (Serial.available())
  {
    char chr = Serial.read();

    if (chr == 'p')
    {
      idx = 0;
      val_idx = 0;
    }
    else if (chr == 's')
    {
      idx = 1;
      val_idx = 0;
    }
    else if (chr == 'e')
    {
      idx = 2;
      val_idx = 0;
    }
    else if (chr == 'w')
    {
      idx = 3;
      val_idx = 0;
    }
    else if (chr == ',')
    {
      int val = atoi(value);
      if (idx == 0)
      {
        reach_goal(plate, val);
      }
      else if (idx == 1)
      {
        reach_shoulder_goal(val);
      }
      else if (idx == 2)
      {
        reach_goal(elbow, val);
      }
      else if (idx == 3)
      {
        reach_goal(wrist, val);
      }

      value[0] = '0';
      value[1] = '0';
      value[2] = '0';
      value[3] = '\0';
      val_idx = 0;
    }
    else
    {
      if (val_idx < 3)
      {
        value[val_idx] = chr;
        val_idx++;
      }
    }
  }
}
