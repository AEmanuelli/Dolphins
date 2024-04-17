import csv
import sys
import os
from tqdm.auto import tqdm 
import math


sys.path.append('/home/alexis/Documents/GitHub/Dolphins')  # Add the root directory to sys.path

from DNN_whistle_detection.Predict_and_extract.utils import process_audio_file

# Function to process intervals for a single recording
def process_recording(csv_rows, audio_file_path, saving_folder):
    # Extract recording ID
    recording_id = csv_rows[0][0]  # Assuming recording ID is in the first column

    # # Dossier de sauvegarde des images spécifique à l'enregistrement
    # recording_saving_folder = os.path.join(saving_folder, recording_id)
    # os.makedirs(recording_saving_folder, exist_ok=True)
    # Process each interval for this recording
    for row in csv_rows:
        start_time = float(row[2])
        end_time = float(row[3])
        # Option 1 : arrondir pour avoir un joli float
        # start_time_processed = round(math.floor(start_time * 10) / 10, 1) # Arrondi au supérieur, à un chiffre après la virgule 
        # end_time_processed = round(math.ceil(end_time * 10) / 10, 1)   # Arrondi à l'inférieur, à un chiffre après la virgule

        # Option 2 : découper dans le même format que notre convertisseur audio-->image
        start_time_processed = start_time - (start_time % 0.4)
        end_time_processed = end_time + (0.4 - (end_time % 0.4))


        # Traitement de l'intervalle audio
        try:
            process_audio_file(audio_file_path, saving_folder=saving_folder, start_time=start_time_processed, end_time=end_time_processed, save=True)
            print(f"OK pour {audio_file_path}")
            break
        except Exception as e:
            continue

total_lines = 5027
# Main function
def main():
    # Chemin du fichier CSV
    csv_file_path = "/media/DOLPHIN1/AllWhistlesSubClustering.csv"

    # Chemin du dossier contenant les fichiers audio WAV
    audio_folder_path = "/media/zf31/Dolphins/Sound/" 

    # Dossier de sauvegarde des images
    saving_folder = "DNN_whistle_detection/Train_model/whistles_from_csv/ugly_coherent_images"
    # saving_folder = "DNN_whistle_detection/Train_model/whistles_from_csv/beautiful spec"

    # Lecture du fichier CSV
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header

        current_recording_id = None
        current_recording_intervals = []

        for row in tqdm(reader, desc="Processing", total=total_lines, unit="row", colour="blue", bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"):
            recording_id = row[0]  # Recording ID is assumed to be the first column
            recording_id = row[0]  # Recording ID is assumed to be the first column
            if recording_id != current_recording_id:
                # Process intervals for the previous recording
                if current_recording_intervals:
                    process_recording(current_recording_intervals, os.path.join(audio_folder_path, current_recording_id + ".wav"), saving_folder)
                # Start processing intervals for a new recording
                current_recording_id = recording_id
                current_recording_intervals = []

            # Append current interval to the list
            current_recording_intervals.append(row)

        # Process the last recording
        if current_recording_intervals:
            process_recording(current_recording_intervals, os.path.join(audio_folder_path, current_recording_id + ".wav"), saving_folder)

if __name__ == "__main__":
    main()
