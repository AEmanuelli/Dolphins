import cv2

def inserer_images_sous_video(video_path, images, instants, duree, output_path):
    """
    Insère des images sous une vidéo aux instants spécifiés pour la durée spécifiée et enregistre la vidéo modifiée.

    Args:
        video_path (str): Chemin vers la vidéo d'entrée.
        images (list): Liste des chemins vers les images à insérer.
        instants (list): Liste des instants (en secondes) pour chaque image.
        duree (int): Durée (en secondes) pendant laquelle chaque image est affichée.
        output_path (str): Chemin de sortie pour enregistrer la vidéo modifiée.
    """

    # Charger la vidéo
    video_capture = cv2.VideoCapture(video_path)

    # Définir le FPS (Frames Per Second) de la vidéo
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    # Récupérer les dimensions de la première image
    first_image = cv2.imread(images[0])
    video_width = first_image.shape[1]
    video_height = first_image.shape[0]

    # Calculer les nombres de frames pour chaque instant
    instants_frames = [int(instant * fps) for instant in instants]

    # Lire les images
    images_loaded = [cv2.imread(image) for image in images]

    # Récupérer les dimensions des images
    image_heights, image_widths = zip(*[image.shape[:2] for image in images_loaded])

    # Calculer la hauteur maximale parmi les images
    max_height = max(image_heights)

    # Définir le temps écoulé en secondes
    temps_ecoule = 0

    # Indice de l'image à afficher
    current_image_index = 0

    # Créer un objet VideoWriter pour enregistrer la vidéo modifiée
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Format de compression vidéo
    output_video = cv2.VideoWriter(output_path, fourcc, fps, (video_width, video_height))

    # Lire la vidéo frame par frame
    while video_capture.isOpened():
        ret, frame = video_capture.read()

        if not ret:
            break

        # Vérifier si l'instant actuel correspond à l'instant d'une image
        if temps_ecoule in instants_frames:
            # Insérer l'image sous la vidéo
            frame[0:max_height, 0:image_widths[current_image_index]] = images_loaded[current_image_index]

            # Calculer le décalage pour la prochaine image si les instants des images sont successifs
            if current_image_index < len(images_loaded) - 1 and instants_frames[current_image_index] == instants_frames[current_image_index + 1]:
                offset = image_widths[current_image_index]
            else:
                offset = 0

            # Mettre à jour l'indice de l'image à afficher
            current_image_index += 1

        # Écrire le frame modifié dans la vidéo de sortie
        output_video.write(frame)

        # Incrémenter le temps écoulé
        temps_ecoule += 1

        # Vérifier si la durée d'affichage de l'image est écoulée
        if temps_ecoule in [instant + duree * fps for instant in instants_frames]:
            # Réinitialiser l'indice de l'image à afficher
            current_image_index = 0

    # Libérer la capture vidéo et fermer les fenêtres OpenCV
    video_capture.release()
    output_video.release()
    cv2.destroyAllWindows()

# Exemple d'utilisation
video_path = '/home/alexis/Desktop/final_output.mp4'
images = ["/home/alexis/Documents/GitHub/Dolphins/images/Exp_01_Feb_2024_1145_channel_0-0.4.jpg",
           "/home/alexis/Documents/GitHub/Dolphins/images/Exp_01_Feb_2024_1145_channel_0-0.4.jpg"]
instants = [1, 4]  # Instants en secondes pour chaque image
duree = 3  # Durée en secondes pendant laquelle chaque image est affichée
output_path = '/home/alexis/Desktop/test/final_output.mp4'

# Appel de la fonction pour insérer les images sous la vidéo
inserer_images_sous_video(video_path, images, instants, duree, output_path)
