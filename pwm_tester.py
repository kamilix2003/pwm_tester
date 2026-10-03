
from output_supervisor import OutputSupervisor

from human_interface.lcd_driver import LCDDriver
from human_interface.encoder_driver import Encoder

from machine import Pin, Timer

import os
import sys

class PWMTester:

    modes = ["selection", "edit"]

    def __init__(self):
        self.output_supervisor = OutputSupervisor()

        self.lcd_driver = LCDDriver()
        self.lcd_driver.current_output_instance = self.output_supervisor.current_output

        self.encoder = Encoder()

        self.mode = "selection"

        self.channel_selection = False

        self.led_pin = Pin(25, Pin.OUT)
        self.heartbeat_timer = Timer(-1, mode=Timer.PERIODIC, freq=1, callback=lambda t: self.led_pin.toggle())


    def setup(self):
        
        pass

    def loop(self):

        if self.encoder.button_long_pressed:
            self.output_supervisor.set_current_output_by_id((self.output_supervisor.get_current_output_id() + 1) % len(self.output_supervisor.outputs))
            self.lcd_driver.current_output_instance = self.output_supervisor.current_output
            self.encoder.button_long_pressed = False

        if self.encoder.button_pressed:
            self.encoder.button_pressed = False
            if self.mode == "selection":
                self.mode = "edit"
                self.lcd_driver.cursor_blink = True
            elif self.mode == "edit":
                self.mode = "selection"
                self.lcd_driver.cursor_blink = False

        if self.encoder.value != 0:
            try: 
                if self.mode == "selection":
                    self.output_supervisor.current_output.increment_menu_index(self.encoder.value)
                elif self.mode == "edit":
                    self.output_supervisor.current_output.get_current_callback()(self.encoder.value)
                else:
                    print(f"Unknown mode: {self.mode}")
            except Exception as e:
                print(f"Error occurred while calling callback: {e}")
            self.encoder.value = 0

        pass