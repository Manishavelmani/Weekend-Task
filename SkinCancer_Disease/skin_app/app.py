from flask import (Flask,render_template,request,session)
import time
import os
from flask import send_file
from werkzeug.utils import secure_filename

from utils.prediction import (predict_skin_disease,get_preprocessed_image,CLASS_NAMES)
from utils.gradcam import generate_gradcam
from utils.saliency import generate_saliency
from utils.diagnosis_report import generate_diagnosis_report
from utils.model_report import generate_model_report


# ================= Flask App =================

app = Flask(__name__)

app.secret_key = "skin_disease_project"


# ================= Paths =================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR,"static","uploads")

app.config["OUTPUT_FOLDER"] = os.path.join(BASE_DIR,"static","outputs")

os.makedirs(app.config["UPLOAD_FOLDER"],exist_ok=True)

os.makedirs(app.config["OUTPUT_FOLDER"],exist_ok=True)

# ================= Dashboard =================

@app.route("/")
def dashboard():

    return render_template("dashboard.html")



# diagnosis upload image then predict the disease and confidence level
#then show  original image and gramcam ,saliency image

@app.route("/diagnosis", methods=["GET", "POST"])
def diagnosis():

    image_path = None
    disease = None
    confidence = None
    probabilities = None

    gradcam_path = None
    saliency_path = None


    if request.method == "POST":

        file = request.files.get("image")


        if file and file.filename != "":


            filename = secure_filename(
                file.filename
            )


            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )


            file.save(filepath)


            # path used in HTML

            image_path = (
                "uploads/" + filename
            )



            # ================= Prediction =================

            disease, confidence, probabilities = predict_skin_disease(
                filepath
            )



            # ================= Preprocess =================

            image = get_preprocessed_image(
                filepath
            )



            # ================= Unique filenames =================

            timestamp = str(
                int(time.time())
            )


            gradcam_filename = (
                f"gradcam_{timestamp}.jpg"
            )


            saliency_filename = (
                f"saliency_{timestamp}.jpg"
            )



            # ================= Grad-CAM =================

            gradcam_output = os.path.join(
                app.config["OUTPUT_FOLDER"],
                gradcam_filename
            )


            generate_gradcam(
                image,
                filepath,
                gradcam_output
            )


            gradcam_path = (
                "outputs/" + gradcam_filename
            )



            # ================= Saliency =================

            saliency_output = os.path.join(
                app.config["OUTPUT_FOLDER"],
                saliency_filename
            )


            generate_saliency(
                image,
                filepath,
                saliency_output
            )


            saliency_path = (
                "outputs/" + saliency_filename
            )



            # ================= Debug =================

            print(
                "Image:",
                filepath
            )

            print(
                "GradCAM:",
                gradcam_output,
                os.path.exists(gradcam_output)
            )


            print(
                "Saliency:",
                saliency_output,
                os.path.exists(saliency_output)
            )



            # ================= Session =================

            session["image_path"] = image_path

            session["disease"] = disease

            session["confidence"] = confidence

            session["gradcam_path"] = gradcam_path

            session["saliency_path"] = saliency_path



    return render_template(
        "diagnosis.html",
        image_path=image_path,
        disease=disease,
        confidence=confidence,
        probabilities=probabilities,
        class_names=CLASS_NAMES,
        gradcam_path=gradcam_path,
        saliency_path=saliency_path
    )



# ================= Analytics =================

@app.route("/analytics")
def analytics():

    return render_template(
        "analytics.html"
    )



# ================= Reports =================
@app.route("/reports")
def reports():

    return render_template(
        "reports.html",
        image_path=session.get("image_path"),
        disease=session.get("disease"),
        confidence=session.get("confidence"),
        gradcam_path=session.get("gradcam_path"),
        saliency_path=session.get("saliency_path")
    )



# ================= Download Diagnosis Report =================

@app.route("/download_diagnosis_report")
def download_diagnosis_report():


    report_folder = os.path.join(
        BASE_DIR,
        "static",
        "reports"
    )


    os.makedirs(
        report_folder,
        exist_ok=True
    )


    report_path = os.path.join(
        report_folder,
        "Skin_Disease_Diagnosis_Report.pdf"
    )


    generate_diagnosis_report(

        output_path=report_path,

        image_path=os.path.join(
            app.static_folder,
            session.get("image_path")
        ),

        gradcam_path=os.path.join(
            app.static_folder,
            session.get("gradcam_path")
        ),

        saliency_path=os.path.join(
            app.static_folder,
            session.get("saliency_path")
        ),

        disease=session.get(
            "disease"
        ),

        confidence=session.get(
            "confidence"
        )

    )


    return send_file(
        report_path,
        as_attachment=True
    )



# ================= Download Model Report =================

@app.route("/download_model_report")
def download_model_report():


    report_folder = os.path.join(
        BASE_DIR,
        "static",
        "reports"
    )


    os.makedirs(
        report_folder,
        exist_ok=True
    )


    report_path = os.path.join(
        report_folder,
        "Model_Comparison_Report.pdf"
    )


    generate_model_report(
        report_path
    )


    return send_file(
        report_path,
        as_attachment=True
    )

# ================= Run =================

if __name__ == "__main__":

    app.run(
        debug=True
    )