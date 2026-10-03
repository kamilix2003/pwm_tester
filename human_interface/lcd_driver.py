
from machine import Pin, I2C, Timer
from config import LcdConfig, PinConfig
from .lcd import LCD

from outputs.pwm_driver import PWMDriver

class LCDDriver:

    def __init__(self):

        self.i2c = I2C(
            0,
            scl=Pin(PinConfig.LCD_SCL_PIN, mode=Pin.OPEN_DRAIN),
            sda=Pin(PinConfig.LCD_SDA_PIN, mode=Pin.OPEN_DRAIN),
            freq=1_000_000,
        )
        self.lcd = LCD(
            self.i2c,
            # addr=LcdConfig.I2C_ADDRESS,
            rows=LcdConfig.ROWS,
            cols=LcdConfig.COLS,
            backlight=LcdConfig.BACKLIGHT_ON,
        )

        self.refresh_timer = Timer(-1, mode=Timer.PERIODIC, freq=30, callback=self._refresh_callback)

        self.current_output_instance: PWMDriver | None = None

        self.current_lines = ("", "")
        self.cursor_position = (0, 0)
        self.cursor_blink = False

    def _refresh_callback(self, timer):
        if self.current_output_instance is None:
            line1, line2 = "No Output", ""
        else:
            line1, line2 = self.current_output_instance.get_lcd_lines()
            cursor_x, cursor_y = self.current_output_instance.get_lcd_cursor_position()
            self.lcd.set_cursor(cursor_x, cursor_y)
            self.lcd.show_cursor(self.cursor_blink)
        if (line1, line2) != self.current_lines:
            self.current_lines = (line1, line2)
            self.cursor_position = (cursor_x, cursor_y)
            self.lcd.clear()
            self.lcd.home()
            self.lcd.write(line1)
            self.lcd.set_cursor(0, 1)
            self.lcd.write(line2)