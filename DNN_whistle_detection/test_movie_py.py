import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from moviepy.editor import VideoFileClip

class VideoImagePlayer:
    def __init__(self, root, video_path, display_duration, video_scale):
        self.root = root
        self.video_path = video_path
        self.display_duration = display_duration
        self.video_scale = video_scale
        self.playback_speed = 1

        self.frame_label = tk.Label(root)
        self.frame_label.grid(row=0, column=0, columnspan=2)

        self.play_button = ttk.Button(root, text="Play", command=self.play_video)
        self.play_button.grid(row=1, column=0, padx=5)

        self.speed_label = ttk.Label(root, text="Speed: 1x")
        self.speed_label.grid(row=1, column=1)

        self.speed_up_button = ttk.Button(root, text="Speed Up", command=self.speed_up)
        self.speed_up_button.grid(row=2, column=0, padx=5)

        self.slow_down_button = ttk.Button(root, text="Slow Down", command=self.slow_down)
        self.slow_down_button.grid(row=2, column=1, padx=5)

        self.playing = False
        self.video_clip = VideoFileClip(self.video_path)

    def play_video(self):
        if not self.playing:
            self.play_button.config(text="Pause")
            self.playing = True
            self._play_video()
        else:
            self.play_button.config(text="Play")
            self.playing = False

    def speed_up(self):
        self.playback_speed *= 2
        self.speed_label.config(text="Speed: {}x".format(self.playback_speed))

    def slow_down(self):
        self.playback_speed /= 2
        self.speed_label.config(text="Speed: {}x".format(self.playback_speed))

    def _play_video(self):
        duration = self.video_clip.duration
        current_time = 0

        while current_time < duration and self.playing:
            frame = self.video_clip.get_frame(current_time)
            frame_pil = Image.fromarray(frame)

            # Affichage de l'image dans Tkinter
            photo = ImageTk.PhotoImage(image=frame_pil)
            self.frame_label.config(image=photo)
            self.frame_label.image = photo

            # Mise à jour de l'heure actuelle
            current_time += self.display_duration / 1000 * self.playback_speed

            # Limiter le taux de rafraîchissement
            self.root.update()

    def clean_up(self):
        self.video_clip.close()

# Fonction principale
def main():
    root = tk.Tk()
    root.title("Video Player")

    video_path = "/media/DOLPHIN/Analyses_alexis/2023_analysed/Exp_05_Mar_2024_1545_channel_1/extraits/extrait_283_313.mp4"  # Mettez le chemin de votre vidéo
    images_paths = ["/home/alexis/Documents/GitHub/Dolphins/DNN_whistle_detection/images_/Exp_01_Feb_2024_1145_channel_0.wav-2250.jpg"]  # Ajoutez les chemins de vos images si nécessaire
    instants = [5]  # Ajoutez les instants si nécessaire
    display_duration = 1000  # Durée d'affichage de chaque image en millisecondes
    video_scale = 0.2  # Facteur d'échelle de la vidéo

    player = VideoImagePlayer(root, video_path, display_duration, video_scale)
    root.mainloop()

    player.clean_up()

if __name__ == "__main__":
    main()
