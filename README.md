# Tact - Haptic Feedback System

**A simplified mediated social touch system for rapid prototyping**

## Overview

Tact is a proof-of-concept haptic feedback system that translates virtual touch events into physical sensations through vibrotactile motors. Built for the Arduino 101 platform, this MVP prototype demonstrates core haptic communication concepts with a focus on rapid assembly and testing.

## Connection to Opus (in development)

**Tact** is a small-scale, rapid-prototyping platform for experimenting with the exact kind of mediated touch and haptic communication explored in _Virtual Encounters of the Haptic Kind_. The paper demonstrates how real-time, multi-point haptics can increase presence, naturalness, and emotional connection in virtual environments. Tact distills that down into a simple, controllable, and quick-to-build system so you can test those principles without the overhead of a full VR setup.

For **Opus**, which aims to translate emotional or contextual cues into **expressive haptic feedback**, Tact serves as:

- **A sandbox** — letting you trial different haptic patterns, intensities, and gesture styles in real hardware.
- **A learning tool** — giving you hands-on insight into latency, comfort, spatial motor placement, and perception, all of which are critical for making Opus feel natural.
- **A stepping stone** — providing a minimal but functional framework for collision/event-driven haptics that can later be adapted to Opus’ AI-driven emotional signal processing.

In short, Tact is a **bridge**: it takes the academic ideas from the paper and grounds them in a lightweight, experimental form you can iterate on quickly, generating practical knowledge that directly feeds into the haptic design language and technical implementation of Opus.


### Key Features

- **3-4 Vibrotactile Motors**: Spatial haptic feedback on back of hand or forearm
- **First Contact Detection**: Distinct 75ms pulses for initial touch events
- **Pressure Scaling**: Linear vibration intensity based on penetration depth (20-70% PWM)
- **Simple Assembly**: One-hour build time with basic components
- **USB Serial Communication**: CSV-format messages at 115200 baud
- **Fixed Calibration**: Hardcoded parameters for immediate operation

## Quick Start

### Prerequisites

- Arduino 101 (Intel Curie)
- 3-4 ERM vibrotactile motors (10mm coin type)
- Arduino IDE with Intel Curie board support
- Python 3.7+ with pip
- USB cable and basic wiring materials

### 5-Minute Setup

**Option A: Automated Setup (Recommended)**
```bash
cd Tact
./setup.sh
```

**Option B: Manual Setup**

1. **Clone and Navigate**
   ```bash
   cd Tact
   ```

2. **Upload Firmware**
   - Open `firmware/tact_haptic_controller.ino` in Arduino IDE
   - Select Arduino/Genuino 101 board
   - Upload to your Arduino 101

3. **Install Host Dependencies**
   ```bash
   # Create virtual environment (recommended)
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r host-app/requirements.txt
   ```

4. **Test Connection**
   ```bash
   source venv/bin/activate  # if using virtual environment
   python host-app/tact_host_simulator.py --test
   ```

### Hardware Setup

**Motor Connections:**
- Motor 0 → Pin 3 (PWM)
- Motor 1 → Pin 5 (PWM) 
- Motor 2 → Pin 6 (PWM)
- Motor 3 → Pin 9 (PWM)
- All motor grounds → Arduino GND

**Mounting:**
- Attach motors to back of hand or forearm using velcro/tape
- Space motors 2-3 inches apart for spatial differentiation
- Ensure good skin contact for effective feedback

## Project Structure

```
Tact/
├── firmware/
│   └── tact_haptic_controller.ino    # Arduino 101 firmware
├── host-app/
│   ├── tact_host_simulator.py        # Python host application
│   └── requirements.txt              # Python dependencies
├── docs/
│   └── assembly_guide.md             # Detailed assembly instructions
├── tests/
│   └── system_validation.py          # Automated test suite
├── hardware/
│   └── wiring_diagram.md             # Hardware setup guide
├── examples/
│   └── basic_usage.py                # Usage examples and demos
├── .trae/documents/
│   └── Tact_PRD.md                   # Product Requirements Document
├── quick_start.py                    # One-command setup script
├── setup.sh                          # Automated setup script
└── README.md                         # This file
```

