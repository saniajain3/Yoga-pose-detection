from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import re
import csv
import numpy as np
from sklearn.metrics import accuracy_score
import pickle


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

x_train, x_temp, y_train, y_temp = train_test_split(
    x, y, test_size=0.1, random_state=10)


x_val, x_test, y_val, y_test = train_test_split(
    x_temp, y_temp, test_size=0.5, random_state=10)

knn_classifier = KNeighborsClassifier(n_neighbors=9)
dt_classifier = DecisionTreeClassifier()
rf_classifier = RandomForestClassifier(random_state=21)
# Create the ensemble
ensemble_classifier = VotingClassifier(estimators=[
    ('dt', dt_classifier),
    ('knn', knn_classifier),
    ('rf', rf_classifier)
], voting='soft')
ensemble_classifier.fit(x_train, y_train)
y_pred = ensemble_classifier.predict(x_test)
print(accuracy_score(y_test, y_pred))
print(ensemble_classifier.score(x_val, y_val))
path = "D:\ml-sip"
with open('finalized_ensemble_soft.sav', 'wb') as f:
    pickle.dump(ensemble_classifier, f)

# elbow curve plot for knn
# error = []
# # Calculating error for K values between 1 and 40
# for i in range(1, 40):
#     knn = KNeighborsClassifier(n_neighbors=i)
#     knn.fit(x, y)
#     pred_i = knn.predict(x)
#     error.append(np.mean(pred_i != y))
# plt.figure(figsize=(12, 6))
# plt.plot(range(1, 40), error, color='red', linestyle='dashed', marker='o',
#          markerfacecolor='blue', markersize=10)
# plt.title('Error Rate K Value')
# plt.xlabel('K Value')
# plt.ylabel('Mean Error')
# plt.show()
