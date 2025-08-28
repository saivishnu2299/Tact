#!/usr/bin/env python3
"""
Tact Host Simulator
Python application for simulating VR touch events and sending haptic commands
to the Arduino 101 via USB serial communication.

This script provides a simple interface for testing the Tact haptic feedback system
with predefined gesture patterns and manual control options.
"""

import serial
import time
import threading
import sys
import math
from typing import List, Tuple

class TactHostSimulator:
    def __init__(self, port: str = None, baud_rate: int = 115200):
        self.port = port
        self.baud_rate = baud_rate
        self.serial_connection = None
        self.is_connected = False
        self.num_motors = 4
        
    def connect(self) -> bool:
        """Establish serial connection to Arduino."""
        if self.port is None:
            self.port = self.find_arduino_port()
            
        if self.port is None:
            print("Error: Could not find Arduino port. Please specify manually.")
            return False
            
        try:
            self.serial_connection = serial.Serial(self.port, self.baud_rate, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize
            self.is_connected = True
            print(f"Connected to Arduino on {self.port}")
            
            # Read initial messages from Arduino
            for _ in range(10):
                if self.serial_connection.in_waiting:
                    response = self.serial_connection.readline().decode().strip()
                    print(f"Arduino: {response}")
                time.sleep(0.1)
                
            return True
        except Exception as e:
            print(f"Error connecting to Arduino: {e}")
            return False
    
    def find_arduino_port(self) -> str:
        """Attempt to find Arduino port automatically."""
        import serial.tools.list_ports
        
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if 'Arduino' in port.description or 'USB' in port.description:
                return port.device
        
        # Fallback to common port names
        common_ports = ['/dev/ttyACM0', '/dev/ttyUSB0', 'COM3', 'COM4']
        for port in common_ports:
            try:
                test_serial = serial.Serial(port, self.baud_rate, timeout=0.5)
                test_serial.close()
                return port
            except:
                continue
                
        return None
    
    def send_touch_event(self, actuator_id: int, penetration_depth: float, first_contact: bool) -> bool:
        """Send a single touch event to the Arduino."""
        if not self.is_connected:
            print("Error: Not connected to Arduino")
            return False
            
        # Validate parameters
        if actuator_id < 0 or actuator_id >= self.num_motors:
            print(f"Error: Invalid actuator ID {actuator_id}")
            return False
            
        penetration_depth = max(0.0, min(1.0, penetration_depth))
        first_contact_flag = 1 if first_contact else 0
        
        # Format CSV message
        message = f"{actuator_id},{penetration_depth:.2f},{first_contact_flag}\n"
        
        try:
            self.serial_connection.write(message.encode())
            print(f"Sent: {message.strip()}")
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
    
    def gesture_stroke(self, duration: float = 2.0, intensity: float = 0.6):
        """Simulate a stroking gesture across all motors."""
        print(f"Executing stroke gesture (duration: {duration}s, intensity: {intensity})")
        
        steps = int(duration * 20)  # 20 Hz update rate
        for step in range(steps):
            for motor_id in range(self.num_motors):
                # Create wave pattern across motors
                phase = (step / steps) * 2 * 3.14159  # Full cycle
                motor_phase = phase + (motor_id * 3.14159 / 2)  # Offset each motor
                depth = max(0, intensity * (0.5 + 0.5 * abs(math.sin(motor_phase))))
                
                first_contact = (step == 0 and motor_id == 0)
                self.send_touch_event(motor_id, depth, first_contact)
                
            time.sleep(0.05)  # 20 Hz
        
        # Turn off all motors
        for motor_id in range(self.num_motors):
            self.send_touch_event(motor_id, 0.0, False)
    
    def gesture_pat(self, motor_id: int = 1, intensity: float = 0.8):
        """Simulate a patting gesture on a specific motor."""
        print(f"Executing pat gesture on motor {motor_id} (intensity: {intensity})")
        
        # Quick pulse pattern
        self.send_touch_event(motor_id, intensity, True)  # First contact
        time.sleep(0.1)
        self.send_touch_event(motor_id, intensity * 0.7, False)
        time.sleep(0.1)
        self.send_touch_event(motor_id, intensity * 0.4, False)
        time.sleep(0.1)
        self.send_touch_event(motor_id, 0.0, False)  # Release
    
    def gesture_poke(self, motor_id: int = 2, intensity: float = 0.9):
        """Simulate a poking gesture - sharp contact and release."""
        print(f"Executing poke gesture on motor {motor_id} (intensity: {intensity})")
        
        self.send_touch_event(motor_id, intensity, True)  # Sharp first contact
        time.sleep(0.05)
        self.send_touch_event(motor_id, 0.0, False)  # Quick release
    
    def gesture_squeeze(self, duration: float = 1.5, max_intensity: float = 0.7):
        """Simulate a squeezing gesture - gradual pressure increase/decrease."""
        print(f"Executing squeeze gesture (duration: {duration}s, max intensity: {max_intensity})")
        
        steps = int(duration * 20)  # 20 Hz
        for step in range(steps):
            # Triangular intensity pattern
            if step < steps // 2:
                intensity = (step / (steps // 2)) * max_intensity
            else:
                intensity = ((steps - step) / (steps // 2)) * max_intensity
            
            # Apply to all motors simultaneously
            for motor_id in range(self.num_motors):
                first_contact = (step == 0)
                self.send_touch_event(motor_id, intensity, first_contact)
            
            time.sleep(0.05)  # 20 Hz
        
        # Release all motors
        for motor_id in range(self.num_motors):
            self.send_touch_event(motor_id, 0.0, False)
    
    def interactive_mode(self):
        """Interactive command-line interface for manual testing."""
        print("\n=== Tact Interactive Mode ===")
        print("Commands:")
        print("  stroke - Execute stroke gesture")
        print("  pat [motor_id] - Execute pat gesture (default motor 1)")
        print("  poke [motor_id] - Execute poke gesture (default motor 2)")
        print("  squeeze - Execute squeeze gesture")
        print("  manual [motor_id] [depth] [first_contact] - Send manual command")
        print("  test - Run all gesture tests")
        print("  quit - Exit interactive mode")
        print()
        
        while True:
            try:
                command = input("Tact> ").strip().split()
                if not command:
                    continue
                    
                cmd = command[0].lower()
                
                if cmd == 'quit':
                    break
                elif cmd == 'stroke':
                    self.gesture_stroke()
                elif cmd == 'pat':
                    motor_id = int(command[1]) if len(command) > 1 else 1
                    self.gesture_pat(motor_id)
                elif cmd == 'poke':
                    motor_id = int(command[1]) if len(command) > 1 else 2
                    self.gesture_poke(motor_id)
                elif cmd == 'squeeze':
                    self.gesture_squeeze()
                elif cmd == 'manual':
                    if len(command) >= 4:
                        motor_id = int(command[1])
                        depth = float(command[2])
                        first_contact = bool(int(command[3]))
                        self.send_touch_event(motor_id, depth, first_contact)
                    else:
                        print("Usage: manual [motor_id] [depth] [first_contact]")
                elif cmd == 'test':
                    self.run_gesture_tests()
                else:
                    print(f"Unknown command: {cmd}")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def run_gesture_tests(self):
        """Run all predefined gesture tests."""
        print("\n=== Running Gesture Tests ===")
        
        print("\n1. Testing stroke gesture...")
        self.gesture_stroke(duration=2.0, intensity=0.6)
        time.sleep(1)
        
        print("\n2. Testing pat gestures...")
        for motor_id in range(self.num_motors):
            print(f"   Pat on motor {motor_id}")
            self.gesture_pat(motor_id, 0.8)
            time.sleep(0.5)
        
        print("\n3. Testing poke gestures...")
        for motor_id in range(self.num_motors):
            print(f"   Poke on motor {motor_id}")
            self.gesture_poke(motor_id, 0.9)
            time.sleep(0.5)
        
        print("\n4. Testing squeeze gesture...")
        self.gesture_squeeze(duration=1.5, max_intensity=0.7)
        
        print("\nGesture tests complete!")
    
    def disconnect(self):
        """Close serial connection."""
        if self.serial_connection:
            self.serial_connection.close()
            self.is_connected = False
            print("Disconnected from Arduino")

def main():
    import argparse
    import math
    
    parser = argparse.ArgumentParser(description='Tact Haptic Feedback Host Simulator')
    parser.add_argument('--port', help='Serial port (auto-detect if not specified)')
    parser.add_argument('--baud', type=int, default=115200, help='Baud rate (default: 115200)')
    parser.add_argument('--test', action='store_true', help='Run gesture tests and exit')
    parser.add_argument('--interactive', action='store_true', help='Start interactive mode')
    
    args = parser.parse_args()
    
    # Create simulator instance
    simulator = TactHostSimulator(port=args.port, baud_rate=args.baud)
    
    # Connect to Arduino
    if not simulator.connect():
        sys.exit(1)
    
    try:
        if args.test:
            simulator.run_gesture_tests()
        elif args.interactive:
            simulator.interactive_mode()
        else:
            # Default: run a quick demo
            print("Running quick demo...")
            time.sleep(1)
            simulator.gesture_poke(0)
            time.sleep(1)
            simulator.gesture_pat(1)
            time.sleep(1)
            simulator.gesture_stroke()
            print("Demo complete. Use --interactive for manual control.")
            
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        simulator.disconnect()

if __name__ == '__main__':
    main()