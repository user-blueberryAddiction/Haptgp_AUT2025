import time
import board
import busio
import adafruit_veml7700

# Initialisation de la communication I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Création de l'objet capteur
veml7700 = adafruit_veml7700.VEML7700(i2c)

# Optionnel : configuration du gain et du temps d’intégration
# (augmente la sensibilité si la lumière est faible)
veml7700.light_gain = veml7700.ALS_GAIN_1
veml7700.integration_time = veml7700.ALS_IT_100MS

print("=== Lecture du capteur VEML7700 ===")
print("Adresse I2C :", hex(veml7700.i2c_device.device_address))

while True:
    ambient = veml7700.lux          # luminosité ambiante (lux)
    white = veml7700.white          # lumière blanche
    raw = veml7700.light            # valeur brute ALS

    print(f"Ambiant: {ambient:.2f} lux | White: {white} | Raw ALS: {raw}")
    time.sleep(1)