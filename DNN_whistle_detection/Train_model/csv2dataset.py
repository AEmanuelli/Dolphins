import csv
import sys
import os
from tqdm.auto import tqdm 
import math


sys.path.append('/home/alexis/Documents/GitHub/Dolphins')  # Add the root directory to sys.path

from DNN_whistle_detection.Predict_and_extract.utils import process_audio_file, process_audio_file_alternative

# Function to process intervals for a single recording
def process_recording(csv_rows, audio_file_path, saving_folder, alternative = False, window_size = .4, margin = 0.3, neg_per_int =5):
    """
    Creates dataset material for a single recording.

    Parameters:
    - csv_rows (list): List of rows from the CSV file containing intervals.
    - audio_file_path (str): Path to the audio file.
    - saving_folder (str): Path to the folder where images will be saved.
    - alternative (bool): Flag indicating whether to use an alternative processing method (default: False).
    - window_size (float): Size of the window (in seconds) for each interval (default: 0.4).
    - margin (float): Minimum percentage of the length of positive images that we want to be labeled as positive according to the csv (default: 30).
    - neg_per_int (int) : quantity of negative images extracted where there are no positives (default : 5).

    Returns:
    - None
    """

    saving_folder_pos = os.path.join(saving_folder, "positives")
    saving_folder_neg = os.path.join(saving_folder, "negatives")
    
    
    # # Dossier de sauvegarde des images spécifique à l'enregistrement
    # # Extract recording ID
    # recording_id = csv_rows[0][0]  # Assuming recording ID is in the first column
    # recording_saving_folder = os.path.join(saving_folder, recording_id)
    # os.makedirs(recording_saving_folder, exist_ok=True)
    # Process each interval for this recording


    end_time_pos_cache = 0
    for row in csv_rows:
        start_time_neg = end_time_pos_cache
        start_time_pos = float(row[2]) + margin*window_size

        end_time_neg = float(row[2])- margin*window_size
        end_time_pos = float(row[3]) - margin*window_size

        ok_neg = (end_time_neg-start_time_neg) >= 30 # Si les whistles sont espacés de moins de 30s on ne prélève pas de négatifs


        end_time_pos_cache = end_time_pos + 2*margin*window_size 
        
        # Option 1 : arrondir pour avoir un joli float
        # start_time_processed = round(math.floor(start_time * 10) / 10, 1) # Arrondi au supérieur, à un chiffre après la virgule 
        # end_time_processed = round(math.ceil(end_time * 10) / 10, 1)   # Arrondi à l'inférieur, à un chiffre après la virgule

        # Option 2 : découper dans le même format que notre convertisseur audio-->image
        start_time_processed_pos = start_time_pos - (start_time_pos % 0.4)
        end_time_processed_pos = end_time_pos + (0.4 - (end_time_pos % 0.4))
        
        
        start_time_processed_neg = start_time_neg - (start_time_neg % 0.4) + 5*window_size
        end_time_processed_neg = end_time_neg + (0.4 - (end_time_pos % 0.4)) - 5*window_size

        try:
            if alternative : 
                # Traitement de l'intervalle audio POSITIF
                process_audio_file_alternative(audio_file_path, saving_folder=saving_folder_pos, start_time=start_time_processed_pos, 
                                               end_time=end_time_processed_pos, save=True)
                if ok_neg:
                    # Traitement de l'intervalle audio NÉGATIF
                    process_audio_file_alternative(audio_file_path, saving_folder=saving_folder_neg, start_time=start_time_processed_neg, 
                                                end_time=end_time_processed_neg, batch_size = neg_per_int, save=True)
            else:   
                # Traitement de l'intervalle audio POSITIF 
                process_audio_file(audio_file_path, saving_folder=saving_folder_pos, start_time=start_time_processed_pos, 
                                   end_time=end_time_processed_pos, save=True)
                if ok_neg:
                    # Traitement de l'intervalle audio NÉGATIF
                    process_audio_file(audio_file_path, saving_folder=saving_folder_neg, start_time=start_time_processed_neg, 
                                                end_time=end_time_processed_neg, batch_size = neg_per_int, save=True)
            print(f"OK pour {audio_file_path}")
            break
        except Exception as e:
            continue
        

def count_lines_in_csv(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        return sum(1 for row in reader)


# Main function
def main():
    # Chemin du fichier CSV
    csv_file_path = "DNN_whistle_detection/Train_model/AllWhistlesSubClustering_final.csv"
    total_lines = count_lines_in_csv(csv_file_path)
    # Chemin du dossier contenant les fichiers audio WAV
    audio_folder_path = "/media/zf31/Dolphins/Sound/" 

    # Dossier de sauvegarde des images
    saving_folder = "DNN_whistle_detection/Train_model/whistles_from_csv/test"
    # saving_folder = "DNN_whistle_detection/Train_model/whistles_from_csv/ugly_coherent_images"
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
