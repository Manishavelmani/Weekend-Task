from flask import Flask, render_template, request,send_from_directory
import pandas as pd
import numpy as np
import joblib
from report_generator import create_prediction_report
app = Flask(__name__)

# Load trained model
model = joblib.load("models/model.pkl")
features = joblib.load("models/features.pkl")


data = pd.read_csv("cleaned/cleaned_house_data.csv")

optimized_results = pd.read_csv("reports/optimized_results.csv")
model_results=pd.read_csv("reports/model_results.csv")

best_model = optimized_results.iloc[0]

# ===========================
# Home Page 
# ===========================
@app.route("/")
@app.route("/dashboard")
def dashboard():

    return render_template(

        "dashboard.html",

        total_rows=data.shape[0],

        total_columns=data.shape[1],

        best_model=best_model["Model"],

        mae=best_model["MAE"],

        rmse=best_model["RMSE"],

        r2_score=best_model["R2 Score"]

    )


# ===========================
# Prediction Page
# ===========================
@app.route("/prediction")
def prediction():
    return render_template("prediction.html")

# ===========================
# Predict House Price
# ===========================

@app.route("/predict", methods=["POST"])
def predict():

    overallqual = float(request.form["OverallQual"])
    grlivarea = float(request.form["GrLivArea"])
    garagecars = float(request.form["GarageCars"])
    totalbathrooms = float(request.form["TotalBathrooms"])
    totalbsmtsf = float(request.form["TotalBsmtSF"])
    yearbuilt = float(request.form["YearBuilt"])
    totalhousearea = float(request.form["TotalHouseArea"])
    houseage = float(request.form["HouseAge"])
    overallcond = float(request.form["OverallCond"])
    fullbath = float(request.form["FullBath"])

    user_data = np.array([[
        overallqual,
        grlivarea,
        garagecars,
        totalbathrooms,
        totalbsmtsf,
        yearbuilt,
        totalhousearea,
        houseage,
        overallcond,
        fullbath
    ]])

    prediction = model.predict(user_data)[0]

    # Store inputs for PDF
    features = {
        "Overall Quality": overallqual,
        "Living Area": grlivarea,
        "Garage Cars": garagecars,
        "Total Bathrooms": totalbathrooms,
        "Basement Area": totalbsmtsf,
        "Year Built": yearbuilt,
        "Total House Area": totalhousearea,
        "House Age": houseage,
        "Overall Condition": overallcond,
        "Full Bathrooms": fullbath
    }

    # Generate NEW PDF every prediction
    create_prediction_report(features, prediction)

    return render_template(
        "prediction.html",
        prediction=prediction
    )
# ===========================
# Analytics
# ===========================
@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


# ===========================
# Model Comparison
# ===========================
@app.route("/comparison")
def comparison():

    return render_template(

        "comparison.html",

        model_results=model_results.to_dict(orient="records"),

        optimized_results=optimized_results.to_dict(orient="records")

    )
# ===========================
# Report Page
# ===========================
@app.route("/reports")
def reports():

    return render_template("reports.html")
# ===========================
# Download Reports
# ===========================
@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(
        "reports",
        filename,
        as_attachment=True
    )

# ===========================
# Run Flask
# ===========================
if __name__ == "__main__":
    app.run(debug=True)