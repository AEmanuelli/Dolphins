import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from scipy.signal.windows import blackman
from scipy.io import wavfile
from tqdm import tqdm
import cProfile
def generate_spectrograms(recording_folder_path, saving_folder, start_time=0, save=True):
    files = os.listdir(recording_folder_path)

    # Calculate the spectrogram parameters
    wlen = 2048  # window length
    hop = round(0.8 * wlen)  # window hop size
    nfft = 2048  # number of fft points
    sliding_w = 0.4  # sliding window size
    cut_low_frequency = 3  # cut below 3k
    cut_high_frequency = 20  # cut above 20k

    # Target image size in pixels
    target_width_px = 1166
    target_height_px = 880
    win = blackman(wlen, sym=False)

    images = []

    for file_name in tqdm(files, desc="Generating spectrograms"):
        if not os.path.isdir(os.path.join(recording_folder_path, file_name)):
            images += process_audio_file(file_name, recording_folder_path, saving_folder, start_time, save, wlen, hop, nfft, sliding_w, cut_low_frequency, cut_high_frequency, target_width_px, target_height_px, win)

    return images

def process_audio_file(file_name, recording_folder_path, saving_folder, start_time, save, wlen, hop, nfft, sliding_w, cut_low_frequency, cut_high_frequency, target_width_px, target_height_px, win):
    images = []

    # Load sound recording
    fs, x = wavfile.read(os.path.join(recording_folder_path, file_name))
    x = np.float32(x)  # convert to single precision to save memory
    N = len(x)  # signal length

    low = int(start_time * fs)
    up = low + int(0.8 * fs)
    file_name_ex = start_time  # the start in second

    # Calculate total number of iterations for the while loop
    total_iterations = int(np.ceil((N / fs - start_time - 0.8) / sliding_w))

    for _ in tqdm(range(total_iterations), desc=f"Processing frames for file: {file_name}", leave=False):
        x_w = x[low:up]
        
        # Calculate the spectrogram
        f, t, Sxx = spectrogram(x_w, fs, nperseg=wlen, noverlap=hop, nfft=nfft, window=win)
        Sxx = 20 * np.log10(np.abs(Sxx))  # Convert to dB

        # Create the spectrogram plot
        fig, ax = plt.subplots()
        ax.pcolormesh(t, f / 1000, Sxx, cmap='gray')
        ax.set_ylim(cut_low_frequency, cut_high_frequency)

        # ax.set_aspect('auto')  # Adjust aspect ratio
        ax.set_axis_off()  # Turn off axis
        # Resize the figure directly before saving
        fig.set_size_inches(target_width_px / plt.rcParams['figure.dpi'], target_height_px / plt.rcParams['figure.dpi'])

        # Save the spectrogram as a JPG image without borders
        if save: 
            image_name = os.path.join(saving_folder, file_name + '-' + str(file_name_ex) + '.jpg')
            fig.savefig(image_name, bbox_inches='tight', pad_inches=0, dpi=plt.rcParams['figure.dpi'])  # Save without borders
            plt.close(fig)
        else: 
            images.append(fig)
            if len(images) >= 100:
                # Fermer les figures pour libérer la mémoire
                plt.close('all')
                return images

        low += int(sliding_w * fs)
        file_name_ex += sliding_w
        up = low + int(0.8 * fs)

    return images

if __name__ == "__main__":
    recording_folder_path = '/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/recordings'
    saving_folder = '/users/zfne/emanuell/Documents/GitHub/Dolphins/DNN_whistle_detection/image_test_without_mat_blackman'

    profiler = cProfile.Profile()
    profiler.enable()

    generate_spectrograms(recording_folder_path, saving_folder, save = False, start_time=10)

    profiler.disable()
    # profiler.print_stats()
