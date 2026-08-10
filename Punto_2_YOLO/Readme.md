# Punto 2 - Revisión del funcionamiento de YOLO

## Objetivo

Revisar y comprender el funcionamiento de YOLO a partir del material suministrado por el docente.

Como complemento a la revisión teórica, se realizó una prueba básica utilizando Python, OpenCV y Ultralytics para observar el funcionamiento del modelo en tiempo real mediante la cámara del computador.

## ¿Qué es YOLO?

YOLO significa **You Only Look Once**.

Es una arquitectura de visión artificial utilizada para la detección de objetos en imágenes y video.

Su principal característica es que analiza una imagen y realiza las detecciones en una sola etapa, permitiendo identificar objetos de manera rápida y siendo adecuada para aplicaciones en tiempo real.

## Información obtenida por YOLO

Al procesar una imagen, YOLO puede entregar información como:

- Clase del objeto detectado.
- Posición del objeto dentro de la imagen.
- Caja delimitadora o *bounding box*.
- Nivel de confianza de la detección.

## Flujo básico de funcionamiento

El funcionamiento general utilizado durante la prueba fue:

```text
Cámara
   |
   v
Captura de imagen
   |
   v
Modelo YOLO
   |
   v
Detección de objetos
   |
   v
Clase + confianza + posición
   |
   v
Visualización con OpenCV
```

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

Posteriormente se instalaron las librerías requeridas:

```bash
pip install ultralytics opencv-python
```

## Modelo utilizado

Para realizar la prueba se utilizó:

```text
yolov8n.pt
```

Este corresponde a la versión **Nano de YOLOv8**, adecuada para realizar pruebas de detección en tiempo real debido a su menor costo computacional.

## Carga del modelo

El modelo se carga utilizando la librería Ultralytics:

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
```

Una vez cargado, el modelo queda disponible para procesar imágenes o video.

## Captura de video

Para obtener imágenes en tiempo real se utilizó OpenCV:

```python
import cv2

cap = cv2.VideoCapture(0)
```

El valor `0` corresponde normalmente a la cámara principal del computador.

Cada imagen obtenida de la cámara se denomina `frame`.

```python
ret, frame = cap.read()
```

## Procesamiento mediante YOLO

Cada frame capturado puede enviarse al modelo mediante:

```python
results = model.predict(
    source=frame,
    verbose=False
)
```

YOLO procesa la imagen y devuelve los objetos detectados.

## Resultados de la detección

Los resultados obtenidos contienen información de cada objeto identificado.

Por ejemplo:

```python
for box in results[0].boxes:
    class_id = int(box.cls.item())
    confidence = float(box.conf.item())
```

`class_id` representa la clase identificada y `confidence` representa el nivel de confianza de la detección.

El nombre correspondiente a una clase puede obtenerse mediante:

```python
class_name = model.names[class_id]
```

## Visualización

Ultralytics permite generar automáticamente una imagen con las cajas delimitadoras y nombres de los objetos detectados:

```python
annotated_frame = results[0].plot()
```

Posteriormente OpenCV permite mostrar el resultado:

```python
cv2.imshow("YOLO", annotated_frame)
```

De esta manera es posible observar en tiempo real los objetos reconocidos por el modelo.

## Conclusión

La revisión permitió comprender el flujo básico de funcionamiento de YOLO:

1. Se obtiene una imagen.
2. La imagen se entrega al modelo.
3. YOLO procesa la información.
4. Se identifican los objetos presentes.
5. Para cada detección se obtiene una clase, posición y nivel de confianza.
6. Los resultados pueden utilizarse posteriormente dentro de otras aplicaciones.

## Archivo de prueba

Como evidencia de la revisión se incluye:

```text
yolo_test.py
```

Este programa permite comprobar el funcionamiento de YOLO utilizando la cámara del computador.

## Referencia

Material suministrado por el docente:

https://github.com/dialejobv/aplicacion_sistemas_embebidos
