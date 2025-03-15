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
MQTT_TOPIC = "sensores/linea"  # Cambiamos el tópico para reflejar el uso del sensor de línea
MQTT_PORT = 1883

# Configuración del pin para el sensor KY-033
sensor_pin = Pin(12, Pin.IN)  # Pin de entrada para el sensor de línea

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
        keepalive=60  # Aumentamos el keepalive a 60 segundos
    )
    client.connect()
    print("Conectado a %s, en el topico %s" % (MQTT_BROKER, MQTT_TOPIC))
    return client

#Conectar a wifi
conectar_wifi()

#Conectar al broker MQTT
client = None
while client is None:
    try:
        client = conecta_broker()
    except OSError as e:
        print(f"Error al conectar al broker: {e}. Reintentando en 5 segundos...")
        sleep(5)

#Ciclo infinito
while True:
    try:
        # Leer el estado del sensor KY-033
        estado_sensor = sensor_pin.value()  # 0 = línea detectada, 1 = sin línea

        if estado_sensor == 0:
            # Publicar en MQTT: Línea detectada
            mensaje = "Línea detectada"
            print(mensaje)
            client.publish(MQTT_TOPIC, mensaje)
        else:
            # Publicar en MQTT: Sin línea
            mensaje = "Sin línea"
            print(mensaje)
            client.publish(MQTT_TOPIC, mensaje)

        sleep(1)  # Esperar 1 segundo antes de la siguiente lectura

    except OSError as e:
        print(f"Error de conexión MQTT: {e}. Reconectando...")
        client = None
        while client is None:
            try:
                client = conecta_broker()
            except OSError as e:
                print(f"Error al reconectar: {e}. Reintentando en 5 segundos...")
                sleep(5)