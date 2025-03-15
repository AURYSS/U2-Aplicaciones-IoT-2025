#import para acceso a red
import network
#Para usar protocolo MQTT
from umqtt.simple import MQTTClient

#Importamos modulos necesarios
from machine import Pin, PWM
from time import sleep

#Propiedades para conectar a un cliente MQTT
MQTT_BROKER = "192.168.137.138"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "actuador/led2color"
MQTT_PORT = 1883

# Configuración del pin para el LED de 2 colores
led_pin = Pin(12, Pin.OUT)  # Pin de salida para controlar el LED
led_pwm = PWM(led_pin)      # Configurar PWM para control de intensidad

#Función para conectar a WiFi
def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('AURORA', '13082005')
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("\nWiFi Conectada!")

#Funcion para subscribir al broker, topic
def conecta_broker():
    client = MQTTClient(
        MQTT_CLIENT_ID,
        MQTT_BROKER,
        port=MQTT_PORT,
        user=MQTT_USER,
        password=MQTT_PASSWORD,
        keepalive=0
    )
    client.connect()
    print("Conectado a %s, en el topico %s" % (MQTT_BROKER, MQTT_TOPIC))
    return client

#Conectar a wifi
conectar_wifi()

#Conectar al broker MQTT
client = conecta_broker()

#Ciclo infinito
while True:
    # Encender el LED en color rojo (ajusta el valor PWM según sea necesario)
    led_pwm.duty(1023)  # Máxima intensidad para rojo
    mensaje = "LED Rojo encendido"
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje)
    sleep(1)

    # Encender el LED en color verde (ajusta el valor PWM según sea necesario)
    led_pwm.duty(512)  # Intensidad media para verde
    mensaje = "LED Verde encendido"
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje)
    sleep(1)

    # Apagar el LED
    led_pwm.duty(0)  # Intensidad 0 para apagar
    mensaje = "LED Apagado"
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje)
    sleep(1)