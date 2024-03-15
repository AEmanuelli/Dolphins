import tensorflow as tf
import threading
from predict_online_parallel import process_predict_extract

# Définir le dossier contenant les anciens fichiers CSV
dossier_anciens_csv = "/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/predictions"
dossier_csv = "/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/2023"  # Update with your actual path
model_path = "models/model_vgg.h5"
recording_folder_path = "/media/DOLPHIN_ALEXIS1/2023"  # Update with your actual path
saving_folder = '/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/2023'  # Update with your actual path
dossier_anciens_csv = "/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/predictions"  # Update with your actual path
# Paramètres pour le profilage
run_metadata = tf.compat.v1.RunMetadata()
opts = tf.compat.v1.profiler.ProfileOptionBuilder.float_operation()

# Créer une fonction pour l'exécution de process_predict_extract avec le profilage
def run_with_profiling():
    with tf.compat.v1.Session() as sess:
        process_predict_extract(
            recording_folder_path,
            saving_folder,
            start_time=0,
            end_time=1800,
            batch_size=75,
            save=False,
            save_p=True,
            model_path="models/model_vgg.h5",
            max_workers=32,
            sess=sess,  # Passer la session TensorFlow à la fonction
            run_metadata=run_metadata
        )

        # Récupérer les informations de profilage
        flops = tf.compat.v1.profiler.profile(
            graph=sess.graph,
            run_meta=run_metadata,
            cmd='op', options=opts
        )

        # Afficher les informations de profilage
        print(f"Total floating point operations: {flops.total_float_ops}")

# Démarrer le profilage dans un thread séparé
profiling_thread = threading.Thread(target=run_with_profiling)
profiling_thread.start()

# Continuer l'exécution de votre programme principal ici
# ...
