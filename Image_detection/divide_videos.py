import os
import subprocess
from multiprocessing import Pool
import pandas as pd

def splitin4(args):
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
        p.map(splitin4, tasks)

    print("All videos have been split and saved.")

# # Example usage
# video_directory = '/home/alexis/Desktop/Test_combo_launch/step 0/'
# out_dir = '/home/alexis/Desktop/Test_combo_launch/step 1/'
# split_videos_in_directory(video_directory, out_dir=out_dir)


