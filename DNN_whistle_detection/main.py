# from process_predictions import process_prediction_files_in_folder
from predict_online_parallel import process_predict_extract
import os 
import sys

# Redirection de la sortie standard et d'erreur de TensorFlow vers /dev/null (Unix) ou NUL (Windows)
if os.name == 'posix':  # Unix
    # os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Ignorer les messages d'information et de débogage de TensorFlow
    sys.stdout = open(os.devnull, 'w')
#     sys.stderr = open(os.devnull, 'w')

if __name__ == "__main__":
 
    model_path = "models/model_vgg.h5"
    # Sur PC Faadil 
    recording_folder_path = "/media/DOLPHIN_ALEXIS1/2023"  
    saving_folder = '/media/DOLPHIN_ALEXIS1/Analyses_alexis/2023_analysed' 
    dossier_csv = "/media/DOLPHIN_ALEXIS1/Analyses_alexis/2023_analysed" 
    
    # Sur PC Alexis
    # dossier_csv = "/media/DOLPHIN/Analyses_alexis/2023_analysed/"  
    # recording_folder_path = "/media/DOLPHIN/2023/" 
    # saving_folder = '/media/DOLPHIN/Analyses_alexis/2023_analysed/'

    dossier_anciens_csv = "/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/predictions"  #plus à jour 
    process_predict_extract(recording_folder_path, saving_folder, start_time=0, 
                            end_time=1800, batch_size=75, save=False, save_p=True, 
                            model_path="models/model_vgg.h5", max_workers = 8)

    # process_prediction_files_in_folder(dossier_csv, recording_folder_path=recording_folder_path, max_workers = 16)