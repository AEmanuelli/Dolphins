import os
import subprocess
from utils import Checkpoint


repertoire_videos = '/home/alexis/Desktop/test-divide-vids'

# Créer un sous-répertoire pour les vidéos divisées
sous_repertoire_divisees = os.path.join(repertoire_videos, 'video_divided_"')

os.makedirs(sous_repertoire_divisees, exist_ok=True)


# Parcours de tous les fichiers vidéo dans le répertoire
for nom_fichier in os.listdir(repertoire_videos):
    chemin_fichier = os.path.join(repertoire_videos, nom_fichier)
    
    # Ignorer les fichiers qui ne sont pas des vidéos
    if not nom_fichier.endswith('.mp4'):
        continue
    
    else :
        # Liste des positions et des numéros correspondants
        positions = ['supérieur gauche', 'supérieur droit', 'inférieur gauche', 'inférieur droit']
        numeros = ['11', '12', '21', '22']
        
        # Diviser la vidéo d'origine en quatre sous-vidéos en utilisant crop
        for position, numero in zip(positions, numeros):
            nom_sortie = f'{nom_fichier.split(".")[0]}_{numero}.mp4'
            chemin_sortie = os.path.join(sous_repertoire_divisees, nom_sortie)
            if os.path.isfile(chemin_sortie):
                print(f"Le fichier {nom_sortie} existe déjà. Passage à l'étape suivante.")
                continue
            # Utilisation de ffmpeg pour découper la vidéo en utilisant crop
            crop_value = '1920:1080:0:0' if 'supérieur gauche' in position else '1920:1080:1920:0' if 'supérieur droit' in position else '1920:1080:0:1080' if 'inférieur gauche' in position else '1920:1080:1920:1080'
            subprocess.run([
                'ffmpeg',
                '-i', chemin_fichier,
                '-vf', f"crop={crop_value}",
                '-c:a', 'copy',
                chemin_sortie
            ])

print("Toutes les sous-vidéos ont été créées en utilisant crop sans augmenter la taille finale.")