# =============================================================================
#********************* IMPORTS
# =============================================================================
import os
from concurrent.futures import ThreadPoolExecutor
from whistle2vid import *
import re

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

def extraire_extraits_video(intervalles, fichier_video, dossier_sortie_video):
    # Chargement de la vidéo
    video = mp.VideoFileClip(fichier_video)
    
    # Calculer le nombre total d'extraits à générer
    total_extraits = len(intervalles)
    
    # Afficher une barre de progression
    with tqdm(total=total_extraits, desc=f'Extraction pour {fichier_video}') as pbar:
        # Parcourir les intervalles
        for i, intervalle in enumerate(intervalles):
            debut, fin = intervalle
            nom_sortie = f'extrait_{debut}_{fin}.mp4'  # Nom de sortie basé sur l'intervalle

            chemin_sortie = os.path.join(dossier_sortie_video, nom_sortie)  # Chemin complet de sortie
            if not os.path.exists(chemin_sortie):
                # Extraire l'extrait correspondant à l'intervalle
                extrait = video.subclip(debut, fin)
                # Sauvegarder l'extrait vidéo
                extrait.write_videofile(chemin_sortie, verbose=False)
            else : 
                print("zbzbz")
        
    # Libérer la mémoire en supprimant l'objet VideoFileClip
    video.close()


def process_non_empty_file(prediction_file_path, folder_name, recording_folder_path, folder_path):
    intervalles = lire_csv_extraits(prediction_file_path)
    intervalles_fusionnes = fusionner_intervalles(intervalles, hwindow=5)
    # print(intervalles_fusionnes)
    print(folder_name)
    fichier_video = trouver_fichier_video(folder_name, recording_folder_path)
    if fichier_video:
        dossier_sortie_video = os.path.join(folder_path, "extraits")
        os.makedirs(dossier_sortie_video, exist_ok=True)


        # # A supprimer après le premier run 
        # import shutil
        # dossier_sortie_video_a_supprimer = os.path.join(item_path, "pas_d_extraits")
        # shutil.rmtree(dossier_sortie_video_a_supprimer) if os.path.exists(dossier_sortie_video_a_supprimer) else None
        # ####

        extraire_extraits_video(intervalles_fusionnes, fichier_video, dossier_sortie_video)

def handle_empty_file(folder_path, folder_name):
    dossier_sortie_video = os.path.join(folder_path, "pas_d_extraits")
    t_file_name = transform_file_name(folder_name)

    # A supprimer après le premier run 
    import shutil
    dossier_sortie_video_a_supprimer = os.path.join(folder_path, "extraits")
    shutil.rmtree(dossier_sortie_video_a_supprimer) if (os.path.exists(dossier_sortie_video_a_supprimer) and not os.listdir(dossier_sortie_video_a_supprimer)) else None
    ####

    os.makedirs(dossier_sortie_video, exist_ok=True)
    txt_file_path = os.path.join(dossier_sortie_video, f"No_whistles_detected.txt")
    with open(txt_file_path, 'w') as txt_file:
        txt_file.write(f"No whistles detected in {t_file_name} ")
    print(f"Empty CSV file for {t_file_name}. No video extraction will be performed. A message has been saved to {txt_file_path}.")

def handle_missing_file(folder_path, folder_name):
    t_file_name = transform_file_name(folder_name)
    dossier_sortie_video = os.path.join(folder_path, "pas_d_extraits")
    os.makedirs(dossier_sortie_video, exist_ok=True)
    txt_file_path = os.path.join(dossier_sortie_video, f"No_CSV_found.txt")
    with open(txt_file_path, 'w') as txt_file:
        txt_file.write(f"No CSV found in {t_file_name}")
    print(f"Missing CSV file for {t_file_name}. No video extraction will be performed.")

def process_prediction_file(prediction_file_path, folder_name, recording_folder_path, folder_path):
    t_file_name = transform_file_name(folder_name)
    print(f"processing : {t_file_name}")
    empty = False 
    if os.path.exists(prediction_file_path):
        # Check if the file is empty
        with open(prediction_file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) <= 1:
                empty = True
    else:
        # File is missing
        handle_missing_file(folder_path, folder_name)
        return

    if not empty:
        # File exists and is not empty
        process_non_empty_file(prediction_file_path, folder_name, recording_folder_path, folder_path)
    else:
        # File exists but is empty
        handle_empty_file(folder_path, folder_name)

def process_folder(root, folder_name, recording_folder_path, folder_path):
    csv_file_name = folder_name + ".wav_predictions.csv"
    # print(csv_file_name, csv_file_path)
    prediction_file_path = os.path.join(root, folder_name, csv_file_name)
    print("Prediction file path:", prediction_file_path)
    if os.path.exists(prediction_file_path): #s'assure de l'existence du ficheir csv
        process_prediction_file(prediction_file_path, folder_name, recording_folder_path, folder_path)

def process_prediction_files_in_folder(root, recording_folder_path, max_workers=8):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for folder_name in tqdm(os.listdir(root), leave=True):
            folder_path = os.path.join(root, folder_name)
            if os.path.isdir(folder_path):
                executor.submit(process_folder, root, folder_name, recording_folder_path, folder_path)
# def process_prediction_files_in_folder(folder_path, recording_folder_path="/media/DOLPHIN_ALEXIS1/2023", max_workers = 16):
#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         for root, _, files in os.walk(folder_path):
#             for file_name in files:
#                 if file_name.endswith(".csv"):
#                     prediction_file_path = os.path.join(root, file_name)
#                     docname = "_".join(os.path.splitext(file_name)[0].split("_")[:7])
#                     extract_folder_path = os.path.join(root, "extraits")
#                     executor.submit(process_prediction_file, prediction_file_path, file_name, recording_folder_path, extract_folder_path)