## Usage

### Basic Operation

1. **Connect Arduino** via USB
2. **Run Host Simulator**:
   ```bash
   python tact_host_simulator.py --interactive
   ```
3. **Try Commands**:
   - `stroke` - Sweeping gesture across all motors
   - `pat 1` - Quick pat on motor 1
   - `poke 2` - Sharp poke on motor 2
   - `squeeze` - Gradual pressure on all motors

### Message Protocol

The system uses CSV-format messages over USB serial:
```
actuator_id,penetration_depth,first_contact
```

**Examples:**
- `2,0.58,1` - Motor 2, 58% penetration, first contact
- `0,0.25,0` - Motor 0, 25% penetration, sustained contact
- `1,0.0,0` - Motor 1, no contact (stop)

### Gesture Patterns

**Stroke**: Sequential activation across motors with wave pattern
**Pat**: Quick pulse with decay on single motor
**Poke**: Sharp contact and immediate release
**Squeeze**: Gradual intensity increase/decrease on all motors

## Technical Specifications

### Fixed Parameters (MVP)

- **First Contact Pulse**: 75ms duration at 90% PWM
- **Sustained Contact**: 20-70% PWM linear scaling
- **Penetration Threshold**: 0.1 (ignore below)
- **Update Rate**: 20-30 Hz
- **Serial Baud**: 115200

### Hardware Constraints

- **Power**: USB-powered, single motor limitation
- **Current**: ~100mA peak per motor
- **Voltage**: 5V from Arduino, optional resistors for 3V motors
- **Response Time**: <100ms latency

## Assembly Guide

See [`docs/assembly_guide.md`](docs/assembly_guide.md) for detailed step-by-step instructions. Target assembly time: **60 minutes**.

### Assembly Steps Summary

1. **Prepare Arduino 101** (5 min)
2. **Wire Motors** (10 min)
3. **Mount to Wearable** (10 min)
4. **Upload Firmware** (10 min)
5. **Setup Host App** (10 min)
6. **Test & Calibrate** (8 min)
7. **Demo Preparation** (5 min)

## Testing

### Automated Tests
```bash
# Run all gesture tests
python tact_host_simulator.py --test

# Interactive mode for manual testing
python tact_host_simulator.py --interactive
```

### Validation Checklist

- [ ] All motors respond to commands
- [ ] First-contact pulses are distinguishable
- [ ] Intensity scaling works correctly
- [ ] Spatial differentiation across motors
- [ ] <100ms response time
- [ ] Comfortable for 10+ minutes
- [ ] Gesture patterns recognizable

## Troubleshooting

### Common Issues

**Motors not responding:**
- Check wiring connections
- Verify PWM pin assignments
- Test with multimeter

**Serial communication errors:**
- Check COM port selection
- Verify baud rate (115200)
- Try different USB cable

**Weak vibration:**
- Check motor power connections
- Verify PWM output levels
- Consider removing series resistors

## Development

### Adding New Gestures

1. **Define Pattern**: Create time-varying actuator sequences
2. **Implement in Host**: Add method to `TactHostSimulator` class
3. **Test**: Verify with interactive mode
4. **Document**: Add to gesture library

### Firmware Modifications

- **Parameters**: Modify constants in firmware for different behavior
- **Motors**: Change `NUM_MOTORS` and `MOTOR_PINS` for different configurations
- **Protocol**: Extend CSV parser for additional data fields

## Contributing

This is a prototype system designed for rapid experimentation. Contributions welcome:

- Hardware improvements and alternative mounting solutions
- Additional gesture patterns and interaction modes
- Performance optimizations and parameter tuning
- Documentation and assembly guide improvements

## License

Open source - see individual file headers for specific licensing.

## References

- Based on research in mediated social touch and haptic communication
- Optimized for Arduino 101 (Intel Curie) platform
- Designed for rapid prototyping and educational use

## Support

For assembly questions or technical issues:
1. Check the troubleshooting section
2. Review the assembly guide
3. Test with provided validation scripts
4. Document any modifications for future reference

---
