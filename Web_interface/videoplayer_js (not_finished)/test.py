from flask import Flask, render_template, url_for, send_file
import os
import re
from moviepy.editor import VideoFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

app = Flask(__name__)

# Chemin du dossier contenant les analyses
analyses_folder = "/media/DOLPHIN/Analyses_alexis/2023_analysed"

@app.route('/')
def index():
    # Liste des expériences disponibles
    experiments = []
    for experiment_folder in os.listdir(analyses_folder):
        experiment_path = os.path.join(analyses_folder, experiment_folder)
        if os.path.exists(os.path.join(experiment_path, "extraits")):
            experiments.append(experiment_folder)
    return render_template('index.html', experiments=experiments)

@app.route('/experiment/<experiment_name>')
def experiment(experiment_name):
    experiment_path = os.path.join(analyses_folder, experiment_name)
    # Liste des vidéos dans le dossier 'extraits'
    videos = []
    videos_path = os.path.join(experiment_path, "extraits")
    for video_file in os.listdir(videos_path):
        if video_file.endswith(".mp4"):
            videos.append(video_file)
    return render_template('experiment.html', experiment_name=experiment_name, videos=videos)

@app.route('/video/<experiment_name>/<video_name>')
def video(experiment_name, video_name):
    video_path = os.path.join(analyses_folder, experiment_name, "extraits", video_name)
    clip = VideoFileClip(video_path)
    duration = clip.duration
    clip.close()
    images = []
    # Extraire le temps1 et temps2 du nom de la vidéo
    temps1, temps2 = map(float, video_name.split('.')[0].split('_')[1:3])
    # Chemin du dossier des images positives
    images_folder = os.path.join(analyses_folder, experiment_name, "positive")
    for image_file in os.listdir(images_folder):
        if image_file.endswith(".jpg"):
            # Extraire le temps de l'image à partir du nom de fichier en utilisant une expression régulière
            match = re.match(r'(\d+\.\d+)-(\d+\.\d+)\.jpg', image_file)
            if match:
                image_temps1, image_temps2 = map(float, match.groups())
                # Vérifier si l'image est dans l'intervalle de temps de la vidéo
                if temps1 <= image_temps1 and image_temps2 <= temps2:
                    images.append(image_file)
    return render_template('video.html', experiment_name=experiment_name, video_name=video_name, duration=duration, images=images)



@app.route('/image/<experiment_name>/<video_name>/<image_name>')
def image(experiment_name, video_name, image_name):
    image_path = os.path.join(analyses_folder, experiment_name, "positive", image_name)
    return send_file(image_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
