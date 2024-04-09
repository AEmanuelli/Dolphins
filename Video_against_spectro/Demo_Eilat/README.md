# Structure

- 📂 Demo_Eilat/
    - 📂 static/
        - 📜 styles_dolphin.css: CSS file for webpage design.
    - 📂 templates/
        - 📜 index.html: Homepage allowing users to select a year from available options (2023/2024).
        - 📜 select_day.html: Page for selecting a day from available options.
        - 📜 select_hour.html: Page for selecting an hour from available options.
        - 📜 select_month.html: Page for selecting a month from available options.
        - 📜 show_files.html: Page for choosing a video excerpt from available options in two channels for the selected recording.
        - 📜 thank_you.html: Page displayed after submitting a comment, with a redirection link to index.html.
        - 📜 video.html: Interface for commenting on the video excerpt.
    - 📂 Vid_demo_Eilat/
        - 📂 Contains sample results of extractions.
    - 📜 app_demo_eilat.py: This file contains the backend logic of the web application.
    - 📜 requirements.txt: Configuration file listing dependencies required for the backend.
    - 📜 README.md: You are here! This file provides an overview of the contents and setup instructions for the Demo_Eilat web application.

## Indications

### To run the demo

1. Navigate to the directory:

```bash
cd Video_against_spectro/Demo_Eilat
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

or 

```bash
pip3 install -r requirements.txt
```

3. Run the app locally:

```bash

python app_demo_eilat.py
```