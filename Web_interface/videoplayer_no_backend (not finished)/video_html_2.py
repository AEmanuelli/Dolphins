import os

# Chemin où seront enregistrés les fichiers HTML
output_directory = os.path.abspath("Web_interface/videoplayer_no_backend (not finished)/video_html")

# Créer le répertoire s'il n'existe pas déjà
os.makedirs(output_directory, exist_ok=True)

# Dossier global contenant les expériences
global_folder = "/home/alexis/Desktop/Test video_html_gen/"

# Récupérer les noms des expériences
experiment_names = [experiment for experiment in os.listdir(global_folder) if os.path.isdir(os.path.join(global_folder, experiment))]

# Boucle sur chaque expérience
for experiment_name in experiment_names:
    # Chemin vers le dossier de l'expérience
    experiment_path = os.path.join(global_folder, experiment_name)
    
    # Chemin vers le dossier des extraits vidéos
    video_folder = os.path.join(experiment_path, "extraits")
    
    # Récupérer les chemins des vidéos dans le dossier des extraits
    vid_paths = [os.path.join(video_folder, file) for file in os.listdir(video_folder)]
    
    # Chemin vers le dossier des vidéos positives
    positive_folder = os.path.join(experiment_path, "positive")
    
    # Récupérer les chemins des vidéos positives
    positive_images = [os.path.join(positive_folder, file) for file in os.listdir(positive_folder)]
    
    # Boucle pour créer un fichier HTML par extrait vidéo
    for i, path in enumerate(vid_paths):
        # Nom du fichier HTML
        html_file = f"{experiment_name}_video_{i}.html"

        # Chemin complet du fichier HTML
        file_path = os.path.join(output_directory, html_file)

        # Contenu HTML avec le nom de fichier, la vidéo correspondante et les images positives associées
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Vidéo - {experiment_name} - Vidéo {i}</title>
            <link rel="stylesheet" href="styles_dolphin.css">
        </head>
        <body>
        <div class="container">
            <div class="content">
                <h1>Vidéo: {experiment_name} - Vidéo {i}</h1>
                <video width="640" height="480" controls>
                    <source src="{path}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
            <div class="sidebar">
                <h2>Vidéos positives associées :</h2>
                <ul class="image-list">
        """

        # Ajouter les images positives associées
        for positive_im in positive_images:
            html_content += f'<li><img src="{positive_im}" alt="Positive Image"></li>'

        html_content += f"""
                </ul>
            </div>
            <!-- Formulaire de soumission -->
            <form class="contact-form" name="basedatos" action="https://docs.google.com/forms/d/e/1FAIpQLSeOteTktbzc6kLPKKQW8uHde1ml3WWcyfolzj0m9CRPdJctaA/formResponse" target="_self" method="POST">
                <input type="hidden" name="entry.1008522387" value="{experiment_name}">
                <input type="hidden" name="entry.971205134" value="{os.path.splitext(os.path.basename(path))[0]}">
                <div class="input-group tm-mb-30"> <input name="entry.1637143753" class="form-control rounded-0 border-top-0 border-end-0 border-start-0" placeholder="Nom" type="text"> </div>
                <div class="input-group tm-mb-30">
                    <textarea name="entry.1104629907" class="form-control rounded-0 border-top-0 border-end-0 border-start-0" placeholder="Commentaire" style="height: 100px;"></textarea>
                </div> 
                <div class="input-group justify-content-end"> <input class="btn btn-primary tm-btn-pad-2" value="Envoyer" type="submit"> </div>
            </form>
        </div>
        <script>
            // Vous pouvez conserver le script JavaScript existant ici
        </script>
        </body>
        </html>
        """

        # Écrire le contenu HTML dans le fichier
        with open(file_path, "w") as f:
            f.write(html_content)

        print(f"Fichier HTML '{html_file}' créé avec succès !")
