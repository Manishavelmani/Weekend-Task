from flask import Flask, render_template, request, send_file
import os
import pickle
import pandas as pd
import numpy as np
import tensorflow as tf

from werkzeug.utils import secure_filename


app = Flask(__name__)


# ==================================================
# BASE DIRECTORY
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ==================================================
# MODEL AND VECTORIZER PATHS
# ==================================================

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "ann_early_stopping.keras"
)

TFIDF_PATH = os.path.join(
    BASE_DIR,
    "models",
    "tfidf_vectorizer.pkl"
)


# ==================================================
# UPLOAD FOLDER
# ==================================================

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "static",
    "uploads"
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ==================================================
# LOAD BEST ANN MODEL
# ==================================================

model = tf.keras.models.load_model(
    MODEL_PATH
)

print("ANN model loaded successfully.")


# ==================================================
# LOAD TF-IDF VECTORIZER
# ==================================================

with open(TFIDF_PATH, "rb") as file:
    tfidf_vectorizer = pickle.load(file)

print("TF-IDF vectorizer loaded successfully.")


# ==================================================
# MODEL PERFORMANCE
# ==================================================

model_results = {

    "ANN": {
        "accuracy": 0.8943,
        "precision": 0.8926,
        "recall": 0.8974,
        "f1": 0.8950,
        "roc_auc": 0.9605
    },

    "RNN": {
        "accuracy": 0.5379,
        "precision": 0.5671,
        "recall": 0.3351,
        "f1": 0.4213,
        "roc_auc": 0.5465
    },

    "LSTM": {
        "accuracy": 0.8825,
        "precision": 0.8749,
        "recall": 0.8937,
        "f1": 0.8842,
        "roc_auc": 0.9448
    },

    "GRU": {
        "accuracy": 0.8928,
        "precision": 0.9064,
        "recall": 0.8770,
        "f1": 0.8915,
        "roc_auc": 0.9577
    },

    "Bi-LSTM": {
        "accuracy": 0.8793,
        "precision": 0.8981,
        "recall": 0.8567,
        "f1": 0.8769,
        "roc_auc": 0.9482
    }
}


# ==================================================
# HOME DASHBOARD
# ==================================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        results=model_results
    )


# ==================================================
# SENTIMENT PREDICTION
# ==================================================

@app.route("/predict", methods=["GET", "POST"])
def predict():

    prediction = None
    confidence = None

    positive_probability = None
    negative_probability = None

    review = ""

    if request.method == "POST":

        review = request.form.get(
            "review",
            ""
        )

        if review.strip():

            # --------------------------------------
            # Convert review to TF-IDF
            # --------------------------------------

            review_tfidf = tfidf_vectorizer.transform(
                [review]
            )


            # --------------------------------------
            # ANN Prediction
            # --------------------------------------

            probability = model.predict(
                review_tfidf,
                verbose=0
            )[0][0]


            probability = float(probability)


            # --------------------------------------
            # Class Probabilities
            # --------------------------------------

            positive_probability = probability

            negative_probability = 1 - probability


            # --------------------------------------
            # Sentiment
            # --------------------------------------

            if probability >= 0.5:

                prediction = "Positive"

                confidence = probability

            else:

                prediction = "Negative"

                confidence = 1 - probability


    return render_template(
        "predict.html",
        prediction=prediction,
        confidence=confidence,
        positive_probability=positive_probability,
        negative_probability=negative_probability,
        review=review
    )


# ==================================================
# MODEL COMPARISON
# ==================================================

@app.route("/comparison")
def comparison():

    return render_template(
        "comparison.html",
        results=model_results
    )


# ==================================================
# TEXT ANALYTICS
# ==================================================

@app.route("/analytics")
def analytics():

    dataset_statistics = {

        "total_reviews": 50000,

        "positive_reviews": 25000,

        "negative_reviews": 25000
    }

    return render_template(
        "analytics.html",
        stats=dataset_statistics
    )


# ==================================================
# BATCH PREDICTION
# ==================================================

@app.route("/batch", methods=["GET", "POST"])
def batch():

    results = None

    summary = None

    if request.method == "POST":

        file = request.files.get("file")


        # ------------------------------------------
        # Check file
        # ------------------------------------------

        if not file or file.filename == "":

            return render_template(
                "batch.html",
                error="Please upload a CSV file."
            )


        if not file.filename.lower().endswith(".csv"):

            return render_template(
                "batch.html",
                error="Please upload a CSV file."
            )


        # ------------------------------------------
        # Save uploaded file
        # ------------------------------------------

        filename = secure_filename(
            file.filename
        )

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(filepath)


        # ------------------------------------------
        # Read CSV
        # ------------------------------------------

        df = pd.read_csv(filepath)


        # ------------------------------------------
        # Check Review column
        # ------------------------------------------

        if "Review" not in df.columns:

            return render_template(
                "batch.html",
                error="CSV must contain a 'Review' column."
            )


        # ------------------------------------------
        # Handle missing reviews
        # ------------------------------------------

        reviews = (
            df["Review"]
            .fillna("")
            .astype(str)
        )


        # ------------------------------------------
        # Convert reviews to TF-IDF
        # ------------------------------------------

        review_tfidf = tfidf_vectorizer.transform(
            reviews
        )


        # ------------------------------------------
        # Predict
        # ------------------------------------------

        probabilities = model.predict(
            review_tfidf,
            verbose=0
        ).ravel()


        # ------------------------------------------
        # Convert probability to sentiment
        # ------------------------------------------

        predictions = np.where(
            probabilities >= 0.5,
            "Positive",
            "Negative"
        )


        # ------------------------------------------
        # Add results to dataframe
        # ------------------------------------------

        df["Sentiment"] = predictions


        df["Confidence"] = np.where(
            probabilities >= 0.5,
            probabilities,
            1 - probabilities
        )


        # ------------------------------------------
        # Save prediction results
        # ------------------------------------------

        output_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            "prediction_results.csv"
        )

        df.to_csv(
            output_path,
            index=False
        )


        # ------------------------------------------
        # Prediction summary
        # ------------------------------------------

        summary = {

            "total": len(df),

            "positive": int(
                (df["Sentiment"] == "Positive").sum()
            ),

            "negative": int(
                (df["Sentiment"] == "Negative").sum()
            )
        }


        # ------------------------------------------
        # Convert dataframe for HTML
        # ------------------------------------------

        results = df.to_dict(
            orient="records"
        )


    return render_template(
        "batch.html",
        results=results,
        summary=summary
    )


# ==================================================
# DOWNLOAD BATCH RESULTS
# ==================================================

@app.route("/download")
def download():

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "prediction_results.csv"
    )


    if not os.path.exists(filepath):

        return "No prediction file available."


    return send_file(
        filepath,
        as_attachment=True
    )


# ==================================================
# RUN FLASK APPLICATION
# ==================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )

