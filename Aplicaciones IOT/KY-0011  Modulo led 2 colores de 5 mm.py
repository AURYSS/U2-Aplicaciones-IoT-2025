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
MQTT_TOPIC = "sensores/led"

MQTT_PORT = 1883

# Configuración de pines
led_rojo_pin = Pin(12, Pin.OUT)  # Pin de salida para el color rojo del LED
led_verde_pin = Pin(13, Pin.OUT)  # Pin de salida para el color verde del LED

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
    client = MQTTClient(MQTT_CLIENT_ID,
    MQTT_BROKER, port=MQTT_PORT,
    user=MQTT_USER,
    password=MQTT_PASSWORD,
    keepalive=0)
    client.connect()
    print("Conectado a %s, en el topico %s"%(MQTT_BROKER, MQTT_TOPIC))
    return client

#Conectar a wifi
conectar_wifi()
#Conectando a un broker mqtt
client = conecta_broker()

#Ciclo infinito
while True:
    # Encender el LED rojo
    led_rojo_pin.value(1)
    led_verde_pin.value(0)

    # Publicar en MQTT
    mensaje = "LED rojo encendido"
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje)
    
    sleep(1)
    
    # Apagar el LED rojo
    led_rojo_pin.value(0)

    # Publicar en MQTT
    mensaje = "LED rojo apagado"
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje)
    
    sleep(1)
    
    # Encender el LED verde
    led_rojo_pin.value(0)
    led_verde_pin.value(1)

    # Publicar en MQTT
    mensaje = "LED verde encendido"
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje)
    
    sleep(1)
    
    # Apagar el LED verde
    led_verde_pin.value(0)

    # Publicar en MQTT
    mensaje = "LED verde apagado"
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje)
    
    sleep(1)