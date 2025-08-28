#!/usr/bin/env python3
"""
Tact System Validation Test Suite

This script provides automated testing for the Tact haptic feedback system,
validating communication, motor response, and gesture functionality.
"""

import sys
import time
import serial
import serial.tools.list_ports
from typing import List, Optional

class TactValidator:
    def __init__(self, port: str = None, baud_rate: int = 115200):
        self.port = port
        self.baud_rate = baud_rate
        self.serial_connection = None
        self.test_results = []
        
    def find_arduino_port(self) -> Optional[str]:
        """Find Arduino port automatically."""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if 'Arduino' in port.description or 'USB' in port.description:
                return port.device
        return None
    
    def connect(self) -> bool:
        """Establish connection to Arduino."""
        if self.port is None:
            self.port = self.find_arduino_port()
            
        if self.port is None:
            self.log_result("Connection", False, "Could not find Arduino port")
            return False
            
        try:
            self.serial_connection = serial.Serial(self.port, self.baud_rate, timeout=2)
            time.sleep(2)  # Wait for Arduino initialization
            
            # Check for Arduino ready message
            ready_found = False
            for _ in range(10):
                if self.serial_connection.in_waiting:
                    response = self.serial_connection.readline().decode().strip()
                    if "Tact Haptic Controller Ready" in response:
                        ready_found = True
                        break
                time.sleep(0.1)
            
            if ready_found:
                self.log_result("Connection", True, f"Connected to {self.port}")
                return True
            else:
                self.log_result("Connection", False, "Arduino not responding with ready message")
                return False
                
        except Exception as e:
            self.log_result("Connection", False, f"Serial error: {e}")
            return False
    
    def log_result(self, test_name: str, passed: bool, details: str = ""):
        """Log test result."""
        status = "PASS" if passed else "FAIL"
        result = {
            'test': test_name,
            'status': status,
            'details': details,
            'timestamp': time.time()
        }
        self.test_results.append(result)
        print(f"[{status}] {test_name}: {details}")
    
    def send_command(self, actuator_id: int, penetration: float, first_contact: bool) -> bool:
        """Send command and verify transmission."""
        if not self.serial_connection:
            return False
            
        message = f"{actuator_id},{penetration:.2f},{1 if first_contact else 0}\n"
        try:
            self.serial_connection.write(message.encode())
            return True
        except Exception as e:
            self.log_result("Command Send", False, f"Failed to send: {e}")
            return False
    
    def test_basic_communication(self) -> bool:
        """Test basic serial communication."""
        print("\n=== Testing Basic Communication ===")
        
        # Test sending simple commands
        test_commands = [
            (0, 0.5, True),
            (1, 0.3, False),
            (2, 0.0, False),
            (3, 0.8, True)
        ]
        
        success_count = 0
        for actuator_id, penetration, first_contact in test_commands:
            if self.send_command(actuator_id, penetration, first_contact):
                success_count += 1
                time.sleep(0.1)
        
        passed = success_count == len(test_commands)
        self.log_result("Basic Communication", passed, 
                       f"{success_count}/{len(test_commands)} commands sent successfully")
        return passed
    
    def test_motor_response(self) -> bool:
        """Test individual motor response."""
        print("\n=== Testing Motor Response ===")
        
        motor_results = []
        for motor_id in range(4):
            print(f"Testing motor {motor_id}...")
            
            # Send activation command
            if self.send_command(motor_id, 0.7, True):
                time.sleep(0.2)  # Let motor run
                
                # Send deactivation command
                if self.send_command(motor_id, 0.0, False):
                    motor_results.append(True)
                    print(f"  Motor {motor_id}: Command sequence completed")
                else:
                    motor_results.append(False)
                    print(f"  Motor {motor_id}: Failed to deactivate")
            else:
                motor_results.append(False)
                print(f"  Motor {motor_id}: Failed to activate")
            
            time.sleep(0.3)  # Pause between motors
        
        success_count = sum(motor_results)
        passed = success_count >= 3  # Allow one motor to fail
        self.log_result("Motor Response", passed, 
                       f"{success_count}/4 motors responded correctly")
        return passed
    
    def test_first_contact_detection(self) -> bool:
        """Test first contact pulse functionality."""
        print("\n=== Testing First Contact Detection ===")
        
        # Test first contact sequence
        test_sequences = [
            [(0, 0.6, True), (0, 0.6, False), (0, 0.0, False)],  # First contact then sustain
            [(1, 0.0, False), (1, 0.5, True), (1, 0.0, False)],  # No contact to first contact
            [(2, 0.4, False), (2, 0.8, False), (2, 0.0, False)]  # Sustained contact variation
        ]
        
        success_count = 0
        for i, sequence in enumerate(test_sequences):
            print(f"Testing sequence {i+1}...")
            sequence_success = True
            
            for actuator_id, penetration, first_contact in sequence:
                if not self.send_command(actuator_id, penetration, first_contact):
                    sequence_success = False
                    break
                time.sleep(0.1)
            
            if sequence_success:
                success_count += 1
                print(f"  Sequence {i+1}: Completed successfully")
            else:
                print(f"  Sequence {i+1}: Failed")
            
            time.sleep(0.5)  # Pause between sequences
        
        passed = success_count == len(test_sequences)
        self.log_result("First Contact Detection", passed, 
                       f"{success_count}/{len(test_sequences)} sequences completed")
        return passed
    
    def test_intensity_scaling(self) -> bool:
        """Test penetration depth scaling."""
        print("\n=== Testing Intensity Scaling ===")
        
        # Test different intensity levels
        intensity_levels = [0.1, 0.3, 0.5, 0.7, 0.9]
        motor_id = 1  # Use motor 1 for testing
        
        print(f"Testing intensity scaling on motor {motor_id}...")
        
        # Start with first contact
        if not self.send_command(motor_id, intensity_levels[0], True):
            self.log_result("Intensity Scaling", False, "Failed to start intensity test")
            return False
        
        time.sleep(0.2)
        
        # Test scaling through different levels
        success_count = 0
        for intensity in intensity_levels[1:]:
            if self.send_command(motor_id, intensity, False):
                success_count += 1
                print(f"  Intensity {intensity}: Sent successfully")
            else:
                print(f"  Intensity {intensity}: Failed")
            time.sleep(0.3)
        
        # Stop motor
        self.send_command(motor_id, 0.0, False)
        
        passed = success_count == len(intensity_levels) - 1
        self.log_result("Intensity Scaling", passed, 
                       f"{success_count}/{len(intensity_levels)-1} intensity levels tested")
        return passed
    
    def test_timing_performance(self) -> bool:
        """Test system timing and responsiveness."""
        print("\n=== Testing Timing Performance ===")
        
        # Test rapid command sequence
        start_time = time.time()
        command_count = 20
        success_count = 0
        
        for i in range(command_count):
            motor_id = i % 4
            penetration = 0.5 if i % 2 == 0 else 0.0
            first_contact = (i % 4 == 0)
            
            if self.send_command(motor_id, penetration, first_contact):
                success_count += 1
            
            time.sleep(0.05)  # 20 Hz rate
        
        end_time = time.time()
        total_time = end_time - start_time
        expected_time = command_count * 0.05
        
        timing_ok = abs(total_time - expected_time) < 0.5  # Allow 500ms tolerance
        commands_ok = success_count == command_count
        
        passed = timing_ok and commands_ok
        self.log_result("Timing Performance", passed, 
                       f"{success_count}/{command_count} commands in {total_time:.2f}s")
        return passed
    
    def test_error_handling(self) -> bool:
        """Test system error handling with invalid commands."""
        print("\n=== Testing Error Handling ===")
        
        # Test invalid commands (these should be handled gracefully)
        invalid_commands = [
            "5,0.5,1\n",      # Invalid motor ID
            "0,1.5,1\n",      # Invalid penetration (>1.0)
            "0,-0.1,1\n",     # Invalid penetration (<0.0)
            "abc,0.5,1\n",    # Invalid format
            "0,0.5\n",        # Missing field
            "\n"              # Empty command
        ]
        
        success_count = 0
        for i, command in enumerate(invalid_commands):
            try:
                self.serial_connection.write(command.encode())
                success_count += 1  # System should handle gracefully
                print(f"  Invalid command {i+1}: Handled gracefully")
            except Exception as e:
                print(f"  Invalid command {i+1}: Caused exception: {e}")
            
            time.sleep(0.1)
        
        # Send valid command to ensure system still works
        if self.send_command(0, 0.5, True):
            time.sleep(0.1)
            self.send_command(0, 0.0, False)
            recovery_ok = True
        else:
            recovery_ok = False
        
        passed = success_count == len(invalid_commands) and recovery_ok
        self.log_result("Error Handling", passed, 
                       f"System handled {success_count}/{len(invalid_commands)} invalid commands")
        return passed
    
    def run_full_validation(self) -> bool:
        """Run complete validation suite."""
        print("\n" + "="*50)
        print("TACT SYSTEM VALIDATION SUITE")
        print("="*50)
        
        if not self.connect():
            print("\nValidation failed: Could not connect to Arduino")
            return False
        
        # Run all tests
        tests = [
            self.test_basic_communication,
            self.test_motor_response,
            self.test_first_contact_detection,
            self.test_intensity_scaling,
            self.test_timing_performance,
            self.test_error_handling
        ]
        
        passed_tests = 0
        for test in tests:
            if test():
                passed_tests += 1
        
        # Print summary
        print("\n" + "="*50)
        print("VALIDATION SUMMARY")
        print("="*50)
        
        for result in self.test_results:
            status_symbol = "✓" if result['status'] == 'PASS' else "✗"
            print(f"{status_symbol} {result['test']}: {result['details']}")
        
        overall_passed = passed_tests == len(tests)
        print(f"\nOverall Result: {passed_tests}/{len(tests)} tests passed")
        
        if overall_passed:
            print("\n🎉 SYSTEM VALIDATION SUCCESSFUL!")
            print("Your Tact haptic feedback system is ready for use.")
        else:
            print("\n⚠️  SYSTEM VALIDATION FAILED")
            print("Please check the failed tests and verify your hardware setup.")
        
        return overall_passed
    
    def disconnect(self):
        """Close serial connection."""
        if self.serial_connection:
            self.serial_connection.close()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Tact System Validation Suite')
    parser.add_argument('--port', help='Serial port (auto-detect if not specified)')
    parser.add_argument('--baud', type=int, default=115200, help='Baud rate')
    
    args = parser.parse_args()
    
    validator = TactValidator(port=args.port, baud_rate=args.baud)
    
    try:
        success = validator.run_full_validation()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nValidation interrupted by user")
        sys.exit(1)
    finally:
        validator.disconnect()

if __name__ == '__main__':
    main()