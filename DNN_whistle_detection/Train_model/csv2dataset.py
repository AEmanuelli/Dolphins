import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from scipy.io import wavfile
from tqdm import tqdm
from DNN_whistle_detection.Predict_and_extract.process_predictions import process_audio_file

# Exemple d'utilisation avec un fichier CSV contenant les intervalles de temps
def main():
    # Chemin du fichier CSV
    csv_file_path = "comments.csv"

    # Chemin du fichier audio WAV
    audio_file_path = "/media/DOLPHIN1/temp_alexis/Exp_01_Dec_2023_1345_channel_0.wav"

    # Dossier de sauvegarde des images
    saving_folder = "./images"

    # Lecture du fichier CSV
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            start_time = float(row[0])  # Début de l'intervalle
            end_time = float(row[1])    # Fin de l'intervalle
            # Traitement de l'intervalle audio
            process_audio_file(audio_file_path, saving_folder=saving_folder, start_time=start_time, end_time=end_time, save=True)

if __name__ == "__main":
    main()

