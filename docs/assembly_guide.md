# Tact Haptic Feedback System - Assembly Guide

## Overview

This guide will help you assemble the Tact haptic feedback prototype in approximately **one hour**. The system uses 3-4 vibrotactile motors connected directly to an Arduino 101, with simple mounting using velcro or tape.

## Required Components

### Hardware
- **Arduino 101** (Intel Curie)
- **3-4 ERM Vibrotactile Motors** (10mm coin type, 3V operation)
  - Recommended: Adafruit Product ID 1201 or similar
- **Connecting Wires** (jumper wires or hookup wire)
- **USB Cable** (for Arduino 101)
- **Mounting Materials**:
  - Velcro straps (preferred) OR
  - Elastic bands OR
  - Medical tape
- **Optional**: 10-20 ohm resistors (if motors run too hot)

### Software
- **Arduino IDE** (version 1.8.0 or later)
- **Python 3.7+** with pip
- **pyserial library**

## Assembly Steps (60 minutes total)

### Step 1: Prepare Arduino 101 (5 minutes)

1. **Install Arduino IDE** if not already installed
   - Download from: https://www.arduino.cc/en/software
   - Install Intel Curie board package via Board Manager

2. **Connect Arduino 101** via USB
   - Use the provided USB cable
   - Wait for driver installation (Windows/Mac)

3. **Verify Connection**
   - Open Arduino IDE
   - Select "Arduino/Genuino 101" from Tools > Board
   - Select correct COM port from Tools > Port
   - Upload a simple blink sketch to verify functionality

### Step 2: Wire Motors to Arduino (10 minutes)

**Motor Pin Assignments:**
- Motor 0: Pin 3 (PWM)
- Motor 1: Pin 5 (PWM)
- Motor 2: Pin 6 (PWM)
- Motor 3: Pin 9 (PWM)

**Wiring Instructions:**

1. **Identify Motor Terminals**
   - Most ERM motors have two wires (red/black or unmarked)
   - Polarity doesn't matter for basic vibration

2. **Connect Motors to Arduino**
   ```
   Motor 0: Red wire → Pin 3, Black wire → GND
   Motor 1: Red wire → Pin 5, Black wire → GND
   Motor 2: Red wire → Pin 6, Black wire → GND
   Motor 3: Red wire → Pin 9, Black wire → GND
   ```

3. **Power Considerations**
   - Motors will be powered from Arduino's 5V line via PWM
   - USB provides sufficient current for single motor operation
   - If motors get too hot, add 10-20 ohm resistors in series

**Wiring Diagram (Text):**
```
Arduino 101        Motors
┌─────────┐       ┌─────────┐
│   Pin 3 ├───────┤ Motor 0 │
│   Pin 5 ├───────┤ Motor 1 │
│   Pin 6 ├───────┤ Motor 2 │
│   Pin 9 ├───────┤ Motor 3 │
│     GND ├───┬───┤   GND   │
│         │   └───┤   GND   │
│         │   ┌───┤   GND   │
│         │   └───┤   GND   │
└─────────┘       └─────────┘
```

### Step 3: Mount Motors to Wearable (10 minutes)

**Back of Hand Configuration (Recommended):**

1. **Prepare Mounting Surface**
   - Clean back of hand or use a thin glove as base
   - Ensure skin contact area is dry

2. **Motor Placement**
   ```
   Back of Hand Layout:
   
        [Motor 1]     [Motor 2]
            │             │
            │    Hand     │
            │             │
        [Motor 0]     [Motor 3]
   
   Spacing: 2-3 inches between motors
   ```

3. **Secure Motors**
   - **Velcro Method** (preferred):
     - Attach velcro hook side to motor housing
     - Wrap velcro loop strap around hand/wrist
   - **Tape Method**:
     - Use medical tape or sports tape
     - Ensure motors maintain skin contact
   - **Elastic Band Method**:
     - Thread elastic through motor mounting holes
     - Adjust tension for comfort

**Alternative: Forearm Configuration**
- Mount motors in a line along forearm
- Use elastic sleeve or tape wrap
- Easier for testing, less precise spatial feedback

