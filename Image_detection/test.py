import cv2
import pandas as pd
import os
from tqdm import tqdm
import numpy as np
from multiprocessing import Pool

def process_frame_quadrants(frame, contour_threshold, fps, frame_count, skip_frames, fourcc, frame_width, frame_height, output_dir):
    """
    Process each quadrant of the frame and return a list of detected motions
    """
    quadrants = {
        'upper left': frame[:frame_height // 2, :frame_width // 2],
        'upper right': frame[:frame_height // 2, frame_width // 2:],
        'lower left': frame[frame_height // 2:, :frame_width // 2],
        'lower right': frame[frame_height // 2:, frame_width // 2:]
    }
    if frame.shape[0] != frame_height or frame.shape[1] != frame_width:
        return  # Skip processing if frame size does not match
    for position, quadrant in quadrants.items():
        gray = cv2.cvtColor(quadrant, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        if position not in process_frame_quadrants.background_frames:
            process_frame_quadrants.background_frames[position] = gray
            continue

        diff_frame = cv2.absdiff(process_frame_quadrants.background_frames[position], gray)
        thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

        cnts, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        motion_detected = any(cv2.contourArea(contour) >= contour_threshold for contour in cnts)
        
        if motion_detected:
            if position not in process_frame_quadrants.video_writers:
                segment_file = os.path.join(output_dir, f"{position}_segment_{frame_count // fps}.mp4")
                process_frame_quadrants.video_writers[position] = cv2.VideoWriter(segment_file, fourcc, fps, (frame_width // 2, frame_height // 2))
            process_frame_quadrants.video_writers[position].write(quadrant)
        elif position in process_frame_quadrants.video_writers:
            process_frame_quadrants.video_writers[position].release()
            del process_frame_quadrants.video_writers[position]

        process_frame_quadrants.background_frames[position] = gray

# Initialize static variables for background frames and video writers
process_frame_quadrants.background_frames = {}
process_frame_quadrants.video_writers = {}

def find_dolphins_in(video_path, duration_threshold=1.71, contour_threshold=1850, skip_frames=3):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Failed to read the video: {video_path}")
        return pd.DataFrame()

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_dir = os.path.join(os.path.dirname(video_path), "detected_dolphins")
    os.makedirs(output_dir, exist_ok=True)

    with tqdm(total=total_frames // skip_frames, desc=f"Processing Video {video_path}") as pbar:
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % skip_frames != 0:
                frame_count += 1
                continue

            process_frame_quadrants(frame, contour_threshold, fps, frame_count, skip_frames, fourcc, frame_width, frame_height, output_dir)

            frame_count += 1
            pbar.update(1)

    # Release all video writers
    for writer in process_frame_quadrants.video_writers.values():
        writer.release()

    cap.release()

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

# Main execution (remains unchanged)
video_directory = '/media/DOLPHIN/2023/'
out_dir = '/media/DOLPHIN/Test_alexis/'
folder_path = out_dir
global_motion_df = analyze_videos_in_folder(folder_path)
print(global_motion_df)
