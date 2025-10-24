import RPi.GPIO as GPIO
import time

BUZZER_PIN = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

pwm = GPIO.PWM(BUZZER_PIN, 440)
pwm.start(50)

# --- Définition de toutes les notes nécessaires ---
E4 = 330
F4 = 349
G4 = 392
A4 = 440
B4 = 494
C5 = 523
D5 = 587
E5 = 659
F5 = 698
G5 = 784
A5 = 880
B5 = 988
C6 = 1047

# ---- Super Mario Bros (version abrégée ~15 s) ----
melody = [
    E5,E5,0,E5,0,C5,E5,0,G5,0,0,0,G4,0,0,0,
    C5,0,0,G4,0,E4,0,A4,0,B4,0,A4,0,G4,E5,G5,A5,
    F5,G5,0,E5,0,C5,D5,B4,0,0,0
]
durations = [
    0.12,0.12,0.12,0.12,0.12,0.12,0.12,0.12,0.25,0.12,0.12,0.12,0.25,0.12,0.12,0.12,
    0.25,0.12,0.12,0.12,0.25,0.12,0.12,0.12,0.25,0.12,0.12,0.12,0.25,0.12,0.12,0.12,
    0.25,0.25,0.25,0.12,0.12,0.12,0.25,0.12,0.12,0.12
]

print("🎵 Lecture du thème Mario (15 s)")

for note, dur in zip(melody, durations):
    if note == 0:
        pwm.ChangeDutyCycle(0)  # silence
    else:
        pwm.ChangeFrequency(note)
        pwm.ChangeDutyCycle(50)
    time.sleep(dur)

pwm.stop()
GPIO.cleanup()
print("✅ Terminé !")
