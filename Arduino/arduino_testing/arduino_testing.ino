// Arduino Code

const int leftMotorPin = 2;   // Pin number for the left motor
const int rightMotorPin = 3;  // Pin number for the right motor

void setup() {
  Serial.begin(9600);   // Start serial communication
  pinMode(leftMotorPin, OUTPUT);
  pinMode(rightMotorPin, OUTPUT);

  // Initially, stop the motors
  digitalWrite(leftMotorPin, LOW);
  digitalWrite(rightMotorPin, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');  // Read the incoming command
    command.trim();  // Remove leading and trailing whitespaces

    // Perform actions based on the received command
    if (command == "turn on") {
      // Turn on an LED or perform any other action
    } else if (command == "turn off") {
      // Turn off an LED or perform any other action
    } else if (command == "turn left") {
      // Turn left by activating the left motor
      digitalWrite(leftMotorPin, HIGH);
    } else if (command == "turn right") {
      // Turn right by activating the right motor
      digitalWrite(rightMotorPin, HIGH);
    } else if (command == "go forward") {
      // Go forward by activating both motors
      digitalWrite(leftMotorPin, HIGH);
      digitalWrite(rightMotorPin, HIGH);
    } else if (command == "go backward") {
      // Go backward by reversing both motors
      digitalWrite(leftMotorPin, LOW);
      digitalWrite(rightMotorPin, LOW);
    }
    // Add more conditions based on your specific requirements
  }
}
