document.addEventListener("DOMContentLoaded", function() {
    var videoListContainer = document.getElementById("videoList");

    // Function to generate video list
    function generateVideoList(videos) {
        videos.forEach(function(video) {
            var videoName = video.split('.')[0];
            var videoLink = document.createElement('a');
            videoLink.href = "#";
            videoLink.textContent = videoName;
            videoLink.addEventListener('click', function(event) {
                event.preventDefault();
                playVideo(videoName);
            });
            videoListContainer.appendChild(videoLink);
            videoListContainer.appendChild(document.createElement('br'));
        });
    }

    // Function to play video
    function playVideo(videoName) {
        var videoPlayer = document.getElementById("videoPlayer");
        var additionalImagesList = document.getElementById("additionalImagesList");
        
        // Set video source
        videoPlayer.src = "{{ url_for('static', filename='videos/' + analysis_folder + '/' + experiment_folder + '/' + videoName) }}";

        // Fetch images associated with the video
        fetchImages(videoName).then(function(images) {
            additionalImagesList.innerHTML = ""; // Clear previous images
            images.forEach(function(image) {
                var img = document.createElement('img');
                img.src = "{{ url_for('image', analysis_folder=analysis_folder, experiment_folder=experiment_folder, video_name=videoName, image_name=image) }}";
                img.alt = image;
                additionalImagesList.appendChild(img);
            });
        }).catch(function(error) {
            console.error('Error fetching images:', error);
        });
    }

    // Function to fetch images associated with the video
    function fetchImages(videoName) {
        return new Promise(function(resolve, reject) {
            fetch("images.json")
                .then(response => response.json())
                .then(data => {
                    if (data.hasOwnProperty(videoName)) {
                        resolve(data[videoName]);
                    } else {
                        reject("No images found for video: " + videoName);
                    }
                })
                .catch(error => reject(error));
        });
    }

    // Fetch videos from the folder
    fetch('videos.json')
        .then(response => response.json())
        .then(data => {
            generateVideoList(data.videos);
        })
        .catch(error => console.error('Error:', error));
});

