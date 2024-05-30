# empty 

# /media/DOLPHIN/Analyses_alexis/Batch_gestion/ZIPS_Batch1_ok/Batch1_csv (chunk2-5)/chunk3/Exp_01_Mar_2021_0745am.wav_predictions.csv
import os
import shutil

import os

def rename_folders_with_wav(root_folder):
    for root, dirs, files in os.walk(root_folder):
        for dir_name in dirs:
            if dir_name.endswith('.wav'):
                old_path = os.path.join(root, dir_name)
                new_path = os.path.join(root, dir_name[:-4])  # Remove .wav extension
                os.rename(old_path, new_path)
                print(f'Renamed: {old_path} -> {new_path}')

# Example usage:
# Replace 'your_folder_path' with the path to the folder containing subfolders to be renamed.




# Exemple d'utilisation
source_directory = '/media/DOLPHIN/Analyses_alexis/Batch_gestion/ZIPS_Batch1_ok/Batch1_csv (chunk2-5)/'
destination_directory = '/media/DOLPHIN/Analyses_alexis/2021_analysed/'
rename_folders_with_wav(destination_directory)


