import cv2
import pandas as pd
import os
from tqdm import tqdm

def find_dolphins_in(video_path, duration_threshold=1.71, contour_threshold=1850*4):
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

    with tqdm(total=total_frames, desc="Processing Video") as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

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

# Example usage
video_path = "/home/alexis/Desktop/video/output.mp4"
motion_df = find_dolphins_in(video_path)
print(motion_df)


# Prochaine etape : ameliorer la fonction pour la generaluiser a dautre videos 