document.addEventListener("DOMContentLoaded", function() {
    var videoListContainer = document.getElementById("videoList");

    // Function to generate video list
    function generateVideoList(videos) {
        videos.forEach(function(video) {
            var videoName = video.split('.')[0];
            var videoTime = videoName.split('_').slice(1).map(function(t) { return parseFloat(t); });
            var videoLink = document.createElement('a');
            videoLink.href = "#";
            videoLink.textContent = videoName;
            videoLink.addEventListener('click', function(event) {
                event.preventDefault();
                playVideo(video, videoTime);
            });
            videoListContainer.appendChild(videoLink);
            videoListContainer.appendChild(document.createElement('br'));
        });
    }

    // Function to play video
    function playVideo(videoName, videoTime) {
        var videoPlayer = document.getElementById("videoPlayer");
        var additionalImage = document.getElementById("additionalImage");
        
        // Set video source
        videoPlayer.src = "videos/" + videoName;

        // Define timings and corresponding images
        var startTime = videoTime[0];
        var endTime = videoTime[1];
        var imageFileName = startTime + "_" + (startTime + 0.4) + ".jpg";

        // Set additional image source
        additionalImage.src = "images/" + imageFileName;

        // Show the additional image
        additionalImage.style.display = "inline";
    }

    // Fetch videos from the folder
    fetch('videos.json')
        .then(response => response.json())
        .then(data => {
            generateVideoList(data.videos);
        })
        .catch(error => console.error('Error:', error));
});
