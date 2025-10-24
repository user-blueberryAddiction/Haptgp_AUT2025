import smbus2, time, math

I2C_BUS = 1
ADDR = 0x06          # confirm with: i2cdetect -y 1
REG_ANGLE_MSB = 0x03 # datasheet: MSB then LSB
REG_ANGLE_LSB = 0x04

bus = smbus2.SMBus(I2C_BUS)

def read_angle_raw14():
    """Returns 14-bit raw angle (0..16383) or None on error."""
    try:
        data = bus.read_i2c_block_data(ADDR, REG_ANGLE_MSB, 2)
        msb, lsb = data[0], data[1]
        raw14 = ((msb << 6) | (lsb & 0x3F)) & 0x3FFF
        return raw14
    except Exception as e:
        print("I2C error:", e)
        return None

def raw_to_deg(raw14):
    return raw14 * (360.0 / 16384.0)

print("Rotate the magnet slowly through a full turn...")
min_raw, max_raw = 16383, 0
samples = 0

# Optional: press Enter to set current position as zero
zero_raw = None
zero_set = False

start = time.time()
try:
    while True:
        raw = read_angle_raw14()
        if raw is None:
            time.sleep(0.1)
            continue

        # Track span
        min_raw = min(min_raw, raw)
        max_raw = max(max_raw, raw)
        samples += 1

        # Compute angle with optional zeroing
        if zero_raw is None:
            angle = raw_to_deg(raw)
        else:
            # wrap-safe subtraction
            delta = (raw - zero_raw) & 0x3FFF
            angle = raw_to_deg(delta)

        print(f"raw={raw:5d}  angle={angle:7.2f}°  span_raw=[{min_raw},{max_raw}]  span_deg≈{raw_to_deg((max_raw-min_raw)&0x3FFF):.1f}°", end="\r")
        time.sleep(0.05)

        # Simple keyboard zeroing (press Enter once in the terminal)
        if not zero_set and time.time() - start > 1.0:
            import sys, select
            if select.select([sys.stdin], [], [], 0)[0]:
                _ = sys.stdin.readline()
                zero_raw = raw
                zero_set = True
                print("\nZero set to current position.")
except KeyboardInterrupt:
    print("\nDone.")
    print(f"Observed raw span: {min_raw}..{max_raw} (≈ {raw_to_deg((max_raw-min_raw)&0x3FFF):.1f}°)")
