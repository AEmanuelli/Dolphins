import os

def trouver_fichier_video(fichier_audio, dossier_videos):
    # Extraire la date et l'heure du nom de fichier audio
    nom_fichier_audio = os.path.basename(fichier_audio)
    elements_nom_audio = nom_fichier_audio.split("_")
    date_heure_audio = elements_nom_audio[2] + "_" + elements_nom_audio[3]  # Format: "Aug_2023_0845"

    # Parcourir tous les fichiers vidéo dans le dossier
    for fichier_video in os.listdir(dossier_videos):
        if fichier_video.endswith(".mp4"):
            # Extraire la date et l'heure du nom de fichier vidéo
            elements_nom_video = fichier_video.split("_")
            date_heure_video = elements_nom_video[2] + "_" + elements_nom_video[3]  # Format: "Aug_2023_1645"

            # Comparer les dates et heures pour trouver une correspondance
            if date_heure_audio == date_heure_video:
                return os.path.join(dossier_videos, fichier_video)

    return None  # Aucun fichier vidéo correspondant trouvé

# Chemin vers le dossier contenant les fichiers vidéo
dossier_videos = "/media/DOLPHIN_ALEXIS/temp_alexis/1_08"

# Exemple de nom de fichier audio
fichier_audio = "Exp_01_Aug_2023_0845_channel_1.wav"

# Rechercher le fichier vidéo correspondant
fichier_video_correspondant = trouver_fichier_video(fichier_audio, dossier_videos)

if fichier_video_correspondant:
    print("Fichier vidéo correspondant trouvé :", fichier_video_correspondant)
else:
    print("Aucun fichier vidéo correspondant trouvé.")
