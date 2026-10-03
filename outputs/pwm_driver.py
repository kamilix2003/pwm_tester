
from machine import Pin, PWM

class PWMDriver:

    Min_frequency = 1
    Max_frequency = 1_000
    Default_frequency = 50

    Default_pulse_duration_ms = 1

    Max_duty_u16 = 65_535


    def __init__(self, pin_num: int, id: int = 0):

        self.pin_num = pin_num
        self.pin = Pin(self.pin_num, Pin.OUT)
        self.id = id

        self.current_menu_idx = 0
        
        self.pwm = PWM(self.pin)
        self.pwm.freq(self.Default_frequency)
        self.pwm.duty_u16(0)  # Start with 0% duty cycle

        self.menu_list = [
            {
                "cursor_loc": (9, 0),
                "callback": lambda value: self.frequency(self.pwm.freq() + (value * 100)),
            },
            {
                "cursor_loc": (10, 0),
                "callback": lambda value: self.frequency(self.pwm.freq() + (value * 10)),
            },
            {
                "cursor_loc": (11, 0),
                "callback": lambda value: self.frequency(self.pwm.freq() + value),
            },
            {
                "cursor_loc": (2, 1),
                "callback": lambda value: self.set_duty_cycle(self.get_duty_cycle() + (value * 10)),
            },
            {
                "cursor_loc": (3, 1),
                "callback": lambda value: self.set_duty_cycle(self.get_duty_cycle() + value),
            },
            {
                "cursor_loc": (7, 1),
                "callback": lambda value: self.set_pulse_duration(self.get_pulse_duration() + (value * 10000)),
            },
            {
                "cursor_loc": (8, 1),
                "callback": lambda value: self.set_pulse_duration(self.get_pulse_duration() + (value * 1000)),
            },
            {
                "cursor_loc": (9, 1),
                "callback": lambda value: self.set_pulse_duration(self.get_pulse_duration() + (value * 100)),
            },
            {
                "cursor_loc": (10, 1),
                "callback": lambda value: self.set_pulse_duration(self.get_pulse_duration() + (value * 10)),
            },
            {
                "cursor_loc": (11, 1),
                "callback": lambda value: self.set_pulse_duration(self.get_pulse_duration() + value),
            },
        ]

    def get_current_callback(self):
        return self.menu_list[self.current_menu_idx].get("callback")

    def get_lcd_cursor_position(self):
        return self.menu_list[self.current_menu_idx].get("cursor_loc")

    def increment_menu_index(self, increment: int = 1):
        self.current_menu_idx = (self.current_menu_idx + increment) % len(self.menu_list)

    def frequency(self, frequency: int):
        if frequency < self.Min_frequency or frequency > self.Max_frequency:
            raise ValueError(f"Frequency must be between {self.Min_frequency} and {self.Max_frequency} Hz, got {frequency} Hz")
        self.pwm.freq(frequency)

    def __set_duty_cycle_raw(self, duty_u16: int):
        if duty_u16 < 0 or duty_u16 > self.Max_duty_u16:
            raise ValueError(f"Duty cycle must be between 0 and {self.Max_duty_u16} (u16)")
        self.pwm.duty_u16(duty_u16)

    def set_duty_cycle(self, duty_cycle: float):
        if duty_cycle < 0.0 or duty_cycle > 100.0:
            if duty_cycle < 0.0 and self.get_duty_cycle() <= 1.0:
                self.pwm.duty_u16(0)  # Set duty cycle to 0% for negative pulse duration
            raise ValueError("Duty cycle must be between 0.0 and 100.0 percent")
        
        duty_u16 = int((duty_cycle / 100.0) * self.Max_duty_u16)
        self.__set_duty_cycle_raw(duty_u16)

    def get_duty_cycle(self) -> float:
        duty_u16 = self.pwm.duty_u16()
        return (duty_u16 / self.Max_duty_u16) * 100.0

    def set_pulse_duration(self, pulse_duration_us: int):
        if pulse_duration_us < 0:
            if self.get_pulse_duration() <= 1:
                self.pwm.duty_u16(0)  # Set duty cycle to 0% for negative pulse duration
            raise ValueError("Pulse duration must be a positive integer (microseconds)")
        
        self.pwm.duty_ns(pulse_duration_us * 1_000)  # Convert microseconds to nanoseconds

    def get_pulse_duration(self) -> int:
        duty_ns = self.pwm.duty_ns()
        return duty_ns // 1_000  # Convert nanoseconds to microseconds

    def get_lcd_lines(self) -> tuple[str, str]:
        line1 = f"CH{self.id} {'ON ' if self.pwm.duty_u16() > 0 else 'OFF'} F{self.pwm.freq():03}Hz"
        line2 = f"D{int(self.get_duty_cycle()):03}% P{self.get_pulse_duration():05}us"
        return (line1, line2)

    def __str__(self) -> str:
        out1, out2 = self.get_lcd_lines()
        return f"{out1}\n{out2}"
        