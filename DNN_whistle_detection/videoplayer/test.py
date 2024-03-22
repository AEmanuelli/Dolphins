from flask import Flask, render_template, url_for, send_file
import os

app = Flask(__name__)

# Chemin du dossier contenant les analyses
analyses_folder = "/media/DOLPHIN/Analyses_alexis/2023_analysed"

@app.route('/')
def index():
    # Liste des expériences disponibles
    experiments = []
    for experiment_folder in os.listdir(analyses_folder):
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
    return send_file(video_path, mimetype='video/mp4')

@app.route('/image/<experiment_name>/<video_name>/<image_name>')
def image(experiment_name, video_name, image_name):
    image_path = os.path.join(analyses_folder, experiment_name, "positive", image_name)
    return send_file(image_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
