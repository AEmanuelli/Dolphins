# =============================================================================
#********************* IMPORTS
# =============================================================================

import warnings
import sys
import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from scipy.signal.windows import blackman
from scipy.io import wavfile
from tqdm import tqdm 
import cProfile
import pstats
import cv2
from concurrent.futures import ThreadPoolExecutor
from tensorflow.keras.applications.vgg16 import preprocess_input
from whistle2vid import *
import tensorflow as tf
import concurrent.futures
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
matplotlib.use('Agg')

# =============================================================================
#********************* FUNCTIONS
# =============================================================================

def process_prediction_file(prediction_file_path, file_name, recording_folder_path):
    go = True 
    with open(prediction_file_path, 'r') as file:
        lines = file.readlines()
        if len(lines) <= 1:
            go = False
    if os.path.exists(prediction_file_path) and go :
        # File exists and is not empty
        process_non_empty_file(prediction_file_path, file_name, recording_folder_path)
    elif os.path.exists(prediction_file_path):
        # File exists but is empty
        handle_empty_file(prediction_file_path, file_name)
    else:
        # File is missing
        handle_missing_file(prediction_file_path, file_name)

def process_non_empty_file(prediction_file_path, file_name, recording_folder_path):
    intervalles = lire_csv_extraits(prediction_file_path)
    intervalles_fusionnes = fusionner_intervalles(intervalles, hwindow=5)
    # print(intervalles_fusionnes)

    fichier_video = trouver_fichier_video(file_name, recording_folder_path)
    if fichier_video:
        filename = "_".join(os.path.splitext(file_name)[0].split("_")[:7])
        dossier_sortie_video = f"./extraits/{filename}"
        os.makedirs(dossier_sortie_video, exist_ok=True)

        extraire_extraits_video(intervalles_fusionnes, fichier_video, dossier_sortie_video)

def handle_empty_file(prediction_file_path, file_name):
    dossier_sortie_video = f"./extraits/{file_name}"
    txt_file_path = os.path.join(dossier_sortie_video, f"No_whistles_detected.txt")
    with open(txt_file_path, 'w') as txt_file:
        txt_file.write(f"No whistles detected in {file_name} ")
    print(f"Empty CSV file for {file_name}. No video extraction will be performed. A message has been saved to {txt_file_path}.")

def handle_missing_file(prediction_file_path, file_name):
    dossier_sortie_video = f"./extraits/{file_name}"
    txt_file_path = os.path.join(dossier_sortie_video, f"No_CSV_found.txt")
    with open(txt_file_path, 'w') as txt_file:
        txt_file.write(f"No CSV found in {file_name}")
    print(f"Missing CSV file for {file_name}. No video extraction will be performed.")

def prepare_csv_data(file_path, record_names, positive_initial, positive_finish):
    part = file_path.split('wav-')

    name = part[0] + "wav"
    record_names.append(name)
    
    ini = part[1].replace(".jpg", "")
    ini = float(ini)
    positive_initial.append(ini)
    
    fin = ini + 0.8
    fin = round(fin, 1)
    positive_finish.append(fin)
    
    return record_names, positive_initial, positive_finish

def save_csv(record_names, positive_initial, positive_finish, class_1_scores, csv_path):
    df = {'file_name': record_names,
    'initial_point': positive_initial,
    'finish_point': positive_finish,
    'confidence': class_1_scores}

    df = pd.DataFrame(df)
    
    df.to_csv(csv_path, index=False)

