# Dolphin Image Detection (Yolo)

This repository is dedicated to the detection of dolphins in camera images. It consists of two folders:

1. Variance based with thresholding methods (unsuccessful) : 
    This folder contains the code for variance-based detection of dolphins in images. It utilizes variance-based algorithms to identify regions of interest that are likely to contain dolphins. However, this approach was not successful in achieving satisfactory results. The code includes various techniques such as adaptive thresholding, morphological operations, and contour detection.

2. Finetune YOLO : 
    This folder contains the code for fine-tuning the YOLO v5 object detection model specifically for dolphin detection. It provides instructions and code for training the model on dolphin image datasets to improve its accuracy and performance. The code includes data preprocessing, model configuration, training, and evaluation steps.

The goal of the code in this folder is to develop an accurate and efficient dolphin video detection system.


To use this code, follow these steps:

1. Navigate to the project directory:
```
cd /users/zfne/emanuell/Documents/GitHub/Dolphins/Dolphin_image_detection\ \(Yolo\)/
```
2. Install requirements
```
pip install -r requirements.txt
```

3. Run the dolphin detection script:

# Directory Structure

## Finetune Yolo
- `dolphin_image_detection_yolov5.ipynb`: Jupyter notebook for dolphin image detection using YOLOv5. [https://www.kaggle.com/alexisemanuelli/yolo-5-for-dolphins]
- `finetune yolo dolphins NDD20.ipynb`: Jupyter notebook for finetuning YOLOv5 on dolphin images from NDD20 dataset.
- `Format Data and Train YOLO after retrieving CVAT data.ipynb`: Notebook focused on formatting data and training YOLO for dolphin image detection. It includes code for extracting files from a ZIP archive, creating directories, and moving files to the appropriate locations for training and validation. Finally, contaions code for video creation after finetuning.
- `Prepare NDD20 Yolo dataset.ipynb`: This notebook prepares NDD20 dataset for YOLO finetuning. It loads labels from a JSON file, creates directories for YOLO format labels and images, splits the data into train and validation sets, and converts polyline annotations to bounding box labels.
- `yolokaggle.ipynb`: Attempt of utilizing the Grounding DINO and CLIP models for dolphin detection. 

## Variance based with thresholding methods (unsuccessful)
Mainly code I made a long time ago and not useful one, maybe one day I'll get back to it but not today 