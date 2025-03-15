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
MQTT_TOPIC = "sensores/rele"  # Tópico para el relé

MQTT_PORT = 1883

# Configuración del pin del relé (KY-019)
rele_pin = Pin(12, Pin.OUT)  # Pin de salida para el relé

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
    try:
        client = MQTTClient(MQTT_CLIENT_ID,
                            MQTT_BROKER,
                            port=MQTT_PORT,
                            user=MQTT_USER,
                            password=MQTT_PASSWORD,
                            keepalive=60)  # Aumentamos el keepalive
        client.connect()
        print("Conectado a %s, en el topico %s" % (MQTT_BROKER, MQTT_TOPIC))
        return client
    except Exception as e:
        print("Error al conectar al broker MQTT:", e)
        return None

#Conectar a wifi
conectar_wifi()

#Conectar al broker MQTT
client = conecta_broker()

#Ciclo infinito
while True:
    try:
        # Activar el relé
        rele_pin.value(1)  # Encender el relé

        # Publicar en MQTT
        mensaje = f"Relé activado"
        print(mensaje)
        
        # Verificar si el cliente MQTT está conectado
        if client is None:
            print("Reconectando al broker MQTT...")
            client = conecta_broker()
        
        # Publicar el mensaje
        if client is not None:
            client.publish(MQTT_TOPIC, f"{mensaje}")
        
        sleep(1)  # Mantener el relé activado por 1 segundo
        
        # Desactivar el relé
        rele_pin.value(0)  # Apagar el relé

        # Publicar en MQTT
        mensaje = f"Relé desactivado"
        print(mensaje)
        
        # Verificar si el cliente MQTT está conectado
        if client is None:
            print("Reconectando al broker MQTT...")
            client = conecta_broker()
        
        # Publicar el mensaje
        if client is not None:
            client.publish(MQTT_TOPIC, f"{mensaje}")
        
        sleep(1)  # Esperar 1 segundo antes de repetir
    
    except OSError as e:
        print("Error de conexión:", e)
        client = None  # Forzar reconexión en la siguiente iteración
        