def process_audio_file(file_path, saving_folder="./images", batch_size=50, start_time=0, end_time=None, save=False, wlen=2048,
                       nfft=2048, sliding_w=0.4, cut_low_frequency=3, cut_high_frequency=20, target_width_px=903,
                       target_height_px=677):
    try:
        # Load sound recording
        fs, x = wavfile.read(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found.")
            # Create the saving folder if it doesn't exist
    if save and not os.path.exists(saving_folder):
        os.makedirs(saving_folder)
    # Calculate the spectrogram parameters
    hop = round(0.8 * wlen)  # window hop size
    win = blackman(wlen, sym=False)
    # win = np.blackman(wlen)

    images = []
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    N = len(x)  # signal length

    if end_time is not None:
        N = min(N, int(end_time * fs))

    low = int(start_time * fs)
    up = low + int(0.8 * fs)
    file_name_ex = start_time  # the start in second
    for _ in tqdm(range(batch_size), desc=f"Processing batch : second {start_time} to {start_time+batch_size*.4}", leave=False):
        if up > N:  # Check if the upper index exceeds the signal length
            break
        x_w = x[low:up]
        
        # Calculate the spectrogram
        f, t, Sxx = spectrogram(x_w, fs, nperseg=wlen, noverlap=hop, nfft=nfft, window=win)
        Sxx = 20 * np.log10(np.abs(Sxx))  # Convert to dB

        # Create the spectrogram plot
        fig, ax = plt.subplots()
        ax.pcolormesh(t, f / 1000, Sxx, cmap='gray')
        ax.set_ylim(cut_low_frequency, cut_high_frequency)

        ax.set_axis_off()  # Turn off axis
        fig.set_size_inches(target_width_px / plt.rcParams['figure.dpi'], target_height_px / plt.rcParams['figure.dpi'])
        
        # Adjust margins
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
      
        # Save the spectrogram as a JPG image without borders
        if save:
            image_name = os.path.join(saving_folder, f"{file_name}-{file_name_ex}.jpg")
            fig.savefig(image_name, dpi=plt.rcParams['figure.dpi'])  # Save without borders

        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        images.append(image)

        low += int(sliding_w * fs)
        file_name_ex += sliding_w
        up = low + int(0.8 * fs)

    plt.close('all')  # Close all figures to release memory

    return images

def process_and_predict(file_path, batch_duration, start_time, end_time, batch_size, model, save_p, saving_folder_file):
    file_name = os.path.basename(file_path)
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

    for batch in tqdm(range(num_batches), desc="Batches", leave=False, colour='blue'):
        start = batch * batch_duration + start_time
        images = process_audio_file(file_path, saving_folder_file, batch_size=batch_size, start_time=start, end_time=end_time)
        saving_positive = os.path.join(saving_folder_file, "positive")
        
        sys.stdout = open(os.devnull, 'w')

        for idx, image in enumerate(images):
            image_start_time = start + idx * 0.4
            image_end_time = image_start_time + 0.4
            im_cop = image
            image = cv2.resize(image, (224, 224))
            image = np.expand_dims(image, axis=0)
            image = preprocess_input(image)
            prediction = model.predict(image)
            
            if prediction[0][1] > prediction[0][0]:
                record_names.append(file_name)
                positive_initial.append(image_start_time)
                positive_finish.append(image_end_time)
                class_1_scores.append(prediction[0][1])
            
                if save_p:
                    if not os.path.exists(saving_folder_file):
                        os.makedirs(saving_positive)
                    image_name = os.path.join(saving_positive, f"{image_start_time}-{image_end_time}.jpg")
                    cv2.imwrite(image_name, im_cop)

        sys.stdout = sys.__stdout__
        
    return record_names, positive_initial, positive_finish, class_1_scores

def process_predict_extract_worker(file_name, recording_folder_path, saving_folder, start_time, end_time, batch_size, save_p, model_path, csv_path, pbar):
    pbar.set_postfix(file=file_name)
    date_and_channel = os.path.splitext(file_name)[0]
    print("Processing:", date_and_channel)
    prediction_file_path = f"predictions/{file_name}_predictions.csv"
    saving_folder_file = os.path.join(saving_folder, f"{date_and_channel}")

    file_path = os.path.join(recording_folder_path, file_name)

    if os.path.isdir(file_path) or not file_name.lower().endswith(('1.wav', '.wave', "0.wav")) or (os.path.exists(prediction_file_path)): #and os.path.exists(saving_positive)):
        print(f"Non-audio or channel 2 or already predicted : {file_name}. Skipping processing.")
        return
    
    model = tf.keras.models.load_model(model_path)
    batch_duration = batch_size * 0.4
    record_names, positive_initial, positive_finish, class_1_scores = process_and_predict(file_path, batch_duration, start_time, end_time, batch_size, model, save_p, saving_folder_file)
    save_csv(record_names, positive_initial, positive_finish, class_1_scores, prediction_file_path)    
    process_prediction_file(prediction_file_path, file_name, recording_folder_path)
    pbar.update()

def process_predict_extract(recording_folder_path, saving_folder, start_time=1750, end_time=1800, batch_size=50, save=False, save_p=True, model_path="models/model_vgg.h5", csv_path="predictions.csv"):
    files = os.listdir(recording_folder_path)
    batch_duration = batch_size * 0.4

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        with tqdm(total=len(files), desc="Processing Files", position=0, leave=False, colour='green') as pbar:
            for file_name in files:
                futures.append(executor.submit(process_predict_extract_worker, file_name, recording_folder_path, saving_folder, start_time, end_time, batch_size, save_p, model_path, csv_path, pbar))
            
            for future in concurrent.futures.as_completed(futures):
                future.result()

def main():
    model_path = "models/model_vgg.h5"
    recording_folder_path = "/media/DOLPHIN_ALEXIS/2023"  # Update with your actual path
    saving_folder_image = '/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/2023_images'  # Update with your actual path
    dossier_csv = "/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/predictions"  # Update with your actual path
    
    process_predict_extract(recording_folder_path, saving_folder_image, start_time=0, 
                            end_time=1800, batch_size=50, save=False, save_p=True, 
                            model_path="models/model_vgg.h5", csv_path="predictions.csv")

if __name__ == "__main__":
    main()