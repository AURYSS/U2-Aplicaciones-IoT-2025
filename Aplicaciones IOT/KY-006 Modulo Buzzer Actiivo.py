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
MQTT_TOPIC = "actuadores/buzzer"  # Cambiamos el tópico para reflejar el uso del buzzer

MQTT_PORT = 1883

# Configuración del pin del buzzer (KY-012)
buzzer_pin = Pin(12, Pin.OUT)  # Pin de salida para el buzzer

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
    # Activar el buzzer
    buzzer_pin.value(1)  # Encender el buzzer

    # Publicar en MQTT
    mensaje = f"Buzzer encendido"
    print(mensaje)
    client.publish(MQTT_TOPIC, f"{mensaje}")
    
    sleep(1)  # Mantener el buzzer encendido por 1 segundo
    
    # Desactivar el buzzer
    buzzer_pin.value(0)  # Apagar el buzzer

    # Publicar en MQTT
    mensaje = f"Buzzer apagado"
    print(mensaje)
    client.publish(MQTT_TOPIC, f"{mensaje}")
    
    sleep(1)  # Esperar 1 segundo antes de repetir