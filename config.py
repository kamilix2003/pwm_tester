
class PinConfig:
    
    PWM_OUTPUT_PINS = [12, 13, 10, 11] 

    ENCODER_A = 7
    ENCODER_B = 8
    ENCODER_BUTTON = 9

    WS2812_DATA_PIN = 6

    LCD_SDA_PIN = 4
    LCD_SCL_PIN = 5


class LcdConfig:
    I2C_ADDRESS = None  # Set to None to auto-detect
    BACKLIGHT_ON = True

    ROWS = 2
    COLS = 16