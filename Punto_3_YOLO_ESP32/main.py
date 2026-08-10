from machine import Pin
import network
import time

BROKER = "test.mosquitto.org"

TOPIC = b"umng/embebidos/yolo_esp32/johan_niko_8f21c6"

LED_RED = Pin(25, Pin.OUT)
LED_GREEN = Pin(26, Pin.OUT)

LED_RED.off()
LED_GREEN.off()

print("Conectando a WiFi...")

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("Wokwi-GUEST", "")

while not wifi.isconnected():
    print(".", end="")
    time.sleep(0.2)

print()
print("WiFi conectado")
print(wifi.ifconfig())

try:
    from umqtt.simple import MQTTClient

except ImportError:

    print("Instalando umqtt.simple...")

    import mip
    mip.install("umqtt.simple")

    from umqtt.simple import MQTTClient

def recibir_mensaje(topic, msg):

    comando = msg.decode().strip()

    print("Mensaje recibido:", comando)

    if comando == "car":

        LED_RED.on()
        LED_GREEN.off()

        print("CARRO -> LED ROJO ON")


    elif comando == "motorcycle":

        LED_RED.off()
        LED_GREEN.on()

        print("MOTO -> LED VERDE ON")

    else:

        LED_RED.off()
        LED_GREEN.off()

        print("SIN DETECCION -> LEDs OFF")

print("Conectando a MQTT...")

client = MQTTClient(
    client_id="esp32_wokwi_yolo_8f21c6",
    server=BROKER,
    port=1883,
    keepalive=60
)

client.set_callback(recibir_mensaje)

client.connect()

client.subscribe(TOPIC)

print("MQTT conectado")
print("Esperando detecciones...")

ultimo_ping = time.ticks_ms()

while True:

    client.check_msg()

    # Mantener viva la conexion MQTT
    if time.ticks_diff(
        time.ticks_ms(),
        ultimo_ping
    ) > 30000:

        client.ping()

        ultimo_ping = time.ticks_ms()

    time.sleep_ms(50)