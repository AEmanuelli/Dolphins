from flask import Flask, render_template, send_file, request,  Response
import os
import csv
from datetime import datetime

analyses_folder = os.path.abspath("Video_against_spectro/Demo_Eilat/Vid_demo_Eilat")

app = Flask(__name__)

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
            # Check if the folder contains a subfolder named "extraits_avec_audio"
            if os.path.isdir(os.path.join(analyses_folder, folder, "extraits_avec_audio")):
                # Check if the folder contains any CSV files
                csv_files = [file for file in os.listdir(os.path.join(analyses_folder, folder)) if file.endswith('.csv')]
                if csv_files:
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
    # Liste de tous les mois dans l'année
    all_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Récupérer les mois disponibles pour une année donnée
    months = set()
    for folder in get_folders_by_date(year=year):
        _, folder_month, _, _ = extract_date_and_time(folder)
        if folder_month:
            months.add(folder_month)

    # Trier les mois dans l'ordre chronologique en utilisant l'index dans la liste all_months
    sorted_months = sorted(months, key=lambda x: all_months.index(x))

    return render_template("select_month.html", year=year, months=sorted_months)

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
    # Construire le chemin du dossier correspondant à l'année, au mois, au jour et à l'heure spécifiés pour les deux canaux
    folder_path_channel_0 = os.path.join(analyses_folder, f"Exp_{day}_{month}_{year}_{hour}_channel_0")
    folder_path_channel_1 = os.path.join(analyses_folder, f"Exp_{day}_{month}_{year}_{hour}_channel_1")

    # Vérifier la présence du dossier "extraits" pour chaque canal
    folder_path_channel_0_extraits = os.path.join(folder_path_channel_0, "extraits_avec_audio")
    folder_path_channel_1_extraits = os.path.join(folder_path_channel_1, "extraits_avec_audio")

    # Récupérer la liste des fichiers dans les dossiers "extraits" des deux canaux s'ils existent
    # Fonction pour extraire le nombre du nom de fichier
    extract_number = lambda filename: int(filename.split('_')[1])

    # Trier les fichiers du premier dossier
    files_channel_0 = sorted(os.listdir(folder_path_channel_0_extraits), key=extract_number) if os.path.exists(folder_path_channel_0_extraits) else []

    # Trier les fichiers du deuxième dossier
    files_channel_1 = sorted(os.listdir(folder_path_channel_1_extraits), key=extract_number) if os.path.exists(folder_path_channel_1_extraits) else []

    # Vérifier la présence du dossier "pas_d_extraits" pour chaque canal
    folder_path_channel_0_no_extracts = os.path.join(folder_path_channel_0, "pas_d_extraits")
    folder_path_channel_1_no_extracts = os.path.join(folder_path_channel_1, "pas_d_extraits")

    reasons_channel_0 = ""
    reasons_channel_1 = ""

    def get_reasons(folder_path):
        reasons = ""
        if os.path.exists(folder_path):
            files = os.listdir(folder_path)
            for file_name in files:
                if file_name.endswith(".txt"):
                    reason_file_path = os.path.join(folder_path, file_name)
                    with open(reason_file_path, "r") as file:
                        reasons = file.read()
                    break  # Sortir de la boucle une fois que le fichier texte est trouvé
        return reasons


    reasons_channel_0 = get_reasons(folder_path_channel_0_no_extracts)
    reasons_channel_1 = get_reasons(folder_path_channel_1_no_extracts)


    return render_template("show_files.html", year=year, month=month, day=day, hour=hour,
                           files_channel_0=files_channel_0, files_channel_1=files_channel_1,
                           reasons_channel_0=reasons_channel_0, reasons_channel_1=reasons_channel_1)

@app.route("/submit_form", methods=["POST"])
def submit_form():
    try:
        # Extract form data
        entry_1008522387 = request.form["entry.1008522387"]
        entry_971205134 = request.form["entry.971205134"]
        entry_1637143753 = request.form["entry.1637143753"]
        entry_1104629907 = request.form["entry.1104629907"]
        
        # Process the form data as needed (e.g., save to a database)
        
        # Optionally, you can redirect to a "Thank You" page after successful submission
        return render_template("thank_you.html")
    except Exception as e:
        # Log any errors that occur during form submission
        print("Error submitting form:", e)
        # Optionally, redirect to an error page
        return render_template("error.html")

@app.route("/videos/<experiment_name>/<video_name>")
def video(experiment_name, video_name):
    images = []
    video_start = int(video_name.split('_')[1])
    video_end = int(video_name.split('_')[2].split('.')[0])
    positive_folder = os.path.join(analyses_folder, experiment_name, 'positive')
    if os.path.exists(positive_folder):
        for filename in os.listdir(positive_folder):
            print(filename)
            if filename.endswith(".jpg"):
                img_start = float(filename.split('-')[0])
                if img_start >= video_start and img_start <= video_end:
                    images.append(filename)
    # Rendre le modèle HTML avec les commentaires et le nom de la vidéo
    return render_template("video.html", experiment_name=experiment_name, video_name=video_name, images = images)

@app.route("/static/videos/<experiment_name>/<video_name>")
def static_video(experiment_name, video_name):
    video_path = os.path.join(analyses_folder, experiment_name, 'extraits_avec_audio', video_name)
    return send_file(video_path)
                    
@app.route("/static/images/<experiment_name>/<image_name>")
def static_image(experiment_name, image_name):
    image_path = os.path.join(analyses_folder, experiment_name, 'positive', image_name)
    return send_file(image_path)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)