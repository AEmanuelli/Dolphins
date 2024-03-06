import csv
import moviepy.editor as mp
import os
from tqdm import tqdm
#%%
# =============================================================================
#********************* FUNCTIONS
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
                print("Erreur de conversion en nombre flottant. La première colonne sera ignorée.")
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

def extraire_extraits_video(intervalles, fichier_video, dossier_sortie='./'):
    # Chargement de la vidéo
    video = mp.VideoFileClip(fichier_video)
    
    # Vérifier si le dossier de sortie existe, sinon le créer
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)
    
    # Calculer le nombre total d'extraits à générer
    total_extraits = len(intervalles)
    
    # Afficher une barre de progression
    with tqdm(total=total_extraits, desc='Extraction des extraits') as pbar:
        # Parcourir les intervalles
        for i, intervalle in enumerate(intervalles):
            debut, fin = intervalle
            # Extraire l'extrait correspondant à l'intervalle
            extrait = video.subclip(debut, fin)
            nom_sortie = f'extrait_{debut}_{fin}.mp4'  # Nom de sortie basé sur l'intervalle
            chemin_sortie = os.path.join(dossier_sortie, nom_sortie)  # Chemin complet de sortie
            # Sauvegarder l'extrait vidéo
            extrait.write_videofile(chemin_sortie, verbose=False)
            pbar.update(1)  # Mettre à jour la barre de progression
    
    # Libérer la mémoire en supprimant l'objet VideoFileClip
    video.close()

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
