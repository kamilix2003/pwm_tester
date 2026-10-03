
from machine import Pin
from time import ticks_ms
import micropython
micropython.alloc_emergency_exception_buf(200)

from config import PinConfig
from .debouncer import Debouncer

class Encoder:

    _TRANSITIONS = (
         0, -1,  1,  0,
         1,  0,  0, -1,
        -1,  0,  0,  1,
         0,  1, -1,  0
    )

    def __init__(self):
        self.pin_a = Pin(PinConfig.ENCODER_A, Pin.IN, Pin.PULL_UP)
        self.pin_b = Pin(PinConfig.ENCODER_B, Pin.IN, Pin.PULL_UP)
        self.pin_button = Pin(PinConfig.ENCODER_BUTTON, Pin.IN, Pin.PULL_UP)

        self._pin_button_debouncer = Debouncer(self.pin_button, Pin.IRQ_FALLING | Pin.IRQ_RISING, self._button_irq, debounce_time_ms=100)

        self._last_state = (self.pin_a.value() << 1) | self.pin_b.value()
        self.step = 1
        self.value = 0
        self._sub_step = 0

        self.button_pressed = False
        self.button_long_pressed = False

        self._long_press_start_time = None
        self._long_press_threshold_ms = 500  # 1 second for long press

        self.pin_a.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._encoder_irq)
        self.pin_b.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._encoder_irq)

    def set_current_output_instance(self, output_instance):
        self.current_output_instance = output_instance

    def _encoder_irq(self, pin: Pin):
        # Read current pin levels directly
        curr_state = (self.pin_a.value() << 1) | self.pin_b.value()
        
        if curr_state == self._last_state:
            return

        # Combine old state and new state into a 4-bit index
        idx = (self._last_state << 2) | curr_state
        self._last_state = curr_state

        delta = self._TRANSITIONS[idx]
        if delta != 0:
            self._sub_step += delta
            
            # Most standard rotary encoders (like KY-040) have 4 transitions per detent (click)
            if self._sub_step >= 4:
                self._sub_step = 0
                self._update_value(self.step)
            elif self._sub_step <= -4:
                self._sub_step = 0
                self._update_value(-self.step)

    def _update_value(self, delta):
        self.value += delta

    def _button_irq(self, pin: Pin):
        if pin.value() == 0:  # Button pressed
            self._long_press_start_time = ticks_ms()
            self.button_pressed = True
        else:  # Button released
            print(f"Button released. Long press start time: {self._long_press_start_time}")
            if self._long_press_start_time is not None:
                elapsed_time = ticks_ms() - self._long_press_start_time
                if elapsed_time >= self._long_press_threshold_ms:
                    print(f"Long press detected. Elapsed time: {elapsed_time} ms")
                    self.button_long_pressed = True
            self._long_press_start_time = None
        pass