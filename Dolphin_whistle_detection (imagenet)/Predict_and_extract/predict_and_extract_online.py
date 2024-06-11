# =============================================================================
#********************* IMPORTS
# =============================================================================
import warnings
import sys
import os
import pandas as pd
import numpy as np
from scipy.io import wavfile
from tqdm import tqdm 
import cv2
from tensorflow.keras.applications.vgg16 import preprocess_input
import tensorflow as tf
import concurrent.futures
from utils import *
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Ignorer les messages d'information et de débogage de TensorFlow


# =============================================================================
#********************* FUNCTIONS
# =============================================================================

def process_and_predict(file_path, batch_duration, start_time, end_time, batch_size, model, save_p, saving_folder_file):
    file_name = os.path.basename(file_path)
    transformed_file_name = transform_file_name(file_name)
    fs, x = wavfile.read(file_path)
    N = len(x)

    if end_time is not None:
        N = min(N, int(end_time * fs))

    total_duration = (N / fs) - start_time
    record_names = []
    positive_initial = []
    positive_finish = []
    class_1_scores = []
    num_batches = int(np.ceil(total_duration / batch_duration))

    for batch in tqdm(range(num_batches), desc=f"Batches for {transformed_file_name}", leave=False, colour='blue'):
        start = batch * batch_duration + start_time
        images = process_audio_file(file_path, saving_folder_file, batch_size=batch_size, start_time=start, end_time=end_time)
        saving_positive = os.path.join(saving_folder_file, "positive")
        
        image_batch = []
        time_batch = []

        for idx, image in enumerate(images):
            im_cop = image
            image_start_time = round(start + idx * 0.4, 2)
            image_end_time = round(image_start_time + 0.4, 2)

            image = cv2.resize(image, (224, 224))
            image = np.expand_dims(image, axis=0)
            image = preprocess_input(image)
            
            image_batch.append(image)
            time_batch.append((im_cop, image_start_time, image_end_time))

        if image_batch:
            image_batch = np.vstack(image_batch)
            predictions = model.predict(image_batch, verbose=0)
            for idx, prediction in enumerate(predictions):
                im_cop, image_start_time, image_end_time = time_batch[idx]
                if prediction[1] > prediction[0]:
                    record_names.append(file_name)
                    positive_initial.append(image_start_time)
                    positive_finish.append(image_end_time)
                    class_1_scores.append(prediction[1])
                    if save_p:
                        if not os.path.exists(saving_positive):
                            os.makedirs(saving_positive)
                        image_name = os.path.join(saving_positive, f"{image_start_time}-{image_end_time}.jpg")
                        cv2.imwrite(image_name, im_cop)

    return record_names, positive_initial, positive_finish, class_1_scores

def process_predict_extract_worker(file_name, recording_folder_path, saving_folder, start_time, end_time, batch_size, 
                                   save_p, model, pbar):
    # pbar.set_postfix(file=file_name)
    date_and_channel = os.path.splitext(file_name)[0]
    
    print("Processing:", date_and_channel) 
    saving_folder_file = os.path.join(saving_folder, f"{date_and_channel}")
    os.makedirs(saving_folder_file, exist_ok=True)
    prediction_file_path = os.path.join(saving_folder_file, f"{date_and_channel}.wav_predictions.csv")

    file_path = os.path.join(recording_folder_path, file_name)

    if not file_name.lower().endswith(".wav") or (os.path.exists(prediction_file_path)) :#or ("channel_2" in file_path): #and os.path.exists(saving_positive)):
        print(f"Non-audio or channel 2 or already predicted : {file_name}. Skipping processing.")
        return

    batch_duration = batch_size * 0.4
    record_names, positive_initial, positive_finish, class_1_scores = process_and_predict(file_path, batch_duration, start_time, end_time, batch_size, model, save_p, saving_folder_file)
    save_csv(record_names, positive_initial, positive_finish, class_1_scores, prediction_file_path)    
    # process_prediction_file(prediction_file_path, file_name, recording_folder_path)
    pbar.update()

def process_predict_extract(recording_folder_path, saving_folder, start_time=0, end_time=1800, batch_size=50, 
                            save=False, save_p=True, model_path="models/model_vgg.h5", max_workers = 16, specific_files = None):
    files = os.listdir(recording_folder_path)
    sorted_files = sorted(files, key=lambda x: os.path.getctime(os.path.join(recording_folder_path, x)), reverse=False)
    
    if specific_files:
        sorted_files = sorted(specific_files, key=lambda x: os.path.getctime(os.path.join(recording_folder_path, x)), reverse=False)


    mask_count = 0  # Compteur pour les fichiers filtrés par le masque
    model = tf.keras.models.load_model(model_path)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []

        with tqdm(total=len(files), desc="Files that are not going to be processed right now : ", position=0, leave=True, colour='green') as pbar:
            for file_name in sorted_files:
                file_path = os.path.join(recording_folder_path, file_name)
                prediction_file_path = os.path.join(saving_folder, f"{file_name}_predictions.csv")
                mask = (os.path.isdir(file_path) or 
                            not file_name.lower().endswith('.wav') or 
                            os.path.exists(prediction_file_path))
                    
                if mask:
                    mask_count += 1
                    pbar.update(1)  # Incrémenter la barre de progression pour les fichiers filtrés
                    continue
                
                future = executor.submit(process_predict_extract_worker, file_name, recording_folder_path, 
                                         saving_folder, start_time, end_time, batch_size, save_p, model, pbar)
                future.add_done_callback(lambda _: pbar.update(1))  # Mettre à jour la barre de progression lorsque le thread termine
                futures.append(future)

            for future in concurrent.futures.as_completed(futures):
                future.result()
