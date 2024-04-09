import os 
import sys
# # Redirection de la sortie standard et d'erreur de TensorFlow vers /dev/null (Unix) ou NUL (Windows)
# if os.name == 'posix':  # Unix
#     # os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Ignorer les messages d'information et de débogage de TensorFlow
#     sys.stdout = open(os.devnull, 'w')
# #     sys.stderr = open(os.devnull, 'w')

from process_predictions import process_prediction_files_in_folder
# from predict_and_extract_online import process_predict_extract


if __name__ == "__main__":  
 
    model_path = "DNN_whistle_detection/models/model_vgg.h5"

    # Sur PC Faadil 
    # from predict_online_parallel import process_predict_extract

    # recordings = "/media/DOLPHIN_ALEXIS/2023"  
    # saving_folder = '/media/DOLPHIN_ALEXIS/Analyses_alexis/2023_analysed' 
    # root = "/media/DOLPHIN_ALEXIS/Analyses_alexis/2023_analysed" 
    
    # # Sur PC Alexis

    root = "/media/DOLPHIN/Analyses_alexis/2023_analysed/"  
    recordings = "/media/DOLPHIN/2023/" 
    saving_folder = '/media/DOLPHIN/Analyses_alexis/2023_analysed/'

    dossier_anciens_csv = "/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/predictions"  #plus à jour 
    # process_predict_extract(recordings, saving_folder, start_time=0, 
    #                         end_time=1800, batch_size=75, save=False, save_p=True, 
    #                         model_path="DNN_whistle_detection/models/model_vgg.h5", max_workers = 8)

    process_prediction_files_in_folder(root, recording_folder_path=recordings, max_workers = 10)
