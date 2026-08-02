# 🩺 AI-Based Skin Disease Diagnosis System using Deep Learning and Explainable AI

An AI-powered web application that classifies skin diseases from dermoscopic images using **Deep Learning** and provides **Explainable AI (XAI)** visualizations using **Grad-CAM** and **Saliency Maps**. The project is developed using **TensorFlow/Keras** and deployed using **Flask** with a modern Bootstrap 5 interface.

---

# 📌 Project Overview

Skin diseases are among the most common health conditions worldwide. Early diagnosis plays an important role in successful treatment. This project uses Deep Learning models to classify skin diseases from dermoscopic images and explains predictions using Explainable AI techniques.

The project covers the complete machine learning pipeline from data preprocessing to deployment.

---

# 🎯 Objectives

- Develop an automated skin disease classification system.
- Compare multiple CNN and Transfer Learning models.
- Select the best-performing model.
- Visualize predictions using Explainable AI.
- Deploy the final model using Flask.

---

# 📂 Dataset

**Dataset:** HAM10000

**Total Images:** 10,015

**Number of Classes:** 7

### Disease Classes

- Actinic Keratosis
- Basal Cell Carcinoma
- Benign Keratosis
- Dermatofibroma
- Melanoma
- Melanocytic Nevus
- Vascular Lesion

---

# 🧠 Deep Learning Models

The following models were implemented and compared:

- Basic CNN
- Deep CNN
- CNN + Batch Normalization
- CNN + Dropout
- MobileNetV2
- DenseNet121
- EfficientNetB0
- ResNet50 (Final Selected Model)

---

# 📊 Final Model Performance

## Final Selected Model

**ResNet50**

| Metric | Score |
|---------|-------|
| Accuracy | **66.93%** |
| Precision | **44.80%** |
| Recall | **66.93%** |
| F1 Score | **53.67%** |

---

# 🌐 Flask Application

The Flask web application consists of four major modules.

## 🏠 Dashboard

- Dataset Summary
- Model Information
- Best Model
- Performance Summary
- Model Comparison
- Quick Navigation

---

## 🔬 Diagnosis

- Upload Skin Image
- Disease Prediction
- Confidence Score
- Probability Distribution
- Grad-CAM Visualization
- Saliency Map Visualization

---

## 📊 Analytics

- Phase 4 Baseline Model Comparison
- Final Model Comparison
- Confusion Matrix
- Accuracy Comparison
- ROC Curve

---

## 📄 Reports

- Download Diagnosis Report
- Download Model Comparison Report

---

# 🔥 Explainable AI

The application explains predictions using:

- Grad-CAM
- Saliency Map

These techniques highlight the image regions responsible for the model prediction.

---

# 🛠 Technologies Used

### Programming Language

- Python

### Deep Learning

- TensorFlow
- Keras

### Image Processing

- OpenCV

### Data Analysis

- NumPy
- Pandas

### Visualization

- Matplotlib
- Seaborn

### Web Development

- Flask
- HTML5
- CSS3
- Bootstrap 5

### Version Control

- Git
- GitHub

---

# 📁 Project Structure

```text
SkinCancer_Disease/

│
├── dataset/
│
├── notebooks/
│
├── skin_app/
│   ├── app.py
│   ├── templates/
│   ├── static/
│   ├── utils/
│   ├── models/
│   └── requirements.txt
│
├── results_final.csv
├── phase4_model_comparison.csv
├── requirement.txt
├── Pipfile
├── Pipfile.lock
├── README.md
└── .gitignore
```

---

# 🔄 Project Workflow

```text
HAM10000 Dataset
        │
        ▼
Data Preprocessing
        │
        ▼
Data Augmentation
        │
        ▼
Deep Learning Models
        │
        ▼
Transfer Learning
        │
        ▼
Model Evaluation
        │
        ▼
Explainable AI
        │
        ▼
Flask Deployment
```

---

# 📈 Model Comparison

| Model | Test Accuracy |
|--------|--------------|
| Basic CNN | 31.80% |
| Deep CNN | 43.51% |
| CNN + Batch Normalization | 46.71% |
| CNN + Dropout | 49.04% |
| MobileNetV2 | 50.38% |
| DenseNet121 | 55.89% |
| EfficientNetB0 | 59.02% |
| ResNet50 | **66.93%** |

---

# 📊 Result Files

### phase4_model_comparison.csv

Contains the performance of baseline CNN models.

### results_final.csv

Contains the comparison results of all transfer learning models.

---

# 📸 Application Screenshots

## 🏠 Dashboard

> Insert Dashboard Screenshot

```text
images/dashboard.png
```

---

## 🔬 Diagnosis Page

> Insert Diagnosis Screenshot

```text
images/diagnosis.png
```

---

## 📊 Analytics Page

> Insert Analytics Screenshot

```text
images/analytics.png
```

---

## 📄 Reports Page

> Insert Reports Screenshot

```text
images/reports.png
```

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/SkinCancer_Disease.git
```

---

## Navigate to Project

```bash
cd SkinCancer_Disease
```

---

## Install Dependencies

```bash
pip install -r requirement.txt
```

*(If you rename it to `requirements.txt`, update the command accordingly.)*

---

## Run Flask

```bash
cd skin_app

python app.py
```

---

## Open Browser

```text
http://127.0.0.1:5000
```

---

# 🚀 Future Enhancements

- Mobile Application
- Cloud Deployment
- PDF Report Generation
- Doctor Recommendation System
- Patient History Management
- Real-Time Skin Disease Detection
