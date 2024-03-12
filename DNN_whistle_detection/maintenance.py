import concurrent.futures
import os
from tqdm import tqdm
import joblib
import os
from tqdm import tqdm
from predict_online_parallel import process_predict_extract_worker, process_prediction_files_in_folder
import joblib
import os
from tqdm import tqdm

def process_predict_extract_joblib(recording_folder_path, saving_folder, start_time=1750, end_time=1800, batch_size=50, save=False, save_p=True, model_path="models/model_vgg.h5", csv_path="predictions.csv"):
    files = os.listdir(recording_folder_path)
    mask_count = 0  # Compteur pour les fichiers filtrés par le masque

    with tqdm(total=len(files), desc="Processing Files", position=0, leave=False, colour='green') as pbar:
        joblib.Parallel(n_jobs=16, prefer="threads")(joblib.delayed(process_file)(file_name, recording_folder_path, saving_folder, start_time, end_time, batch_size, save_p, model_path, csv_path, pbar) for file_name in files)

def process_predict_extract_process_pool(recording_folder_path, saving_folder, start_time=1750, end_time=1800, batch_size=50, save=False, save_p=True, model_path="models/model_vgg.h5", csv_path="predictions.csv"):
    files = os.listdir(recording_folder_path)
    mask_count = 0  # Compteur pour les fichiers filtrés par le masque
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=16) as executor:
        futures = []
        with tqdm(total=len(files), desc="Processing Files", position=0, leave=False, colour='green') as pbar:
            for file_name in files:
                file_path = os.path.join(recording_folder_path, file_name)
                prediction_file_path = os.path.join(saving_folder, f"{file_name}.pkl")
                mask = (os.path.isdir(file_path) or 
                            not file_name.lower().endswith(('1.wav', '.wave', "0.wav")) or 
                            os.path.exists(prediction_file_path))
                    
                if mask:
                    mask_count += 1
                    pbar.update(1)  # Incrémenter la barre de progression pour les fichiers filtrés
                    continue
                
                future = executor.submit(process_predict_extract_worker, file_name, recording_folder_path, saving_folder, start_time, end_time, batch_size, save_p, model_path, csv_path, pbar)
                future.add_done_callback(lambda _: pbar.update(1))  # Mettre à jour la barre de progression lorsque le processus termine
                futures.append(future)

            for future in concurrent.futures.as_completed(futures):
                future.result()

def process_predict_extract(recording_folder_path, saving_folder, max_workers=16, start_time=1750, end_time=1800, batch_size=50, save=False, save_p=True, model_path="models/model_vgg.h5", csv_path="predictions.csv"):
    files = os.listdir(recording_folder_path)
    mask_count = 0  # Compteur pour les fichiers filtrés par le masque
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        with tqdm(total=len(files), desc="Processing Files", position=0, leave=False, colour='green') as pbar:
            for file_name in files:
                file_path = os.path.join(recording_folder_path, file_name)
                prediction_file_path = os.path.join(saving_folder, f"{file_name}.pkl")
                mask = (os.path.isdir(file_path) or 
                            not file_name.lower().endswith(('1.wav', '.wave', "0.wav")) or 
                            os.path.exists(prediction_file_path))
                    
                if mask:
                    mask_count += 1
                    pbar.update(1)  # Incrémenter la barre de progression pour les fichiers filtrés
                    continue
                
                future = executor.submit(process_predict_extract_worker, file_name, recording_folder_path, saving_folder, start_time, end_time, batch_size, save_p, model_path, csv_path, pbar)
                future.add_done_callback(lambda _: pbar.update(1))  # Mettre à jour la barre de progression lorsque le thread termine
                futures.append(future)

            for future in concurrent.futures.as_completed(futures):
                future.result()


if __name__ == "__main__":
    dossier_csv = "/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/predictions"  # Update with your actual path
    model_path = "models/model_vgg.h5"
    recording_folder_path = "/media/DOLPHIN_ALEXIS/2023"  # Update with your actual path
    saving_folder_image = '/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/2023_images'  # Update with your actual path
    dossier_csv = "/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/predictions"  # Update with your actual path
    process_predict_extract(recording_folder_path, saving_folder_image, start_time=0, 
                            end_time=1800, batch_size=50, save=False, save_p=True, 
                            model_path="models/model_vgg.h5", csv_path="predictions.csv")
    process_prediction_files_in_folder(dossier_csv)
