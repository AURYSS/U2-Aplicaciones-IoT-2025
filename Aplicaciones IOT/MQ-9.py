# Importar módulos necesarios
import network
from umqtt.simple import MQTTClient
from machine import Pin, ADC
from time import sleep

# Propiedades MQTT
MQTT_BROKER = "192.168.137.138"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "MQ9_Sensor"
MQTT_TOPIC = "sensores/mq9"

MQTT_PORT = 1883

# Configuración del sensor MQ-9
mq9_ao = ADC(Pin(34))  # Salida analógica (AO)
mq9_ao.atten(ADC.ATTN_11DB)  # Ajustar rango de 0-3.3V

mq9_do = Pin(12, Pin.IN)  # Salida digital (DO/EO)

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

# Función para conectar al broker MQTT
def conecta_broker():
    client = MQTTClient(MQTT_CLIENT_ID,
                        MQTT_BROKER, port=MQTT_PORT,
                        user=MQTT_USER,
                        password=MQTT_PASSWORD,
                        keepalive=0)
    client.connect()
    print("Conectado a %s, en el tópico %s" % (MQTT_BROKER, MQTT_TOPIC))
    return client

# Conectar a WiFi
conectar_wifi()
# Conectar a un broker MQTT
client = conecta_broker()

# Bucle infinito para leer el sensor
while True:
    valor_analogico = mq9_ao.read()  # 0 - 4095
    valor_digital = mq9_do.value()  # 0 o 1

    mensaje = f"MQ-9 | AO: {valor_analogico} | DO: {valor_digital}"
    print(mensaje)
    client.publish(MQTT_TOPIC, mensaje)

    sleep(2)  # Evita saturar MQTT
