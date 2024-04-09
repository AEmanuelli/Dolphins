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
    # lower_right = frame[frame_height//2:, frame_width//2:]

    return [upper_left, upper_right, lower_left]#, lower_right]

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
# def process_quadrant(quadrant, background, contour_threshold):
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
def process_quadrant(quadrant, background, contour_threshold,threshold =30 ):
    """
    Process each quadrant to detect motion. Modified to check the number of channels before converting to grayscale.
    """
    # Check if the quadrant is already in grayscale
    if len(quadrant.shape) == 3 and quadrant.shape[2] == 3:
        quadrant = cv2.cvtColor(quadrant, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(quadrant, background)
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    motion = False
    for contour in contours:
        if cv2.contourArea(contour) > contour_threshold:
            motion = True
            break
    return motion
# def find_dolphins_in(video_path, duration_threshold=2.0, contour_threshold=4000, skip_frames=1):
#     already_added_to_list = [False, False, False, False]
#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         print(f"Failed to read the video: {video_path}")
#         return pd.DataFrame()

#     fps = cap.get(cv2.CAP_PROP_FPS)
#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     output_dir = os.path.join(os.path.dirname(video_path), "detected_dolphins")
#     os.makedirs(output_dir, exist_ok=True)

#     motion_detected = [False, False, False, False]  # For each quadrant
#     motion_before = [False, False, False, False]  # For each quadrant
#     motion_times = [[0, 0], [0, 0], [0, 0], [0, 0]]  # Start and end times for motion in each quadrant
#     video_writer = None
#     frame_count = 0
#     current_output_path = ""
#     ret, first_frame = cap.read()
#     if not ret:
#         # print(f"Failed to read the first frame of the video: {video_path}")
#         cap.release()
#         return pd.DataFrame()
#     quadrants = split_frame_into_quadrants(first_frame, frame_width, frame_height)
#     backgrounds = [cv2.cvtColor(q, cv2.COLOR_BGR2GRAY) for q in quadrants]

#     rows_list = []  # To store the details of each motion segment
#     motion_in_frame = False
#     frame_buffer = []  # Buffer to store frames
#     motion_segment_started = False
#     already_added_to_list = [False, False, False, False]  # Track if motion data is already added to the list for each quadrant

#     with tqdm(total=total_frames, desc=f"Processing Video {video_path}") as pbar:
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             motion_in_frame = False  # Reset motion flag for the current frame
#             quadrants = split_frame_into_quadrants(frame, frame_width, frame_height)

#             for i, quadrant in enumerate(quadrants):
#                 if i >= 2:
#                     break
#                 motion_detected[i] = process_quadrant(quadrant, backgrounds[i], contour_threshold)
#                 duration = motion_times[i][1] - motion_times[i][0]
#                 print(f"Quadrant {i+1} Current Motion Duration: {duration} seconds")
#                 if motion_detected[i]:
#                     if not motion_before[i]:
#                         motion_times[i][0] = frame_count / fps
#                         motion_before[i] = True
#                     motion_times[i][1] = frame_count / fps
                    
                    
#                 elif motion_before[i]:
                    
#                     if duration >= duration_threshold:
#                         motion_in_frame = True
#                         if not already_added_to_list[i]:
#                             rows_list.append({"Segment": len(rows_list) + 1, "Start": motion_times[i][0], "End": motion_times[i][1], "File": current_output_path, "Quadrant": i+1})
#                             already_added_to_list[i] = True
#                     motion_before[i] = False
#                     motion_times[i] = [0, 0]
#                     already_added_to_list[i] = False

#             # if motion_in_frame:
#             #     # if not motion_segment_started:
#             #     #     motion_segment_started = True
#             #     #     frame_buffer = []
#             #     frame_buffer.append(frame)

#             # elif motion_segment_started:
#             #     # Save the buffered frames as a video segment
#             #     current_output_path = os.path.join(output_dir, f"segment_{frame_count}.mp4")
#             #     video_writer = cv2.VideoWriter(current_output_path, fourcc, fps, (frame_width, frame_height))

#             #     for buffered_frame in frame_buffer:
#             #         video_writer.write(buffered_frame)

#                 # video_writer.release()
#                 # video_writer = None
#                 motion_segment_started = False


#             #background update is to be implemented here 
                

#             frame_count += 1
#             pbar.update(1)

#         if video_writer is not None:
#             video_writer.release()

#     cap.release()
#     return  pd.DataFrame(rows_list) 


def find_motion_in_video_matrix(video_path, contour_threshold=1900, threshold = 30, skip_frames=3, bf_size = 5):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Failed to read the video: {video_path}")
        return np.array([])

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Initialize the backgrounds and buffers for each quadrant
    ret, first_frame = cap.read()
    if not ret:
        cap.release()
        return np.array([])

    quadrants = split_frame_into_quadrants(first_frame, frame_width, frame_height)
    backgrounds = [cv2.cvtColor(q, cv2.COLOR_BGR2GRAY) for q in quadrants]
    buffers = [[bg] for bg in backgrounds]

    # Create a numpy array to store motion data for each frame
    motion_matrix = np.zeros((total_frames // skip_frames, 3), dtype=bool)

    frame_processed = 0
    for frame_idx in tqdm(range(total_frames), desc=f"Processing Video {video_path}"):
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % skip_frames == 0:
            quadrants = split_frame_into_quadrants(frame, frame_width, frame_height)

            for i, quadrant in enumerate(quadrants):
                gray_quadrant = cv2.cvtColor(quadrant, cv2.COLOR_BGR2GRAY)
                
                # Update the buffer
                buffers[i].append(gray_quadrant)
                if len(buffers[i]) > bf_size:
                    buffers[i].pop(0)

                # Compute the running mean for the background
                updated_background = np.mean(buffers[i], axis=0).astype(np.uint8)
                
                motion_matrix[frame_processed, i] = process_quadrant(gray_quadrant, updated_background, contour_threshold, threshold = threshold)
                if motion_matrix[frame_processed, i]:
                    break

            frame_processed += 1

    cap.release()
    return motion_matrix



#a tester 
def convert_matrix_to_motion_times(motion_matrix, fps=10, sf=3, duration_threshold = 2.0):
    """
    Convert the motion matrix to motion times.
    Each row in the matrix corresponds to a frame, and each column to a quadrant.
    """
    num_frames, num_quadrants = motion_matrix.shape
    motion_times = {quadrant: [] for quadrant in range(num_quadrants)}


    for quadrant in range(num_quadrants):
        start_frame = None
        for frame in range(num_frames):
            if motion_matrix[frame, quadrant] and start_frame is None:
                start_frame = frame
            elif not motion_matrix[frame, quadrant] and start_frame is not None:
                end_frame = frame
                start_time = start_frame * sf / fps
                end_time = end_frame * sf / fps
                duration = end_time - start_time
                if duration >= duration_threshold:
                    motion_times[quadrant].append((start_time, end_time))
                start_frame = None

        # Check if the last segment extends to the end of the video and meets duration threshold
        if start_frame is not None:
            end_time = num_frames * sf / fps
            duration = end_time - (start_frame * sf / fps)
            if duration >= duration_threshold:
                motion_times[quadrant].append((start_frame * sf / fps, end_time))

    return motion_times



# def find_motion_in_video_matrix_optimized(video_path, contour_threshold=4000, skip_frames=1):
#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         print(f"Failed to read the video: {video_path}")
#         return np.array([])

#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#     ret, first_frame = cap.read()
#     if not ret:
#         cap.release()
#         return np.array([])

#     quadrants = split_frame_into_quadrants(first_frame, frame_width, frame_height)
#     backgrounds = [cv2.cvtColor(q, cv2.COLOR_BGR2GRAY) for q in quadrants]

#     # Create a numpy array to store motion data for each frame
#     # The size is reduced based on the skip_frames factor
#     motion_matrix = np.zeros((total_frames // skip_frames, 4), dtype=bool)

#     frame_idx = 0
#     for _ in tqdm(range(total_frames // skip_frames), desc=f"Processing Video {video_path}"):
#         if not ret:
#             break

#         quadrants = split_frame_into_quadrants(frame, frame_width, frame_height)

#         for i, quadrant in enumerate(quadrants):
#             gray_quadrant = process_quadrant_modified(quadrant, backgrounds[i], contour_threshold)
#             motion_matrix[frame_idx, i] = gray_quadrant

#         frame_idx += 1
#         # Skip the specified number of frames
#         for _ in range(skip_frames):
#             ret, frame = cap.read()

#     cap.release()
#     return motion_matrix

# Optimized function call (still requires a video file):
# video_path = "/path/to/your/video.mp4"
# motion_matrix = find_motion_in_video_matrix_optimized(video_path)
# print(motion_matrix)


# Example usage:
# fps = 30  # Frame rate of the video
# motion_times = convert_matrix_to_motion_times(motion_matrix, fps)
# print(motion_times)





# # Créer un objet de profilage
# profiler = cProfile.Profile()
# profiler.enable()

# sf = 3
# bf = 8
# thresh = 1800
# threshold = 30
# # Example usage (commented out as it requires a video file):
# video_path = "/home/alexis/Desktop/video/testvideo_2min.mp4"
# motion_matrix = find_motion_in_video_matrix(video_path,contour_threshold=thresh, bf_size = bf, skip_frames=sf)
# print(motion_matrix)

# np.save("/home/alexis/Desktop/video/mm.npy", motion_matrix)

# mm = np.load("/home/alexis/Desktop/video/mm.npy")
# mt = convert_matrix_to_motion_times(mm, 10, sf=sf)
# print(mt)
# profiler.disable()

# # Créer des statistiques à partir des données profilées
# stats = pstats.Stats(profiler).sort_stats('cumtime')
# stats.print_stats()



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

# # Main execution
# video_directory = '/home/alexis/Desktop/video'
# out_dir = '/home/alexis/Desktop/video_out'
# folder_path = video_directory
# global_motion_df = analyze_videos_in_folder(folder_path)
# print(global_motion_df)

import cProfile
import pstats
import numpy as np
import cv2  # Assurez-vous que OpenCV est installé
from tqdm import tqdm

# Assurez-vous que les fonctions find_motion_in_video_matrix et convert_matrix_to_motion_times sont définies

# Valeurs de paramètres à tester
contour_thresholds = [1500, 1800, 2100, 2400, 2700]
bf_sizes = [3, 5, 8, 10, 12]
skip_frames_values = [1, 2, 3, 4, 5]
thresholds = [20, 30, 40, 50, 60]

# Chemin vers la vidéo
video_path = "/home/alexis/Desktop/video/testvideo_2min.mp4"

# Fichier pour sauvegarder les résultats
results_file = "/home/alexis/Desktop/video/results.txt"

with open(results_file, "w") as file:
    for thresh in contour_thresholds:
        for bf in bf_sizes:
            for sf in skip_frames_values:
                for threshold in thresholds:
                    profiler = cProfile.Profile()
                    profiler.enable()

                    # Exécuter la détection de mouvement
                    motion_matrix = find_motion_in_video_matrix(video_path, contour_threshold=thresh, bf_size=bf, skip_frames=sf, threshold=threshold)

                    # Sauvegarder et charger la matrice de mouvement
                    filename = f"/home/alexis/Desktop/video/mm_thresh{thresh}_bf{bf}_sf{sf}_threshold{threshold}.npy"
                    np.save(filename, motion_matrix)
                    mm = np.load(filename)

                    # Convertir en temps de mouvement
                    mt = convert_matrix_to_motion_times(mm, 10, sf=sf)

                    profiler.disable()

                    # Calculer le nombre d'instants dans le quadrant 1
                    num_instants_quadrant_1 = len(mt[0])

                    # Écrire les résultats dans le fichier
                    file.write(f"thresh={thresh}, bf={bf}, sf={sf}, threshold={threshold}, Instants Quadrant 1: {num_instants_quadrant_1}\n")

                    # Profilage
                    stats = pstats.Stats(profiler)
                    stats.sort_stats('cumtime')
                    stats.dump_stats(filename.replace('.npy', '.prof'))

                    # Écrire les détails des temps de mouvement
                    file.write(str(mt) + "\n\n")à