import d1mini
import inputs
from utime import sleep_ms
import micropython
import machine
import math
from mecanum import MecanumDrive

# receiver channel 2
PIN_NICK = d1mini.PIN_D3
# receiver channel 4
PIN_ROLL = d1mini.PIN_D1
# receiver channel 1
PIN_YAW = d1mini.PIN_D4

# pin connected to the start button that enables the firmware
PIN_START = d1mini.PIN_D0

# set the CPU frequency to 160 MHz and increase optimization level
# This greatly improves the accuracy of the inputs.
machine.freq(160000000)
micropython.opt_level(3)

# minimum and maximum values from inputs received during calibration
_minima = None
_maxima = None

def scale_inputs(values):
    """scale external ranges from the receiver to internal ones"""
    count = len(values)
    return tuple(2 * ((value - _minima[i]) / (_maxima[i] - _minima[i])) - 1 for i, value in enumerate(values))

def calibrate_inputs(inputs):
    """interactively retrieve input value ranges"""
    print('Move inputs to min and max positions!')
    minima = maxima = inputs.value()
    count = len(minima)
    for i in range(100):
        sleep_ms(50)
        value = inputs.value()
        minima = tuple(min(minima[i], value[i]) for i in range(count))
        maxima = tuple(max(maxima[i], value[i]) for i in range(count))
    print('minima:', tuple('{:4d}'.format(i) for i in minima))
    print('maxima:', tuple('{:4d}'.format(i) for i in maxima))
    global _minima, _maxima
    _minima, _maxima = minima, maxima

def filter_inputs(values):
    """transform input values

    The resulting output is a vector of a length not greater than one. The code
    uses the absolute value of the three components to determine the lenght of
    the resulting vector (L-∞ norm), clamped to a maximum of one.
    """
    # compute L-∞ norm
    norm = max(abs(r) for r in values)
    if norm <= 0.001:
        # avoid divisions by zero-like values
        return (0, 0, 0)
    # compute L-1 norm, which limits the valid result vectors
    length = sum(abs(x) for x in values)
    # compute scale factor
    scale = min(norm, 1) / length
    # scale inputs
    return tuple(r * scale for r in values)

def run():
    """main entry point of the firmware"""
    # init inputs
    # The 200ms delay are used to fill the input queue with values before calibration
    dc = inputs.DutyCycle([PIN_ROLL, PIN_NICK, PIN_YAW])
    sleep_ms(200)
    calibrate_inputs(dc)

    md = MecanumDrive()
    while True:
        v_in = dc.value()
        v_scaled = scale_inputs(v_in)
        v_filtered = filter_inputs(v_scaled)
        v_move = md.move(*v_filtered)
        print(tuple('{:+1.2f}'.format(i) for i in v_scaled),
              tuple('{:+1.2f}'.format(i) for i in v_filtered),
              tuple('{:+1.2f}'.format(i) for i in v_move))
        sleep_ms(500)

if __name__ == '__main__':
    print('Push button to start or control-C to abort.')
    wait = machine.Pin(PIN_START, machine.Pin.IN)
    while True:
        if wait():
            break
        sleep_ms(300)
        print('.')
    run()
