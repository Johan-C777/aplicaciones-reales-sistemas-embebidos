# Punto 3 - Integración YOLO con ESP32 en Wokwi

## Objetivo

Integrar YOLO con un ESP32 simulado en Wokwi para controlar dos LEDs dependiendo del objeto detectado mediante la cámara del computador.

El comportamiento requerido es:

- Cuando se detecta un **carro**, se enciende el LED rojo.
- Cuando se detecta una **motocicleta**, se enciende el LED verde.
- Cuando no se detecta ninguno de los dos objetos, ambos LEDs permanecen apagados.

## Arquitectura del sistema

El sistema está dividido en dos partes principales:

1. Procesamiento de visión artificial en el computador.
2. Control de los LEDs mediante un ESP32 simulado en Wokwi.

El flujo general es:

```text
Cámara del computador
        |
        v
      YOLOv8
        |
        v
Identificación del objeto
        |
        v
     MQTT
        |
        v
ESP32 simulado en Wokwi
        |
   +----+----+
   |         |
   v         v
LED rojo   LED verde
  Carro       Moto
```

## Herramientas utilizadas

- Python
- Ultralytics YOLOv8
- OpenCV
- Paho MQTT
- MicroPython
- ESP32
- Wokwi
- MQTT
- Visual Studio Code

## Modelo utilizado

Para la detección de objetos se utilizó:

```text
yolov8n.pt
```

El modelo YOLOv8 Nano permite realizar detecciones en tiempo real utilizando la cámara del computador.

## Clases utilizadas

Para este ejercicio únicamente se procesan las clases:

```python
TARGET_CLASSES = {"car", "motorcycle"}
```

Estas clases corresponden a:

- `car`: carro.
- `motorcycle`: motocicleta.

## Nivel mínimo de confianza

Para evitar detecciones poco confiables se configuró:

```python
MIN_CONFIDENCE = 0.45
```

Por lo tanto, únicamente se procesan detecciones con una confianza igual o superior al 45 %.

## Funcionamiento de YOLO

La cámara se abre mediante OpenCV:

```python
cap = cv2.VideoCapture(0)
```

Cada imagen capturada se envía al modelo YOLO:

```python
results = model.predict(
    source=frame,
    conf=MIN_CONFIDENCE,
    verbose=False
)
```

Después se obtiene la clase de cada objeto detectado:

```python
class_id = int(box.cls.item())
class_name = model.names[class_id]
```

El programa determina si se detectó un carro o una motocicleta.

## Estados del sistema

El programa utiliza tres posibles estados:

```text
car
motorcycle
none
```

### Carro detectado

Cuando YOLO identifica la clase:

```text
car
```

el computador publica mediante MQTT:

```text
car
```

El ESP32 recibe este mensaje y realiza:

```text
LED rojo  = ON
LED verde = OFF
```

### Motocicleta detectada

Cuando YOLO identifica:

```text
motorcycle
```

se publica:

```text
motorcycle
```

El ESP32 realiza:

```text
LED rojo  = OFF
LED verde = ON
```

### Sin detección

Si no se detecta ninguno de los objetos:

```text
none
```

el ESP32 apaga ambos LEDs.

```text
LED rojo  = OFF
LED verde = OFF
```

## Comunicación MQTT

La comunicación entre Python y el ESP32 se realizó mediante MQTT.

Se utilizó el broker:

```text
test.mosquitto.org
```

y el tópico:

```text
umng/embebidos/yolo_esp32/johan_niko_8f21c6
```

El programa ejecutado en el computador actúa como **publicador MQTT**.

El ESP32 en Wokwi actúa como **suscriptor MQTT**.

La comunicación puede representarse como:

```text
Python / YOLO
    |
    | Publica
    v
Broker MQTT
    |
    | Suscripción
    v
ESP32 Wokwi
```

## Envío desde Python

La publicación MQTT se realiza mediante la librería Paho MQTT:

