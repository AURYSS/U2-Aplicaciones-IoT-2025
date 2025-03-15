#import para acceso a red
import network
#Para usar protocolo MQTT
from umqtt.simple import MQTTClient

#Importamos modulos necesarios
from machine import Pin, ADC
from time import sleep

#Propiedades para conectar a un cliente MQTT
MQTT_BROKER = "192.168.137.138"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "joystick_client"
MQTT_TOPIC = "actuador/joystick"
MQTT_PORT = 1883

# Configuración de pines para el joystick
joystick_x = ADC(Pin(34))  # Pin ADC para el eje X
joystick_y = ADC(Pin(35))  # Pin ADC para el eje Y
joystick_button = Pin(32, Pin.IN, Pin.PULL_UP)  # Pin digital para el botón

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

#Funcion para conectar al broker MQTT
def conecta_broker():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD, keepalive=60)
    client.connect()
    print("Conectado a %s, en el topico %s" % (MQTT_BROKER, MQTT_TOPIC))
    return client

#Funcion para reconectar en caso de fallo
def reconectar_mqtt():
    print("Reconectando al broker MQTT...")
    try:
        client = conecta_broker()
        return client
    except Exception as e:
        print("Error al reconectar:", e)
        return None

#Conectar a wifi
conectar_wifi()

#Conectar al broker MQTT
client = conecta_broker()

#Ciclo infinito
while True:
    try:
        # Leer los valores del joystick
        x_value = joystick_x.read()
        y_value = joystick_y.read()
        button_state = joystick_button.value()

        # Publicar en MQTT
        mensaje = f"Joystick - X: {x_value}, Y: {y_value}, Botón: {'Presionado' if button_state == 0 else 'presionado'}"
        print(mensaje)
        client.publish(MQTT_TOPIC, mensaje)
        
        sleep(1)  # Esperar 1 segundo antes de la siguiente lectura

    except OSError as e:
        print("Error de conexión MQTT:", e)
        client = reconectar_mqtt()  # Intentar reconectar
        if client is None:
            print("No se pudo reconectar. Reintentando en 5 segundos...")
            sleep(5)