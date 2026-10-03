# PWM testster

## Functionalities

### PWM mode

All parameters listed as integers
- Frequency: 1 - 999 Hz
- Duty cycle: 0 - 100 %
- Pulse duration: 1us - 9999ms

duty cycle and pulse duration are complementary, both should calculated from underlying uint16 value which the only value that should be store

### LED mode

- LED count: 1 - 99
- RGB - actual values
- HSL - calculated to/from RGB
- HSV - calculated to/from RGB

## Human interfaces

### 16x2 LCD i2c display 

- **Parameter selection mode** - places cursor under first letter of the paramters
- **Parameter edit mode** - blinks the first letter of the parameter, where cursor is placed

**First line always**:
1. Currently selected channel
2. Channel state On/Off
3. Channel mode PWM, WS28, etc.
    - Number of leds
    - frequency

**Second line depending on channel mode**:
- PWM parameters:
    - duty cycle in percent 0 - 100
    - pulse duration in us
- WS28 led strip parameters
    - RGB, HSL, HSV switchable 

| Line   | 1       | 2 | 3   | 4 | 5 | 6     | 7        | 8 | 9   | 10  | 11    | 12  | 13               | 14 | 15 | 16 |
|--------|---------|---|-----|---|---|-------|----------|---|-----|-----|-------|-----|------------------|----|----|----|
| Always | C       | H | 1-4 | - | O | N/F   | F        | - | P/L | W/E | M/D   | -   | F(freq)/C(count) | 9  | 9  | 9  |
| PWM    | D(duty) | 1 | 0   | 0 | % | -     | P(pulse) | 9 | 9   | 9   | 9     | u/m | s                | -  | -  | -  |
| WS28   | R/H/H   | 2 | 5   | 5 | - | G/S/S | 2        | 5 | 5   | -   | B/L/V | 2   | 5                | 5  | -  | -  |

all values should have constant length, eg. value 15 should be displayed `015` when 3 characer spaces are availabe

### Rotory encoder with built in switch

- **Clockwise** and **counter clockwise rotation** moves the increases and decreases value respectivaly
- **Short press** switches between parameter **selection** and **edit** mode
- **Long press** unused

### WS2812b leds - one per PWM channel

Each PWM channel has its own WS2812b led which indicates following information for the user:

- Red - Channel is enabled
- Blue - Channel is selected for modification(displayed on the LCD)
- Green - Unused

Colors can be mix, for example channel can be at the same time enabled and selected

## Program structure