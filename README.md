
to be written


https://sites.google.com/view/dolphinstest/ 

https://www.zebrain.bio.ens.psl.eu/delfin/

  ├── templates
│   │   │   └── video.html
│   │   └── test.py
│   └── whistle2vid.py
├── DNN_whistle_detection
│   ├── classify_again.ipynb
│   ├── __init__.py
│   ├── models
│   │   ├── Augmented_dataset.h5
│   │   ├── CNN_Vgg_V2.h5
│   │   ├── model_finetuned_vgg.h5
│   │   ├── model_vgg.h5
│   │   └── MPFTACC95+.h5
│   ├── Predict_and_extract
│   │   ├── Extraction_with_kaggle
│   │   │   ├── utility_script (extraction_using_kaggle).py
│   │   │   └── Whistle_pipeline_(extraction_with_kaggle).ipynb
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── maintenance.py
│   │   ├── pipeline.ipynb
│   │   ├── predict_and_extract_online.py
│   │   ├── predict_online.py
│   │   ├── process_predictions.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-39.pyc
│   │   │   ├── predict_and_extract_online.cpython-39.pyc
│   │   │   ├── process_predictions.cpython-311.pyc
│   │   │   ├── process_predictions.cpython-38.pyc
│   │   │   ├── process_predictions.cpython-39.pyc
│   │   │   ├── utils.cpython-311.pyc
│   │   │   ├── utils.cpython-38.pyc
│   │   │   └── utils.cpython-39.pyc
│   │   ├── Show_newly_detected_stuff.py
│   │   ├── utils.py
│   │   └── vidéoaudio.py
│   ├── README.md
│   ├── requirements.txt
│   └── Train_model
│       ├── Create_dataset
│       │   ├── AllWhistlesSubClustering_final.csv
│       │   ├── create_batch_data.py
│       │   ├── DNN précision - CSV_EVAL.csv
│       │   ├── dolphin_signal_train.csv
│       │   ├── save_spectrogram.m
│       │   └── timings
│       │       ├── negatives.csv
│       │       └── positives.csv
│       ├── csv2dataset.py
│       ├── dataset2csv.py
│       ├── fine-tune2.ipynb
│       ├── fine-tune.ipynb
│       ├── __init__.py
│       └── Train.py
├── Dolphin_image_detection (Yolo)
│   ├── Finetune Yolo
│   │   ├── dolphin_image_detection_yolov5.ipynb
│   │   ├── finetune-yolo-dolphins-ndd20.ipynb
│   │   ├── finetune yolo dolphins NDD20.ipynb
│   │   ├── Format Data and Train YOLO after retrieving CVAT data.ipynb
│   │   ├── Prepare NDD20 Yolo dataset.ipynb
│   │   └── yolokaggle.ipynb
│   └── Variance based with thresholding methods (unsuccessful)
│       ├── checkpoint.csv
│       ├── detect_dolphins_in.py
│       ├── detect dolphins.ipynb
│       ├── divide_videos.py
│       ├── sauvegarde.py
│       ├── Split&detect_online.py
│       ├── test.py
│       └── utils.py
├── README.md
├── requirements_conda.txt
├── requirements_pip_freeze.txt
├── test_predictions.png
├── Video_against_spectro
│   └── test_text
└── Web_interface
    ├── Aborted_ideas
    │   ├── AWS_hosting
    │   │   ├── index.html
    │   │   ├── paths.json
    │   │   └── testing.html
    │   ├── Nexctcloud_using_API
    │   │   ├── nextcloud_embed.html
    │   │   └── nextcloud.py
    │   ├── videoplayer_flask
    │   │   ├── app.py
    │   │   ├── app_sauvegarde.py
    │   │   ├── app.wsgi
    │   │   ├── Demo_Eilat
    │   │   │   ├── app_demo_eilat.py
    │   │   │   ├── Demo_Eilat
    │   │   │   │   ├── app_demo_eilat.py
    │   │   │   │   ├── README.md
    │   │   │   │   ├── requirements.txt
    │   │   │   │   ├── static
    │   │   │   │   │   ├── styles.css
    │   │   │   │   │   └── styles_dolphin.css
    │   │   │   │   ├── templates
    │   │   │   │   │   ├── index.html
    │   │   │   │   │   ├── select_day.html
    │   │   │   │   │   ├── select_hour.html
    │   │   │   │   │   ├── select_month.html
    │   │   │   │   │   ├── show_files.html
    │   │   │   │   │   ├── thank_you.html
    │   │   │   │   │   └── video.html
    │   │   │   │   └── Vid_demo_Eilat
    │   │   │   │       ├── Exp_03_Mar_2024_1345_channel_0
    │   │   │   │       │   └── Exp_03_Mar_2024_1345_channel_0.wav_predictions.csv
    │   │   │   │       └── Exp_03_Mar_2024_1345_channel_1
    │   │   │   │           └── Exp_03_Mar_2024_1345_channel_1.wav_predictions.csv
    │   │   │   ├── README.md
    │   │   │   ├── requirements.txt
    │   │   │   ├── static
    │   │   │   │   ├── styles.css
    │   │   │   │   └── styles_dolphin.css
    │   │   │   ├── templates
    │   │   │   │   ├── index.html
    │   │   │   │   ├── select_day.html
    │   │   │   │   ├── select_hour.html
    │   │   │   │   ├── select_month.html
    │   │   │   │   ├── show_files.html
    │   │   │   │   ├── thank_you.html
    │   │   │   │   └── video.html
    │   │   │   └── Vid_demo_Eilat
    │   │   │       ├── Exp_03_Mar_2024_1345_channel_0
    │   │   │       │   └── Exp_03_Mar_2024_1345_channel_0.wav_predictions.csv
    │   │   │       └── Exp_03_Mar_2024_1345_channel_1
    │   │   │           └── Exp_03_Mar_2024_1345_channel_1.wav_predictions.csv
    │   │   ├── php
    │   │   │   └── tests.php
    │   │   ├── static
    │   │   │   ├── styles.css
    │   │   │   └── styles_dolphin.css
    │   │   ├── templates
    │   │   │   ├── index.html
    │   │   │   ├── select_day.html
    │   │   │   ├── select_hour.html
    │   │   │   ├── select_month.html
    │   │   │   ├── show_files.html
    │   │   │   ├── thank_you.html
    │   │   │   └── video.html
    │   │   └── templates_sauvegarde
    │   │       ├── index.html
    │   │       ├── index_sauvegarde.html
    │   │       ├── select_day.html
    │   │       ├── select_hour.html
    │   │       ├── select_month.html
    │   │       ├── show_files.html
    │   │       └── video.html
    │   ├── videoplayer_js (not_finished)
    │   │   ├── express.js
    │   │   ├── index.html
    │   │   ├── processFile.js
    │   │   ├── script.js
    │   │   ├── styles.css
    │   │   ├── templates
    │   │   │   ├── experiment.html
    │   │   │   ├── index.html
    │   │   │   └── video.html
    │   │   ├── test.py
    │   │   ├── tkt.js
    │   │   ├── videoplayer.html
    │   │   └── videos.json
    │   └── videoplayer_no_backend (not finished)
    │       ├── embed.html
    │       ├── extraits_avec_audio
    │       │   ├── json_vid.py
    │       │   ├── videos.json
    │       │   └── vid.html
    │       ├── tests.php
    │       ├── video_html_2.py
    │       ├── video_html.py
    │       └── videos.json
    └── Working webpage : nextcloud
        ├── JSON_PATHS_generator.bash
        ├── paths.json
        ├── script_F&F.js
        ├── styles_F&F.css
        ├── WEBSITE_F&F.html
        └── WEBSITE.html
