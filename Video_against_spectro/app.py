from flask import Flask, render_template, send_file, request
import os


def trouver_fichier_video(fichier_csv, dossier_videos = "/media/DOLPHIN/2023/"):
    # Extraire la date et l'heure du nom de fichier CSV
    try: 
        elements_nom_csv = fichier_csv.split("_")
        date_heure_csv = elements_nom_csv[1] + "_"+ elements_nom_csv[2] + "_" + elements_nom_csv[3] + "_"+elements_nom_csv[4]  # Format: "Aug_2023_0845"
    except IndexError: 
        # print(f"{fichier_video} n'a pas le bon format.")
        return None

    # Parcourir tous les fichiers vidéo dans le dossier
    for fichier_video in os.listdir(dossier_videos):
        if fichier_video.endswith(".mp4"):
            try: 
                # Extraire la date et l'heure du nom de fichier vidéo
                elements_nom_video = fichier_video.split("_")
                date_heure_video = elements_nom_video[1] + "_" + elements_nom_video[2] + "_" + elements_nom_video[3] + "_" + elements_nom_video[4]  # Format: "Aug_2023_1645"
            except IndexError: 
                # print(f"{fichier_video} n'a pas le bon format.")
                continue
            # Comparer les dates et heures pour trouver une correspondance
            if date_heure_csv == date_heure_video:
                return os.path.join(dossier_videos, fichier_video)

    print(f"Aucun fichier vidéo correspondant trouvé pour le fichier CSV {fichier_csv}")
    return None


app = Flask(__name__)

# Chemin du dossier contenant les analyses
analyses_folder = "/media/DOLPHIN/Analyses_alexis/2023_analysed"
video_folder = "/media/DOLPHIN/2023/"
def extract_date_and_time(folder_name):
    # Extraction de l'année, du mois, du jour et de l'heure à partir du nom de dossier
    parts = folder_name.split('_')
    if len(parts) >= 5:
        day = parts[1]
        month = parts[2]
        year = parts[3]
        hour = parts[4]
        return year, month, day, hour
    else:
        # Si le format du nom de dossier est incorrect, retournez des valeurs par défaut
        return None, None, None, None

def get_folders_by_date(year=None, month=None, day=None):
    """
    Récupère les dossiers correspondants à une date spécifique.
    Si aucun paramètre n'est spécifié, renvoie tous les dossiers.
    """
    folders = []
    for folder in os.listdir(analyses_folder):
        folder_year, folder_month, folder_day, _ = extract_date_and_time(folder)
        if (not year or folder_year == year) and \
           (not month or folder_month == month) and \
           (not day or folder_day == day):
            folders.append(folder)
    return folders

@app.route("/")
def index():
    # Récupérer les années disponibles
    years = set()
    for folder in get_folders_by_date():
        year, _, _, _ = extract_date_and_time(folder)
        if year:
            years.add(year)
    return render_template("index.html", years=sorted(years))

@app.route("/<year>")
def select_month(year):
    # Récupérer les mois disponibles pour une année donnée
    months = set()
    for folder in get_folders_by_date(year=year):
        _, folder_month, _, _ = extract_date_and_time(folder)
        if folder_month:
            months.add(folder_month)
    return render_template("select_month.html", year=year, months=sorted(months))

@app.route("/<year>/<month>")
def select_day(year, month):
    # Récupérer les jours disponibles pour un mois donné et une année donnée
    days = set()
    for folder in get_folders_by_date(year=year, month=month):
        _, _, folder_day, _ = extract_date_and_time(folder)
        if folder_day:
            days.add(folder_day)
    return render_template("select_day.html", year=year, month=month, days=sorted(days))

@app.route("/<year>/<month>/<day>")
def select_hour(year, month, day):
    # Récupérer les heures disponibles pour un jour donné, un mois donné et une année donnée
    hours = set()
    for folder in get_folders_by_date(year=year, month=month, day=day):
        _, _, _, folder_hour = extract_date_and_time(folder)
        if folder_hour:
            hours.add(folder_hour)
    return render_template("select_hour.html", year=year, month=month, day=day, hours=sorted(hours))

@app.route("/<year>/<month>/<day>/<hour>")
def show_files(year, month, day, hour):
    # Construire le chemin du dossier correspondant à l'année, au mois, au jour et à l'heure spécifiés
    folder_path_channel_0 = os.path.join(analyses_folder, f"Exp_{day}_{month}_{year}_{hour}_channel_0", "extraits")
    folder_path_channel_1 = os.path.join(analyses_folder, f"Exp_{day}_{month}_{year}_{hour}_channel_1", "extraits")

    # Récupérer la liste des fichiers dans les dossiers extraits des deux canaux
    files_channel_0 = sorted(os.listdir(folder_path_channel_0)) if os.path.exists(folder_path_channel_0) else []
    files_channel_1 = sorted(os.listdir(folder_path_channel_1)) if os.path.exists(folder_path_channel_1) else []
    return render_template("show_files.html", year=year, month=month, day=day, hour=hour, files_channel_0=files_channel_0, files_channel_1=files_channel_1)

@app.route("/videos/<experiment_name>/<video_name>")
def video(experiment_name, video_name):
    # Récupérer les images correspondant à la vidéo
    full_vid_link = trouver_fichier_video(experiment_name)
    if full_vid_link:
        vid_name = os.path.basename(full_vid_link)  # Extracts the filename from the full video link
        
    else:
        vid_name = None  # Handle the case where no video link is found
    print(vid_name)
    images = []
    video_start = int(video_name.split('_')[1])
    video_end = int(video_name.split('_')[2].split('.')[0])
    positive_folder = os.path.join(analyses_folder, experiment_name, 'positive')
    if os.path.exists(positive_folder):
        for filename in os.listdir(positive_folder):
            if filename.endswith(".jpg"):
                img_start = float(filename.split('-')[0])
                if img_start >= video_start and img_start <= video_end:
                    images.append(filename)
    return render_template("video.html", experiment_name=experiment_name, video_name=video_name, images=images, vid_name = vid_name)

@app.route("/static/videos/<experiment_name>/<video_name>")
def static_video(experiment_name, video_name):
    video_path = os.path.join(analyses_folder, experiment_name, 'extraits', video_name)
    return send_file(video_path)

@app.route("/static/videos_supplementary/<video_name>")
def static_supplementary_video(video_name):
    # Construct the path to the supplementary video file
    supplementary_video_path = os.path.join(video_folder, video_name)
    return send_file(supplementary_video_path)

@app.route("/static/images/<experiment_name>/<image_name>")
def static_image(experiment_name, image_name):
    image_path = os.path.join(analyses_folder, experiment_name, 'positive', image_name)
    return send_file(image_path)

@app.route('/save_text', methods=['POST'])
def save_text():
    submitted_text = request.form['input_text']
    with open('submitted_text.txt', 'a') as file:
        file.write(submitted_text + '\n')
    return 'Text saved successfully!'

if __name__ == "__main__":
    app.run(debug=True)