# =============================================================================
#********************* IMPORTS
# =============================================================================
import os
from concurrent.futures import ThreadPoolExecutor
from whistle2vid import *
import tensorflow as tf

# =============================================================================
#********************* FUNCTIONS
# =============================================================================


def extraire_extraits_video(intervalles, fichier_video, dossier_sortie):
    # Chargement de la vidéo
    video = mp.VideoFileClip(fichier_video)
    
    # Vérifier si le dossier de sortie existe, sinon le créer
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)
    
    # Calculer le nombre total d'extraits à générer
    total_extraits = len(intervalles)
    
    # Afficher une barre de progression
    with tqdm(total=total_extraits, desc=f'Extraction pour {dossier_sortie}') as pbar:
        # Parcourir les intervalles
        for i, intervalle in enumerate(intervalles):
            debut, fin = intervalle
            nom_sortie = f'extrait_{debut}_{fin}.mp4'  # Nom de sortie basé sur l'intervalle

            chemin_sortie = os.path.join(dossier_sortie, nom_sortie)  # Chemin complet de sortie
            if not os.path.exists(chemin_sortie):
                # Extraire l'extrait correspondant à l'intervalle
                extrait = video.subclip(debut, fin)
                # Sauvegarder l'extrait vidéo
                extrait.write_videofile(chemin_sortie, verbose=False)
            else : 
                print("zbzbz")
        
    # Libérer la mémoire en supprimant l'objet VideoFileClip
    video.close()


def process_non_empty_file(prediction_file_path, file_name, recording_folder_path, dossier_sortie_video):
    intervalles = lire_csv_extraits(prediction_file_path)
    intervalles_fusionnes = fusionner_intervalles(intervalles, hwindow=5)
    # print(intervalles_fusionnes)

    fichier_video = trouver_fichier_video(file_name, recording_folder_path)
    if fichier_video:
        filename = "_".join(os.path.splitext(file_name)[0].split("_")[:7])
        os.makedirs(dossier_sortie_video, exist_ok=True)

        extraire_extraits_video(intervalles_fusionnes, fichier_video, dossier_sortie_video)

def handle_empty_file(dossier_sortie_video, file_name):
    txt_file_path = os.path.join(dossier_sortie_video, f"No_whistles_detected.txt")
    with open(txt_file_path, 'w') as txt_file:
        txt_file.write(f"No whistles detected in {file_name} ")
    print(f"Empty CSV file for {file_name}. No video extraction will be performed. A message has been saved to {txt_file_path}.")

def handle_missing_file(dossier_sortie_video, file_name):
    txt_file_path = os.path.join(dossier_sortie_video, f"No_CSV_found.txt")
    with open(txt_file_path, 'w') as txt_file:
        txt_file.write(f"No CSV found in {file_name}")
    print(f"Missing CSV file for {file_name}. No video extraction will be performed.")

def process_prediction_file(prediction_file_path, file_name, recording_folder_path, dossier_sortie_extraits):
    go = True 
    with open(prediction_file_path, 'r') as file:
        lines = file.readlines()
        if len(lines) <= 1:
            go = False
    if os.path.exists(prediction_file_path) and go :
        # File exists and is not empty
        process_non_empty_file(prediction_file_path, file_name, recording_folder_path, dossier_sortie_extraits)
    elif os.path.exists(prediction_file_path):
        # File exists but is empty
        handle_empty_file(dossier_sortie_extraits, file_name)
    else:
        # File is missing
        handle_missing_file(dossier_sortie_extraits, file_name)

def process_prediction_files_in_folder(folder_path, recording_folder_path="/media/DOLPHIN_ALEXIS1/2023", max_workers = 16):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith(".csv"):
                    prediction_file_path = os.path.join(root, file_name)
                    docname = "_".join(os.path.splitext(file_name)[0].split("_")[:7])
                    extract_folder_path = os.path.join(root, "extraits")
                    if not os.path.exists(extract_folder_path) or not os.listdir(extract_folder_path):
                        executor.submit(process_prediction_file, prediction_file_path, file_name, recording_folder_path, extract_folder_path)


