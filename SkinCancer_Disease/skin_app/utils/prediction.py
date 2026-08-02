import os

import cv2
import numpy as np
import tensorflow as tf

from tensorflow.keras.applications.resnet50 import preprocess_input


# --------------------------------------------------
# Model Path
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "resnet50_model_final.keras"
)


# --------------------------------------------------
# Load Model
# --------------------------------------------------

model = tf.keras.models.load_model(
    MODEL_PATH
)


# --------------------------------------------------
# Class Names
# --------------------------------------------------

CLASS_NAMES = [

    "Actinic Keratosis",

    "Basal Cell Carcinoma",

    "Benign Keratosis",

    "Dermatofibroma",

    "Melanoma",

    "Melanocytic Nevus",

    "Vascular Lesion"

]


# --------------------------------------------------
# Image Preprocessing
# --------------------------------------------------

def preprocess_image(image_path):

    image = cv2.imread(
        image_path
    )

    image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    image = cv2.resize(
        image,
        (224,224)
    )

    image = image.astype(
        np.float32
    )

    image = preprocess_input(
        image
    )

    image = np.expand_dims(
        image,
        axis=0
    )

    return image


# --------------------------------------------------
# Prediction Function
# --------------------------------------------------

def predict_skin_disease(image_path):

    image = preprocess_image(
        image_path
    )

    prediction = model.predict(
        image,
        verbose=0
    )

    predicted_index = np.argmax(
        prediction
    )

    disease = CLASS_NAMES[
        predicted_index
    ]

    confidence = float(
        prediction[0][predicted_index]
    )

    probabilities = prediction[0]

    return (

        disease,

        confidence,

        probabilities

    )


# --------------------------------------------------
# Return Preprocessed Image
# (Used for Grad-CAM & Saliency)
# --------------------------------------------------

def get_preprocessed_image(image_path):

    return preprocess_image(
        image_path
    )