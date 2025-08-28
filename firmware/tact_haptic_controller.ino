/*
 * Tact Haptic Feedback Controller
 * Arduino 101 Firmware for Mediated Social Touch System
 * 
 * This firmware implements the core haptic feedback logic for the Tact system,
 * parsing CSV messages from a host application and controlling 3-4 vibrotactile motors
 * with fixed calibration parameters for rapid prototyping.
 */

// Fixed calibration parameters (hardcoded for MVP)
const int FIRST_CONTACT_PULSE_DURATION = 75;  // milliseconds
const int FIRST_CONTACT_AMPLITUDE = 230;      // 90% PWM (230/255)
const int SUSTAINED_CONTACT_MIN_AMPLITUDE = 51;  // 20% PWM (51/255)
const int SUSTAINED_CONTACT_MAX_AMPLITUDE = 179; // 70% PWM (179/255)
const float PENETRATION_THRESHOLD = 0.1;      // ignore values below this

// Motor configuration
const int NUM_MOTORS = 4;
const int MOTOR_PINS[NUM_MOTORS] = {3, 5, 6, 9}; // PWM pins on Arduino 101

// Contact state tracking
bool previous_contact[NUM_MOTORS] = {false, false, false, false};
unsigned long pulse_start_time[NUM_MOTORS] = {0, 0, 0, 0};
bool in_first_contact_pulse[NUM_MOTORS] = {false, false, false, false};

// Serial communication
const int BAUD_RATE = 115200;
String input_buffer = "";

void setup() {
  // Initialize serial communication
  Serial.begin(BAUD_RATE);
  while (!Serial) {
    ; // Wait for serial port to connect
  }
  
  // Initialize motor pins
  for (int i = 0; i < NUM_MOTORS; i++) {
    pinMode(MOTOR_PINS[i], OUTPUT);
    analogWrite(MOTOR_PINS[i], 0); // Start with motors off
  }
  
  Serial.println("Tact Haptic Controller Ready");
  Serial.println("Format: actuator_id,penetration_depth,first_contact");
  
  // Run motor test sequence
  runMotorTest();
}

void loop() {
  // Handle serial input
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      processMessage(input_buffer);
      input_buffer = "";
    } else {
      input_buffer += c;
    }
  }
  
  // Update motor states (handle first contact pulses)
  updateMotorStates();
  
  // Small delay for ~30Hz update rate
  delay(33);
}

void processMessage(String message) {
  message.trim();
  if (message.length() == 0) return;
  
  // Parse CSV: actuator_id,penetration_depth,first_contact
  int first_comma = message.indexOf(',');
  int second_comma = message.indexOf(',', first_comma + 1);
  
  if (first_comma == -1 || second_comma == -1) {
    Serial.println("Error: Invalid message format");
    return;
  }
  
  int actuator_id = message.substring(0, first_comma).toInt();
  float penetration_depth = message.substring(first_comma + 1, second_comma).toFloat();
  int first_contact = message.substring(second_comma + 1).toInt();
  
  // Validate actuator ID
  if (actuator_id < 0 || actuator_id >= NUM_MOTORS) {
    Serial.println("Error: Invalid actuator ID");
    return;
  }
  
  // Apply penetration threshold
  if (penetration_depth < PENETRATION_THRESHOLD) {
    penetration_depth = 0.0;
    first_contact = 0;
  }
  
  // Update contact state and control motor
  updateActuator(actuator_id, penetration_depth, first_contact == 1);
}

void updateActuator(int actuator_id, float penetration_depth, bool is_first_contact) {
  bool current_contact = (penetration_depth > 0.0);
  
  // Detect first contact transition
  if (is_first_contact && !previous_contact[actuator_id] && current_contact) {
    // Trigger first contact pulse
    startFirstContactPulse(actuator_id);
  } else if (current_contact && !in_first_contact_pulse[actuator_id]) {
    // Apply sustained contact vibration
    applySustainedVibration(actuator_id, penetration_depth);
  } else if (!current_contact) {
    // Stop motor and reset state
    analogWrite(MOTOR_PINS[actuator_id], 0);
    previous_contact[actuator_id] = false;
    in_first_contact_pulse[actuator_id] = false;
  }
  
  // Update previous contact state
  if (current_contact) {
    previous_contact[actuator_id] = true;
  }
}

void startFirstContactPulse(int actuator_id) {
  analogWrite(MOTOR_PINS[actuator_id], FIRST_CONTACT_AMPLITUDE);
  pulse_start_time[actuator_id] = millis();
  in_first_contact_pulse[actuator_id] = true;
  
  Serial.print("First contact pulse: Motor ");
  Serial.println(actuator_id);
}

void applySustainedVibration(int actuator_id, float penetration_depth) {
  // Linear scaling from min to max amplitude based on penetration depth
  int amplitude = SUSTAINED_CONTACT_MIN_AMPLITUDE + 
                  (int)((SUSTAINED_CONTACT_MAX_AMPLITUDE - SUSTAINED_CONTACT_MIN_AMPLITUDE) * penetration_depth);
  
  // Clamp to valid range
  amplitude = constrain(amplitude, SUSTAINED_CONTACT_MIN_AMPLITUDE, SUSTAINED_CONTACT_MAX_AMPLITUDE);
  
  analogWrite(MOTOR_PINS[actuator_id], amplitude);
}

void updateMotorStates() {
  unsigned long current_time = millis();
  
  // Check for expired first contact pulses
  for (int i = 0; i < NUM_MOTORS; i++) {
    if (in_first_contact_pulse[i]) {
      if (current_time - pulse_start_time[i] >= FIRST_CONTACT_PULSE_DURATION) {
        in_first_contact_pulse[i] = false;
        // Motor will be updated by next sustained contact message
      }
    }
  }
}

void runMotorTest() {
  Serial.println("Running motor test sequence...");
  
  for (int i = 0; i < NUM_MOTORS; i++) {
    Serial.print("Testing motor ");
    Serial.print(i);
    Serial.print(" on pin ");
    Serial.println(MOTOR_PINS[i]);
    
    // Test with medium intensity
    analogWrite(MOTOR_PINS[i], 128);
    delay(500);
    analogWrite(MOTOR_PINS[i], 0);
    delay(200);
  }
  
  Serial.println("Motor test complete. Ready for operation.");
}