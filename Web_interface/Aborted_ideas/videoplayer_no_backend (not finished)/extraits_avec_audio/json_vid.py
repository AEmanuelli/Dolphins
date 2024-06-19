import os
import json

def list_videos(directory):
    videos = []
    for filename in os.listdir(directory):
        if filename.endswith('.mp4'):  # Filtrer les fichiers .mp4
            videos.append({'name': filename, 'src': os.path.join(directory, filename)})
    return videos

def write_to_json(videos, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(videos, json_file, indent=4)

# Répertoire contenant les vidéos
video_directory = 'Web_interface/videoplayer_no_backend (not finished)/extraits_avec_audio/'

# Liste des vidéos dans le répertoire spécifié
videos = list_videos(video_directory)

# Écriture des vidéos dans un fichier JSON
output_file = 'Web_interface/videoplayer_no_backend (not finished)/extraits_avec_audio/videos.json'
write_to_json(videos, output_file)

print(f"Les vidéos ont été écrites dans le fichier JSON '{output_file}'.")
