# import argparse

# from process_predictions import process_prediction_files_in_folder
# from predict_and_extract_online import process_predict_extract

# def read_file_list(file_path):
#     """Read a list of files from a text file."""
#     with open(file_path, 'r') as file:
#         files = file.read().splitlines()
#     return files

# if __name__ == "__main__":
#     # Définition des paramètres par défaut
#     default_model_path = "DNN_whistle_detection/models/model_vgg.h5"
#     default_root = "/media/DOLPHIN_ALEXIS/Analyses_alexis/2023_analysed/"
#     default_recordings = "/media/DOLPHIN_ALEXIS/2023/"
#     default_saving_folder = '/media/DOLPHIN_ALEXIS/Analyses_alexis/2023_analysed/'
#     default_dossier_anciens_csv = "/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/predictions"
#     default_start_time = 0
#     default_end_time = None
#     default_batch_size = 75
#     default_save = False
#     default_save_p = True
#     default_max_workers = 8

#     # Analyse des arguments de la ligne de commande
#     parser = argparse.ArgumentParser(description='Description du script')
#     parser.add_argument('--model_path', default=default_model_path, help='Chemin vers le modèle')
#     parser.add_argument('--root', default=default_root, help='Chemin vers le répertoire racine')
#     parser.add_argument('--recordings', default=default_recordings, help='Chemin vers les enregistrements')
#     parser.add_argument('--saving_folder', default=default_saving_folder, help='Dossier de sauvegarde')
#     parser.add_argument('--dossier_anciens_csv', default=default_dossier_anciens_csv, help='Dossier des anciens fichiers CSV')
#     parser.add_argument('--start_time', type=int, default=default_start_time, help='Temps de début')
#     parser.add_argument('--end_time', type=int, default=default_end_time, help='Temps de fin')
#     parser.add_argument('--batch_size', type=int, default=default_batch_size, help='Taille du lot')
#     parser.add_argument('--save', type=bool, default=default_save, help='Enregistrer ou non')
#     parser.add_argument('--save_p', type=bool, default=default_save_p, help='Enregistrer ou non Positifs')
#     parser.add_argument('--max_workers', type=int, default=default_max_workers, help='Nombre maximal de travailleurs')
#     parser.add_argument('--specific_files', help='Chemin vers un fichier contenant la liste des fichiers à traiter')

#     args = parser.parse_args()

#     # Lire la liste des fichiers spécifiques si fournie
#     specific_files = read_file_list(args.specific_files) if args.specific_files else None

#     # Appel des fonctions avec les paramètres définis
#     process_predict_extract(args.recordings, args.saving_folder, args.start_time, args.end_time, args.batch_size, args.save, args.save_p, args.model_path, args.max_workers, specific_files = specific_files)
#     process_prediction_files_in_folder(args.root, args.recordings, args.max_workers, audio=True)

import os
import time

def get_creation_time(file_path):
    """
    Retourne le temps de création du fichier ou dossier en timestamp.
    """
    return os.path.getctime(file_path)

def write_new_folders_to_txt(reference_file, directory, output_file):
    """
    Écrit tous les dossiers créés après le fichier de référence dans un fichier texte.
    """
    # Obtient le temps de création du fichier de référence
    ref_time = get_creation_time(reference_file)
    
    # Ouvre le fichier de sortie en mode écriture
    with open(output_file, 'w') as f:
        # Parcourt tous les dossiers dans le répertoire spécifié
        for item_name in os.listdir(directory):
            item_path = os.path.join(directory, item_name)
            if os.path.isdir(item_path):
                # Vérifie si le dossier a été créé après le fichier de référence
                if get_creation_time(item_path) > ref_time:
                    f.write(f"{item_name}\n")
                    print(f"Dossier ajouté: {item_name}")

# Chemin du fichier de référence
reference_file = '/media/DOLPHIN/Analyses_alexis/2023_analysed/Exp_24_Dec_2023_1145_channel_1'
# Répertoire à analyser
directory = '/media/DOLPHIN/Analyses_alexis/2023_analysed'
# Chemin du fichier de sortie
output_file = '/media/DOLPHIN/Analyses_alexis/file.txt'

# Appelle la fonction pour écrire les nouveaux dossiers dans le fichier texte
# write_new_folders_to_txt(reference_file, directory, output_file)
import os
import shutil

def move_folders_from_txt_to_garbage(txt_file, src_directory, dst_directory):
    # Vérifie si le fichier texte existe
    if not os.path.exists(txt_file):
        print(f"Le fichier texte {txt_file} n'existe pas.")
        return
    
    # Vérifie si le répertoire de destination existe, sinon le crée
    if not os.path.exists(dst_directory):
        os.makedirs(dst_directory)
        print(f"Le répertoire destination {dst_directory} a été créé.")
    
    # Ouvre le fichier texte et lit les noms des dossiers
    with open(txt_file, 'r') as f:
        folders = f.readlines()
    
    # Parcourt chaque dossier listé dans le fichier texte
    for folder_name in folders:
        folder_name = folder_name.strip()
        src_folder_path = os.path.join(src_directory, folder_name)
        dst_folder_path = os.path.join(dst_directory, folder_name)
        
        # Vérifie si le dossier source existe
        if os.path.exists(src_folder_path):
            # Déplace le dossier
            shutil.move(src_folder_path, dst_folder_path)
            print(f"Dossier déplacé: {folder_name}")
        else:
            print(f"Le dossier {folder_name} n'existe pas dans {src_directory}.")

# Chemin du fichier texte contenant les noms des dossiers
txt_file = output_file
# Répertoire source
src_directory = '/media/DOLPHIN/Analyses_alexis/2023_analysed'
# Répertoire de destination
dst_directory = '/media/DOLPHIN/Analyses_alexis/potential_garbage'

# Appelle la fonction pour déplacer les dossiers
move_folders_from_txt_to_garbage(txt_file, src_directory, dst_directory)
