import os
import shutil

import os
import shutil
import os
import shutil

def move_files(source_dir, target_dir, file_extension):
    print(f"Moving files with extension {file_extension} from {source_dir} to {target_dir}")
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(file_extension):
                source_file_path = os.path.join(root, file)
                target_file_path = os.path.join(target_dir, file)
                print(f"Moving {source_file_path} to {target_file_path}")
                try:
                    shutil.move(source_file_path, target_file_path)
                except Exception as e:
                    print(f"Error moving {source_file_path} to {target_file_path}: {e}")

def merge_folders(folder1, folder2, folder3):
    # print(f"Merging folders: {folder1}, {folder2}, {folder3}")
    for root, dirs, files in os.walk(folder3):
        for file in files:
            if file.endswith(".csv"):
                source_file_path = os.path.join(root, file)
                # print(f"Processing CSV file: {source_file_path}")
                try:
                    date_time_channel = "_".join(file.split("_")[1:7])
                    video_file = f"Exp_{date_time_channel}"
                    video_source_dir = os.path.join(folder2, video_file)
                    video_target_dir = os.path.join(folder1, video_file)
                    # print(f"CSV file: {source_file_path}, Video file: {video_source_dir}, Target directory: {video_target_dir}")
                    
                    if os.path.exists(video_source_dir):
                        os.makedirs(video_target_dir, exist_ok=True)
                        print(f"Moving video file to '2023_images' folder: {video_source_dir}")
                        shutil.move(video_source_dir, video_target_dir)
                        print(f"Moving CSV file to 'extraits' folder: {source_file_path}")
                        shutil.move(source_file_path, video_target_dir)
                    else:
                        continue
                        print(f"No matching video file found for {file}.")
                except IndexError:
                    print(f"Error: No matching video file found for {file}.")
                except Exception as e:
                    print(f"An error occurred: {e}")

# Chemins des dossiers
dossier_2023_extraits = "/media/DOLPHIN1/temp_alexis/fusion /2023_images"
dossier_extraits = "/media/DOLPHIN1/temp_alexis/fusion /extraits"
dossier_predictions = "/media/DOLPHIN1/temp_alexis/fusion /predictions"

# Fusion des dossiers
merge_folders(dossier_2023_extraits, dossier_extraits, dossier_predictions)

print("Fusion des dossiers terminée avec succès !")




