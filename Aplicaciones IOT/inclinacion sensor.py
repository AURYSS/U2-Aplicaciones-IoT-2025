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
MQTT_TOPIC = "sensores/inclinacion"  # Tópico para el KY-020

MQTT_PORT = 1883

# Configuración del pin del sensor de inclinación (KY-020)
inclinacion_pin = Pin(12, Pin.IN, Pin.PULL_UP)  # Habilitar resistencia pull-up interna

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
    # Leer el estado del sensor de inclinación
    estado = inclinacion_pin.value()  # 0 si está inclinado, 1 si no está inclinado

    # Publicar en MQTT
    if estado == 0:  # Si el valor es 0, está inclinado
        mensaje = "Sensor inclinado"
    else:  # Si el valor es 1, no está inclinado
        mensaje = "Sensor no inclinado"
    
    print(mensaje)
    client.publish(MQTT_TOPIC, f"{mensaje}")
    
    sleep(1)  # Esperar 1 segundo antes de repetir