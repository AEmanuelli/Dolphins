import os
import shutil

import os
import shutil
import os
import shutil
# from predict_online_parallel import process_prediction_files_in_folderpr

# =============================================================================
#********************* MERGE
# =============================================================================
                    
def move_csv_files(folder1, folder2, folder3):
    for root, dirs, files in os.walk(folder3):
        for file in files:
            if file.endswith(".csv"):
                try:
                    video_file_wav = "_".join(file.split("_")[0:7])
                    source_file_path = os.path.join(root, file)
                    video_file = os.path.splitext(video_file_wav)[0]
                    video_target_dir = os.path.join(folder1, video_file)
                    video_target_dir_wav = os.path.join(folder1, video_file_wav)

                    # Check if the target directories exist with or without .wav extension
                    if os.path.exists(video_target_dir):
                        target_dir = video_target_dir
                    elif os.path.exists(video_target_dir_wav):
                        target_dir = video_target_dir_wav
                    else:
                        raise FileNotFoundError("No matching video directory found.")

                    # Move the CSV file to the target directory
                    target_csv_path = os.path.join(target_dir, file)
                    os.makedirs(target_dir, exist_ok=True)
                    shutil.move(source_file_path, target_csv_path)
                    print(f"Moved CSV file to folder: {target_csv_path}")

                except IndexError:
                    print(f"Error: No matching video file found for {file}.")
                except Exception as e:
                    print(f"An error occurred: {e}")


# Chemins des dossiers
dossier_2023_extraits = "/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/2023"
dossier_extraits = "/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/extraits"
dossier_predictions = "/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/predictions"

# move_csv_files(dossier_2023_extraits, dossier_extraits, dossier_predictions)
# print("Fusion des dossiers terminée avec succès !")



# =============================================================================
#********************* Juste extraits
# =============================================================================


import os

def rename_folders(directory):
    for root, dirs, files in os.walk(directory):
        for d in dirs:
            if os.path.isdir(os.path.join(root, d)):  # Vérifie si c'est un dossier
                old_name = os.path.join(root, d)
                new_name = os.path.join(root, d.rstrip('.wav'))  # Supprime '.wav' s'il est présent
                if old_name != new_name:
                    os.rename(old_name, new_name)
                    print(f"Renamed folder: {old_name} to {new_name}")

# Exemple d'utilisation
directory = "/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/2023"  # Remplacez par le chemin absolu ou relatif du dossier
# rename_folders(directory)

def rename_subfolders(parent_folder):
    for root, dirs, files in os.walk(parent_folder):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            subdirs = next(os.walk(dir_path))[1]  # Liste des sous-dossiers
            
            for subdir_name in subdirs:
                subdir_path = os.path.join(dir_path, subdir_name)
                
                # Vérifier si le nom du sous-dossier commence par les 10 premiers caractères du nom du dossier parent
                if subdir_name.startswith(os.path.basename(dir_path)[:10]):
                    new_name = "extraits"
                    new_subdir_path = os.path.join(dir_path, new_name)
                    
                    # Renommer le sous-dossier interne
                    os.rename(subdir_path, new_subdir_path)
                    print(f"Sous-dossier renommé : {subdir_path} -> {new_subdir_path}")
        break

# Chemin du dossier parent
# parent_folder = "/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/2023"

# Appel de la fonction pour renommer les sous-dossiers
# rename_subfolders(parent_folder)
# Liste pour stocker les noms des dossiers de niveau 1 ne contenant pas de sous-dossier nommé "positive"


parent_folder = "/media/DOLPHIN/Analyses_alexis/2023_analysed/"
folders_without_positive_subfolder = []
i=0
for directory in os.listdir(parent_folder):
    subfolder_path = os.path.join(parent_folder, directory)
    if os.path.isdir(subfolder_path):  # Vérifie si c'est un dossier
        
        if all(subdir not in os.listdir(subfolder_path) for subdir in ["extraits", "pas_d_extraits"]):
            folders_without_positive_subfolder.append(subfolder_path)
        # if directory+".wav" in os.listdir(subfolder_path) : 
        #     import shutil
        #     mab = os.path.join(subfolder_path,directory+".wav" )
        #     print(mab)
        #     shutil.rmtree(mab)
        #     ####


print(len(folders_without_positive_subfolder))
for i, folder in enumerate(folders_without_positive_subfolder):
    print(folder)
    if i>10:
        break