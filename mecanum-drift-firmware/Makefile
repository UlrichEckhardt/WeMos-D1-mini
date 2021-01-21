# ensure `ampy` usability
# For an introduction to `ampy`, see:
# https://techtutorialsx.com/2017/06/04/esp32-esp8266-micropython-uploading-files-to-the-file-system/
ampy-setup-check:
	@ampy > /dev/null || echo "you need to install ampy (pip install adafruit-ampy)"
	@test -n "${DEVICE}" || echo "you have to set DEVICE to the target device for upload"
.PHONY: ampy-setup-check

# upload the firmware to the D1
upload: ampy-setup-check
	ampy --port "${DEVICE}" put d1mini.py
	ampy --port "${DEVICE}" put inputs.py
.PHONY: upload

# start the firmware on the D1
run-firmware: upload
	ampy run --port "${DEVICE}" main.py
.PHONY: run-firmware
