import network
from umqtt.simple import MQTTClient
from machine import ADC, Pin
from time import sleep
import json

# Propiedades para conectar a un cliente MQTT
MQTT_BROKER = "192.168.137.138"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "esp32_sensor_mq135"
MQTT_TOPIC = "sensores/mq135"  # Tópico para el sensor MQ-135
MQTT_PORT = 1883

# Configuración del pin del sensor MQ-135
SENSOR_DIGITAL_PIN = 13  # Pin GPIO para el sensor MQ-135 (conectado al DO)
SENSOR_ANALOG_PIN = 34   # Pin ADC para el sensor MQ-135 (conectado al AO)

# Inicializar pines del sensor
sensor_digital = Pin(SENSOR_DIGITAL_PIN, Pin.IN)
sensor_analog = ADC(Pin(SENSOR_ANALOG_PIN), atten=ADC.ATTN_11DB)

# Función para conectar a WiFi
def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('AURORA', '13082005')  # Cambia el SSID y la contraseña según tu red WiFi
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("\nWiFi Conectada!")

# Función para conectarse al broker MQTT
def conecta_broker():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD, keepalive=60)
    client.connect()
    print(f"Conectado al broker {MQTT_BROKER} en el tópico {MQTT_TOPIC}")
    return client

# Conectar a WiFi
conectar_wifi()

# Conectar al broker MQTT
client = conecta_broker()

# Ciclo infinito
while True:
    try:
        # Leer el estado digital del sensor
        estado_digital = sensor_digital.value()

        # Leer el valor analógico del sensor
        valor_analogico = sensor_analog.read()

        # Crear el mensaje con los datos del sensor
        mensaje = {
            "sensor": "mq135",
            "estado_digital": "gas_detectado" if estado_digital == 0 else "no_gas",
            "valor_analogico": valor_analogico
        }

        print("Publicando:", mensaje)
        client.publish(MQTT_TOPIC, json.dumps(mensaje))  # Enviar datos en formato JSON

    except Exception as e:
        print(f"Error: {e}")
        # Intentar reconectar al broker MQTT en caso de error
        try:
            client.disconnect()
            client = conecta_broker()
        except Exception as ex:
            print(f"Error al reconectar: {ex}")

    sleep(2)  # Esperar 2 segundos antes de la siguiente lectura