```python
publish.single(
    TOPIC,
    payload=estado,
    hostname=BROKER,
    port=1883
)
```

El valor de `estado` puede ser:

```text
car
motorcycle
none
```

## Optimización de la comunicación

Para evitar enviar el mismo mensaje continuamente en cada frame de video, se almacena el estado anterior:

```python
estado_anterior = None
```

El mensaje MQTT únicamente se publica cuando cambia la detección:

```python
if estado_actual != estado_anterior:
    enviar_estado(estado_actual)
    estado_anterior = estado_actual
```

Por ejemplo:

```text
none -> car          Envía "car"
car  -> car          No envía
car  -> car          No envía
car  -> none         Envía "none"
none -> motorcycle   Envía "motorcycle"
```

Esto reduce la cantidad de mensajes enviados al broker.

## ESP32 en Wokwi

El ESP32 utiliza los siguientes pines:

| Elemento | GPIO |
|---|---:|
| LED rojo | GPIO 25 |
| LED verde | GPIO 26 |

El ESP32 se conecta a la red WiFi virtual de Wokwi:

```python
wifi.connect("Wokwi-GUEST", "")
```

Posteriormente se conecta al broker MQTT y se suscribe al tópico utilizado por el programa de YOLO.

## Recepción de mensajes

Cada mensaje MQTT recibido es procesado mediante una función callback.

La lógica utilizada es:

```python
if comando == "car":
    LED_RED.on()
    LED_GREEN.off()

elif comando == "motorcycle":
    LED_RED.off()
    LED_GREEN.on()

else:
    LED_RED.off()
    LED_GREEN.off()
```

De esta manera el estado de los LEDs depende directamente del resultado obtenido mediante YOLO.

## Secuencia completa de funcionamiento

1. Se inicia la simulación del ESP32 en Wokwi.
2. El ESP32 se conecta a `Wokwi-GUEST`.
3. El ESP32 se conecta al broker MQTT.
4. El ESP32 se suscribe al tópico correspondiente.
5. Se ejecuta `yolo_mqtt.py` en el computador.
6. OpenCV abre la cámara.
7. YOLO analiza cada frame.
8. Se determina si existe un carro, una motocicleta o ninguno.
9. Python publica el estado mediante MQTT.
10. El ESP32 recibe el mensaje.
11. Se actualizan los LEDs.

## Resultado

El sistema desarrollado cumple con el funcionamiento solicitado:

```text
Carro detectado
      |
      v
LED rojo encendido
```

```text
Motocicleta detectada
        |
        v
LED verde encendido
```

Cuando no existe ninguna detección:

```text
Ambos LEDs apagados
```

## Archivos

### `yolo_mqtt.py`

Programa ejecutado en el computador.

Realiza:

- Captura de video.
- Detección mediante YOLO.
- Clasificación del objeto.
- Publicación MQTT.

### `main.py`

Programa MicroPython ejecutado en el ESP32 de Wokwi.

Realiza:

- Conexión WiFi.
- Conexión MQTT.
- Recepción de mensajes.
- Control de LEDs.

### `diagram.json`

Contiene la configuración del circuito utilizado en Wokwi.

## Ejecución

Primero se inicia la simulación del ESP32 en Wokwi.

Posteriormente, desde el entorno virtual de Python:

```bash
python yolo_mqtt.py
```

Para finalizar el programa se presiona:

```text
Q
```

Al finalizar, el programa publica el estado:

```text
none
```

para apagar ambos LEDs.

## Conclusión

La práctica permitió integrar un sistema de visión artificial con un sistema embebido simulado.

YOLO se encarga del procesamiento computacional de las imágenes, mientras que el ESP32 recibe únicamente el resultado de la detección.

La comunicación mediante MQTT permite separar ambas partes del sistema y transmitir los comandos necesarios para controlar las salidas digitales del ESP32.
