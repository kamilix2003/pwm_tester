from machine import I2C, Pin
from time import sleep_ms

class LCD:
    """Easy-to-use LCD I2C driver for MicroPython (Pico, ESP32, ESP8266, etc.)."""

    def __init__(self, i2c: I2C, addr = None, rows: int = 2, cols: int = 16, backlight: bool = True):
        self.i2c = i2c
        self.rows = rows
        self.cols = cols
        self._backlight = 0x08 if backlight else 0x00
        self._state = 0x00

        # If no address is provided, auto-detect the first I2C device
        if addr is None:
            devices = self.i2c.scan()
            if not devices:
                raise RuntimeError("No I2C devices found. Check wiring!")
            self.addr = devices[0]  # pick the first device
            print(f"Auto-detected I2C LCD at address 0x{self.addr:02X}")
        else:
            self.addr = addr

        self._init_lcd()

    # ------------------ Public API ------------------

    def clear(self):
        """Clear the display."""
        self._cmd(0x01, delay=3)

    def home(self):
        """Return cursor to home position."""
        self._cmd(0x02, delay=3)

    def show_cursor(self, blink=False):
        """Show the cursor (optionally blinking)."""
        mode = 0x0E if not blink else 0x0F
        self._cmd(mode)

    def hide_cursor(self):
        """Hide the cursor."""
        self._cmd(0x0C)

    def backlight(self, on=True):
        """Turn backlight on or off."""
        self._backlight = 0x08 if on else 0x00
        self._write(self._state)

    def set_cursor(self, col=0, row=0):
        """Move cursor to column and row."""
        row_offsets = [0x00, 0x40, 0x14, 0x54]
        self._cmd(0x80 | (col + row_offsets[row]))

    def write(self, text: str, col=None, row=None):
        """Write text (optionally at a specific position)."""
        if col is not None and row is not None:
            self.set_cursor(col, row)
        for ch in text:
            self._data(ord(ch))

    def custom_char(self, index, bitmap):
        """Define a custom character (0–7)."""
        self._cmd(0x40 | (index << 3))
        for line in bitmap[:8]:
            self._data(line)

    def draw_custom(self, index):
        """Print a previously defined custom char."""
        self._data(index)

    # ------------------ Internal ------------------

    def _init_lcd(self):
        sleep_ms(20)
        for _ in range(3):
            self._init_nibble(0x30)
            sleep_ms(5)
        self._init_nibble(0x20)  
        self._cmd(0x28)          
        self._cmd(0x0C)          
        self.clear()

    def _cmd(self, cmd, delay=1):
        self._send(cmd, 0)
        if delay:
            sleep_ms(delay)

    def _data(self, data):
        self._send(data, 1)

    def _send(self, val, rs):
        self._write((val & 0xF0) | rs)
        self._write(((val << 4) & 0xF0) | rs)

    def _write(self, data):
        self.i2c.writeto(self.addr, bytes([data | self._backlight]))
        self._pulse(data)

    def _pulse(self, data):
        self.i2c.writeto(self.addr, bytes([data | 0x04 | self._backlight]))
        self.i2c.writeto(self.addr, bytes([(data & ~0x04) | self._backlight]))

    def _init_nibble(self, nibble):
        data = nibble & 0xF0
        self.i2c.writeto(self.addr, bytes([data | self._backlight]))
        self._pulse(data)
