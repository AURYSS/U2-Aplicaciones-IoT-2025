# Importar módulos necesarios
import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep

# Propiedades MQTT
MQTT_BROKER = "192.168.137.138"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "sensores/boton"
MQTT_PORT = 1883

# Configuración del Foto Interruptor (KY-004) como entrada con pull-up
boton = Pin(12, Pin.IN, Pin.PULL_UP)  

# Función para conectar a WiFi
def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('AURORA', '13082005')
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("\nWiFi Conectada!")

# Función para conectar al broker MQTT con manejo de errores
def conecta_broker():
    while True:
        try:
            client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,
                                user=MQTT_USER, password=MQTT_PASSWORD, keepalive=30)
            client.connect()
            print("Conectado a %s, en el tópico %s" % (MQTT_BROKER, MQTT_TOPIC))
            return client
        except OSError:
            print("Error de conexión MQTT, reintentando...")
            sleep(5)

# Conectar a WiFi
conectar_wifi()
# Conectar a MQTT
client = conecta_broker()

# Estado anterior del botón
estado_anterior = boton.value()

# Ciclo infinito para monitorear el botón
while True:
    estado_actual = boton.value()

    # Detectar cambio de estado (presionado o liberado)
    if estado_actual != estado_anterior:
        mensaje = "Botón presionado" if estado_actual == 0 else "Botón liberado"
        print(mensaje)

        try:
            client.publish(MQTT_TOPIC, mensaje)
        except OSError:
            print("Error al publicar, reconectando...")
            client = conecta_broker()

        estado_anterior = estado_actual  # Actualizar estado

    sleep(0.1)  # Evita rebotes del botón
