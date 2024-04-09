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
import re
from concurrent.futures import ThreadPoolExecutor
from tensorflow.keras.applications.vgg16 import preprocess_input
import tensorflow as tf
import concurrent.futures
from whistle2vid import *
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
matplotlib.use('Agg')
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Igno    rer les messages d'information et de débogage de TensorFlow


# =============================================================================
#********************* FUNCTIONS
# =============================================================================
def transform_file_name(file_name):
    # Utilisation d'une expression régulière pour extraire les parties nécessaires du nom de fichier
    match = re.match(r'Exp_(\d{2})_(\w{3})_(\d{4})_(\d{4})_channel_(\d)', file_name)
    if match:
        day = match.group(1)
        month = match.group(2)
        year = match.group(3)[2:]  # Récupération des deux derniers chiffres de l'année
        time = match.group(4)
        channel = match.group(5)
        transformed_name = f"{day}_{month}_{year}_{time}_c{channel}"
        return transformed_name
    else:
        return None

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
    for _ in range(batch_size):#, desc=f"Processing batch : second {start_time} to {start_time+batch_size*.4}", leave=False):
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
        
        for idx, image in enumerate(images):
            im_cop = image
            image_start_time = round(start + idx * 0.4, 2)
            image_end_time = round(image_start_time + 0.4, 2)

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

            # Libérer les ressources TensorFlow après chaque prédiction
            # tf.keras.backend.clear_session()
        
    # Libérer les ressources GPU explicitement
    # tf.config.experimental.clear_memory()
    
    return record_names, positive_initial, positive_finish, class_1_scores

def process_predict_extract_worker(file_name, recording_folder_path, saving_folder, start_time, end_time, batch_size, 
                                   save_p, model, pbar):
    # pbar.set_postfix(file=file_name)
    date_and_channel = os.path.splitext(file_name)[0]
    print("Processing:", date_and_channel) 
    saving_folder_file = os.path.join(saving_folder, f"{date_and_channel}")
    prediction_file_path = os.path.join(saving_folder_file, f"{date_and_channel}.wav_predictions.csv")

    file_path = os.path.join(recording_folder_path, file_name)

    if os.path.isdir(file_path) or not file_name.lower().endswith(('1.wav', '.wave', "0.wav")) or (os.path.exists(prediction_file_path)): #and os.path.exists(saving_positive)):
        print(f"Non-audio or channel 2 or already predicted : {file_name}. Skipping processing.")
        return
    batch_duration = batch_size * 0.4
    record_names, positive_initial, positive_finish, class_1_scores = process_and_predict(file_path, batch_duration, start_time, end_time, batch_size, model, save_p, saving_folder_file)
    save_csv(record_names, positive_initial, positive_finish, class_1_scores, prediction_file_path)    
    # process_prediction_file(prediction_file_path, file_name, recording_folder_path)
    pbar.update()

def process_predict_extract(recording_folder_path, saving_folder, start_time=0, end_time=1800, batch_size=50, 
                            save=False, save_p=True, model_path="models/model_vgg.h5", max_workers = 16):
    files = os.listdir(recording_folder_path)
    sorted_files = sorted(files, key=lambda x: os.path.getctime(os.path.join(recording_folder_path, x)), reverse=True)
    mask_count = 0  # Compteur pour les fichiers filtrés par le masque
    model = tf.keras.models.load_model(model_path)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []

        with tqdm(total=len(files), desc="Processing Files", position=0, leave=True, colour='green') as pbar:
            for file_name in sorted_files:
                file_path = os.path.join(recording_folder_path, file_name)
                prediction_file_path = os.path.join(saving_folder, f"{file_name}_predictions.csv")
                old_pp = "/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/predictions"
                mask = (os.path.isdir(file_path) or 
                            not file_name.lower().endswith(('1.wav', "0.wav")) or 
                            os.path.exists(prediction_file_path) or 
                            os.path.exists(os.path.join(old_pp, f"{file_name}_predictions.csv")))
                    
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