# Importar módulos necesarios
import network
from umqtt.simple import MQTTClient
from machine import Pin, PWM
from time import sleep

# Propiedades para conectar a un cliente MQTT
MQTT_BROKER = "192.168.137.138"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "leds/rgb"
MQTT_PORT = 1883

# Configuración de pines para LED RGB (KY-016)
led_rojo = PWM(Pin(14))  # Pin para el color rojo
led_verde = PWM(Pin(15))  # Pin para el color verde
led_azul = PWM(Pin(16))  # Pin para el color azul

# Configurar la frecuencia PWM (0-1023 en ESP8266 / 0-255 en ESP32)
led_rojo.freq(1000)
led_verde.freq(1000)
led_azul.freq(1000)

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
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,
                            user=MQTT_USER, password=MQTT_PASSWORD, keepalive=0)
        client.connect()
        print(f"Conectado a {MQTT_BROKER}, en el tópico {MQTT_TOPIC}")
        return client
    except OSError as e:
        print("Error al conectar con MQTT:", e)
        return None

# Función para encender el LED RGB con un color
def set_color(r, g, b):
    led_rojo.duty(r)
    led_verde.duty(g)
    led_azul.duty(b)

# Conectar a WiFi
conectar_wifi()
# Conectar a MQTT
client = conecta_broker()

# Ciclo infinito cambiando de colores
while True:
    try:
        # Rojo
        set_color(1023, 0, 0)
        mensaje = "LED RGB: Rojo"
        print(mensaje)
        if client:
            client.publish(MQTT_TOPIC, mensaje)
        sleep(1)

        # Verde
        set_color(0, 1023, 0)
        mensaje = "LED RGB: Verde"
        print(mensaje)
        if client:
            client.publish(MQTT_TOPIC, mensaje)
        sleep(1)

        # Azul
        set_color(0, 0, 1023)
        mensaje = "LED RGB: Azul"
        print(mensaje)
        if client:
            client.publish(MQTT_TOPIC, mensaje)
        sleep(1)

    except OSError as e:
        print("Error de conexión:", e)
        client = None  # Si falla MQTT, intenta reconectar en el próximo ciclo

