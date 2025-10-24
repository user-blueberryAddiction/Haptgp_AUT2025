import time
import board
import neopixel

# === Paramètres à adapter ===
NUM_LEDS = 12          # nombre de LED sur l'anneau
PIXEL_PIN = board.D21  # GPIO21 (PWM)
ORDER = neopixel.GRB   # la plupart des WS2812B = GRB
BRIGHTNESS = 0.2       # 0.0 à 1.0 (0.2 = 20%)

pixels = neopixel.NeoPixel(
    PIXEL_PIN,
    NUM_LEDS,
    brightness=BRIGHTNESS,
    auto_write=False,
    pixel_order=ORDER,
)

def color_wipe(color, delay=0.03):
    for i in range(NUM_LEDS):
        pixels[i] = color
        pixels.show()
        time.sleep(delay)

def theater_chase(color, delay=0.05, cycles=10):
    for j in range(cycles):
        for q in range(3):
            for i in range(0, NUM_LEDS, 3):
                pixels[(i + q) % NUM_LEDS] = color
            pixels.show()
            time.sleep(delay)
            for i in range(0, NUM_LEDS, 3):
                pixels[(i + q) % NUM_LEDS] = (0, 0, 0)

def wheel(pos):
    # 0-255 => arc-en-ciel RGB
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    pos -= 170
    return (0, pos * 3, 255 - pos * 3)

def rainbow_cycle(wait=0.02, cycles=3):
    for j in range(256 * cycles):
        for i in range(NUM_LEDS):
            idx = (i * 256 // NUM_LEDS + j) & 255
            pixels[i] = wheel(idx)
        pixels.show()
        time.sleep(wait)

def solid(color, seconds=2):
    pixels.fill(color)
    pixels.show()
    time.sleep(seconds)

try:
    # Couleurs fixes (R, G, B)
    solid((255, 0, 0), 1.0)   # rouge
    solid((0, 255, 0), 1.0)   # vert
    solid((0, 0, 255), 1.0)   # bleu
    solid((255, 255, 255), 0.5)  # blanc

    # Animations
    color_wipe((255, 120, 0), 0.02)      # orange qui remplit
    theater_chase((0, 255, 50), 0.05, 12)
    rainbow_cycle(0.01, 4)

finally:
    # Éteindre proprement
    pixels.fill((0, 0, 0))
    pixels.show()
