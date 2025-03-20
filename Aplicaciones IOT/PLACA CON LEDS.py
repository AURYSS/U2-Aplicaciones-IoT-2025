from machine import Pin
import time

# Configuración de los pines GPIO para los LEDs
led1 = Pin(12, Pin.OUT)
led2 = Pin(27, Pin.OUT)
led3 = Pin(25, Pin.OUT)
led4 = Pin(32, Pin.OUT)
led5 = Pin(13, Pin.OUT)

# Función para apagar todos los LEDs
def apagar_todos():
    led1.value(0)
    led2.value(0)
    led3.value(0)
    led4.value(0)
    led5.value(0)

# Función para encender todos los LEDs
def encender_todos():
    led1.value(1)
    led2.value(1)
    led3.value(1)
    led4.value(1)
    led5.value(1)

# Secuencia 1: Encendido progresivo
def secuencia_progresiva():
    leds = [led1, led2, led3, led4, led5]
    for led in leds:
        led.value(1)
        time.sleep(0.2)
    apagar_todos()

# Secuencia 2: Encendido alternado
def secuencia_alternada():
    leds = [led1, led2, led3, led4, led5]
    for i in range(5):
        leds[i].value(1)
        time.sleep(0.2)
        leds[i].value(0)
    apagar_todos()

# Secuencia 3: Parpadeo simultáneo
def parpadeo_simultaneo():
    for _ in range(5):
        encender_todos()
        time.sleep(0.3)
        apagar_todos()
        time.sleep(0.3)

# Bucle principal para ejecutar las secuencias
while True:
    print("Secuencia: Progresiva")
    secuencia_progresiva()
    time.sleep(1)
    
    print("Secuencia: Alternada")
    secuencia_alternada()
    time.sleep(1)
    
    print("Secuencia: Parpadeo Simultáneo")
    parpadeo_simultaneo()
    time.sleep(1) 