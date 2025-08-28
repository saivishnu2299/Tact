# Tact Haptic Feedback System - Hardware Documentation

## Component Specifications

### Arduino 101 (Intel Curie)
- **Microcontroller**: Intel Curie (32-bit)
- **Operating Voltage**: 3.3V (5V tolerant I/O)
- **Digital I/O Pins**: 14 (4 PWM)
- **PWM Pins**: 3, 5, 6, 9
- **Power Supply**: USB (5V) or external (7-12V)
- **Current per I/O Pin**: 20mA

### ERM Vibrotactile Motors
- **Type**: Eccentric Rotating Mass (ERM)
- **Size**: 10mm coin type (recommended)
- **Operating Voltage**: 3V nominal (2-5V range)
- **Current Draw**: 60-100mA at 3V
- **Frequency**: ~150-200 Hz
- **Mounting**: Adhesive back or mounting holes

**Recommended Models:**
- Adafruit Product ID 1201
- Sparkfun ROB-08449
- Generic 10mm coin vibration motors

## Wiring Diagrams

### Basic 4-Motor Configuration

```
Arduino 101                    Motors
┌─────────────┐               ┌─────────────┐
│             │               │   Motor 0   │
│       Pin 3 ├───────────────┤ (+) Red     │
│             │               │             │
│       Pin 5 ├───────────────┤   Motor 1   │
│             │               │ (+) Red     │
│             │               │             │
│       Pin 6 ├───────────────┤   Motor 2   │
│             │               │ (+) Red     │
│             │               │             │
│       Pin 9 ├───────────────┤   Motor 3   │
│             │               │ (+) Red     │
│             │               │             │
│         GND ├─────┬─────────┤ (-) Black   │
│             │     ├─────────┤ (-) Black   │
│             │     ├─────────┤ (-) Black   │
│             │     └─────────┤ (-) Black   │
│             │               │             │
│         USB ├─── Power      │             │
└─────────────┘               └─────────────┘
```

### 3-Motor Simplified Configuration

```
Arduino 101                    Motors
┌─────────────┐               ┌─────────────┐
│             │               │   Motor 0   │
│       Pin 3 ├───────────────┤ (+) Red     │
│             │               │             │
│       Pin 5 ├───────────────┤   Motor 1   │
│             │               │ (+) Red     │
│             │               │             │
│       Pin 6 ├───────────────┤   Motor 2   │
│             │               │ (+) Red     │
│             │               │             │
│         GND ├─────┬─────────┤ (-) Black   │
│             │     ├─────────┤ (-) Black   │
│             │     └─────────┤ (-) Black   │
│             │               │             │
│         USB ├─── Power      │             │
└─────────────┘               └─────────────┘
```

### With Optional Current Limiting Resistors

```
Arduino 101                    Motors
┌─────────────┐               ┌─────────────┐
│             │    10-20Ω     │   Motor 0   │
│       Pin 3 ├───[RESISTOR]──┤ (+) Red     │
│             │    10-20Ω     │             │
│       Pin 5 ├───[RESISTOR]──┤   Motor 1   │
│             │    10-20Ω     │ (+) Red     │
│       Pin 6 ├───[RESISTOR]──┤             │
│             │    10-20Ω     │   Motor 2   │
│       Pin 9 ├───[RESISTOR]──┤ (+) Red     │
│             │               │             │
│         GND ├─────┬─────────┤ (-) Black   │
│             │     ├─────────┤ (-) Black   │
│             │     └─────────┤ (-) Black   │
│             │               │             │
│         USB ├─── Power      │             │
└─────────────┘               └─────────────┘

Note: Add resistors if motors get too hot or draw excessive current
```

## Physical Layout Options

### Back of Hand Configuration

```
     Wrist
       │
   ┌───┴───┐
   │ [M1]  │ [M2]     M = Motor
   │       │          Numbers correspond
   │  Hand │          to Arduino pins
   │       │
   │ [M0]  │ [M3]
   └───────┘
    Fingers

Spacing: 2-3 inches between motors
Mounting: Velcro straps, elastic bands, or tape
```

### Forearm Configuration

```
   Elbow                    Wrist
     │                        │
     ▼                        ▼
   [M0]──[M1]──[M2]──[M3]
     │    │    │    │
   2-3" spacing between motors

Mounting: Elastic sleeve or tape wrap
Advantages: Easier assembly, stable mounting
Disadvantages: Less precise spatial feedback
```

## Power Considerations

### Current Requirements

| Component | Current Draw | Notes |
|-----------|--------------|-------|
| Arduino 101 | ~50mA | Base consumption |
| Motor (each) | 60-100mA | At 3V operation |
| Total (4 motors) | ~450mA | If all motors at full power |
| USB Limit | 500mA | Standard USB 2.0 port |

### Power Management Strategy

**MVP Approach (Recommended):**
- Only one motor at full power simultaneously
- PWM control reduces average current
- USB power sufficient for prototype

