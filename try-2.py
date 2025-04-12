from sip import *
import pickle

# real time video capture
import cv2
import mediapipe as mp
import numpy as np
import os
import time

import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
import re
import csv
import numpy as np
from sklearn.neighbors import KNeighborsClassifier


def read_landmarks_from_csv(file_path):
    landmarks_data = []
    labels = []

    with open(file_path, "r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            landmarks_str = row[0]
            label = row[1] if len(row) > 1 else ""

            landmarks = []
            for match in re.finditer(
                r"x: (\d+\.\d+)\s+y: (\d+\.\d+)\s+z: (-?\d+\.\d+)", landmarks_str
            ):
                x = float(match.group(1))
                y = float(match.group(2))
                z = float(match.group(3))
                landmarks.extend([x, y, z])

            landmarks_data.append(landmarks)
            labels.append(label)

    max_length = max(len(landmarks) for landmarks in landmarks_data)
    landmarks_data = [
        landmarks + [0] * (max_length - len(landmarks)) for landmarks in landmarks_data
    ]

    return np.array(landmarks_data), labels


x, y = read_landmarks_from_csv("D:\Code\Python\landmarks.csv")

model = pickle.load(open("D:\ml-sip\\finalized_ensemble method.sav", "rb"))
while True:
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        landmarks1 = []
        ret, frame = cap.read()
        if not ret:
            print("Ignoring empty camera frame.")
            continue
        # Process the frame
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        image = equalize(image)
        image, landmarkss = landmarks(image)
        landmarks1.append(landmarkss)
        print(landmarks1)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        label = model.predict(landmarkss)
        print(label)
        try:
            cv2.imshow("MediaPipe Pose", image)
        except:
            pass
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
