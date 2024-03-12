import os
import shutil

def move_files(source_dir, target_dir, file_extension):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(file_extension):
                source_file_path = os.path.join(root, file)
                target_file_path = os.path.join(target_dir, file)
                shutil.move(source_file_path, target_file_path)

def merge_folders(folder1, folder2, folder3):
    for root, dirs, files in os.walk(folder3):
        for file in files:
            if file.endswith(".csv"):
                source_file_path = os.path.join(root, file)
                # Extracting date and time from CSV filename
                date_time = "_".join(file.split("_")[2:4])
                # Finding corresponding video file
                video_file = f"Exp_{date_time}_channel_1.wav.mp4"
                video_source_dir = os.path.join(folder2, video_file)
                video_target_dir = os.path.join(folder1, date_time)
                os.makedirs(video_target_dir, exist_ok=True)
                # Moving CSV file to "extraits" folder
                shutil.move(source_file_path, folder2)
                # Moving video file to "2023_images" folder
                shutil.move(video_source_dir, video_target_dir)

# Chemins des dossiers
dossier_2023_extraits = "/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/2023_images"
dossier_extraits = "/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/extraits"
dossier_predictions = "/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/predictions"

# Fusion des dossiers
merge_folders(dossier_2023_extraits, dossier_extraits, dossier_predictions)

print("Fusion des dossiers terminée avec succès !")
