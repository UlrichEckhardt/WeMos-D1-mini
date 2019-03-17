https://wiki.wemos.cc/products:retired:d1_mini_v3.0.0
https://wiki.wemos.cc/products:d1:d1_mini

# connecting to the D1

    screen /dev/ttyUSB0 115200
    # hit Control-D for a soft reset
    # hit Control-E for paste mode


# setting up the virtual environment for the simulation

    . env/bin/activate.fish


# TODO

 * Calibrate light intensity. What is the perceived illumination comparing
   all LEDs at 50% to only half of them at 100%?


Pins:

D0: 16
D1: 5
D2: 4
D3: 0 Pull Up   
D4: 2 LED
D5: 14
D6: 12
D7: 13
D8: 15 Pull Down

