import argparse

from process_predictions import process_prediction_files_in_folder
# from predict_and_extract_online import process_predict_extract

def read_file_list(file_path):
    """Read a list of files from a text file."""
    with open(file_path, 'r') as file:
        files = file.read().splitlines()
    return files

if __name__ == "__main__":
    # Définition des paramètres par défaut
    default_model_path = "DNN_whistle_detection/models/model_vgg.h5"
    default_root = "/media/DOLPHIN/Analyses_alexis/2023_analysed/"
    default_recordings = "/media/DOLPHIN/2023/"
    default_saving_folder = '/media/DOLPHIN_ALEXIS/Analyses_alexis/2023_analysed/'
    default_start_time = 0
    default_end_time = None
    default_batch_size = 64
    default_save = False
    default_save_p = True
    default_max_workers = 8
    default_exit = "/media/DOLPHIN/Analyses_alexis/Extracted_segments/2023/"


    # Analyse des arguments de la ligne de commande
    parser = argparse.ArgumentParser(description='Description du script')
    parser.add_argument('--model_path', default=default_model_path, help='Chemin vers le modèle')
    parser.add_argument('--root', default=default_root, help='Chemin vers le répertoire racine')
    parser.add_argument('--recordings', default=default_recordings, help='Chemin vers les enregistrements')
    parser.add_argument('--saving_folder', default=default_saving_folder, help='Dossier de sauvegarde')

    parser.add_argument('--start_time', type=int, default=default_start_time, help='Temps de début')
    parser.add_argument('--end_time', type=int, default=default_end_time, help='Temps de fin')
    parser.add_argument('--batch_size', type=int, default=default_batch_size, help='Taille du lot')
    parser.add_argument('--save', type=bool, default=default_save, help='Enregistrer ou non')
    parser.add_argument('--save_p', type=bool, default=default_save_p, help='Enregistrer ou non Positifs')
    parser.add_argument('--max_workers', type=int, default=default_max_workers, help='Nombre maximal de travailleurs')
    parser.add_argument('--specific_files', help='Chemin vers un fichier contenant la liste des fichiers à traiter')
    parser.add_argument('--audio_only_saving_folder', default=default_exit, help='Enregistrer extraits audios ou ?')
    args = parser.parse_args()

    # Lire la liste des fichiers spécifiques si fournie
    specific_files = read_file_list(args.specific_files) if args.specific_files else None

    # Appel des fonctions avec les paramètres définis
    # process_predict_extract(args.recordings, args.saving_folder, args.start_time, args.end_time, args.batch_size, args.save, args.save_p, args.model_path, args.max_workers, specific_files = specific_files)
    process_prediction_files_in_folder(args.root, args.recordings, args.max_workers, exit = args.audio_only_saving_folder, audio=False, audio_only= True)

