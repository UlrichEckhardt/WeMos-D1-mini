from micropython import const

PIN_D0 = const(16)
PIN_D1 = const(5)
PIN_D2 = const(4)
# Pull Up
PIN_D3 = const(0)
# LED
PIN_D4 = const(2)
PIN_D5 = const(14)
PIN_D6 = const(12)
PIN_D7 = const(13)
# Pull Down
PIN_D8 = const(15)

# wired to USB-to-serial converted
# Using them crashes any serial connection like the REPL prompt!
PIN_TX = const(1)
PIN_RX = const(3)
