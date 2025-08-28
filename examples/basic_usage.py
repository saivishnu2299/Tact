#!/usr/bin/env python3
"""
Tact Haptic Feedback System - Basic Usage Examples

This script demonstrates common usage patterns for the Tact system,
including basic touch simulation, gesture patterns, and testing scenarios.

Usage:
    python basic_usage.py [--port COM_PORT] [--demo DEMO_NAME]

Examples:
    python basic_usage.py --demo touch_test
    python basic_usage.py --demo gesture_demo
    python basic_usage.py --port /dev/ttyACM0 --demo interactive
"""

import sys
import time
import argparse
from pathlib import Path

# Add parent directory to path to import tact_host_simulator
sys.path.append(str(Path(__file__).parent.parent / 'host-app'))

try:
    from tact_host_simulator import TactHostSimulator
except ImportError:
    print("Error: Could not import TactHostSimulator. Make sure you're running from the correct directory.")
    sys.exit(1)

def demo_touch_test(controller):
    """
    Basic touch test - activate each motor individually
    """
    print("\n=== Touch Test Demo ===")
    print("Testing each motor individually...")
    
    for motor_id in range(4):
        print(f"\nActivating Motor {motor_id}...")
        
        # First contact pulse
        controller.send_touch_event(motor_id, 0.5, first_contact=True)
        time.sleep(0.5)
        
        # Sustained contact with varying intensity
        for intensity in [0.2, 0.4, 0.6, 0.8]:
            print(f"  Intensity: {intensity:.1f}")
            controller.send_touch_event(motor_id, intensity, first_contact=False)
            time.sleep(0.3)
        
        # Release
        controller.send_touch_event(motor_id, 0.0, first_contact=False)
        time.sleep(0.5)
    
    print("Touch test complete!")

def demo_gesture_patterns(controller):
    """
    Demonstrate common gesture patterns
    """
    print("\n=== Gesture Patterns Demo ===")
    
    # Stroke pattern
    print("\nStroke pattern (left to right)...")
    controller.simulate_stroke(duration=2.0, intensity=0.6)
    time.sleep(1)
    
    # Pat pattern
    print("Pat pattern (quick taps)...")
    controller.simulate_pat(taps=3, intensity=0.8)
    time.sleep(1)
    
    # Poke pattern
    print("Poke pattern (single strong contact)...")
    controller.simulate_poke(motor_id=1, intensity=0.9)
    time.sleep(1)
    
    # Squeeze pattern
    print("Squeeze pattern (gradual pressure)...")
    controller.simulate_squeeze(duration=3.0, max_intensity=0.7)
    time.sleep(1)
    
    print("Gesture patterns complete!")

def demo_spatial_patterns(controller):
    """
    Demonstrate spatial feedback patterns
    """
    print("\n=== Spatial Patterns Demo ===")
    
    # Circular pattern
    print("\nCircular activation pattern...")
    motor_sequence = [0, 1, 3, 2, 0]  # Assuming motors arranged in square
    
    for cycle in range(2):
        for motor_id in motor_sequence:
            controller.send_touch_event(motor_id, 0.6, first_contact=True)
            time.sleep(0.2)
            controller.send_touch_event(motor_id, 0.0, first_contact=False)
            time.sleep(0.1)
    
    # Wave pattern
    print("Wave pattern (sequential activation)...")
    for wave in range(3):
        for motor_id in range(4):
            controller.send_touch_event(motor_id, 0.5, first_contact=True)
            time.sleep(0.15)
        
        # Fade out
        for motor_id in range(4):
            controller.send_touch_event(motor_id, 0.0, first_contact=False)
        time.sleep(0.3)
    
    # Simultaneous pattern
    print("Simultaneous activation (all motors)...")
    # Activate all motors with first contact
    for motor_id in range(4):
        controller.send_touch_event(motor_id, 0.7, first_contact=True)
    
    time.sleep(0.5)
    
    # Vary intensity together
    for intensity in [0.3, 0.6, 0.9, 0.6, 0.3]:
        for motor_id in range(4):
            controller.send_touch_event(motor_id, intensity, first_contact=False)
        time.sleep(0.3)
    
    # Release all
    for motor_id in range(4):
        controller.send_touch_event(motor_id, 0.0, first_contact=False)
    
    print("Spatial patterns complete!")

