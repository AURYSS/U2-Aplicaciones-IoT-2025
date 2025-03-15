#import para acceso a red
import network
#Para usar protocolo MQTT
from umqtt.simple import MQTTClient

#Importamos modulos necesarios
from machine import Pin
from time import sleep

#Propiedades para conectar a un cliente MQTT
MQTT_BROKER = "192.168.137.138"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "sensores/pulso"

MQTT_PORT = 1883

# Configuración del pin del sensor KY-004
pulso_pin = Pin(12, Pin.IN, Pin.PULL_UP)  # Pin de entrada con pull-up interno

#Función para conectar a WiFi
def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('AURORA', '13082005')
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("\nWiFi Conectada!")

#Función para conectar al broker MQTT
def conecta_broker():
    client = MQTTClient(MQTT_CLIENT_ID,
                        MQTT_BROKER, port=MQTT_PORT,
                        user=MQTT_USER,
                        password=MQTT_PASSWORD,
                        keepalive=0)
    client.connect()
    print("Conectado a %s, en el tópico %s" % (MQTT_BROKER, MQTT_TOPIC))
    return client

#Conectar a wifi
conectar_wifi()
#Conectando a un broker mqtt
client = conecta_broker()

#Ciclo infinito para leer el sensor
while True:
    estado = pulso_pin.value()  # Lee el estado del botón (0 = presionado, 1 = no presionado)

    if estado == 0:
        mensaje = "Pulso detectado"
        print(mensaje)
        client.publish(MQTT_TOPIC, mensaje)

    sleep(0.1)  # Pequeño retraso para evitar rebotes
