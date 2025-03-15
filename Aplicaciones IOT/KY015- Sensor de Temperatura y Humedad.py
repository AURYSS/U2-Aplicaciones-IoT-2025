#import para acceso a red
import network
#Para usar protocolo MQTT
from umqtt.simple import MQTTClient

#Importamos modulos necesarios
from machine import Pin
from time import sleep
import dht  # Biblioteca para el sensor DHT11/DHT22

#Propiedades para conectar a un cliente MQTT
MQTT_BROKER = "192.168.137.138"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "sensores/temperatura_humedad"  # Cambiamos el tópico para reflejar el uso del KY-015

MQTT_PORT = 1883

# Configuración del pin del sensor KY-015
dht_pin = Pin(12, Pin.IN)  # Conectar el KY-015 al pin 12
dht_sensor = dht.DHT11(dht_pin)  # Usar DHT11 (si tienes un DHT22, cambia a dht.DHT22)

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
    try:
        # Leer los datos del sensor
        dht_sensor.measure()  # Realizar una medición
        temperatura = dht_sensor.temperature()  # Obtener la temperatura en °C
        humedad = dht_sensor.humidity()        # Obtener la humedad en %

        # Publicar en MQTT
        mensaje = f"Temperatura: {temperatura}°C, Humedad: {humedad}%"
        print(mensaje)
        client.publish(MQTT_TOPIC, f"{mensaje}")
    
    except Exception as e:
        print("Error al leer el sensor:", e)
    
    sleep(2)  # Esperar 2 segundos antes de repetir