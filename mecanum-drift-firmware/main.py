import d1mini
import inputs
from utime import sleep_ms
import micropython
import machine

# receiver channel 2
PIN_NICK = d1mini.PIN_D3
# receiver channel 4
PIN_ROLL = d1mini.PIN_D1
# receiver channel 1
PIN_YAW = d1mini.PIN_D4

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

def run():
    """main entry point of the firmware"""
    # init inputs
    # The 200ms delay are used to fill the input queue with values before calibration
    dc = inputs.DutyCycle([PIN_ROLL, PIN_NICK, PIN_YAW])
    sleep_ms(200)
    calibrate_inputs(dc)

    while True:
        v_in = dc.value()
        v_scaled = scale_inputs(v_in)
        print(tuple('{:4d}'.format(i) for i in v_in), tuple('{:+1.2f}'.format(i) for i in v_scaled))
        sleep_ms(500)

