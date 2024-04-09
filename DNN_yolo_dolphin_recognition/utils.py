import os

class Checkpoint:
    def __init__(self, target_directory):
        self.target_directory = target_directory

    def file_exists(self, filename):
        # Construit le chemin complet du fichier
        file_path = os.path.join(self.target_directory, filename)
        # Vérifie si le fichier existe
        return os.path.isfile(file_path)
    

import cv2
from models.common import DetectMultiBackend
from utils.general import check_img_size
from utils.torch_utils import select_device
import torch

def run_on_image(image_path, weights, imgsz=(640, 640), device=''):
    # Initialize the model
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device)
    stride = model.stride
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Load the image
    image = cv2.imread(image_path)
    image = cv2.resize(image, imgsz)  # Resize image to match model's expected input size
    img = torch.from_numpy(image).to(device)
    img = img.permute(2, 0, 1).float()  # Convert HWC to CHW format and to fp32
    img /= 255  # Normalize from 0-255 to 0.0-1.0
    img = img[None]  # add batch dimension

    # Inference
    with torch.no_grad():
        pred = model(img, augment=False, visualize=False)

    # Process detections
    # ... (Add code here to handle the predictions, e.g., draw boxes on the image)

    # Display the image
    cv2.imshow('Image', image)
    cv2.waitKey(0)  # Wait indefinitely until a key is pressed
    cv2.destroyAllWindows()

# Example usage
# run_on_image('path_to_image.jpg', 'path_to_weights/yolov5s.pt')
