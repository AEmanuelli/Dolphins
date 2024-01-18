import cv2
import pandas as pd
import os
from tqdm import tqdm
import numpy as np
from multiprocessing import Pool
import cProfile
import pstats

def split_frame_into_quadrants(frame, frame_width, frame_height):
    """This function divides a given video frame into four equal quadrants: 
    upper left, upper right, lower left, and lower right. It takes the entire frame 
    and its dimensions as input and returns a list of four sub-frames (quadrants)."""

    upper_left = frame[0:frame_height//2, 0:frame_width//2]
    upper_right = frame[0:frame_height//2, frame_width//2:]
    lower_left = frame[frame_height//2:, 0:frame_width//2]
    lower_right = frame[frame_height//2:, frame_width//2:]

    return [upper_left, upper_right, lower_left, lower_right]

# def process_quadrant(quadrant, background, contour_threshold):
#     """processes a single quadrant of a video frame to detect motion. It first converts the quadrant to grayscale and applies Gaussian blurring. 
#     Then, it calculates the absolute difference between the quadrant and a background reference frame, 
#     thresholds the difference to identify significant changes, and dilates the result. 
#     Motion detection is based on finding contours in the thresholded image that exceed a specified size (contour_threshold). It returns a boolean indicating whether 
#     motion was detected in the quadrant."""
    

#     # Convert to grayscale and blur
#     quadrant = cv2.cvtColor(quadrant, cv2.COLOR_BGR2GRAY)
#     quadrant = cv2.GaussianBlur(quadrant, (21, 21), 0)
#         # print(f"Quadrant Shape: {quadrant.shape}")
#         # print(f"Background Shape: {background.shape}")
#     # Check if the dimensions (size) match
#     if quadrant.shape[:2] != background.shape[:2]:
#         raise ValueError("Quadrant and background should have the same dimensions")
#     # Detect motion
#     diff_frame = cv2.absdiff(quadrant, background)
#     _, thresh_frame = cv2.threshold(diff_frame, 3, 255, cv2.THRESH_BINARY)
#     thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

#     cnts, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     motion_detected = any(cv2.contourArea(contour) >= contour_threshold for contour in cnts)

#     return motion_detected
def process_quadrant(quadrant, background, contour_threshold):
    # Convert to grayscale and blur
    quadrant = cv2.cvtColor(quadrant, cv2.COLOR_BGR2GRAY)
    # quadrant = cv2.GaussianBlur(quadrant, (7, 7), 0)

    if quadrant.shape[:2] != background.shape[:2]:
        raise ValueError("Quadrant and background should have the same dimensions")

    # Detect motion
    diff_frame = cv2.absdiff(quadrant, background)
    _, thresh_frame = cv2.threshold(diff_frame, 50, 255, cv2.THRESH_BINARY)
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=1)

    cnts, _ = cv2.findContours(thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) >= contour_threshold:
            print(f"Motion detected! Contour Area: {cv2.contourArea(contour)}")  # Debugging line
            return True  # Early termination if large contour is found

    return False  # No large contour found

def find_dolphins_in(video_path, duration_threshold=2.0, contour_threshold=4000, skip_frames=1):
    already_added_to_list = [False, False, False, False]
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Failed to read the video: {video_path}")
        return pd.DataFrame()

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_dir = os.path.join(os.path.dirname(video_path), "detected_dolphins")
    os.makedirs(output_dir, exist_ok=True)

    motion_detected = [False, False, False, False]  # For each quadrant
    motion_before = [False, False, False, False]  # For each quadrant
    motion_times = [[0, 0], [0, 0], [0, 0], [0, 0]]  # Start and end times for motion in each quadrant
    video_writer = None
    frame_count = 0
    current_output_path = ""
    ret, first_frame = cap.read()
    if not ret:
        print(f"Failed to read the first frame of the video: {video_path}")
        cap.release()
        return pd.DataFrame()
    quadrants = split_frame_into_quadrants(first_frame, frame_width, frame_height)
    backgrounds = [cv2.cvtColor(q, cv2.COLOR_BGR2GRAY) for q in quadrants]

    rows_list = []  # To store the details of each motion segment
    motion_in_frame = False
    frame_buffer = []  # Buffer to store frames
    motion_segment_started = False
    already_added_to_list = [False, False, False, False]  # Track if motion data is already added to the list for each quadrant

    with tqdm(total=total_frames, desc=f"Processing Video {video_path}") as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            motion_in_frame = False  # Reset motion flag for the current frame
            quadrants = split_frame_into_quadrants(frame, frame_width, frame_height)

            for i, quadrant in enumerate(quadrants):
                if i >= 2:
                    break
                motion_detected[i] = process_quadrant(quadrant, backgrounds[i], contour_threshold)

                if motion_detected[i]:
                    if not motion_before[i]:
                        motion_times[i][0] = frame_count / fps
                        motion_before[i] = True
                    motion_times[i][1] = frame_count / fps
                    current_duration = motion_times[i][1] - motion_times[i][0]
                    print(f"Quadrant {i+1} Current Motion Duration: {current_duration} seconds")
                elif motion_before[i]:
                    duration = motion_times[i][1] - motion_times[i][0]
                    if duration >= duration_threshold:
                        motion_in_frame = True
                        if not already_added_to_list[i]:
                            rows_list.append({"Segment": len(rows_list) + 1, "Start": motion_times[i][0], "End": motion_times[i][1], "File": current_output_path, "Quadrant": i+1})
                            already_added_to_list[i] = True
                    motion_before[i] = False
                    motion_times[i] = [0, 0]
                    already_added_to_list[i] = False

            if motion_in_frame:
                if not motion_segment_started:
                    motion_segment_started = True
                    frame_buffer = []

                frame_buffer.append(frame)
            elif motion_segment_started:
                # Save the buffered frames as a video segment
                current_output_path = os.path.join(output_dir, f"segment_{frame_count}.mp4")
                video_writer = cv2.VideoWriter(current_output_path, fourcc, fps, (frame_width, frame_height))

                for buffered_frame in frame_buffer:
                    video_writer.write(buffered_frame)

                video_writer.release()
                video_writer = None
                motion_segment_started = False

            frame_count += 1
            pbar.update(1)

        if video_writer is not None:
            video_writer.release()

    cap.release()


def analyze_videos_in_folder(folder_path):

    """
    This function iterates through all the MP4 video files in a given directory, 
    applies the find_dolphins_in function to each video, and aggregates the results. 
    For each video, it generates a CSV file with the analysis results, which includes information 
    about detected motion segments. 
    Finally, it compiles all individual video analyses into a single DataFrame and saves it as a CSV file. 
    This function provides a comprehensive analysis of all video files in a specified folder.
    """

    global_df = pd.DataFrame()

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.mp4'):
                video_path = os.path.join(root, file)
                try :
                    # Profiling
                    profile = cProfile.Profile()
                    profile.enable()
                    
                    motion_df = find_dolphins_in(video_path)

                    profile.disable()
                    profile_output_file = os.path.join(root, file.rsplit('.', 1)[0] + '_profile_stats.prof')
                    with open(profile_output_file, 'w') as f:
                        ps = pstats.Stats(profile, stream=f)
                        ps.sort_stats('cumulative').print_stats()
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

# Main execution
video_directory = '/home/alexis/Desktop/video'
out_dir = '/home/alexis/Desktop/video_out'
folder_path = video_directory
global_motion_df = analyze_videos_in_folder(folder_path)
print(global_motion_df)


# ValueError: bad marshal data (unknown type code)
# # Replace with your .prof file path
# prof_file_path = '/home/alexis/Desktop/video/testvideo_2min_profile_stats.prof'

# p = pstats.Stats(prof_file_path)
# p.sort_stats('cumulative').print_stats(10)  # Adjust the number to display more or fewer lines 
