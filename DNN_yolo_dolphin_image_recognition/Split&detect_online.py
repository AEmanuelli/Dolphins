# 1. Installation des paquets nécessaires
# !pip install opencv-python opencv-python-headless numpy

import cv2
import numpy as np
import os

# 2. Charger YOLO
net = cv2.dnn.readNet("/home/alexis/Downloads/yolov3.weights", "/home/alexis/Downloads/yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

def detect_people(frame):
    height, width = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if class_id == 0 and confidence > 0.5:  # Classe 0 est "personne" dans YOLO
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str("Person")
            color = (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return frame

# 3. Charger la vidéo
video_path = '/path/to/votre_video.mp4'
cap = cv2.VideoCapture(video_path)

# Obtenir les dimensions des cadres
ret, frame = cap.read()
height, width, _ = frame.shape
sub_height, sub_width = height // 2, width // 2

# 4. Appliquer la détection sur chaque sous-cadre et sauvegarder les vidéos traitées
out1 = cv2.VideoWriter('/kaggle/working/output1.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (sub_width, sub_height))
out2 = cv2.VideoWriter('/kaggle/working/output2.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (sub_width, sub_height))
out3 = cv2.VideoWriter('/kaggle/working/output3.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (sub_width, sub_height))
out4 = cv2.VideoWriter('/kaggle/working/output4.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (sub_width, sub_height))

while ret:
    frame1 = frame[0:sub_height, 0:sub_width]
    frame2 = frame[0:sub_height, sub_width:width]
    frame3 = frame[sub_height:height, 0:sub_width]
    frame4 = frame[sub_height:height, sub_width:width]

    frame1 = detect_people(frame1)
    frame2 = detect_people(frame2)
    frame3 = detect_people(frame3)
    frame4 = detect_people(frame4)

    out1.write(frame1)
    out2.write(frame2)
    out3.write(frame3)
    out4.write(frame4)

    ret, frame = cap.read()

cap.release()
out1.release()
out2.release()
out3.release()
out4.release()
cv2.destroyAllWindows()
