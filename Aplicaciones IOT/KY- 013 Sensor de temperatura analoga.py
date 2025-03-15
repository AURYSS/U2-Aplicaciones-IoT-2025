# Importar módulos necesarios
import network
from umqtt.simple import MQTTClient
from machine import Pin, ADC
from time import sleep
import math

# Propiedades para conectar a un cliente MQTT
MQTT_BROKER = "192.168.137.138"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "sensores/temperatura"  # Cambia el tópico para reflejar la temperatura
MQTT_PORT = 1883

# Configuración del pin del sensor KY-013
sensor_pin = ADC(Pin(34))  # Conectar el sensor KY-013 al pin GPIO34
sensor_pin.atten(ADC.ATTN_11DB)  # Configurar el rango de voltaje de 0 a 3.3V

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
                        keepalive=60)
    client.connect()
    print("Conectado a %s, en el topico %s" % (MQTT_BROKER, MQTT_TOPIC))
    return client

# Función para convertir el valor analógico a temperatura
def leer_temperatura(adc_value):
    # Parámetros del termistor NTC (ajusta según las especificaciones de tu sensor)
    R0 = 10000  # Resistencia a 25°C (10kΩ para el KY-013)
    T0 = 298.15  # Temperatura de referencia en Kelvin (25°C)
    B = 3950  # Coeficiente Beta del termistor (ajusta según el datasheet)

    # Convertir el valor ADC a voltaje (asumiendo un ADC de 12 bits y 3.3V de referencia)
    voltaje = adc_value * 3.3 / 4095

    # Calcular la resistencia del termistor
    R = (3.3 - voltaje) / voltaje * R0

    # Calcular la temperatura en Kelvin usando la ecuación del termistor
    temperatura_k = 1 / (1/T0 + (1/B) * math.log(R/R0))

    # Convertir la temperatura a Celsius
    temperatura_c = temperatura_k - 273.15

    return temperatura_c

# Conectar a WiFi
conectar_wifi()

# Conectar al broker MQTT
client = conecta_broker()

# Ciclo infinito
while True:
    try:
        # Leer el valor analógico del sensor
        adc_value = sensor_pin.read()
        print(f"Valor ADC: {adc_value}")

        # Convertir el valor ADC a temperatura
        temperatura = leer_temperatura(adc_value)
        print(f"Temperatura: {temperatura:.2f}°C")

        # Publicar en MQTT
        mensaje = f"Temperatura: {temperatura:.2f}°C"
        client.publish(MQTT_TOPIC, mensaje)

    except Exception as e:
        print(f"Error: {e}")

    sleep(2)  # Esperar 2 segundos antes de la siguiente lectura