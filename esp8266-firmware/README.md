# Uploading the firmware

```bash
# install esptool (available as esptool.py)
pip install esptool
# clean flash content
esptool.py --port /dev/ttyUSB0 erase_flash
# upload firmware
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 ./esp8266-20200911-v1.13.bin
```


# Filesystem Setup

```bash
# enter REPL prompt
screen /dev/ttyUSB0 115200
# format filesystem
# This will delete boot.py but not brick the board.
>>> import uos
>>> uos.VfsLfs2.mkdir(bdev)
```


# Default boot.py

```python
# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
#import webrepl
#webrepl.start()
gc.collect()
```
