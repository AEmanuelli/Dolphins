import os
import csv
from datetime import datetime
from tqdm import tqdm

def extract_info(filename):
    parts = filename.split('_')
    exp_name = parts[0]
    date_str = '_'.join(parts[1:4])
    time_str = parts[4].split('-')[0]
    datetime_str = f"{date_str} {time_str}"
    start_time = datetime.strptime(datetime_str, "%d_%b_%Y_%I%M%p")
    return exp_name, start_time

def main():
    folder_path_1 = "/media/DOLPHIN/Analyses_alexis/dataset/_last/positives"  # Remplacez cela par le chemin de votre dossier
    output_csv_1 = "positives.csv"
    folder_path_0 = "/media/DOLPHIN/Analyses_alexis/dataset/_last/negatives"  # Remplacez cela par le chemin de votre dossier
    output_csv_0 = "negatives.csv"
    
    files_0 = sorted(os.listdir(folder_path_0))
    files_1 = sorted(os.listdir(folder_path_1))
    
    with open(output_csv_0, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Nom de l\'expérience', 'Temps de début'])
        
        for file in tqdm(files_0, desc="Traitement des fichiers dans le dossier negatives"):
            if file.endswith('.jpg'):
                exp_name, start_time = extract_info(file)
                writer.writerow([exp_name, start_time])
                
    with open(output_csv_1, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Nom de l\'expérience', 'Temps de début'])
        
        for file in tqdm(files_1, desc="Traitement des fichiers dans le dossier positives"):
            if file.endswith('.jpg'):
                exp_name, start_time = extract_info(file)
                writer.writerow([exp_name, start_time])

if __name__ == "__main__":
    main()
