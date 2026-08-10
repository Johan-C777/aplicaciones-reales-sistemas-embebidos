import cv2
from ultralytics import YOLO

MODEL_PATH = "yolov8n.pt"
CAMERA_INDEX = 0
MIN_CONFIDENCE = 0.45

TARGET_CLASSES = {"car", "motorcycle"}

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
print("Muestra un carro o una moto frente a la camara.")
print("Presiona Q para salir.")

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
                print(f"[DETECCION] CARRO | confianza={confidence:.2f}")

            elif class_name == "motorcycle":
                motorcycle_detected = True
                print(f"[DETECCION] MOTO | confianza={confidence:.2f}")

    annotated = result.plot()

    if car_detected:
        cv2.putText(
            annotated,
            "CARRO DETECTADO",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 255),
            2
        )

    if motorcycle_detected:
        cv2.putText(
            annotated,
            "MOTO DETECTADA",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2
        )

    cv2.imshow("YOLO - Carro / Moto", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("[FIN] Programa cerrado")
