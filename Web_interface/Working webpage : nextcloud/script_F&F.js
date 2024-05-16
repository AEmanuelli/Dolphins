// script.js

document.addEventListener("DOMContentLoaded", function() {
    const presentButton = document.querySelector(".present");
    const notPresentButton = document.querySelector(".not-present");
    const form = document.getElementById("form");

    presentButton.addEventListener("click", function() {
        form.submit();
    });

    notPresentButton.addEventListener("click", function() {
        form.submit();
    });
});

function showRandomVideo() {
    var videos = JSON.parse(document.getElementById('videos').textContent);
    var videoContainer = document.getElementById('videoContainer');
    var randomIndex = Math.floor(Math.random() * videos.length);
    var randomVideoUrl = videos[randomIndex];
    var videoElement = document.createElement('video');
    var videoName = randomVideoUrl.substring(randomVideoUrl.lastIndexOf('/') + 1);
    videoElement.src = randomVideoUrl;
    videoElement.controls = true;
    videoElement.style.width = "100%"; // La vidéo occupe 100% de la largeur du conteneur
    videoElement.style.height = "auto"; // La hauteur est calculée automatiquement pour maintenir les proportions
    videoContainer.innerHTML = ''; // Effacer le contenu précédent
    videoContainer.appendChild(videoElement);
    // document.getElementById('videoName').innerText = "Nom de la vidéo : " + videoName;

        

    // Extraire le nom de l'expérience et le nom de la vidéo
    var experimentName = randomVideoUrl.split('/')[7];
    var videoFileName = randomVideoUrl.split('/').pop().split('.')[0];
    // Mettre à jour les valeurs des champs du formulaire
    document.querySelector('input[name="entry.1008522387"]').value = experimentName;
    document.querySelector('input[name="entry.971205134"]').value = videoFileName;
}
        function showRandomVideo() {
            var videos = JSON.parse(document.getElementById('videos').textContent);
            var videoContainer = document.getElementById('videoContainer');
            var randomIndex = Math.floor(Math.random() * videos.length);
            var randomVideoUrl = videos[randomIndex];
            var videoElement = document.createElement('video');
            var videoName = randomVideoUrl.substring(randomVideoUrl.lastIndexOf('/') + 1);
            videoElement.src = randomVideoUrl;
            videoElement.controls = true;
            videoElement.style.width = "100%"; // La vidéo occupe 100% de la largeur du conteneur
            videoElement.style.height = "auto"; // La hauteur est calculée automatiquement pour maintenir les proportions
            videoContainer.innerHTML = ''; // Effacer le contenu précédent
            videoContainer.appendChild(videoElement);
            // document.getElementById('videoName').innerText = "Nom de la vidéo : " + videoName;

        

            // Extraire le nom de l'expérience et le nom de la vidéo
            var experimentName = randomVideoUrl.split('/')[7];
            var videoFileName = randomVideoUrl.split('/').pop().split('.')[0];
            // Mettre à jour les valeurs des champs du formulaire
            document.querySelector('input[name="entry.1008522387"]').value = experimentName;
            document.querySelector('input[name="entry.971205134"]').value = videoFileName;
        }

        document.getElementById('randomVideoButton').addEventListener('click', showRandomVideo);

        

        function getCountry() {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', 'https://ipapi.co/json/', true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    var response = JSON.parse(xhr.responseText);
                    var country = response.country_name;
                    // document.getElementById('country').innerText = "Pays: " + country;
                    document.getElementById('countryInput').value = country; // Mettez à jour le champ du formulaire avec le nom du pays
                
                }
            };
            xhr.send();
        }

        // Fonction pour afficher le texte par défaut
        function showDefaultText() {
            document.getElementById('videoContainer').innerHTML = '<p id="defaultText">Click the big red button below to display a random dolphin video. Please fill out the form to indicate if the dolphins are present and well-visible in the video.</p>';
        }

        // Appeler la fonction pour obtenir le pays lorsque la page est chargée
        window.onload = function() {
            getCountry()
            showDefaultText(); // Appel de la fonction pour afficher le texte par défaut
        };

    

        document.getElementById('form').addEventListener('submit', function(event) {
            // Vérifier si les champs du formulaire sont remplis
            if (document.querySelector('input[name="entry.1008522387"]').value && document.querySelector('input[name="entry.971205134"]').value) {
                // Empêcher le comportement par défaut du formulaire qui est de soumettre les données et de recharger la page
                event.preventDefault();

                // Récupérer les valeurs des champs du formulaire
                var experimentName = randomVideoUrl.split('/')[7];
                var videoFileName = randomVideoUrl.split('/').pop().split('.')[0];
                // var experimentName = document.querySelector('input[name="entry.1008522387"]').value;
                // var videoFileName = document.querySelector('input[name="entry.971205134"]').value;
                // var reviewerName = prompt("Please enter your name : ");
                var dolphin_pres = document.querySelector('input[name="entry.634543729"]').value;
                // var behaviorDescription = document.querySelector('textarea[name="entry.1104629907"]').value;
                
                // var country_name = document.querySelector('input[name="entry.1079664615"]').value;

                // Construire l'URL avec les valeurs des champs du formulaire
                var url = this.action + '?entry.1008522387=' + encodeURIComponent(experimentName) + 
                    // '&entry.634543729=' + encodeURIComponent('Dauphins absent ou peu visibles') +
                    '&entry.971205134=' + encodeURIComponent(videoFileName) + 
                    '&entry.1079664615=' + encodeURIComponent(country) +
                    '&entry.1637143753=' + encodeURIComponent(reviewerName) + 
                    '&entry.634543729=' + encodeURIComponent(reviewerName) +
                    // '&entry.634543729=' + encodeURIComponent(dolphin_pres) +
                    '&entry.1104629907=' + encodeURIComponent(behaviorDescription);

                // Ouvrir le lien du formulaire dans un nouvel onglet
                var newTab = window.open(url, "_blank");

                // Attendre 2 secondes avant de revenir en arrière
                setTimeout(function() {
                    // Fermer le nouvel onglet ouvert
                    newTab.close();
                    // Revenir en arrière dans l'onglet actuel
                    window.history.back();
                    // Réinitialiser les champs du formulaire
                    // document.querySelector('input[name="entry.634543729"]').value = '';
                    document.querySelector('textarea[name="entry.1104629907"]').value = '';
                }, 2000);

            } else {
                // Les champs ne sont pas remplis, empêcher la soumission du formulaire
                event.preventDefault();
                alert('Veuillez remplir tous les champs avant de soumettre le formulaire.');
            }
    });

function getCountry() {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', 'https://ipapi.co/json/', true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    var response = JSON.parse(xhr.responseText);
                    var country = response.country_name;
                    // document.getElementById('country').innerText = "Pays: " + country;
                    document.getElementById('countryInput').value = country; // Mettez à jour le champ du formulaire avec le nom du pays
                
                }
            };
            xhr.send();
        }
// Fonction pour afficher le texte par défaut
        function showDefaultText() {
            document.getElementById('videoContainer').innerHTML = '<p id="defaultText">Click the big red button below to display a random dolphin video. Please fill out the form to indicate if the dolphins are present and well-visible in the video.</p>';
        }

