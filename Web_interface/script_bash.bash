#!/bin/bash

# Chemin vers le dossier source
source_dir="/media/DOLPHIN/Analyses_alexis/2023_analysed"

# Chemin vers le dossier de destination
destination_dir="/media/DOLPHIN/Analyses_alexis/upload_online"

# Créer le dossier de destination s'il n'existe pas
mkdir -p "$destination_dir"

# Parcourir les sous-dossiers du dossier source
for subdir in "$source_dir"/*; do
    # Vérifier si le chemin est un dossier
    if [ -d "$subdir" ]; then
        # Nom du sous-dossier
        subdir_name=$(basename "$subdir")

        # Créer le même sous-dossier dans le dossier de destination
        mkdir -p "$destination_dir/$subdir_name"

        # Copier les sous-dossiers "positive" et "extraits_avec_audio"
        cp -r "$subdir"/positive "$destination_dir/$subdir_name"
        cp -r "$subdir"/extraits_avec_audio "$destination_dir/$subdir_name"
    fi
done


#!/bin/bash

# Chemin vers le dossier des extraits avec audio
source_dir="/media/DOLPHIN/Analyses_alexis/First_launch_website_content"

# Initialiser un tableau JSON
echo "[" > paths.json

# Parcourir les sous-dossiers de niveau 2 nommés "extraits_avec_audio"
find "$source_dir" -mindepth 2 -maxdepth 2 -type d -name "extraits_avec_audio" | while read -r subdir; do
    # Récupérer les chemins complets des fichiers dans le sous-dossier "extraits_avec_audio"
    find "$subdir" -type f | while read -r file; do
        # Remplacer "source_dir" par "zizi" dans le chemin
        modified_path="${file//$source_dir/https://bucket-test-emanuelli-alexis-2.s3.eu-west-3.amazonaws.com}"
        # Ajouter le chemin modifié au tableau JSON
        echo "\"$modified_path\"," >> paths.json
    done
done

# Supprimer la virgule finale et fermer le tableau JSON
sed -i '$s/,$//' paths.json
echo "]" >> paths.json
