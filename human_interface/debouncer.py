
from machine import Pin, Timer

class Debouncer:

    def __init__(self, pin: Pin, trigger: int, callback, debounce_time_ms=20):
        self.pin = pin
        self.callback = callback
        self.debounce_time_ms = debounce_time_ms

        self.callback_ready = True

        self.timer = Timer(-1)
        self.pin.irq(trigger=trigger, handler=self._handle_interrupt)

    def _handle_interrupt(self, pin):
        if self.callback_ready:
            self.callback_ready = False
            self.timer.init(mode=Timer.ONE_SHOT, period=self.debounce_time_ms, callback=self._debounce_callback)
            self.callback(pin)

    def _debounce_callback(self, timer):
        self.callback_ready = True