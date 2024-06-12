# =============================================================================
#********************* IMPORTS
# =============================================================================
import warnings
import os
import numpy as np
from scipy.io import wavfile
from tqdm import tqdm 
import cv2
from tensorflow.keras.applications.vgg16 import preprocess_input
import tensorflow as tf
import concurrent.futures
from utils import *
import argparse
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Ignorer les messages d'information et de débogage de TensorFlow

 

Newly_path = "/media/DOLPHIN_ALEXIS/Analyses_alexis/2023_analysed/Newly_detected_whistles"
model_path = "/users/zfne/emanuell/Downloads/MPFTACC95+.h5"

model_name = os.path.basename(model_path).split(".")[0]
print(f"Model name: {model_name}")

Newly_path = os.path.join(Newly_path, model_name)

# =============================================================================
#********************* FUNCTIONS
# =============================================================================

def process_and_predict(file_path, batch_duration, start_time, end_time, batch_size, model, save_p, saving_folder_file):
    print("Predicting:", file_path)
    file_name = os.path.basename(file_path)
    transformed_file_name = transform_file_name(file_name)
    fs, x = wavfile.read(file_path)
    N = len(x)

    if end_time is not None:
        N = min(N, int(end_time * fs))

    total_duration = (N / fs) - start_time
    record_names = []
    positive_initial = []
    positive_finish = []
    class_1_scores = []
    num_batches = int(np.ceil(total_duration / batch_duration))

    for batch in tqdm(range(num_batches), desc=f"Batches for {transformed_file_name}", leave=False, colour='blue'):
        start = batch * batch_duration + start_time
        images = process_audio_file(file_path, saving_folder_file, batch_size=batch_size, start_time=start, end_time=end_time)
        print("flag0")
        saving_positive = os.path.join(saving_folder_file, "positive")
        
        image_batch = []
        time_batch = []

        for idx, image in enumerate(images):
            im_cop = image
            image_start_time = round(start + idx * 0.4, 2)
            image_end_time = round(image_start_time + 0.4, 2)

            image = cv2.resize(image, (224, 224))
            image = np.expand_dims(image, axis=0)
            image = preprocess_input(image)
            
            image_batch.append(image)
            time_batch.append((im_cop, image_start_time, image_end_time))

        if image_batch:
            print("flag0.5")
            image_batch = np.vstack(image_batch)
            predictions = model.predict(image_batch, verbose=0)
            print("flag0.6")
            print("Predictions:", predictions)
            for idx, prediction in enumerate(predictions):
                im_cop, image_start_time, image_end_time = time_batch[idx]
                print("flag0.7")
                if prediction[1] > prediction[0]:
                    record_names.append(file_name)
                    positive_initial.append(image_start_time)
                    positive_finish.append(image_end_time)
                    class_1_scores.append(prediction[1])
                    print("flag1")
                    if save_p:
                        if not os.path.exists(saving_positive):
                            os.makedirs(saving_positive)
                        image_name = os.path.join(saving_positive, f"{image_start_time}-{image_end_time}.jpg")
                        if not os.path.exists(image_name):

                            name_saving_folder = saving_folder_file.split("/")[-1]
                            new_image_name = os.path.join(Newly_path, name_saving_folder, f"{image_start_time}-{image_end_time}.jpg")
                            try : 
                                os.makedirs(os.path.join(Newly_path, name_saving_folder), exist_ok=True)
                                cv2.imwrite(new_image_name, im_cop)
                                print(f"Saving positive image: {new_image_name}")
                            except:
                                print(f"Error saving image: {new_image_name}")

    return record_names, positive_initial, positive_finish, class_1_scores

def process_predict_extract_worker(file_name, recording_folder_path, saving_folder, start_time, end_time, batch_size, 
                                   save_p, model, pbar):
    # pbar.set_postfix(file=file_name)
    date_and_channel = os.path.splitext(file_name)[0]
    
    print("Processing:", date_and_channel) 
    saving_folder_file = os.path.join(Newly_path, f"{date_and_channel}")
    os.makedirs(saving_folder_file, exist_ok=True)
    prediction_file_path = os.path.join(saving_folder_file, f"{date_and_channel}.wav_predictions.csv")

    file_path = os.path.join(recording_folder_path, file_name)

    if not file_name.lower().endswith(".wav")  :#or ("channel_2" in file_path): #and os.path.exists(saving_positive)):
        print(f"Non-audio or channel 2 or already predicted : {file_name}. Skipping processing.")
        return

    batch_duration = batch_size * 0.4
    record_names, positive_initial, positive_finish, class_1_scores = process_and_predict(file_path, batch_duration, start_time, end_time, batch_size, model, save_p, saving_folder_file)
    save_csv(record_names, positive_initial, positive_finish, class_1_scores, prediction_file_path)    
    # process_prediction_file(prediction_file_path, file_name, recording_folder_path)
    pbar.update()

