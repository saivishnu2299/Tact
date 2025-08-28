#!/usr/bin/env python3
"""
Tact Haptic Feedback System - Quick Start Script

This script provides a one-command setup and test for the Tact system.
It will:
1. Check system requirements
2. Install Python dependencies
3. Detect Arduino connection
4. Run basic functionality test
5. Launch interactive demo

Usage:
    python quick_start.py
"""

import sys
import os
import subprocess
import time
from pathlib import Path

def print_header():
    print("\n" + "=" * 60)
    print("    TACT HAPTIC FEEDBACK SYSTEM - QUICK START")
    print("=" * 60)
    print("This script will set up and test your Tact system.")
    print("Make sure your Arduino 101 is connected via USB.")
    print("=" * 60 + "\n")

def check_python_version():
    """Check if Python version is compatible"""
    print("[1/6] Checking Python version...")
    
    if sys.version_info < (3, 6):
        print("❌ Error: Python 3.6 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - OK")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n[2/6] Installing Python dependencies...")
    
    requirements_file = Path(__file__).parent / "host-app" / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ Error: requirements.txt not found")
        return False
    
    try:
        # Try to import pyserial first
        import serial
        print(f"✅ pyserial {serial.__version__} already available")
        return True
    except ImportError:
        pass
    
    try:
        print("   Installing pyserial...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print("   This system uses an externally managed Python environment.")
        print("   Please create a virtual environment:")
        print("   python3 -m venv venv")
        print("   source venv/bin/activate")
        print("   pip install -r host-app/requirements.txt")
        print("   Then run this script again.")
        return False

def detect_arduino():
    """Detect connected Arduino devices"""
    print("\n[3/6] Detecting Arduino connection...")
    
    try:
        import serial.tools.list_ports
        
        # Look for Arduino devices
        arduino_ports = []
        for port in serial.tools.list_ports.comports():
            if any(keyword in port.description.lower() for keyword in ['arduino', 'genuino', 'intel']):
                arduino_ports.append(port.device)
        
        if not arduino_ports:
            print("❌ No Arduino devices detected")
            print("   Please check:")
            print("   - Arduino 101 is connected via USB")
            print("   - USB cable supports data transfer")
            print("   - Arduino drivers are installed")
            return None
        
        if len(arduino_ports) == 1:
            print(f"✅ Arduino detected on {arduino_ports[0]}")
            return arduino_ports[0]
        else:
            print(f"✅ Multiple Arduino devices detected:")
            for i, port in enumerate(arduino_ports):
                print(f"   {i+1}. {port}")
            return arduino_ports[0]  # Use first one
            
    except ImportError:
        print("❌ Error: pyserial not available")
        return None
    except Exception as e:
        print(f"❌ Error detecting Arduino: {e}")
        return None

def check_firmware(port):
    """Check if Tact firmware is loaded"""
    print("\n[4/6] Checking firmware...")
    
    try:
        import serial
        
        # Try to connect and send test command
        ser = serial.Serial(port, 115200, timeout=2)
        time.sleep(2)  # Wait for Arduino to initialize
        
        # Send test command
        ser.write(b"0,0.5,1\n")
        time.sleep(0.1)
        
        # Try to read response (firmware sends confirmation)
        response = ser.read_all().decode('utf-8', errors='ignore')
        ser.close()
        
        if "Tact" in response or "Motor" in response or len(response) > 0:
            print("✅ Tact firmware detected")
            return True
        else:
            print("⚠️  Warning: Firmware may not be loaded")
            print("   Please upload tact_haptic_controller.ino to your Arduino")
            return False
            
    except Exception as e:
        print(f"⚠️  Warning: Could not verify firmware: {e}")
        print("   Continuing anyway...")
        return True

def run_basic_test(port):
    """Run basic functionality test"""
    print("\n[5/6] Running basic functionality test...")
    
    try:
        # Import the controller
        sys.path.append(str(Path(__file__).parent / 'host-app'))
        from tact_host_simulator import TactHostSimulator
        
        controller = TactHostSimulator(port=port)
        if not controller.connect():
            print("❌ Failed to connect to Tact device")
            return False
        
        print("   Testing motor activation...")
        
        # Test each motor briefly
        for motor_id in range(4):
            print(f"   Motor {motor_id}...", end=" ")
            controller.send_touch_event(motor_id, 0.6, first_contact=True)
            time.sleep(0.3)
            controller.send_touch_event(motor_id, 0.0, first_contact=False)
            time.sleep(0.2)
            print("OK")
        
        controller.disconnect()
        print("✅ Basic test completed successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Error importing controller: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

def launch_demo(port):
    """Launch interactive demo"""
    print("\n[6/6] Launching interactive demo...")
    print("\n" + "=" * 40)
    print("  TACT SYSTEM READY!")
    print("=" * 40)
    print("\nYour Tact haptic feedback system is now ready to use.")
    print("\nOptions:")
    print("  1. Run interactive demo")
    print("  2. Run gesture patterns demo")
    print("  3. Exit")
    
    while True:
        try:
            choice = input("\nSelect option (1-3): ").strip()
            
            if choice == '1':
                print("\nStarting interactive demo...")
                os.system(f'python "{Path(__file__).parent / "examples" / "basic_usage.py"}" --port "{port}" --demo interactive')
                break
            elif choice == '2':
                print("\nStarting gesture demo...")
                os.system(f'python "{Path(__file__).parent / "examples" / "basic_usage.py"}" --port "{port}" --demo gestures')
                break
            elif choice == '3':
                print("\nExiting. Your Tact system is ready for use!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break

def print_next_steps():
    """Print information about next steps"""
    print("\n" + "=" * 60)
    print("  NEXT STEPS")
    print("=" * 60)
    print("\n1. Hardware Assembly:")
    print("   - See docs/assembly_guide.md for detailed instructions")
    print("   - Mount 3-4 vibrotactile motors on hand/forearm")
    print("   - Connect motors to Arduino pins 3, 5, 6, 9")
    
    print("\n2. Software Usage:")
    print("   - Run examples/basic_usage.py for demonstrations")
    print("   - Use host-app/tact_host_simulator.py for custom applications")
    print("   - See tests/system_validation.py for system testing")
    
    print("\n3. Development:")
    print("   - Modify firmware/tact_haptic_controller.ino for custom behavior")
    print("   - Extend host application for your specific use case")
    print("   - See README.md for detailed documentation")
    
    print("\n4. Troubleshooting:")
    print("   - Check hardware/wiring_diagram.md for connection help")
    print("   - See README.md troubleshooting section")
    print("   - Verify motor connections and power supply")
    
    print("\n" + "=" * 60)
    print("  Happy hacking with Tact!")
    print("=" * 60 + "\n")

def main():
    """Main setup and test routine"""
    print_header()
    
    # Step 1: Check Python version
    if not check_python_version():
        return 1
    
    # Step 2: Install dependencies
    if not install_dependencies():
        return 1
    
    # Step 3: Detect Arduino
    arduino_port = detect_arduino()
    if not arduino_port:
        print("\n❌ Setup failed: No Arduino detected")
        print("\nPlease connect your Arduino 101 and try again.")
        return 1
    
    # Step 4: Check firmware
    firmware_ok = check_firmware(arduino_port)
    
    # Step 5: Run basic test (only if firmware seems OK)
    if firmware_ok:
        test_ok = run_basic_test(arduino_port)
        if not test_ok:
            print("\n⚠️  Basic test failed, but continuing...")
    
    # Step 6: Launch demo
    launch_demo(arduino_port)
    
    # Print next steps
    print_next_steps()
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        print("Please check your setup and try again.")
        sys.exit(1)