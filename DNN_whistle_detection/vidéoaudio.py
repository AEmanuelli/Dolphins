import os
from moviepy.editor import VideoFileClip, AudioFileClip
from tqdm import tqdm

def vidéoetaudio(intervalles, fichier_video, fichier_audio, dossier_sortie_video):
    # Chargement de la vidéo et de l'audio
    video = VideoFileClip(fichier_video)
    audio = AudioFileClip(fichier_audio)
    
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
                extrait_video = video.subclip(debut, fin)
                extrait_audio = audio.subclip(debut, fin)
                # Ajouter l'audio à la vidéo extraite
                extrait_video = extrait_video.set_audio(extrait_audio)
                # Sauvegarder l'extrait vidéo avec audio
                extrait_video.write_videofile(chemin_sortie, codec='libx264', audio_codec='aac', fps=video.fps, verbose=False)
            else : 
                print("zbzbz")
            pbar.update(1)
        
    # Libérer la mémoire en supprimant les objets VideoFileClip et AudioFileClip
    video.close()
    audio.close()