def process_predict_extract(recording_folder_path, saving_folder, start_time=0, end_time=1800, batch_size=50, 
                            save=False, save_p=True, model_path="models/model_vgg.h5", max_workers = 16, specific_files = None):
    files = os.listdir(recording_folder_path)
    sorted_files = sorted(files, key=lambda x: os.path.getctime(os.path.join(recording_folder_path, x)), reverse=False)
    
    if specific_files:
        sorted_files = sorted(specific_files, key=lambda x: os.path.getctime(os.path.join(recording_folder_path, x)), reverse=False)


    mask_count = 0  # Compteur pour les fichiers filtrés par le masque
    model = tf.keras.models.load_model(model_path)
    print(f"Model loaded from {model}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []

        with tqdm(total=len(files), desc="Files that are not going to be processed right now : ", position=0, leave=True, colour='green') as pbar:
            for file_name in sorted_files:
                file_path = os.path.join(recording_folder_path, file_name)
                prediction_file_path = os.path.join(saving_folder, f"{file_name}_predictions.csv")
                mask = not file_name.lower().endswith('.wav')
                    
                if mask:
                    mask_count += 1
                    pbar.update(1)  # Incrémenter la barre de progression pour les fichiers filtrés
                    continue
                
                future = executor.submit(process_predict_extract_worker, file_name, recording_folder_path, 
                                         saving_folder, start_time, end_time, batch_size, save_p, model, pbar)
                future.add_done_callback(lambda _: pbar.update(1))  # Mettre à jour la barre de progression lorsque le thread termine
                futures.append(future)

            for future in concurrent.futures.as_completed(futures):
                future.result()


def read_file_list(file_path):
    """Read a list of files from a text file."""
    with open(file_path, 'r') as file:
        files = file.read().splitlines()
    return files

if __name__ == "__main__":
    # # Définition des paramètres par défaut
    # default_model_path = "DNN_whistle_detection/models/model_vgg.h5"
    # default_root = "/media/DOLPHIN/Analyses_alexis/2023_analysed/"
    # default_recordings = "/media/DOLPHIN/2023/"
    # default_saving_folder = '/media/DOLPHIN_ALEXIS/Analyses_alexis/2023_analysed/'
    # default_start_time = 0
    # default_end_time = None
    # default_batch_size = 64
    # default_save = False
    # default_save_p = True
    # default_max_workers = 8
    # default_exit = "/media/DOLPHIN/Analyses_alexis/Extracted_segments/2023/"
    # parser.add_argument('--audio_only_saving_folder', default=default_exit, help='Enregistrer extraits audios ou ?')
# ******************FAADIL PC PARAMS

    # Define default parameters
    default_model_path = model_path
    default_root = "/media/DOLPHIN_ALEXIS/Analyses_alexis/2023_analysed/"
    default_recordings = "/media/DOLPHIN_ALEXIS/2023"#"/media/DOLPHIN_ALEXIS/2023/"
    default_saving_folder = '/media/DOLPHIN_ALEXIS/Analyses_alexis/2023_analysed/'
    default_start_time = 0
    default_end_time = None
    default_batch_size = 64
    default_save = False
    default_save_p = True
    default_max_workers = 1


    # Analyse des arguments de la ligne de commande
    parser = argparse.ArgumentParser(description='Description du script')
    parser.add_argument('--model_path', default=default_model_path, help='Chemin vers le modèle')
    parser.add_argument('--root', default=default_root, help='Chemin vers le répertoire racine')
    parser.add_argument('--recordings', default=default_recordings, help='Chemin vers les enregistrements')
    parser.add_argument('--saving_folder', default=default_saving_folder, help='Dossier de sauvegarde')

    parser.add_argument('--start_time', type=int, default=default_start_time, help='Temps de début')
    parser.add_argument('--end_time', type=int, default=default_end_time, help='Temps de fin')
    parser.add_argument('--batch_size', type=int, default=default_batch_size, help='Taille du lot')
    parser.add_argument('--save', type=bool, default=default_save, help='Enregistrer ou non')
    parser.add_argument('--save_p', type=bool, default=default_save_p, help='Enregistrer ou non Positifs')
    parser.add_argument('--max_workers', type=int, default=default_max_workers, help='Nombre maximal de travailleurs')
    parser.add_argument('--specific_files', help='Chemin vers un fichier contenant la liste des fichiers à traiter')
    
    args = parser.parse_args()

    # Lire la liste des fichiers spécifiques si fournie
    specific_files = read_file_list(args.specific_files) if args.specific_files else None

    # Appel des fonctions avec les paramètres définis
    process_predict_extract(args.recordings, args.saving_folder, args.start_time, args.end_time, args.batch_size, args.save, args.save_p, args.model_path, args.max_workers, specific_files = specific_files)
    # process_prediction_files_in_folder(args.root, args.recordings, args.max_workers, exit = args.audio_only_saving_folder, audio=False, audio_only= True)




