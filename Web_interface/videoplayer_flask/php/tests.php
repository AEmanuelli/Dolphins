<?php
// Chemin vers le dossier vidéo
$dossierVideos = "/home/alexis/Documents/GitHub/Dolphins/website_zebra/extraits_avec_audio/";

// Liste tous les fichiers dans le dossier vidéo
$videos = glob($dossierVideos . "*.mp4");

// Sélectionne une vidéo au hasard
$videoAleatoire = $videos[array_rand($videos)];
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Vidéo Aléatoire</title>
<style>
  body {
    font-family: Arial, sans-serif;
    text-align: center;
  }
  video {
    max-width: 100%;
    margin: 20px 0;
  }
</style>
</head>
<body>
<h1>Vidéo Aléatoire</h1>
<video controls autoplay id="randomVideo"></video>

<script>
  // Chemin vers la vidéo aléatoire
  var videoURL = "<?php echo $videoAleatoire; ?>";

  // Sélection de la balise vidéo
  var videoElement = document.getElementById('randomVideo');

  // Attribution de la source vidéo au lecteur vidéo
  videoElement.src = videoURL;

  // Mise à jour du titre de la page avec le nom de la vidéo sélectionnée
  document.title = videoURL.split('/').pop(); // Obtient le nom de la vidéo à partir de son chemin
</script>

</body>
</html>
