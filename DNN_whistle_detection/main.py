# from predict_online import process_and_predict
from predict_online import *
from whistle2vid import lire_csv_extraits, fusionner_intervalles, extraire_extraits_video, trouver_fichier_video

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
    process_and_predict(recording_folder_path, saving_folder_image, start_time=1780, end_time=1800, save_p =True, save=False)

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


if __name__ == "__main__":
    main()