def demo_interactive_mode(controller):
    """
    Interactive mode for manual testing
    """
    print("\n=== Interactive Mode ===")
    print("Commands:")
    print("  t<motor_id> <intensity>  - Touch motor (e.g., 't0 0.5')")
    print("  f<motor_id> <intensity>  - First contact (e.g., 'f1 0.8')")
    print("  r<motor_id>              - Release motor (e.g., 'r0')")
    print("  stroke                   - Stroke gesture")
    print("  pat                      - Pat gesture")
    print("  poke <motor_id>          - Poke gesture (e.g., 'poke 2')")
    print("  squeeze                  - Squeeze gesture")
    print("  test                     - Run touch test")
    print("  quit                     - Exit interactive mode")
    print()
    
    while True:
        try:
            command = input("Tact> ").strip().lower()
            
            if command == 'quit' or command == 'q':
                break
            elif command == 'test':
                demo_touch_test(controller)
            elif command == 'stroke':
                controller.simulate_stroke()
            elif command == 'pat':
                controller.simulate_pat()
            elif command == 'squeeze':
                controller.simulate_squeeze()
            elif command.startswith('t'):
                parts = command.split()
                if len(parts) == 2:
                    motor_id = int(parts[0][1:])
                    intensity = float(parts[1])
                    controller.send_touch_event(motor_id, intensity, first_contact=False)
                    print(f"Touch motor {motor_id} at {intensity:.2f}")
                else:
                    print("Usage: t<motor_id> <intensity>")
            elif command.startswith('f'):
                parts = command.split()
                if len(parts) == 2:
                    motor_id = int(parts[0][1:])
                    intensity = float(parts[1])
                    controller.send_touch_event(motor_id, intensity, first_contact=True)
                    print(f"First contact motor {motor_id} at {intensity:.2f}")
                else:
                    print("Usage: f<motor_id> <intensity>")
            elif command.startswith('r'):
                motor_id = int(command[1:])
                controller.send_touch_event(motor_id, 0.0, first_contact=False)
                print(f"Released motor {motor_id}")
            elif command.startswith('poke'):
                parts = command.split()
                if len(parts) == 2:
                    motor_id = int(parts[1])
                    controller.simulate_poke(motor_id)
                    print(f"Poke motor {motor_id}")
                else:
                    print("Usage: poke <motor_id>")
            elif command == '':
                continue
            else:
                print(f"Unknown command: {command}")
                
        except (ValueError, IndexError) as e:
            print(f"Error parsing command: {e}")
        except KeyboardInterrupt:
            print("\nExiting interactive mode...")
            break
        except Exception as e:
            print(f"Error: {e}")

def demo_timing_test(controller):
    """
    Test timing and responsiveness
    """
    print("\n=== Timing Test Demo ===")
    print("Testing rapid sequential activation...")
    
    # Rapid sequential test
    start_time = time.time()
    for i in range(20):
        motor_id = i % 4
        controller.send_touch_event(motor_id, 0.5, first_contact=True)
        time.sleep(0.05)  # 50ms intervals
        controller.send_touch_event(motor_id, 0.0, first_contact=False)
        time.sleep(0.05)
    
    elapsed = time.time() - start_time
    print(f"Completed 20 activations in {elapsed:.2f} seconds")
    print(f"Average rate: {20/elapsed:.1f} activations/second")
    
    # Sustained contact timing
    print("\nTesting sustained contact timing...")
    motor_id = 0
    controller.send_touch_event(motor_id, 0.6, first_contact=True)
    
    # Hold for 5 seconds with intensity variations
    for i in range(50):
        intensity = 0.3 + 0.4 * (0.5 + 0.5 * time.sin(i * 0.2))  # Sine wave 0.3-0.7
        controller.send_touch_event(motor_id, intensity, first_contact=False)
        time.sleep(0.1)
    
    controller.send_touch_event(motor_id, 0.0, first_contact=False)
    print("Timing test complete!")

def main():
    parser = argparse.ArgumentParser(description='Tact Haptic Feedback System - Basic Usage Examples')
    parser.add_argument('--port', '-p', default=None, help='Serial port (auto-detect if not specified)')
    parser.add_argument('--demo', '-d', default='all', 
                       choices=['all', 'touch_test', 'gestures', 'spatial', 'interactive', 'timing'],
                       help='Demo to run')
    parser.add_argument('--baudrate', '-b', type=int, default=115200, help='Serial baudrate')
    
    args = parser.parse_args()
    
    print("Tact Haptic Feedback System - Basic Usage Examples")
    print("=" * 50)
    
    # Initialize controller
    try:
        controller = TactHostSimulator(port=args.port, baudrate=args.baudrate)
        if not controller.connect():
            print("Failed to connect to Tact device. Please check:")
            print("1. Arduino is connected via USB")
            print("2. Correct firmware is uploaded")
            print("3. Serial port permissions")
            return 1
        
        print(f"Connected to Tact device on {controller.port}")
        
        # Run selected demo
        if args.demo == 'all':
            demo_touch_test(controller)
            time.sleep(1)
            demo_gesture_patterns(controller)
            time.sleep(1)
            demo_spatial_patterns(controller)
            time.sleep(1)
            demo_timing_test(controller)
        elif args.demo == 'touch_test':
            demo_touch_test(controller)
        elif args.demo == 'gestures':
            demo_gesture_patterns(controller)
        elif args.demo == 'spatial':
            demo_spatial_patterns(controller)
        elif args.demo == 'interactive':
            demo_interactive_mode(controller)
        elif args.demo == 'timing':
            demo_timing_test(controller)
        
        print("\nDemo complete!")
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    finally:
        try:
            controller.disconnect()
        except:
            pass
    
    return 0

if __name__ == '__main__':
    sys.exit(main())