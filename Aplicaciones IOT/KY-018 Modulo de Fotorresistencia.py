import network
from umqtt.simple import MQTTClient
from machine import Pin, ADC
from time import sleep

# 🔹 Configuración de la conexión WiFi
WIFI_SSID = "AURORA"
WIFI_PASSWORD = "13082005"

# 🔹 Propiedades del Broker MQTT
MQTT_BROKER = "192.168.137.138"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "ESP32_LDR"  # Identificador único del cliente
MQTT_TOPIC = "sensores/fotorresistencia"
MQTT_PORT = 1883

# 🔹 Configuración del sensor fotoresistor (KY-018) en el pin 12 del ESP32
ldr_pin = ADC(Pin(32))
ldr_pin.atten(ADC.ATTN_11DB)  # Ajusta el rango de lectura (0-3.3V)

# 🔹 Función para conectar a WiFi
def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
    
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    
    print("\n WiFi Conectada!")
    print("Dirección IP:", sta_if.ifconfig()[0])

# 🔹 Función para conectar al broker MQTT
def conecta_broker():
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD)
        client.connect()
        print(f"Conectado a MQTT Broker: {MQTT_BROKER}")
        return client
    except Exception as e:
        print("❌ Error al conectar al broker MQTT:", e)
        return None

# 🔹 Conectar WiFi
conectar_wifi()

# 🔹 Conectar al Broker MQTT
client = conecta_broker()

# 🔹 Bucle principal
while True:
    try:
        # Leer el valor de la fotorresistencia (0-4095 en ESP32)
        valor_ldr = ldr_pin.read()
        
        # Crear el mensaje a enviar
        mensaje = f"Intensidad de luz: {valor_ldr}"
        print(mensaje)
        
        # Verificar si el cliente MQTT está conectado
        if client is None:
            print("Reconectando al broker MQTT...")
            client = conecta_broker()
        
        # Publicar el mensaje en MQTT
        if client is not None:
            client.publish(MQTT_TOPIC, mensaje)
        
        sleep(1)  # Esperar 1 segundo antes de repetir
    
    except OSError as e:
        print("Error de conexión:", e)
        client = None  # Forzar reconexión en la siguiente iteración
