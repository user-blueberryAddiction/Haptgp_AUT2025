import time
import board
import busio
import adafruit_drv2605

# Use board.I2C() on most CircuitPython boards.
# On Raspberry Pi with Blinka, this also works if I2C is enabled.
i2c = busio.I2C(board.SCL, board.SDA)

drv = adafruit_drv2605.DRV2605(i2c)  # defaults to address 0x5A

# Choose your motor type:
# For eccentric rotating mass (ERM) motors (most coin/cylinder vibes):
drv.use_ERM()
# For LRA actuators (linear resonant), use:
# drv.use_LRM()

# Optionally select effect library (default is TS2200A)
# drv.library = adafruit_drv2605.LIBRARY_TS2200A

# Play a few sample effects by ID (0..123 are valid)
for effect_id in (1, 47, 83, 118):  # strong click, ramp, etc.
    drv.sequence[0] = adafruit_drv2605.Effect(effect_id)
    # clear remaining slots (optional)
    for slot in range(1, 8):
        drv.sequence[slot] = adafruit_drv2605.Effect(0)
    drv.play()
    time.sleep(0.6)
    drv.stop()
    time.sleep(0.25)

print("Done.")
