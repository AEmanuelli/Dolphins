import os

class Checkpoint:
    def __init__(self, target_directory):
        self.target_directory = target_directory

    def file_exists(self, filename):
        # Construit le chemin complet du fichier
        file_path = os.path.join(self.target_directory, filename)
        # Vérifie si le fichier existe
        return os.path.isfile(file_path)