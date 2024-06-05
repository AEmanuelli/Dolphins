import os
import subprocess
from multiprocessing import Pool

def splitin4(args):
    file_path, out_path, position, number, crf, preset = args
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
        '-crf', str(crf),
        '-preset', preset,
        '-c:v', 'libx264',
        '-threads', '2',
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Created {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while processing {file_path}: {e}")

def split_videos_in_directory(directory, out_dir, pool_size=4, crf=23, preset='fast'):
    positions = ['upper left', 'upper right', 'lower left', 'lower right']
    numbers = ['11', '12', '21', '22']

    tasks = []
    for i, file_name in enumerate(os.listdir(directory)):
        if not file_name.endswith('.mp4') or i >= 50:
            continue

        file_path = os.path.join(directory, file_name)
        out_path = os.path.join(out_dir, file_name.rsplit(".", 1)[0])
        os.makedirs(out_path, exist_ok=True)

        for position, number in zip(positions, numbers):
            tasks.append((file_path, out_path, position, number, crf, preset))

    with Pool(pool_size) as p:
        p.map(splitin4, tasks)

    print("All videos have been split and saved.")

# Example usage
video_directory = '/home/alexis/Desktop/New_caméra/'
out_dir = '/home/alexis/Desktop/New_caméra/split/'
split_videos_in_directory(video_directory, out_dir=out_dir, crf=23, preset='fast')
