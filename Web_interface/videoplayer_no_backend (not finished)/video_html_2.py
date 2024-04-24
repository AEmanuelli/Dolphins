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
    video_folder = os.path.join(experiment_path, "extraits_avec_audio")
    
    # Récupérer les chemins des vidéos dans le dossier des extraits
    vid_paths = [os.path.join(video_folder, file) for file in os.listdir(video_folder)]
    
    # Chemin vers le dossier des vidéos positives
    positive_folder = os.path.join(experiment_path, "positive")
    
    # Récupérer les chemins des vidéos positives
    positive_images = [os.path.join(positive_folder, file) for file in os.listdir(positive_folder)]
    print("ZBOOOUBE", len(positive_images))
    

    # Boucle pour créer un fichier HTML par extrait vidéo
    for i, path in enumerate(vid_paths):
        # Nom du fichier HTML
        html_file = f"{experiment_name}_video_{i}.html" # AMDOIFIE 

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
            # html_content += f'<li><img src="{positive_im}" alt="Positive Image"></li>'
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
                            image.src = "{ positive_im }";
                            image.classList.add("small-image"); // Ajouter une classe pour contrôler la taille de l'image
                            var imageContainer = document.createElement("div"); // Créer un conteneur pour positionner l'image
                            
                            imageContainer.appendChild(image);
                            document.body.appendChild(imageContainer);
                            
                            // Marquez que l'image est affichée
                            imageDisplayed = true;

                            // Supprimez l'image après 1 seconde
                            setTimeout(function() {{
                                document.body.removeChild(imageContainer);
                                imageDisplayed = false;
                            }}, 1000);
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