### Step 4: Upload Firmware (10 minutes)

1. **Open Firmware File**
   - Navigate to `firmware/tact_haptic_controller.ino`
   - Open in Arduino IDE

2. **Verify Settings**
   - Board: Arduino/Genuino 101
   - Port: Correct COM port
   - Programmer: Default

3. **Upload Firmware**
   - Click Upload button (arrow icon)
   - Wait for "Done uploading" message
   - Arduino will restart automatically

4. **Verify Upload**
   - Open Serial Monitor (Tools > Serial Monitor)
   - Set baud rate to 115200
   - Should see: "Tact Haptic Controller Ready"
   - Motor test sequence should run automatically

### Step 5: Set Up Host Application (10 minutes)

1. **Install Python Dependencies**
   ```bash
   cd host-app
   pip install -r requirements.txt
   ```

2. **Test Serial Connection**
   ```bash
   python tact_host_simulator.py --port [YOUR_PORT]
   ```
   - Replace [YOUR_PORT] with Arduino's COM port
   - Or omit --port for auto-detection

3. **Verify Communication**
   - Should see "Connected to Arduino on [port]"
   - Arduino messages should appear
   - Quick demo should run automatically

### Step 6: Basic Testing and Calibration (8 minutes)

1. **Motor Function Test**
   ```bash
   python tact_host_simulator.py --test
   ```
   - Each motor should vibrate in sequence
   - Verify all motors respond
   - Check for proper mounting (no loss of contact)

2. **Interactive Testing**
   ```bash
   python tact_host_simulator.py --interactive
   ```
   - Try commands: `poke 0`, `pat 1`, `stroke`, `squeeze`
   - Verify first-contact pulses are distinct
   - Test intensity scaling with manual commands

3. **Comfort Check**
   - Wear device for 2-3 minutes
   - Adjust mounting if uncomfortable
   - Ensure motors maintain skin contact during movement

### Step 7: Final Demo Preparation (5 minutes)

1. **Prepare Demo Script**
   - Test all four gesture types
   - Verify spatial differentiation across motors
   - Practice explaining the system

2. **Troubleshooting Check**
   - Ensure stable USB connection
   - Verify serial communication
   - Test motor responsiveness

## Troubleshooting

### Common Issues

**Motors Not Responding:**
- Check wiring connections
- Verify PWM pin assignments
- Test with multimeter (should see voltage on pins)
- Try uploading firmware again

**Serial Communication Errors:**
- Check COM port selection
- Verify baud rate (115200)
- Try different USB cable
- Restart Arduino IDE

**Motors Too Weak/Strong:**
- Adjust penetration depth values in host app
- Add/remove series resistors
- Check power supply (USB should be sufficient)

**Mounting Issues:**
- Ensure motors maintain skin contact
- Adjust strap tension
- Try different mounting positions
- Use medical tape for better adhesion

### Performance Validation

**Test Checklist:**
- [ ] All 3-4 motors respond to commands
- [ ] First-contact pulses are clearly distinguishable
- [ ] Sustained vibration scales with intensity
- [ ] Spatial differentiation works across motors
- [ ] System responds within 100ms
- [ ] Comfortable for 10+ minute sessions
- [ ] Gesture patterns are recognizable

## Safety Notes

- **Current Limitation**: Only one motor at full power simultaneously
- **Heat Check**: Motors should not get uncomfortably hot
- **Skin Safety**: Remove if any irritation occurs
- **Electrical Safety**: Use only USB power, no external supplies

## Next Steps

Once assembly is complete:
1. Run the full gesture test suite
2. Experiment with custom gesture patterns
3. Document any modifications or improvements
4. Consider expanding to more motors or different mounting options

## Success Criteria

Your prototype is successful if:
- Assembly completed within 60 minutes
- All motors respond to serial commands
- First-contact and sustained feedback are distinguishable
- Basic gesture recognition works
- System demonstrates core haptic communication concept

---

**Total Assembly Time: ~60 minutes**
**Difficulty Level: Beginner to Intermediate**
**Required Skills: Basic electronics, Arduino programming, Python**