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
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "sensor/hall"  # Tópico MQTT para el sensor de efecto Hall
MQTT_PORT = 1883

# Configuración de pines para el sensor KY-035
sensor_ao = ADC(Pin(34))  # Pin ADC para leer la salida analógica (AO)
sensor_ao.atten(ADC.ATTN_11DB)  # Configurar el rango de voltaje de 0 a 3.3V
sensor_do = Pin(12, Pin.IN)  # Pin digital para leer la salida digital (DO)

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
        # Leer el valor analógico del sensor KY-035 (AO)
        valor_analogico = sensor_ao.read()  # Leer el valor analógico (0-4095)

        # Leer el valor digital del sensor KY-035 (DO)
        valor_digital = sensor_do.value()  # 0 = campo magnético detectado, 1 = sin campo magnético

        # Publicar en MQTT: Valores del sensor de efecto Hall
        mensaje_analogico = f"Valor analógico: {valor_analogico}"
        mensaje_digital = f"Valor digital: {'Campo magnético detectado' if valor_digital == 0 else 'Sin campo magnético'}"
        print(mensaje_analogico)
        print(mensaje_digital)
        client.publish(MQTT_TOPIC + "/analogico", mensaje_analogico)
        client.publish(MQTT_TOPIC + "/digital", mensaje_digital)

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