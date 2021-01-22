import d1mini

from time import ticks_us, ticks_diff
from machine import Pin, disable_irq, enable_irq
from micropython import const
from array import array

# number of samples to average over
_QUEUE_SIZE = const(10)

class DutyCycle:
    """duty-cycle measurement on GPIO inputs"""

    def __init__(self, pin_nr):
        """initialize with the GPIO pin number"""
        self.high_state = ticks_us()
        self.samples = array('i', [0] * _QUEUE_SIZE)
        self.idx = 0
        pin = Pin(pin_nr, Pin.IN)
        pin.irq(trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING, handler=self._handler)

    def value(self):
        """retrieve the duty cycle in microseconds"""
        state = disable_irq()
        samples = self.samples[:]
        enable_irq(state)
        return (sum(samples) + _QUEUE_SIZE // 2) // _QUEUE_SIZE

    def _handler(self, pin):
        now = ticks_us()
        if pin.value():
            self.high_state = now
        else:
            self.samples[self.idx] = ticks_diff(self.high_state, now)
            self.idx = (1 + self.idx) % _QUEUE_SIZE
