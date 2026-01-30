# realtime_asl_detector.py
import cv2
import numpy as np
import joblib
from cvzone.HandTrackingModule import HandDetector
import time

MODEL = "asl_model.pkl"
SCALER = "asl_scaler.pkl"
LE = "label_encoder.pkl"

clf = joblib.load(MODEL)
scaler = joblib.load(SCALER)
le = joblib.load(LE)

detector = HandDetector(staticMode=False, maxHands=1, detectionCon=0.6, minTrackCon=0.5)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise SystemExit("Cannot open camera")

prev_time = 0
while True:
    ret, img = cap.read()
    if not ret:
        break

    hands, img = detector.findHands(img, draw=True, flipType=True)  # draw hand landmarks

    if hands:
        hand = hands[0]
        lm = np.array(hand["lmList"]).flatten().reshape(1, -1)
        try:
            lm_scaled = scaler.transform(lm)
            probs = clf.predict_proba(lm_scaled)[0]
            idx = np.argmax(probs)
            pred = le.inverse_transform([idx])[0]
            conf = probs[idx]
        except Exception as e:
            pred = "Err"
            conf = 0.0

        # Draw label
        bbox = hand.get("bbox", None)
        if bbox:
            x, y, w, h = bbox
            cv2.rectangle(img, (x-5,y-5), (x+w+5, y+h+5), (0,255,0), 2)
            cv2.putText(img, f"{pred} {conf:.2f}", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        else:
            cv2.putText(img, f"{pred} {conf:.2f}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    else:
        cv2.putText(img, "No hand", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    # FPS
    curr_time = time.time()
    fps = 1/(curr_time - prev_time) if prev_time != 0 else 0
    prev_time = curr_time
    cv2.putText(img, f"FPS:{int(fps)}", (20, img.shape[0]-20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

    cv2.imshow("ASL Realtime Detector", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
