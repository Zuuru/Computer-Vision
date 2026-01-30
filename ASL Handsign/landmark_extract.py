import cv2
import mediapipe as mp
import os
import csv

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.7
)

BASE_DIR = "dataset/asl_alphabet_train"
OUTPUT = "asl_landmarks.csv"

header = []
for i in range(21):
    header += [f"x{i}", f"y{i}"]
header.append("label")

with open(OUTPUT, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for label in sorted(os.listdir(BASE_DIR)):
        label_path = os.path.join(BASE_DIR, label)

        if not os.path.isdir(label_path):
            continue

        for img_name in os.listdir(label_path):
            img_path = os.path.join(label_path, img_name)

            img = cv2.imread(img_path)
            if img is None:
                continue

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            result = hands.process(img_rgb)

            if result.multi_hand_landmarks:
                hand = result.multi_hand_landmarks[0]
                row = []

                for lm in hand.landmark:
                    row.append(lm.x)
                    row.append(lm.y)

                row.append(label)
                writer.writerow(row)

print("✅ CSV landmark berhasil dibuat!")