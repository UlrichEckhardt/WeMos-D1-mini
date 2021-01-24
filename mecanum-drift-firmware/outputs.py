from machine import Pin, PWM
from micropython import const

# scale value
# Valid PWM duty cycles range from zero to this value.
_SCALE = const(1023)
# Hertz
_FREQUENCY = const(50)
# Period in ms
_PERIOD = const(1000 // _FREQUENCY)
# 1ms
_MIN = const(_SCALE * 1 // _PERIOD)
# 2ms
_MAX = const(_SCALE * 2 // _PERIOD)
# 1.5ms
_NEUTRAL = const((_MAX + _MIN) // 2)

class ServoDriver:
    """servo controller

    This drives servo signals on a set of output pins.
    """

    def __init__(self, pin_nrs):
        self.pwms = []
        for pin_nr in pin_nrs:
            pin = Pin(pin_nr, Pin.OUT)
            pwm = PWM(pin,
                      freq=_FREQUENCY,
                      duty=_NEUTRAL)
            self.pwms.append(pwm)

    def drive(self, values):
        if len(values) != len(self.pwms):
            raise Exception('need exactly {} value'.format(len(self.pwms)))

        for value in values:
            if value < -1 or value > 1:
                raise Exception('value {} out of range [-1 .. +1]'.format(value))

        for i, value in enumerate(values):
            d = ((_MIN + _MAX) + value * (_MAX - _MIN)) / 2
            self.pwms[i].duty(int(d + 0.5))
