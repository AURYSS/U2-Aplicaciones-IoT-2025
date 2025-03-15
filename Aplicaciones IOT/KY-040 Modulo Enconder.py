import network
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep
import json

# Propiedades para conectar a un cliente MQTT
MQTT_BROKER = "192.168.137.138"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "sensores/encoder"  # Tópico para el encoder
MQTT_PORT = 1883

# Configuración del encoder
ENCODER_CLK_PIN = 14  # Pin GPIO para CLK
ENCODER_DT_PIN = 12   # Pin GPIO para DT
ENCODER_SW_PIN = 13   # Pin GPIO para SW (botón)

# Inicializar pines del encoder
clk = Pin(ENCODER_CLK_PIN, Pin.IN, Pin.PULL_UP)
dt = Pin(ENCODER_DT_PIN, Pin.IN, Pin.PULL_UP)
sw = Pin(ENCODER_SW_PIN, Pin.IN, Pin.PULL_UP)

# Variables para el conteo de pasos y estado anterior del encoder
last_clk_state = clk.value()
step_count = 0

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
        # Leer el estado actual del encoder
        current_clk_state = clk.value()

        # Detectar cambios en el estado del encoder
        if current_clk_state != last_clk_state:
            # Determinar la dirección del giro
            if dt.value() != current_clk_state:
                direccion = "horario"
                step_count += 1
            else:
                direccion = "antihorario"
                step_count -= 1

            # Crear el mensaje con los datos del encoder
            mensaje = {
                "sensor": "encoder",
                "direccion": direccion,
                "pasos": step_count
            }

            print("Publicando:", mensaje)
            client.publish(MQTT_TOPIC, json.dumps(mensaje))  # Enviar datos en formato JSON

        # Actualizar el estado anterior del encoder
        last_clk_state = current_clk_state

        # Leer el estado del botón
        boton_presionado = "presionado" if sw.value() == 0 else "no presionado"

        # Si el botón fue presionado, enviar un mensaje adicional
        if boton_presionado == "presionado":
            mensaje_boton = {
                "sensor": "encoder",
                "accion": "boton_presionado"
            }
            print("Publicando:", mensaje_boton)
            client.publish(MQTT_TOPIC, json.dumps(mensaje_boton))  # Enviar datos en formato JSON

    except Exception as e:
        print(f"Error: {e}")
        # Intentar reconectar al broker MQTT en caso de error
        try:
            client.disconnect()
            client = conecta_broker()
        except Exception as ex:
            print(f"Error al reconectar: {ex}")

    sleep(0.01)  # Esperar un breve tiempo antes de la siguiente lectura