"""poll inputs in a loop

This just polls some inputs in a loop and outputs the retrieved values. It can
be used to check this part of the code on its own.
"""
import d1mini
import inputs
from utime import sleep_ms

# receiver channel 2
PIN_NICK = d1mini.PIN_D3
# receiver channel 4
PIN_ROLL = d1mini.PIN_D1
# receiver channel 1
PIN_YAW = d1mini.PIN_D4
# receiver channel 3
PIN_PITCH = d1mini.PIN_D2

def run():
    d = inputs.DutyCycle([PIN_ROLL, PIN_NICK, PIN_YAW, PIN_PITCH])

    while True:
        print(list(d.value()))
        sleep_ms(200)

run()
