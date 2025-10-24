import time
import board
import busio
import cst816

# Use the Pi's primary I2C bus via Blinka
i2c = busio.I2C(board.SCL, board.SDA)

# If you wired RESET/INT, you can pass them as keyword args in some builds.
# The PyPI lib works with just I2C for polling:
touch = cst816.CST816(i2c)

# Quick ID check
if touch.who_am_i():
    print("CST816 detected.")
else:
    print("CST816 not detected. Try tapping the panel to wake it, then rerun.")

# Stream events
while True:
    # get_point() returns an object with x_point, y_point
    p = touch.get_point()
    g = touch.get_gesture()   # numeric/enum gesture code from the chip
    pressed = touch.get_touch()
    dist = touch.get_distance()  # object with x_dist, y_dist (movement)
    print(f"Pos=({p.x_point},{p.y_point})  Gesture={g}  Pressed={pressed}  Δ=({dist.x_dist},{dist.y_dist})")
    time.sleep(0.05)
