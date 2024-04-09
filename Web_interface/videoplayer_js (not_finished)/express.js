const express = require('express');
const app = express();
const fs = require('fs');
const path = require('path');

const videosDirectory = '/media/DOLPHIN/Analyses_alexis/2023_analysed/Exp_01_Aug_2023_1245_channel_0/extraits/';

app.use(express.static('public'));

// Route to fetch video files
app.get('/videos', (req, res) => {
    fs.readdir(videosDirectory, (err, files) => {
        if (err) {
            console.error('Error reading videos directory:', err);
            res.status(500).send('Internal Server Error');
            return;
        }
        res.json(files);
    });
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
