const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();

app.get('/videos', (req, res) => {
    const videosDir = path.join(__dirname, 'videos');
    fs.readdir(videosDir, (err, files) => {
        if (err) {
            res.status(500).send('Error reading videos directory');
            return;
        }
        const videos = files.filter(file => file.endsWith('.mp4'));
        res.json({ videos });
    });
});

app.use(express.static('public')); // Serve static files (HTML, CSS, JS, etc.)

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
