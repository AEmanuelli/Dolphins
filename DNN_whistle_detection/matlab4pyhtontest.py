import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from scipy.signal.windows import blackman
from scipy.io import wavfile
from tqdm import tqdm
import cProfile
import cv2
from tensorflow.keras.applications.vgg16 import preprocess_input
import tensorflow as tf 


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

def process_audio_file(file_path, saving_folder="", batch_size = 10, start_time=0, save=False, wlen=2048, 
                       nfft= 2048, sliding_w= 0.4, cut_low_frequency=3, cut_high_frequency=20, target_width_px= 1166, 
                       target_height_px= 880):
    # Calculate the spectrogram parameters
    hop = round(0.8 * wlen)  # window hop size
    win = blackman(wlen, sym=False)

    images = []
    # Load sound recording
    fs, x = wavfile.read(file_path)
    x = np.float32(x)  # convert to single precision to save memory
    N = len(x)  # signal length

    low = int(start_time * fs)
    up = low + int(0.8 * fs)
    file_name_ex = start_time  # the start in second
    file_name = file_path.split
    # Calculate total number of iterations for the while loop
    total_iterations = int(np.ceil((N / fs - start_time - 0.8) / sliding_w))

    for _ in tqdm(range(total_iterations), desc=f"Processing frames for file: {file_name}", leave=False):
        x_w = x[low:up]
        
        # Calculate the spectrogram
        f, t, Sxx = spectrogram(x_w, fs, nperseg=wlen, noverlap=hop, nfft=nfft, window=win)
        Sxx = 20 * np.log10(np.abs(Sxx))  # Convert to dB

        # Create the spectrogram plot
        fig, ax = plt.subplots()
        ax.pcolormesh(t, f / 1000, Sxx, cmap='gray')
        ax.set_ylim(cut_low_frequency, cut_high_frequency)

        # ax.set_aspect('auto')  # Adjust aspect ratio
        ax.set_axis_off()  # Turn off axis
        # Resize the figure directly before saving
        fig.set_size_inches(target_width_px / plt.rcParams['figure.dpi'], target_height_px / plt.rcParams['figure.dpi'])

        # Save the spectrogram as a JPG image without borders
        if save: 
            image_name = os.path.join(saving_folder, file_name + '-' + str(file_name_ex) + '.jpg')
            fig.savefig(image_name, bbox_inches='tight', pad_inches=0, dpi=plt.rcParams['figure.dpi'])  # Save without borders
            plt.close(fig)
        else: 
            fig.canvas.draw()
            
            image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
            image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
            images.append(image)
            if len(images) >= batch_size:
                # Fermer les figures pour libérer la mémoire
                plt.close('all')
                return images

        low += int(sliding_w * fs)
        file_name_ex += sliding_w
        up = low + int(0.8 * fs)

    return images

import concurrent.futures

def process_and_predict(recording_folder_path, saving_folder, start_time=0, save=False, model_path="models/model_vgg.h5", csv_path="predictions.csv"):
    files = os.listdir(recording_folder_path)
    model = tf.keras.models.load_model(model_path)
    
    record_names = []
    positive_initial = []
    positive_finish = []
    class_1_scores = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        
        for file_name in files:
            if not os.path.isdir(os.path.join(recording_folder_path, file_name)):
                future = executor.submit(process_audio_file, os.path.join(recording_folder_path, file_name), saving_folder, start_time, save)
                futures.append(future)
        
        for future in concurrent.futures.as_completed(futures):
            images = future.result()
            
            for idx, image in enumerate(images):
                image_start_time = start_time + idx * 0.4
                image_end_time = image_start_time + 0.8
                
                image = cv2.resize(image, (224, 224))
                image = np.expand_dims(image, axis=0)
                image = preprocess_input(image)
                prediction = model.predict(image)
                
                if prediction[0][1] > prediction[0][0]:
                    record_names.append(file_name)
                    positive_initial.append(image_start_time)
                    positive_finish.append(image_end_time)
                    class_1_scores.append(prediction[0][1])

    save_csv(record_names, positive_initial, positive_finish, class_1_scores, csv_path)


model_path = "models/model_vgg.h5"
model = tf.keras.models.load_model(model_path)


if __name__ == "__main__":
    recording_folder_path = '/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/recordings'
    filepath ="/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/recordings/Exp_01_Aug_2023_0845_channel_1.wav"
    saving_folder = '/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/test_fullpipeline'

    profiler = cProfile.Profile()
    profiler.enable()
    process_and_predict(recording_folder_path, saving_folder)


    # images = process_audio_file(file_path=filepath, saving_folder=saving_folder, save = False, start_time=10)
    # predictions = []
    # for image in images :
    #     image = cv2.resize(image, (224, 224))
    #     image = np.resize(image,(1,224,224,3))
    #     image = preprocess_input(image)
    #     predictions.append(model.predict(image))
    # filtered_predictions = [prediction for prediction in predictions if prediction[0][1] > prediction[0][0]]
    # print(filtered_predictions)
    
    profiler.disable()
    # profiler.print_stats()
