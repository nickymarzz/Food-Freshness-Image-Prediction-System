# Local GPU Training & Setup Guide

This guide walks you through setting up, configuring, and retraining the **Food Freshness & Produce Category Prediction System** locally using an NVIDIA GPU (e.g., RTX 30/40/50 series) or cloud workstation.

---

## ⚠️ Important Note on TensorFlow & Windows GPU Support

> **Windows Subsystem for Linux (WSL2) Recommendation:**
> TensorFlow officially deprecated native Windows GPU support after version 2.10. Running TensorFlow in native Windows PowerShell/CMD will default to CPU execution.
>
> **To utilize your NVIDIA GPU with CUDA acceleration on Windows, execute within WSL2 (Ubuntu 22.04 / 24.04 LTS).**
> If you are on native Linux, standard CUDA drivers and container runtimes work directly out of the box.

---

## Step 1: Environment Setup

Execute these commands inside your terminal (WSL2 / Linux shell or native terminal):

```bash
# 1. Clone the project repository
git clone https://github.com/nickymarzz/Food-Freshness-Image-Prediction-System.git
cd Food-Freshness-Image-Prediction-System

# 2. Create and activate a clean virtual environment
python3 -m venv venv
source venv/bin/activate
# (On Windows PowerShell: .\venv\Scripts\Activate.ps1)

# 3. Upgrade pip and install all project dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Verify GPU Acceleration

Verify that TensorFlow detects your physical GPU:

```bash
python -c "import tensorflow as tf; print('GPUs Detected:', tf.config.list_physical_devices('GPU'))"
```

A properly configured environment outputs:
```text
GPUs Detected: [PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
```

---

## Step 2: Dataset Acquisition & Organization

1. Download the dataset from Kaggle:
   🔗 **[Fruits and Vegetables Spoilage Dataset](https://www.kaggle.com/datasets/muhriddinmuxiddinov/fruits-and-vegetables-dataset)**
2. Extract the archive. The training pipeline expects raw images organized under `artifacts/data/raw/` in the following directory layout:

```text
artifacts/
└── data/
    └── raw/
        ├── Fruits/
        │   ├── Apple/
        │   │   ├── Fresh/       (contains .jpg / .png images)
        │   │   └── Rotten/
        │   ├── Banana/
        │   │   ├── Fresh/
        │   │   └── Rotten/
        │   ├── Mango/
        │   ├── Orange/
        │   └── Strawberry/
        └── Vegetables/
            ├── Bellpepper/
            │   ├── Fresh/
            │   └── Rotten/
            ├── Carrot/
            ├── Cucumber/
            ├── Potato/
            └── Tomato/
```

### Automated Dataset Directory Formatter

If you extracted the Kaggle archive into a directory named `fruits-and-vegetables-dataset`, run this utility script to sort all produce items automatically:

```python
import shutil
from pathlib import Path

source_dir = Path("fruits-and-vegetables-dataset")
raw_dir = Path("artifacts/data/raw")
categories = {
    'Fruits': ['Mango', 'Banana', 'Orange', 'Apple', 'Strawberry'],
    'Vegetables': ['Cucumber', 'Bellpepper', 'Tomato', 'Potato', 'Carrot']
}

for cat, items in categories.items():
    for item in items:
        for state in ['Fresh', 'Rotten']:
            src = source_dir / cat / f"{state}{item}"
            dst = raw_dir / cat / item / state
            if src.exists():
                dst.mkdir(parents=True, exist_ok=True)
                for f in src.glob("*.*"):
                    if not (dst / f.name).exists():
                        shutil.move(str(f), str(dst / f.name))

print("Dataset organized successfully under artifacts/data/raw/")
```

---

## Step 3: Execute the Full Training Pipeline

Execute the end-to-end reproducible training pipeline:

```bash
python -m src.pipeline.training_pipeline
```

### Pipeline Execution Lifecycle

1. **Data Ingestion:** Validates directory integrity, checks image files for corruption, and generates `metadata.json`.
2. **Data Transformation:** Standardizes RGB images to $224 \times 224$ and creates deterministic 70/15/15 train/val/test splits (`seed=42`).
3. **Freshness Model Training:** Trains the binary MobileNetV2 classifier with early stopping and saves weights to `artifacts/models/mobilenetv2_baseline.keras`.
4. **Category Classifier Training:** Trains the 10-class produce taxonomy classifier with `ReduceLROnPlateau` and saves weights to `artifacts/models/category_classifier.keras`.
5. **Freshness Model Evaluation:** Computes quantitative metrics and exports confusion matrices and ROC curves.
6. **Category Model Evaluation:** Evaluates 10-class produce classification, exports multi-class ROC curves, and generates qualitative error analysis plots.

---

## Step 4: Verification & Web Application Serving

### 1. Test Single Image Inference

```bash
python -m src.pipeline.prediction_pipeline
```

### 2. Launch the Interactive Gradio Interface

```bash
python -m src.app.app
```
Navigate to **`http://localhost:7860`** to test produce classification using upload or webcam input.

### 3. Launch the Production FastAPI REST API

```bash
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```
API documentation is accessible at **`http://localhost:8000/docs`**.
