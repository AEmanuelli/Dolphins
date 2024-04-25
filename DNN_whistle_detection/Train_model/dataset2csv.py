import os
import csv
from tqdm import tqdm

def extract_info(filename):
    parts = filename.rsplit('-', 1)
    file_name = parts[0]
    timing = parts[1].split('.')[0]  # Pour enlever l'extension de fichier (.jpg)
    return file_name, timing

def main():
    folder_path_1 = "/media/DOLPHIN/Analyses_alexis/dataset/_last/positives"  # Remplacez cela par le chemin de votre dossier
    output_csv_1 = "positives.csv"
    folder_path_0 = "/media/DOLPHIN/Analyses_alexis/dataset/_last/negatives"  # Remplacez cela par le chemin de votre dossier
    output_csv_0 = "negatives.csv"
    
    files_0 = sorted(os.listdir(folder_path_0))
    files_1 = sorted(os.listdir(folder_path_1))
    
    with open(output_csv_0, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File', 'Timing'])
        
        for file in tqdm(files_0, desc="Traitement des fichiers dans le dossier negatives"):
            if file.endswith('.jpg'):
                file_name, timing = extract_info(file)
                writer.writerow([file_name, timing])
                
    with open(output_csv_1, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File', 'Timing'])
        
        for file in tqdm(files_1, desc="Traitement des fichiers dans le dossier positives"):
            if file.endswith('.jpg'):
                file_name, timing = extract_info(file)
                writer.writerow([file_name, timing])


# if __name__ == "__main__":
#     main()

import os
import pandas as pd
import glob

# Chemins des répertoires contenant les images positives et négatives
positive_dir = "/media/DOLPHIN/Analyses_alexis/dataset/_last/positives"
negative_dir = "/media/DOLPHIN/Analyses_alexis/dataset/_last/negatives"
# Listes pour stocker les chemins des fichiers et les étiquettes
file_paths = []
labels = []

# Parcours des fichiers d'images positives
for file_path in glob.glob(os.path.join(positive_dir, '*.jpg')):
    file_paths.append(file_path)
    labels.append(1)  # Étiquette pour les images positives

# Parcours des fichiers d'images négatives
for file_path in glob.glob(os.path.join(negative_dir, '*.jpg')):
    file_paths.append(file_path)
    labels.append(0)  # Étiquette pour les images négatives

# Création du DataFrame
data = {'file_names': file_paths, 'labels': labels}
df = pd.DataFrame(data)

# Enregistrement du DataFrame en tant que fichier CSV
df.to_csv('dolphin_signal_train.csv', index=False)

print("Le fichier CSV a été généré avec succès !")