**Alternative Approaches:**
- External 5V power supply (1A capacity)
- Battery pack with voltage regulator
- Current limiting resistors

### Voltage Considerations

- **Arduino Output**: 5V PWM (0-5V)
- **Motor Rating**: 3V nominal
- **PWM Scaling**: 60% duty cycle ≈ 3V average
- **Optional Resistors**: 10-20Ω for current limiting

## Assembly Hardware

### Required Tools
- Soldering iron and solder (for permanent connections)
- Wire strippers
- Multimeter (for testing)
- Hot glue gun (optional, for strain relief)

### Connection Methods

**Breadboard (Prototyping):**
- Use jumper wires
- Easy to modify
- Not suitable for wearable use

**Soldered Connections (Recommended):**
- Direct wire-to-pin soldering
- Heat shrink tubing for insulation
- Strain relief at connection points

**Connector Blocks:**
- Screw terminals for easy disconnection
- Larger profile but more robust
- Good for testing and development

### Mounting Solutions

**Velcro Straps (Recommended):**
- Adjustable tension
- Easy on/off
- Reusable
- Good skin contact

**Medical Tape:**
- Secure adhesion
- Skin-safe
- Single use
- Excellent contact

**Elastic Bands:**
- Comfortable
- Adjustable
- May lose tension over time
- Good for forearm mounting

**Custom Sleeve:**
- Professional appearance
- Consistent positioning
- Requires sewing/fabrication
- Out of scope for MVP

## Testing and Validation

### Electrical Testing

**Continuity Check:**
```bash
# Use multimeter to verify connections
1. Arduino Pin 3 → Motor 0 positive
2. Arduino Pin 5 → Motor 1 positive
3. Arduino Pin 6 → Motor 2 positive
4. Arduino Pin 9 → Motor 3 positive
5. Arduino GND → All motor negatives
```

**Voltage Testing:**
```bash
# With firmware running, measure PWM output
1. Upload test firmware
2. Measure voltage at motor terminals
3. Should see 0-5V depending on PWM duty cycle
4. Verify motors vibrate when voltage applied
```

**Current Testing:**
```bash
# Measure current draw per motor
1. Insert ammeter in series with motor
2. Run motor at various PWM levels
3. Verify current stays within safe limits
4. Check total system current < 500mA
```

### Mechanical Testing

**Vibration Intensity:**
- Test at different PWM levels (20%, 50%, 70%, 90%)
- Verify noticeable intensity differences
- Check for consistent vibration patterns

**Mounting Stability:**
- Wear device for 10+ minutes
- Test during hand/arm movement
- Verify motors maintain skin contact
- Check for comfort and irritation

**Spatial Resolution:**
- Test individual motor activation
- Verify user can distinguish between motors
- Test with eyes closed for tactile-only feedback

## Troubleshooting Guide

### No Motor Response

**Check List:**
1. Verify Arduino power (LED should be on)
2. Check USB connection and driver installation
3. Measure voltage at Arduino PWM pins
4. Test motor with direct 3V connection
5. Verify firmware upload and serial communication

### Weak Vibration

**Possible Causes:**
- Low PWM duty cycle (check firmware parameters)
- High resistance connections
- Motor voltage too low
- Worn or damaged motor

**Solutions:**
- Increase PWM values in firmware
- Check and re-solder connections
- Remove current limiting resistors
- Replace motor

### Overheating

**Symptoms:**
- Motors become hot to touch
- Arduino resets or behaves erratically
- USB port shuts down

**Solutions:**
- Add current limiting resistors (10-20Ω)
- Reduce PWM duty cycles
- Implement single-motor-at-a-time operation
- Use external power supply

### Inconsistent Response

**Possible Causes:**
- Loose connections
- Intermittent serial communication
- Power supply fluctuations
- Firmware timing issues

**Solutions:**
- Secure all connections with solder
- Check USB cable and port
- Add power supply decoupling capacitors
- Review firmware timing loops

## Safety Considerations

### Electrical Safety
- Use only USB power (5V) for MVP
- Avoid external power supplies during initial testing
- Ensure proper insulation of all connections
- Check for short circuits before powering on

### User Safety
- Monitor skin for irritation during extended use
- Ensure motors don't overheat
- Use skin-safe mounting materials
- Limit continuous operation time

### Component Protection
- Don't exceed Arduino pin current limits (20mA)
- Use PWM for motor control, not direct DC
- Protect against reverse polarity
- Consider ESD protection for development

## Future Improvements

### Hardware Enhancements
- Motor driver ICs for higher current capacity
- Battery power with charging circuit
- Custom PCB for compact assembly
- Higher resolution haptic feedback

### Mechanical Improvements
- Custom-fitted wearable design
- Multiple mounting configurations
- Improved motor isolation and positioning
- Wireless connectivity (BLE)

### Performance Upgrades
- More motors for higher spatial resolution
- Different motor types (LRA, piezo)
- Force feedback integration
- Multi-user networking capability