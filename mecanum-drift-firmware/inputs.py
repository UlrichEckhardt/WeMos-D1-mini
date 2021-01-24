from time import ticks_us, ticks_diff
from machine import Pin, disable_irq, enable_irq
from micropython import const
from array import array

# number of samples to average over
_QUEUE_SIZE = const(10)


class _Pin(Pin):
    def __init__(self, pin_nr):
        super().__init__(pin_nr, Pin.IN)
        self.high_state = ticks_us()
        self.samples = array('i', [0] * _QUEUE_SIZE)
        self.idx = 0
        # Note: ESP8266 doesn't support hard IRQs, even though it would improve accuracy here.
        self.irq(trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING, handler=self._handler)

    def _handler(self, pin):
        now = ticks_us()
        if self.value():
            self.high_state = now
        else:
            self.samples[self.idx] = ticks_diff(now, self.high_state)
            self.idx = (1 + self.idx) % _QUEUE_SIZE


class DutyCycle:
    """duty-cycle measurement on GPIO inputs

    Note that this fails when you connect multiple pins to the same signal.
    This causes the handlers for both rising and falling flanks to be triggered
    in parallel, so the timing they produce is skewed. For inputs attached to a
    receiver, this isn't a problem though, because the signals are emitted one
    after the other.
    """

    def __init__(self, pin_nrs):
        """initialize with the GPIO pin number"""
        self._pins = [_Pin(pin_nr) for pin_nr in pin_nrs]

    def value(self):
        """retrieve the duty cycles in microseconds"""
        # copy the values with interrupts disabled
        # TODO: Since these are simple integers, doing so may be overkill and
        # even cause jitters.
        state = disable_irq()
        sampless = [pin.samples[:] for pin in self._pins]
        enable_irq(state)
        return tuple((sum(samples) + _QUEUE_SIZE // 2) // _QUEUE_SIZE for samples in sampless)
