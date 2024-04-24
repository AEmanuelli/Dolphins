import os

# Chemin où seront enregistrés les fichiers HTML
output_directory = os.path.abspath("Web_interface/videoplayer_no_backend (not finished)/video_html")

# Créer le répertoire s'il n'existe pas déjà
os.makedirs(output_directory, exist_ok=True)

folder = "/home/alexis/Documents/GitHub/Dolphins/Web_interface/videoplayer_no_backend (not finished)/extraits_avec_audio"
vid_paths = [os.path.join(folder, file) for file in os.listdir(folder)]

# Boucle pour créer 50 fichiers HTML avec des vidéos différentes
for i, path in enumerate(vid_paths):
    # Nom du fichier HTML
    html_file = f"video_{i}.html"

    # Chemin complet du fichier HTML
    file_path = os.path.join(output_directory, html_file)

    # Contenu HTML avec le nom de fichier et la vidéo correspondante
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vidéo - Vidéo {i}</title>
        <link rel="stylesheet" href="styles_dolphin.css">
    </head>
    <body>
    <div class="container">
        <div class="content">
            <h1>Vidéo: Vidéo {i}</h1>
            <video width="640" height="480" controls>
                <source src="{path}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
        <div class="sidebar">
            <h2>Images associées :</h2>
            <ul class="image-list">
                <!-- Ajoutez ici les images associées si nécessaire -->
            </ul>
        </div>
        <!-- Formulaire de soumission -->
        <form class="contact-form" name="basedatos" action="/submit_form" target="_self" method="POST">
            <input type="hidden" name="entry.1008522387" value="ExperimentName">
            <input type="hidden" name="entry.971205134" value="VideoName">
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
