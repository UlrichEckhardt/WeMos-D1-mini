from inputs import DutyCycle
from utime import sleep_ms
from ujson import dump, load
import micropython
import machine
_FILENAME = 'calibration.json'

def calibrate_inputs(input_pins):
    """interactively retrieve input value ranges"""
    # set the CPU frequency to 160 MHz and increase optimization level
    # This greatly improves the accuracy of the inputs.
    machine.freq(160000000)
    micropython.opt_level(3)

    # init inputs
    # The 200ms delay are used to fill the input queue with values before calibration
    dc = DutyCycle(input_pins)
    sleep_ms(200)

    print('Move inputs to min and max positions!')
    minima = maxima = dc.value()
    count = len(minima)
    for i in range(200):
        sleep_ms(50)
        value = dc.value()
        minima = tuple(min(minima[i], value[i]) for i in range(count))
        maxima = tuple(max(maxima[i], value[i]) for i in range(count))
    print('minima:', tuple('{:4d}'.format(i) for i in minima))
    print('maxima:', tuple('{:4d}'.format(i) for i in maxima))

    res = []
    for i, pin in enumerate(input_pins):
        res.append({"pin": pin,
                    "minimum": minima[i],
                    "maximum": maxima[i]})
    return res

def store_calibration(ranges):
    """store calibration values for inputs"""
    with open(_FILENAME, 'w') as f:
        dump(ranges, f)
        f.write('\n')

def load_calibration():
    """load calibration values for inputs"""
    with open(_FILENAME, 'r') as f:
        return load(f)

def get_transformation(input_pins):
    """load calibration data and return a transformation function between input and internal (-1 ... +1) range"""
    factors = dict()
    for cal in load_calibration():
        index = input_pins.index(cal['pin'])
        maximum = cal['maximum']
        minimum = cal['minimum']
        delta = maximum - minimum
        factors[index] = ((-minimum-maximum) / delta,
                          2 / delta,)

    def transform(inputs):
        return tuple(min(1, max(-1, factors[i][0] + factors[i][1] * value)) for i, value in enumerate(inputs))
    return transform
