# Project Name

This project is designed for the extraction, prediction, and analysis of audio signals, particularly focusing on whistle sounds. The project structure is organized into several modules that handle different aspects of the workflow, from data preparation and model training to prediction and comparison.

## Folder Structure

```
.
├── __init__.py
├── models/
├── Models_vs_years_comparison
│   ├── figs/
│   └── models_vs_years_predictions.ipynb
├── Predict_and_extract
│   ├── Extraction_with_kaggle
│   │   ├── classify_again.ipynb
│   │   ├── utility_script (extraction_using_kaggle).py
│   │   └── Whistle_pipeline_(extraction_with_kaggle).ipynb
│   ├── __init__.py
│   ├── main.py
│   ├── maintenance.py
│   ├── pipeline.ipynb
│   ├── predict_and_extract_online.py
│   ├── predict_online.py
│   ├── process_predictions.py
│   ├── Show_newly_detected_stuff.py
│   ├── utils.py
│   └── vidéoaudio.py
├── README.md
├── requirements.txt
└── Train_model
    ├── Create_dataset
    │   ├── AllWhistlesSubClustering_final.csv
    │   ├── create_batch_data.py
    │   ├── DNN précision - CSV_EVAL.csv
    │   ├── dolphin_signal_train.csv
    │   ├── save_spectrogram.m
    │   └── timings
    │       ├── negatives.csv
    │       └── positives.csv
    ├── csv2dataset.py
    ├── dataset2csv.py
    ├── fine-tune2.ipynb
    ├── fine-tune.ipynb
    ├── __init__.py
    └── Train.py
```

## Contents

### Root Directory
- **`__init__.py`**: Initialization file for the package.
- **`README.md`**: This file, providing an overview and details about the project structure and usage.
- **`requirements.txt`**: Lists all the dependencies required to run the project.

### Models Directory
- **`models/`**: Directory intended for storing trained machine learning models.

### Models_vs_years_comparison
- **`figs/`**: Directory for storing figures and plots generated during model comparison.
- **`models_vs_years_predictions.ipynb`**: Jupyter notebook for comparing model predictions across different years.

### Predict_and_extract
- **`Extraction_with_kaggle`**:
  - **`classify_again.ipynb`**: Jupyter notebook for classifying data again using extracted features.
  - **`utility_script (extraction_using_kaggle).py`**: Python script containing utility functions for extraction.
  - **`Whistle_pipeline_(extraction_with_kaggle).ipynb`**: Jupyter notebook for the whistle extraction pipeline using Kaggle.
- **`__init__.py`**: Initialization file for the `Predict_and_extract` module.
- **`main.py`**: Main script to run the prediction and extraction pipeline.
- **`maintenance.py`**: Script for maintaining and updating the dataset and models.
- **`pipeline.ipynb`**: Jupyter notebook detailing the entire pipeline process.
- **`predict_and_extract_online.py`**: Script for online prediction and extraction.
- **`predict_online.py`**: Script for making predictions online.
- **`process_predictions.py`**: Script for processing and analyzing the predictions.
- **`Show_newly_detected_stuff.py`**: Script to display newly detected features.
- **`utils.py`**: Utility functions used across the `Predict_and_extract` module.
- **`vidéoaudio.py`**: Script for handling video and audio processing.

### Train_model
- **`Create_dataset`**:
  - **`AllWhistlesSubClustering_final.csv`**: Final CSV file for sub-clustering of all whistles.
  - **`create_batch_data.py`**: Script to create batch data from raw datasets.
  - **`DNN précision - CSV_EVAL.csv`**: CSV file containing evaluation metrics of the DNN model.
  - **`dolphin_signal_train.csv`**: CSV file containing training data for dolphin signals.
  - **`save_spectrogram.m`**: MATLAB script for saving spectrograms.
  - **`timings`**:
    - **`negatives.csv`**: CSV file containing negative samples.
    - **`positives.csv`**: CSV file containing positive samples.
- **`csv2dataset.py`**: Script to convert CSV data to dataset format.
- **`dataset2csv.py`**: Script to convert datasets back to CSV format.
- **`fine-tune2.ipynb`**: Jupyter notebook for fine-tuning the model (version 2).
- **`fine-tune.ipynb`**: Jupyter notebook for fine-tuning the model.
- **`__init__.py`**: Initialization file for the `Train_model` module.
- **`Train.py`**: Script to train the machine learning models.

## Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.x
- Jupyter Notebook
- All dependencies listed in `requirements.txt`

### Installation

1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

### Usage

1. **Data Preparation**:
   - Use the scripts in `Train_model/Create_dataset` to prepare your dataset.
   - Ensure your dataset files are correctly formatted and placed in the appropriate directories.

2. **Model Training**:
   - Use the Jupyter notebooks and scripts in `Train_model` to train your models.
   - Fine-tune your models as necessary using the provided notebooks.

3. **Prediction and Extraction**:
   - Run the scripts in `Predict_and_extract` to perform predictions and extract features.
   - Utilize the provided notebooks to classify and process the extracted data.

4. **Analysis**:
   - Use the `Models_vs_years_comparison` module to compare model predictions over different years and visualize the results.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

---

For any questions or issues, please open an issue on GitHub or contact the project maintainers.