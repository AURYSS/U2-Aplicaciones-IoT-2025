from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración de Wi-Fi
ssid = 'AURORA'  # Nombre de la red Wi-Fi
password = '13082005'  # Contraseña de la red Wi-Fi

# Configuración de MQTT
mqtt_server = '192.168.137.138'  # Dirección del broker Mosquitto
mqtt_port = 1883  # Puerto del broker Mosquitto
mqtt_topic_button = "sensores/boton"  # Tema MQTT para el botón
mqtt_topic_laser = "sensores/laser"  # Tema MQTT para el LED láser

# Conexión Wi-Fi
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a la red Wi-Fi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Conexión Wi-Fi establecida:', wlan.ifconfig())

# Configuración de pines
button_pin = Pin(14, Pin.IN, Pin.PULL_UP)  # Pin de entrada del botón
laser_pin = Pin(12, Pin.OUT)  # Pin de salida para el LED láser

# Función para conectar al broker MQTT
def conectar_mqtt():
    try:
        client.connect()
    except Exception as e:
        print("Error al conectar al broker MQTT:", e)
        time.sleep(5)
        conectar_mqtt()

# Función para publicar mensajes al broker MQTT
def publicar_mensaje(topic, message):
    try:
        client.publish(topic, message)
    except OSError as e:
        print("Error al publicar el mensaje:", e)
        try:
            if client.is_connected():
                client.disconnect()
        except Exception as ex:
            print("Error al intentar desconectar:", ex)
        time.sleep(5)
        conectar_mqtt()
        publicar_mensaje(topic, message)

# Conectar a Wi-Fi
conectar_wifi()

# Configuración MQTT
client = MQTTClient("RaspberryPi", mqtt_server)
conectar_mqtt()

try:
    while True:
        # Leer el estado del botón
        button_state = button_pin.value()
        
        # Publicar el estado del botón en el broker MQTT
        if button_state == 0:  # Botón presionado
            message_button = "Botón presionado"
            laser_pin.value(1)  # Encender el LED láser
            message_laser = "Láser encendido"
        else:  # Botón no presionado
            message_button = "Botón no presionado"
            laser_pin.value(0)  # Apagar el LED láser
            message_laser = "Láser apagado"

        # Enviar los datos al topic de MQTT
        publicar_mensaje(mqtt_topic_button, message_button)
        publicar_mensaje(mqtt_topic_laser, message_laser)
        print(message_button)
        print(message_laser)
        
        time.sleep(1)  # Esperar 1 segundo antes de la siguiente lectura

