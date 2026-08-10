# Punto 2 - Revisión y prueba de YOLO

## Objetivo

Revisar el funcionamiento de la arquitectura YOLO presentada en el material suministrado por el docente y realizar una prueba básica de detección de objetos utilizando Python.

## ¿Qué es YOLO?

YOLO significa **You Only Look Once**.

Es una arquitectura de visión artificial utilizada para detectar objetos dentro de imágenes o video en tiempo real.

El modelo puede identificar diferentes objetos y entregar información como:

- Clase detectada.
- Posición del objeto.
- Caja delimitadora.
- Nivel de confianza de la detección.

## Herramientas utilizadas

- Python
- Ultralytics
- YOLOv8
- OpenCV
- Visual Studio Code
- Cámara del computador

## Instalación del entorno

Se creó un entorno virtual de Python mediante:

```bash
python -m venv yolo_env
```

Posteriormente se activó el entorno y se instalaron las librerías necesarias:

```bash
pip install ultralytics opencv-python
```

## Modelo utilizado

Se utilizó el modelo:

```text
yolov8n.pt
```

Este corresponde a la versión **Nano de YOLOv8**, seleccionada por su bajo costo computacional y su capacidad para realizar detecciones en tiempo real.

## Funcionamiento del programa

El programa desarrollado realiza el siguiente procedimiento:

1. Carga el modelo YOLOv8.
2. Abre la cámara del computador mediante OpenCV.
3. Captura continuamente imágenes de la cámara.
4. Envía cada imagen al modelo YOLO.
5. Obtiene los objetos detectados.
6. Identifica la clase de cada objeto.
7. Filtra únicamente las clases de interés.
8. Muestra las detecciones sobre el video.
9. Presenta el nivel de confianza de cada detección.

## Clases de interés

Para el desarrollo del ejercicio se utilizaron las siguientes clases:

```python
TARGET_CLASSES = {"car", "motorcycle"}
```

Estas clases permiten identificar:

- `car`: carro.
- `motorcycle`: motocicleta.

Estas detecciones serán utilizadas posteriormente en el Punto 3 para controlar los LEDs del ESP32.

## Nivel mínimo de confianza

Se estableció un nivel mínimo de confianza para evitar considerar detecciones poco confiables:

```python
MIN_CONFIDENCE = 0.45
```

Esto significa que únicamente se consideran detecciones con una confianza igual o superior al 45 %.

## Captura de video

La cámara se abre mediante OpenCV utilizando:

```python
cap = cv2.VideoCapture(0)
```

El valor `0` corresponde normalmente a la cámara principal del computador.

El video se procesa con una resolución aproximada de:

```text
640 x 480 píxeles
```

## Detección con YOLO

Cada imagen capturada por la cámara se procesa utilizando:

```python
results = model.predict(
    source=frame,
    conf=MIN_CONFIDENCE,
    verbose=False
)
```

YOLO analiza la imagen y devuelve las detecciones encontradas.

Posteriormente se obtiene la clase detectada mediante:

```python
class_name = model.names[class_id]
```

El programa verifica si la clase corresponde a un carro o una motocicleta.

## Detección de carro

Cuando se detecta un carro:

```python
if class_name == "car":
    car_detected = True
```

En la consola se muestra un mensaje indicando la detección y su nivel de confianza.

Ejemplo:

```text
[DETECCION] CARRO | confianza=0.87
```

## Detección de motocicleta

Cuando se detecta una motocicleta:

```python
elif class_name == "motorcycle":
    motorcycle_detected = True
```

En la consola se muestra un mensaje similar a:

```text
[DETECCION] MOTO | confianza=0.76
```

## Visualización

OpenCV muestra en pantalla el video procesado con las cajas de detección generadas por YOLO.

Además, se muestran mensajes como:

```text
CARRO DETECTADO
```

o:

```text
MOTO DETECTADA
```

dependiendo del objeto reconocido.

## Ejecución

Para ejecutar el programa se utiliza:

```bash
python yolo_test.py
```

La aplicación abre la cámara y comienza la detección en tiempo real.

Para finalizar la ejecución se presiona la tecla:

```text
Q
```

## Archivo principal

El archivo principal correspondiente a este punto es:

```text
yolo_test.py
```

Este archivo contiene el código utilizado para probar la detección de objetos mediante YOLO y OpenCV.

## Relación con el Punto 3

Este punto funciona como base para la integración con el ESP32.

En el siguiente punto se utilizarán las detecciones obtenidas por YOLO para realizar el siguiente control:

```text
Carro detectado
      |
      v
LED rojo encendido

Moto detectada
      |
      v
LED verde encendido
```

## Referencia

El funcionamiento de YOLO fue revisado a partir del material suministrado por el docente:

https://github.com/dialejobv/aplicacion_sistemas_embebidos
