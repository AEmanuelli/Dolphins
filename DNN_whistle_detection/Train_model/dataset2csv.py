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

if __name__ == "__main__":
    main()
