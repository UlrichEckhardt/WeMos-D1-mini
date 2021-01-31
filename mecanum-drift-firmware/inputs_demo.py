"""poll inputs in a loop

This just polls some inputs in a loop and outputs the retrieved values. It can
be used to check this part of the code on its own.
"""
import d1mini
import inputs
from utime import sleep_ms
from main import PIN_ROLL, PIN_NICK, PIN_YAW

def run():
    d = inputs.DutyCycle((PIN_ROLL, PIN_NICK, PIN_YAW,))

    while True:
        print(d.value())
        sleep_ms(200)

run()
