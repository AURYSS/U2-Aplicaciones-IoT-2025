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
MQTT_TOPIC = "sensores/buzzer"  # Cambiamos el tópico para reflejar el uso del buzzer

MQTT_PORT = 1883

# Configuración del pin del buzzer pasivo (KY-012)
buzzer_pin = Pin(12, Pin.OUT)  # Pin de salida para el buzzer
buzzer_pwm = PWM(buzzer_pin)    # Configuramos el pin como PWM

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

#Función para generar un tono en el buzzer
def generar_tono(frecuencia, duracion):
    buzzer_pwm.freq(frecuencia)  # Establecer la frecuencia del tono
    buzzer_pwm.duty(512)         # Establecer el ciclo de trabajo (50%)
    sleep(duracion)              # Mantener el tono durante la duración especificada
    buzzer_pwm.duty(0)           # Apagar el buzzer

#Ciclo infinito
while True:
    # Generar un tono de 1000 Hz durante 1 segundo
    generar_tono(1000, 1)  # Frecuencia: 1000 Hz, Duración: 1 segundo

    # Publicar en MQTT
    mensaje = f"Buzzer activado (1000 Hz)"
    print(mensaje)
    client.publish(MQTT_TOPIC, f"{mensaje}")
    
    sleep(1)  # Esperar 1 segundo antes de repetir