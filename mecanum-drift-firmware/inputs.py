import d1mini

from time import ticks_us, ticks_diff
from machine import Pin, disable_irq, enable_irq

class DutyCycle:
    """duty-cycle measurement on GPIO inputs"""

    def __init__(self, pin_nr):
        """initialize with the GPIO pin number"""
        self.high_state = ticks_us()
        self.diff = ticks_diff(self.high_state, self.high_state)
        pin = Pin(pin_nr, Pin.IN)
        pin.irq(trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING, handler=self._handler)

    def value(self):
        """retrieve the duty cycle in microseconds"""
        state = disable_irq()
        res = self.diff
        enable_irq(state)
        return res

    def _handler(self, pin):
        now = ticks_us()
        if pin.value():
            self.high_state = now
        else:
            self.diff = ticks_diff(self.high_state, now)
