import cv2
import pandas as pd
import os
from tqdm import tqdm
# from divide_videos import *
import os
import subprocess
from multiprocessing import Pool

def process_video_segment(args):
    file_path, out_path, position, number = args
    output_name = f'{os.path.basename(file_path).rsplit(".", 1)[0]}_{number}.mp4'
    output_path = os.path.join(out_path, output_name)
    if os.path.isfile(output_path):
        print(f"File {output_name} already exists. Skipping.")
        return

    crop_value = {
        'upper left': '1920:1080:0:0',
        'upper right': '1920:1080:1920:0',
        'lower left': '1920:1080:0:1080',
        'lower right': '1920:1080:1920:1080'
    }[position]

    command = [
    'ffmpeg',
    '-i', file_path,
    '-vf', f"crop={crop_value}",
    '-b:v', '2676k',
    '-c:v', 'libx264',  # Using libx264 instead of hardware acceleration
    '-preset', 'ultrafast',
    '-threads', '2',
    output_path
    ]
   
    subprocess.run(command, check=True)

def split_videos_in_directory(directory, out_dir, pool_size=4):
    positions = ['upper left', 'upper right', 'lower left']
    numbers = ['11', '12', '21']

    tasks = []
    for i, file_name in enumerate(os.listdir(directory)):
        if not file_name.endswith('.mp4') or i >50:
            continue

        file_path = os.path.join(directory, file_name)
        out_path = os.path.join(out_dir, file_name.rsplit(".", 1)[0])
        os.makedirs(out_path, exist_ok=True)

        for position, number in zip(positions, numbers):
            tasks.append((file_path, out_path, position, number))

    with Pool(pool_size) as p:
        p.map(process_video_segment, tasks)

    print("All videos have been split and saved.")

def find_dolphins_in(video_path, duration_threshold=1.71, contour_threshold=1850, skip_frames=3):
    """
    Detects dolphins in a video and saves segments longer than the duration threshold 
    in a "detected_dolphins" folder.

    :param video_path: Path to the video file
    :param duration_threshold: Duration in seconds to qualify as motion
    :param contour_threshold: Threshold for the size of the object to detect
    :return: DataFrame of motion event times and paths to the saved videos
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Failed to read the video: {video_path}")
        return pd.DataFrame()

    # Video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Prepare output directory
    output_dir = os.path.join(os.path.dirname(video_path), "detected_dolphins")
    os.makedirs(output_dir, exist_ok=True)

    # Initialize background subtraction
    ret, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    motion_list = [None, None]
    motion_times = []
    rows_list = []
    frame_count = 0
    video_writer = None
    current_output_path = ""

    with tqdm(total=total_frames // skip_frames, desc=f"Processing Video{video_path}") as pbar:
        while True:
            ret, frame = cap.read()
            if not ret : 
                break
            if frame_count % skip_frames != 0:
                frame_count += 1
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            diff_frame = cv2.absdiff(gray_frame, gray)
            thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
            thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

            cnts, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            motion = any(cv2.contourArea(contour) >= contour_threshold for contour in cnts)

            if motion:
                if video_writer is None:
                    motion_times.append(frame_count / fps)  # Start time
                    current_output_path = os.path.join(output_dir, f"segment_{len(rows_list) + 1}.mp4")
                    video_writer = cv2.VideoWriter(current_output_path, fourcc, fps, (frame_width, frame_height))

                video_writer.write(frame)
            elif video_writer is not None:
                video_writer.release()
                video_writer = None
                motion_times.append(frame_count / fps)  # End time
                if (motion_times[-1] - motion_times[-2]) > duration_threshold:
                    rows_list.append({"Segment": len(rows_list) + 1, "Start": motion_times[-2], "End": motion_times[-1], "File": current_output_path})

            frame_count += 1
            pbar.update(1)

    if video_writer is not None:
        video_writer.release()

    cap.release()
    return pd.DataFrame(rows_list)

def analyze_videos_in_folder(folder_path):
    global_df = pd.DataFrame()

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.mp4'):
                video_path = os.path.join(root, file)

                try:
                    motion_df = find_dolphins_in(video_path)
                    if not motion_df.empty:
                        # Create a CSV file in the same directory as the video, with a similar name
                        csv_file_name = file.rsplit('.', 1)[0] + '_analyzed.csv'
                        csv_file_path = os.path.join(root, csv_file_name)
                        motion_df.to_csv(csv_file_path, index=False)
                        print(f"Data saved to {csv_file_path}")

                    motion_df['video_name'] = file
                    global_df = pd.concat([global_df, motion_df], ignore_index=True)
                except Exception as e:
                    print(f"Error processing file {video_path}: {e}")

    # Save the global DataFrame as a CSV file in the main folder
    global_csv_path = os.path.join(folder_path, 'analyzed_videos_global_data.csv')
    global_df.to_csv(global_csv_path, index=False)
    print(f"Global data saved to {global_csv_path}")

    return global_df

video_directory = '/media/DOLPHIN/2023/'
out_dir = '/media/DOLPHIN/Test_alexis/'
split_videos_in_directory(video_directory, out_dir=out_dir)

# Utilisation de la fonction
folder_path = out_dir
global_motion_df = analyze_videos_in_folder(folder_path)
print(global_motion_df)




#, lancer un double combo split fichier puis analyse des vidéos

# vérifier le bon fonctionnement de mon parcours de fichier dasnun dossier pour trouver les mouvements. 
# essayer de reduire la tailled es fichiers en sortie de divide vids
# essayer d'implémenter Yolov5 : plusieurs options : 
    # 1 renvoyer les moments ou sont generees des prédictions issues d'un vocabulaire marin 
    # 2 renvoyer les moments ou les cadres sont générés dasnla vidéo générée sur Kaggle
    # 3 tenter une implémentation conjointe de mes deux méthodes : vocabulaire marin quand mouvement détécté ? fine tuning plus tard ? 
# comparer find dolphins in à une potentielle implémentation de Yolov5 
# Quand on génère les vidéos diviisées, le pooling a t'il un interet ? mesurer les temps d'execution vace test_video_2min, si non, ou minime, 
#   le checkpointintg est meilleur qaund on les fait une par une. En cas de bug,, les 4 sont niquées d'un coup    
