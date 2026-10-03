
from human_interface.lcd_driver import Timer
from outputs.pwm_driver import PWMDriver, Pin

from neopixel import NeoPixel

from config import PinConfig
    
class OutputSupervisor:

    def __init__(self):

        self.outputs = [ PWMDriver(pin_num=pin, id=i) for i, pin in enumerate(PinConfig.PWM_OUTPUT_PINS) ]
        self.current_output: PWMDriver | None = self.outputs[0]

        self.neopixel = NeoPixel(Pin(PinConfig.WS2812_DATA_PIN), 4)
        self.neopixel_timer = Timer(-1, mode=Timer.PERIODIC, freq=10, callback=lambda t: self._ws_update())
        self.current_output_blink_timer = Timer(-1, mode=Timer.PERIODIC, freq=2, callback=lambda t: self._ws_blink())

    def get_output_by_id(self, output_id: int) -> PWMDriver | None:
        for output in self.outputs:
            if output.id == output_id:
                return output
        return None

    def get_current_output_id(self) -> int | None:
        if self.current_output is not None:
            return self.current_output.id
        return None

    def set_current_output_by_id(self, output_id: int):
        output = self.get_output_by_id(output_id)
        if output is not None:
            self.current_output = output
        else:
            raise ValueError(f"No output found with ID {output_id}")

    def _update_single_led_color(self, neopixel, index, r=None, g=None, b=None):
        current_color = neopixel[index]
        new_color = (
            r if r is not None else current_color[0],
            g if g is not None else current_color[1],
            b if b is not None else current_color[2]
        )
        neopixel[index] = new_color

    def _ws_update(self):
        for i, output in enumerate(self.outputs):
            self._update_single_led_color(self.neopixel, i, r=100 if output.pwm.duty_u16() > 0 else 0)
            if output is not self.current_output:
                self._update_single_led_color(self.neopixel, i, g=0)
        self.neopixel.write()
        pass

    def _ws_blink(self):
        if self.current_output is not None:
            self._update_single_led_color(self.neopixel, self.current_output.id, g=100 if self.neopixel[self.current_output.id][1] == 0 else 0)