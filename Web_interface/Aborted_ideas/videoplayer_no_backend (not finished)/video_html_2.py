import os

def main(global_folder, output_html):

    # Chemin où seront enregistrés les fichiers HTML
    output_directory = os.path.abspath(output_html)

    # Créer le répertoire s'il n'existe pas déjà
    os.makedirs(output_directory, exist_ok=True)

    # Dossier global contenant les expériences
    global_folder = os.path.abspath(global_folder)
    # Récupérer les noms des expériences
    experiment_names = [experiment for experiment in os.listdir(global_folder) if os.path.isdir(os.path.join(global_folder, experiment))]
    
    source = "https://bucket-test-emanuelli-alexis-2.s3.eu-west-3.amazonaws.com/"
    
    # Boucle sur chaque expérience
    for experiment_name in experiment_names:
        # Chemin vers le dossier de l'expérience
        experiment_path = os.path.join(global_folder, experiment_name)
        
        
        # Chemin vers le dossier des extraits vidéos
        video_folder = os.path.join(experiment_path, "extraits_avec_audio")

        # Récupérer les chemins des vidéos dans le dossier des extraits
        vid_paths = [os.path.join(video_folder, file) for file in os.listdir(video_folder)]

        source_path = os.path.join(source, experiment_name, "extraits_avec_audio")
        source_paths = [os.path.join(source_path, file) for file in os.listdir(video_folder)]
        
        # Chemin vers le dossier des vidéos positives
        positive_folder = os.path.join(experiment_path, "positive")

        positive_folder_source = os.path.join(source, experiment_name, "positive")
        
        # Récupérer les chemins des vidéos positives
        positive_images_source = [os.path.join(positive_folder_source, file) for file in os.listdir(positive_folder)]
        positive_images = [os.path.join(positive_folder, file) for file in os.listdir(positive_folder)]

        # Boucle pour créer un fichier HTML par extrait vidéo
        for i, path in enumerate(vid_paths):
            # Nom du fichier HTML
            html_file = f"{experiment_name}_video_{i}.html" # AMDOIFIE ?

            # Chemin complet du fichier HTML
            file_path = os.path.join(output_directory, html_file)

            video_name = os.path.splitext(os.path.basename(path))[0]
            video_start = float(video_name.split("_")[1])
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
                        <source src="{source_paths[i]}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                </div>
                <div class="sidebar">
                    <h2>Spectrograms of associated whistles :</h2>
                    <ul class="image-list">
            """

            # Ajouter les images positives associées
            for j, positive_im in enumerate(positive_images):
                name = os.path.splitext(os.path.basename(positive_im))[0]
                image_start, image_end = map(float, name.split("-"))
                display_time = round(image_start - video_start -.5, 1)
                print(display_time)
                html_content+= f"""
                <script>
                    // Fonction pour afficher une image à la seconde 1 de la vidéo
                    document.addEventListener("DOMContentLoaded", function() {{
                        var video = document.querySelector("video");
                        var imageDisplayed = false;

                        video.addEventListener("timeupdate", function() {{
                            // Vérifiez si la vidéo est à la seconde en question
                            if (video.currentTime >= { display_time } && video.currentTime < { display_time + 2 } && !imageDisplayed) {{
                                // Créez une nouvelle image
                                var image = document.createElement("img");                    
                                image.src = "{ positive_images_source[j] }";
                                // Définissez la forme de découpe de l'image pour afficher uniquement la moitié gauche
                                image.style.width = "15%";
                                image.style.height = "auto"; // Pour maintenir les proportions d'origine
                                document.body.appendChild(image);
                                // Marquez que l'image est affichée
                                imageDisplayed = true;
                                // Supprimez l'image après 5 secondeS
                                setTimeout(function() {{
                                    //document.body.removeChild(image);
                                    imageDisplayed = false;
                                }}, 5000);
                            }}
                        }});
                    }});
                </script>
                """

            html_content += f"""
                        </ul>
                    </div>
                    <!-- Formulaire de soumission -->
                    <div class="form-container-right"> <!-- Ajoutez la classe form-container-right ici -->
                        <form class="contact-form" name="basedatos" action="https://docs.google.com/forms/d/e/1FAIpQLSeOteTktbzc6kLPKKQW8uHde1ml3WWcyfolzj0m9CRPdJctaA/formResponse" target="_self" method="POST">
                            <input type="hidden" name="entry.1008522387" value="{experiment_name}">
                            <input type="hidden" name="entry.971205134" value="{video_name}">
                            <div class="input-group tm-mb-30"> <input name="entry.1637143753" class="form-control rounded-0 border-top-0 border-end-0 border-start-0" placeholder="Nom" type="text"> </div>
                            <div class="input-group tm-mb-30">
                                <textarea name="entry.1104629907" class="form-control rounded-0 border-top-0 border-end-0 border-start-0" placeholder="Commentaire" style="height: 100px;"></textarea>
                            </div> 
                            <div class="input-group justify-content-end"> <input class="btn btn-primary tm-btn-pad-2" value="Envoyer" type="submit"> </div>
                        </form>
                </div>
                </body>
                </html>
                """

            html_content += f"""<style>
                .small-image {{
                    width: 677px; /* Définir la largeur des images */
                    height: auto; /* Garder les proportions originales */
                }}
                .form-container-right {{
                    position: fixed; /* Positionner le formulaire par rapport à la fenêtre */
                    top: 50%; /* Positionner le formulaire au centre verticalement */
                    right: 500px; /* Positionner le formulaire 10px à partir du bord droit */
                    transform: translateY(-50%); /* Centrer verticalement le formulaire */
                }}
            </style>
            """

            # Écrire le contenu HTML dans le fichier
            with open(file_path, "w") as f:
                f.write(html_content)

            print(f"Fichier HTML '{html_file}' créé avec succès !")



def generate_html_index(output_directory):
    # Chemin complet du fichier index HTML
    index_file_path = os.path.join(output_directory, "index.html")

    # Contenu HTML pour l'index
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Index des fichiers HTML générés</title>
    </head>
    <body>
        <h1>Index des fichiers HTML générés</h1>
        <ul>
    """

    # Parcours de tous les fichiers HTML dans le répertoire de sortie
    for file in os.listdir(output_directory):
        if file.endswith(".html"):
            # Ajout d'un lien vers chaque fichier HTML
            html_content += f'<li><a href="{file}">{file}</a></li>'

    # Fermeture des balises HTML
    html_content += """
        </ul>
    </body>
    </html>
    """

    # Écriture du contenu HTML dans le fichier index
    with open(index_file_path, "w") as f:
        f.write(html_content)

    print(f"Fichier index HTML '{index_file_path}' créé avec succès !")


if __name__ == "__main__":
    global_folder = "/media/DOLPHIN/Analyses_alexis/First_launch_website_content/"
    output_html = "/home/alexis/Desktop/Test_aws_website"
    # main(global_folder, output_html)
    generate_html_index(output_html)
