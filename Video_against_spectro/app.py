from flask import Flask, render_template, request, redirect, url_for, send_file
import os

app = Flask(__name__)

# Chemin du dossier contenant les analyses
analyses_folder = "/media/DOLPHIN/Analyses_alexis/2023_analysed"

@app.route("/")
def index():
    # Récupérer la liste des expériences avec des dossiers "extraits"
    experiment_folders = []
    for folder in os.listdir(analyses_folder):
        extracts_folder = os.path.join(analyses_folder, folder, 'extraits')
        if os.path.isdir(extracts_folder):
            experiment_folders.append(os.path.join(analyses_folder, folder))
    return render_template("index.html", experiment_folders=experiment_folders)

@app.route("/experiment/<experiment_name>")
def experiment(experiment_name):
    # Récupérer la liste des vidéos dans le dossier 'extraits'
    videos = []
    extracts_folder = os.path.join(analyses_folder, experiment_name, 'extraits')
    for filename in os.listdir(extracts_folder):
        if filename.endswith(".mp4"):
            videos.append(filename)
    return render_template("experiment.html", experiment_name=experiment_name, videos=videos)

@app.route("/video/<experiment_name>/<video_name>")
def video(experiment_name, video_name):
    # Récupérer les images correspondant à la vidéo
    images = []
    video_path = os.path.join(analyses_folder, experiment_name, 'extraits', video_name)
    video_start = int(video_name.split('_')[1])
    video_end = int(video_name.split('_')[2].split('.')[0])
    positive_folder = os.path.join(analyses_folder, experiment_name, 'positive')
    for filename in os.listdir(positive_folder):
        if filename.endswith(".jpg"):
            img_start = float(filename.split('-')[0])
            if img_start >= video_start and img_start <= video_end:
                images.append(filename)
    return render_template("video.html", experiment_name=experiment_name, video_name=video_name, images=images)

@app.route("/static/videos/<experiment_name>/<video_name>")
def static_video(experiment_name, video_name):
    video_path = os.path.join(analyses_folder, experiment_name, 'extraits', video_name)
    return send_file(video_path)

@app.route("/static/images/<experiment_name>/<image_name>")
def static_image(experiment_name, image_name):
    image_path = os.path.join(analyses_folder, experiment_name, 'positive', image_name)
    return send_file(image_path)

if __name__ == "__main__":
    app.run(debug=True)


