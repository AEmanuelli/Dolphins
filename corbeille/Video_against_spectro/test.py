import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import imageio
import os

# Fonction pour générer le spectrogramme
def generate_spectrogram(audio_file, output_folder):
    # Charger le fichier audio
    y, sr = librosa.load(audio_file)

    # Calculer le spectrogramme
    D = np.abs(librosa.stft(y))
    plt.figure(figsize=(10, 5))
    librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max), sr=sr)
    plt.axis('off')
    
    # Enregistrer le spectrogramme en tant qu'image
    output_file = os.path.join(output_folder, "spectrogram.png")
    plt.savefig(output_file, bbox_inches='tight', pad_inches=0)
    plt.close()

    return output_file

# Fonction pour créer la vidéo spectrogramme
def create_spectrogram_video(spectrogram_image, audio_file, output_file):
    # Charger l'image du spectrogramme
    image = imageio.imread(spectrogram_image)

    # Récupérer la durée du fichier audio
    duration = librosa.get_duration(filename=audio_file)

    # Paramètres de la vidéo
    fps = 30
    duration_frames = int(duration * fps)

    # Créer la vidéo
    writer = imageio.get_writer(output_file, fps=fps)
    for _ in range(duration_frames):
        writer.append_data(image)
    writer.close()

# Utilisation des fonctions
audio_file = "/home/alexis/Desktop/Exp_15_Jul_2023_0945_channel_0.wav"
output_folder = "output_folder"
output_file = "/home/alexis/Desktop/video_spectrogramme.mp4"

# Créer le dossier de sortie s'il n'existe pas
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Générer le spectrogramme
spectrogram_image = generate_spectrogram(audio_file, output_folder)

# Créer la vidéo spectrogramme
create_spectrogram_video(spectrogram_image, audio_file, output_file)

# Supprimer l'image du spectrogramme si nécessaire
os.remove(spectrogram_image)
