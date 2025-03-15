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
MQTT_TOPIC = "sensores/boton"

MQTT_PORT = 1883

# Configuración de pines
boton_pin = Pin(12, Pin.IN, Pin.PULL_UP)  # Pin de entrada para el botón KY-004

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

# Estado anterior del botón
estado_anterior = boton_pin.value()

#Ciclo infinito
while True:
    # Leer el estado actual del botón
    estado_actual = boton_pin.value()
    
    # Si el estado del botón cambia
    if estado_actual != estado_anterior:
        if estado_actual == 0:  # Botón presionado (KY-004 normalmente es HIGH y LOW cuando se presiona)
            mensaje = "Boton presionado"
        else:
            mensaje = "Boton liberado"
        
        # Publicar en MQTT
        print(mensaje)
        client.publish(MQTT_TOPIC, mensaje)
        
        # Actualizar el estado anterior
        estado_anterior = estado_actual
    
    sleep(0.1)  # Pequeña pausa para evitar rebotes del botón