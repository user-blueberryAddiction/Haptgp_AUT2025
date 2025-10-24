import time
import board
import busio
import adafruit_ds3231

i2c = busio.I2C(board.SCL, board.SDA)
rtc = adafruit_ds3231.DS3231(i2c)

# Prend l’heure actuelle du système et l’écrit dans le DS3231
rtc.datetime = time.localtime()

print("L'heure locale de Montréal a été enregistrée dans le DS3231 :")
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
