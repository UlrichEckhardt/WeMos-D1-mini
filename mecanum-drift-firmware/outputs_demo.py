import d1mini
import outputs
from utime import sleep_ms
from math import sin, pi
from main import PIN_Q1, PIN_Q2, PIN_Q3, PIN_Q4

def run():
    """demo each quadrant in turn

    This generates two periods of a sine signal (going full speed in either
    direction on each of the four quadrants in turn.
    """
    ctrl = outputs.ServoDriver([PIN_Q1, PIN_Q2, PIN_Q3, PIN_Q4])

    for q in range(4):
        for i in range(200):
            v = [0, 0, 0, 0]
            v[q] = sin(i * pi / 50)
            ctrl.drive(v)
            sleep_ms(20)

run()
