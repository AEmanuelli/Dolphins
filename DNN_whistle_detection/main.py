# from predict_online import process_and_predict
from predict_online_parallel import *
from whistle2vid import lire_csv_extraits, fusionner_intervalles, extraire_extraits_video

# =============================================================================
#********************* MAIN
# =============================================================================
def main():
    model_path = "models/model_vgg.h5"
    # recording_folder_path = '/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/recordings'
    recording_folder_path = "/media/DOLPHIN_ALEXIS/2023"
    saving_folder_image = '/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/2023_images'
    dossier_csv = "/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/predictions"

    #********************* Créer les fichiers CSV 
    process_and_predict(recording_folder_path, saving_folder_image, start_time=0, end_time=1800, save_p =True, save=False)

    #********************* CSV vers intervalles 
    for fichier in os.listdir(dossier_csv):
        if fichier.endswith(".csv"):  # Vérifie si le fichier est un fichier CSV
            chemin_fichier = os.path.join(dossier_csv, fichier)
            intervalles = lire_csv_extraits(chemin_fichier)
            intervalles_fusionnes = fusionner_intervalles(intervalles, hwindow=5)
            print(intervalles_fusionnes)

            #********************* Trouver le fichier vidéo correspondant
            fichier_video = trouver_fichier_video(fichier, recording_folder_path)
            if fichier_video:
                filename = "_".join(os.path.splitext(fichier)[0].split("_")[:7])
                dossier_sortie_video = f"./extraits/{filename}"#_{channel}"
                os.makedirs(dossier_sortie_video, exist_ok=True)

                #********************* Intervalles vers extraits
                extraire_extraits_video(intervalles_fusionnes, fichier_video, dossier_sortie_video)

# Fonction pour trouver le fichier vidéo correspondant au fichier CSV
def trouver_fichier_video(fichier_csv, dossier_videos):
    # Extraire la date et l'heure du nom de fichier CSV
    elements_nom_csv = fichier_csv.split("_")
    date_heure_csv = elements_nom_csv[2] + "_" + elements_nom_csv[3]  # Format: "Aug_2023_0845"

    # Parcourir tous les fichiers vidéo dans le dossier
    for fichier_video in os.listdir(dossier_videos):
        if fichier_video.endswith(".mp4"):
            # Extraire la date et l'heure du nom de fichier vidéo
            elements_nom_video = fichier_video.split("_")
            date_heure_video = elements_nom_video[2] + "_" + elements_nom_video[3]  # Format: "Aug_2023_1645"

            # Comparer les dates et heures pour trouver une correspondance
            if date_heure_csv == date_heure_video:
                return os.path.join(dossier_videos, fichier_video)

    print(f"Aucun fichier vidéo correspondant trouvé pour le fichier CSV {fichier_csv}")
    return None

if __name__ == "__main__":
    main()
