import cv2
from ultralytics import YOLO
import paho.mqtt.publish as publish

MODEL_PATH = "yolov8n.pt"
CAMERA_INDEX = 0
MIN_CONFIDENCE = 0.45
TARGET_CLASSES = {"car", "motorcycle"}

BROKER = "test.mosquitto.org"
TOPIC = "umng/embebidos/yolo_esp32/johan_niko_8f21c6"

def enviar_estado(estado):
    publish.single(
        TOPIC,
        payload=estado,
        hostname=BROKER,
        port=1883
    )
    print("[MQTT] Estado enviado:", estado)

print("[INIT] Cargando YOLO...")
model = YOLO(MODEL_PATH)
print("[OK] Modelo cargado")

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    raise RuntimeError(
        "No se pudo abrir la camara. "
        "Prueba cambiando CAMERA_INDEX de 0 a 1."
    )

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("[OK] Camara abierta")
print("[OK] MQTT configurado")
print("Muestra un carro o una moto frente a la camara.")
print("Presiona Q para salir.")

estado_anterior = None

while True:
    ret, frame = cap.read()

    if not ret:
        print("[ERROR] No se pudo leer un frame de la camara")
        break

    results = model.predict(
        source=frame,
        conf=MIN_CONFIDENCE,
        verbose=False
    )

    result = results[0]

    car_detected = False
    motorcycle_detected = False

    if result.boxes is not None:
        for box in result.boxes:
            class_id = int(box.cls.item())
            confidence = float(box.conf.item())
            class_name = model.names[class_id]

            if class_name not in TARGET_CLASSES:
                continue

            if class_name == "car":
                car_detected = True
                print(f"[YOLO] CARRO | confianza={confidence:.2f}")

            elif class_name == "motorcycle":
                motorcycle_detected = True
                print(f"[YOLO] MOTO | confianza={confidence:.2f}")

    if car_detected:
        estado_actual = "car"
    elif motorcycle_detected:
        estado_actual = "motorcycle"
    else:
        estado_actual = "none"

    if estado_actual != estado_anterior:
        try:
            enviar_estado(estado_actual)
            estado_anterior = estado_actual
        except Exception as error:
            print("[ERROR MQTT]", error)

    annotated = result.plot()

    if car_detected:
        cv2.putText(
            annotated,
            "CARRO -> LED ROJO",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

    if motorcycle_detected:
        cv2.putText(
            annotated,
            "MOTO -> LED VERDE",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow("YOLO + MQTT + ESP32 Wokwi", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

try:
    enviar_estado("none")
except Exception:
    pass

cap.release()
cv2.destroyAllWindows()

print("[FIN] Programa cerrado")
