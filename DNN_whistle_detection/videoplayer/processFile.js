const fs = require('fs');
const path = require('path');

// Function to read directory and filter files
function readDirectory(directoryPath) {
    return fs.readdirSync(directoryPath).filter(file => fs.statSync(path.join(directoryPath, file)).isFile());
}

// Function to extract videos and corresponding images
function processFiles(videoDirectory, imageDirectory) {
    try {
        const videos = readDirectory(videoDirectory);
        const images = readDirectory(imageDirectory);
        // console.log("Videos:", videos);
        // console.log("Images:", images);
        videos.forEach(video => {
            const videoName = path.parse(video).name;
            const [start, end] = videoName.split('_').slice(1).map(parseFloat);
    
            images.forEach(image => {
                const imageName = path.parse(image).name;
                const [imageStart, imageEnd] = imageName.split('_').map(parseFloat);
    
                if (imageStart >= start && imageStart <= end) {
                    console.log(`Display ${image} at ${imageStart}s`);
                }
            });
        });
                    // Code to display image at specified time
    } catch (error) {
        console.error("Error:", error);
    }
    
}

// Usage
const videoDirectory = '/media/DOLPHIN/Analyses_alexis/2023_analysed/Exp_01_Aug_2023_0845_channel_1/extraits';
const imageDirectory = '/media/DOLPHIN/Analyses_alexis/2023_analysed/Exp_01_Aug_2023_0845_channel_1/positive';
// Before processing files


processFiles(videoDirectory, imageDirectory);
