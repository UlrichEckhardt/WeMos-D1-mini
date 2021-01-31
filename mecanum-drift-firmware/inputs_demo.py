"""poll inputs in a loop

This just polls some inputs in a loop and outputs the retrieved values. It can
be used to check this part of the code on its own.
"""
import array
import d1mini
import inputs
import math
from utime import sleep_ms
from main import PIN_ROLL, PIN_NICK, PIN_YAW

def run():
    d = inputs.DutyCycle((PIN_ROLL, PIN_NICK, PIN_YAW,))

    while True:
        print(d.value())
        sleep_ms(200)

def analyse(count=100):
    """analyse input quality

    This takes measurements to estimate the signal-to-noise ratio of the inputs.
    Keep the inputs stable during the measurement, if you move the sticks on the
    transmitter, these measurements are meaningless.
    """
    d = inputs.DutyCycle((PIN_ROLL, PIN_NICK, PIN_YAW,))
    sleep_ms(200)

    samples = (array.array('i', (0 for i in range(count))),
               array.array('i', (0 for i in range(count))),
               array.array('i', (0 for i in range(count))),)
    for i in range(count):
        sample = d.value()
        for pin in range(3):
            samples[pin][i] = sample[pin]
        sleep_ms(100)
        if ((i + 1) % 50) == 0:
            print('retrieved {} samples.'.format(i + 1))

    averages = tuple(sum(values) / count for values in samples)
    minima = tuple(min(values) for values in samples)
    maxima = tuple(max(values) for values in samples)
    stddevs = [0, 0, 0]
    for i in range(3):
        values = samples[i]
        average = averages[i]
        dev = sum((sample - average)**2 for sample in values)
        stddevs[i] = math.sqrt(dev / (count -1))
    stddevs = tuple(stddevs)

    print('averages {}'.format(averages))
    print('minima {}'.format(minima))
    print('maxima {}'.format(maxima))
    print('min delta {}'.format(tuple(minima[i] - averages[i] for i in range(3))))
    print('max delta {}'.format(tuple(maxima[i] - averages[i] for i in range(3))))
    print('standard deviations {}'.format(stddevs))

if __name__ == '__main__':
    run()
