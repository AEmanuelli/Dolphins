import os
import re
import numpy as np
import pandas as pd
from scipy.io import wavfile
from scipy.signal import spectrogram, blackman
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
import moviepy.editor as mp
import os
from tqdm import tqdm
#%%
# =============================================================================
#********************* FUNCTIONS : Whistle to video 
# =============================================================================

def convertir_texte_en_csv(fichier_texte, fichier_csv, delimiteur="\t", skip_lines = 1):
    """
    Convertit un fichier texte en fichier CSV en traitant une ligne sur deux.

    Args:
        fichier_texte (str): Chemin vers le fichier texte d'entrée.
        fichier_csv (str): Chemin vers le fichier CSV de sortie.
        delimiteur (str, optional): Délimiteur utilisé dans le fichier texte. Par défaut, '\t' (tabulation).
    """
    # Ouvrir le fichier texte en mode lecture
    with open(fichier_texte, 'r') as file:
        lignes = file.readlines()  # Lire toutes les lignes du fichier texte

    # Ouvrir le fichier CSV en mode écriture
    with open(fichier_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Parcourir chaque ligne du fichier texte, en commençant par la deuxième ligne (indice 1)
        for i in range(skip_lines, len(lignes), skip_lines):
            ligne = lignes[i]  # Sélectionner la ligne correspondante
            # Séparer les données en colonnes en utilisant le délimiteur
            colonnes = ligne.strip().split(delimiteur)
            # Écrire les colonnes dans le fichier CSV
            writer.writerow(colonnes)

    print("Conversion terminée avec succès.")

def lire_csv_extraits(nom_fichier):
    intervals = []
    with open(nom_fichier, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Passer à la deuxième ligne pour ignorer le titre des colonnes
        for row in reader:
            try:
                # Convertir les valeurs en nombres flottants et les ajouter à la liste
                debut = float(row[0])
                fin = float(row[1])
                intervals.append((debut, fin))
            except ValueError:
                # Gérer les erreurs de conversion en nombres flottants dans la première colonne
                #print("Erreur de conversion en nombre flottant. La première colonne sera ignorée.")
                debut = float(row[1])
                fin = float(row[2])  # Commencer à partir de la deuxième colonne
                intervals.append((debut, fin))
    return intervals

def fusionner_intervalles(intervalles, hwindow=4):
    # Trier les intervalles par début
    intervalles.sort(key=lambda x: x[0])
    
    # Initialiser la liste résultante
    intervalles_fusionnes = []
    
    # Parcourir les intervalles
    for intervalle in intervalles:
        debut, fin = intervalle
        
        # Arrondir la borne initiale à la seconde inférieure et convertir en entier
        debut_arrondi = int(debut) - hwindow
        
        # Arrondir la borne finale à la seconde supérieure et convertir en entier
        fin_arrondi = int(fin + 0.9999) + hwindow
        
        # Si la liste résultante est vide ou si l'intervalle ne se chevauche pas avec le dernier intervalle fusionné
        if not intervalles_fusionnes or debut_arrondi > intervalles_fusionnes[-1][1]:
            intervalles_fusionnes.append((debut_arrondi, fin_arrondi))
        else:
            # Fusionner l'intervalle avec le dernier intervalle fusionné
            intervalles_fusionnes[-1] = (intervalles_fusionnes[-1][0], max(intervalles_fusionnes[-1][1], fin_arrondi))
    
    # Ajuster les bornes du premier et du dernier intervalle fusionné si nécessaire
    if intervalles_fusionnes:
        premier_intervalle = intervalles_fusionnes[0]
        dernier_intervalle = intervalles_fusionnes[-1]
        
        if premier_intervalle[0] < 0:
            premier_intervalle = (0, premier_intervalle[1])
        
        if dernier_intervalle[1] > 1800:
            dernier_intervalle = (dernier_intervalle[0], 1800)
        
        intervalles_fusionnes[0] = premier_intervalle
        intervalles_fusionnes[-1] = dernier_intervalle
    
    return intervalles_fusionnes

def trouver_fichier_video(fichier_csv, dossier_videos = "/media/DOLPHIN/2023/"):
    # Extraire la date et l'heure du nom de fichier CSV
    elements_nom_csv = fichier_csv.split("_")
    date_heure_csv = elements_nom_csv[1] + "_"+ elements_nom_csv[2] + "_" + elements_nom_csv[3] + "_"+elements_nom_csv[4]  # Format: "Aug_2023_0845"

    # Parcourir tous les fichiers vidéo dans le dossier
    for fichier_video in os.listdir(dossier_videos):
        if fichier_video.endswith(".mp4"):
            try: 
                # Extraire la date et l'heure du nom de fichier vidéo
                elements_nom_video = fichier_video.split("_")
                date_heure_video = elements_nom_video[1] + "_" + elements_nom_video[2] + "_" + elements_nom_video[3] + "_" + elements_nom_video[4]  # Format: "Aug_2023_1645"
            except IndexError: 
                # print(f"{fichier_video} n'a pas le bon format.")
                continue
            # Comparer les dates et heures pour trouver une correspondance
            if date_heure_csv == date_heure_video:
                return os.path.join(dossier_videos, fichier_video)

    print(f"Aucun fichier vidéo correspondant trouvé pour le fichier CSV {fichier_csv}")
    return None
#%%
# =============================================================================
#********************* UTILISATION
# =============================================================================


fichier_texte = "/media/DOLPHIN_ALEXIS/temp_alexis/Label_01_Aug_2023_0845_channel_1.txt"
fichier_csv = "/media/DOLPHIN_ALEXIS/temp_alexis/Label_01_Aug_2023_0845_channel_1.csv"


#********************* txt vers csv
# # Spécifiez le chemin vers le fichier texte d'entrée et le fichier CSV de sortie

# convertir_texte_en_csv(fichier_texte, fichier_csv, skip_lines=1)





# #********************* csv vers intervalles 
# nom_fichier = "/media/DOLPHIN_ALEXIS/temp_alexis/labels_channel_1.csv"
# intervalles = lire_csv_extraits(nom_fichier)
# intervalles_fusionnes = fusionner_intervalles(intervalles, hwindow = 5)
# print(intervalles_fusionnes)


# #********************* intervalles vers extraits
# fichier_video = "/media/DOLPHIN_ALEXIS/temp_alexis/1_08/Exp_01_Aug_2023_1645_cam_all.mp4"  # Chemin vers le fichier vidéo d'entrée
# dossier_sortie = "./extraits/channel_1"
# extraire_extraits_video(intervalles_fusionnes, fichier_video, dossier_sortie)


# import matlab.engine
# eng = matlab.engine.start_matlab()
# # Run a MATLAB script
# eng.eval("/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/save_spectrogram.m", nargout=0)

# # Call a MATLAB function
# result = eng.my_matlab_function(arg1, arg2)



def transform_file_name(file_name):
    # Utilisation d'une expression régulière pour extraire les parties nécessaires du nom de fichier
    match = re.match(r'Exp_(\d{2})_(\w{3})_(\d{4})_(\d{4})_channel_(\d)', file_name)
    if match:
        day = match.group(1)
        month = match.group(2)
        year = match.group(3)[2:]  # Récupération des deux derniers chiffres de l'année
        time = match.group(4)
        channel = match.group(5)
        transformed_name = f"{day}_{month}_{year}_{time}_c{channel}"
        return transformed_name
    else:
        return None

def prepare_csv_data(file_path, record_names, positive_initial, positive_finish):
    part = file_path.split('wav-')

    name = part[0] + "wav"
    record_names.append(name)
    
    ini = part[1].replace(".jpg", "")
    ini = float(ini)
    positive_initial.append(ini)
    
    fin = ini + 0.8
    fin = round(fin, 1)
    positive_finish.append(fin)
    
    return record_names, positive_initial, positive_finish

def save_csv(record_names, positive_initial, positive_finish, class_1_scores, csv_path):
    df = {'file_name': record_names,
    'initial_point': positive_initial,
    'finish_point': positive_finish,
    'confidence': class_1_scores}

    df = pd.DataFrame(df)
    
    df.to_csv(csv_path, index=False)

def process_audio_file(file_path, saving_folder="./images", batch_size=50, start_time=0, end_time=None, save=False, wlen=2048,
                       nfft=2048, sliding_w=0.4, cut_low_frequency=3, cut_high_frequency=20, target_width_px=903,
                       target_height_px=677):
    try:
        # Load sound recording
        fs, x = wavfile.read(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found.")
    
    # Create the saving folder if it doesn't exist
    if save and not os.path.exists(saving_folder):
        os.makedirs(saving_folder)
    
    # Calculate the spectrogram parameters
    hop = round(0.8 * wlen)  # window hop size
    win = blackman(wlen, sym=False)

    images = []
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    N = len(x)  # signal length

    if end_time is not None:
        N = min(N, int(end_time * fs))

    low = int(start_time * fs)
    
    samples_per_slice = int(sliding_w * fs)

    for _ in range(batch_size):
        if low + samples_per_slice > N:  # Check if the slice exceeds the signal length
            break
        x_w = x[low:low + samples_per_slice]
        
        # Calculate the spectrogram
        f, t, Sxx = spectrogram(x_w, fs, nperseg=wlen, noverlap=hop, nfft=nfft, window=win)
        Sxx = 20 * np.log10(np.abs(Sxx))  # Convert to dB

        # Create the spectrogram plot
        fig, ax = plt.subplots()
        ax.pcolormesh(t, f / 1000, Sxx, cmap='gray')
        ax.set_ylim(cut_low_frequency, cut_high_frequency)

        ax.set_axis_off()  # Turn off axis
        fig.set_size_inches(target_width_px / plt.rcParams['figure.dpi'], target_height_px / plt.rcParams['figure.dpi'])
        
        # Adjust margins
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
      
        # Save the spectrogram as a JPG image without borders
        if save:
            image_name = os.path.join(saving_folder, f"{file_name}-{low/fs}.jpg")
            fig.savefig(image_name, dpi=plt.rcParams['figure.dpi'])  # Save without borders

        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        images.append(image)

        low += samples_per_slice

    plt.close('all')  # Close all figures to release memory

    return images
