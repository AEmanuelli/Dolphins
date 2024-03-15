from process_predictions import process_prediction_files_in_folder
from predict_online_parallel import process_predict_extract

# Redirection de la sortie standard et d'erreur de TensorFlow vers /dev/null (Unix) ou NUL (Windows)
# if os.name == 'posix':  # Unix
#     os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Ignorer les messages d'information et de débogage de TensorFlow
#     sys.stdout = open(os.devnull, 'w')
#     sys.stderr = open(os.devnull, 'w')

if __name__ == "__main__":
    dossier_csv = "/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/2023"  # Update with your actual path
    model_path = "models/model_vgg.h5"
    recording_folder_path = "/media/DOLPHIN_ALEXIS1/2023"  # Update with your actual path
    saving_folder = '/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/2023'  # Update with your actual path
    dossier_anciens_csv = "/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/predictions"  # Update with your actual path
    process_predict_extract(recording_folder_path, saving_folder, start_time=0, 
                            end_time=1800, batch_size=75, save=False, save_p=True, 
                            model_path="models/model_vgg.h5", max_workers = 16)

    process_prediction_files_in_folder(dossier_csv, max_workers = 16)