import requests

# Informations de connexion
base_url = 'https://hub.bio.ens.psl.eu'
username = 'EMANUELL'
password = 'TB2y.dvZ8ftB'
folder_path = "dir=/extraits_avec_audio&fileid=10073868"

# Authentification
session = requests.Session()
session.auth = (username, password)

# Requête PROPFIND pour obtenir la liste des fichiers dans le dossier
response = session.request('PROPFIND', f'{base_url}/remote.php/dav/files/{username}{folder_path}')

# Vérification du succès de la requête
if response.status_code == 207:  # Statut 207 correspondant à une réponse multistatus
    # Analyse de la réponse XML pour obtenir les noms des fichiers
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(response.content)
    file_names = [elem.text for elem in tree.findall('.//{DAV:}href') if elem.text.endswith('.txt')]  # Filtrer par extension, par exemple '.txt'

    # Générer des liens de partage pour chaque fichier
    share_links = []
    for file_name in file_names:
        share_response = session.post(f'{base_url}/ocs/v2.php/apps/files_sharing/api/v1/shares', json={
            'path': f'{folder_path}/{file_name}',
            'permissions': 1,  # Autorisation de lecture seulement
            'expireDate': ''  # Laisser vide pour un lien permanent
        })
        share_links.append(share_response.json()['ocs']['data']['url'])

    # Afficher les liens de partage
    for i, link in enumerate(share_links, start=1):
        print(f'Lien de partage pour le fichier {file_names[i-1]} : {link}')
else:
    print(f'La requête a échoué avec le code {response.status_code}.')