from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet

import os



def generate_model_report(output_path):


    doc = SimpleDocTemplate(
        output_path
    )


    styles = getSampleStyleSheet()

    content = []



    # Title

    content.append(
        Paragraph(
            "Skin Disease Classification Model Comparison Report",
            styles["Title"]
        )
    )


    content.append(
        Spacer(1,20)
    )



    # Phase 4 Comparison

    content.append(
        Paragraph(
            "Phase 4 - Baseline Model Performance",
            styles["Heading2"]
        )
    )


    phase4_data = [

        [
            "Model",
            "Train Acc",
            "Val Acc",
            "Test Acc"
        ],


        [
            "Basic CNN",
            "39.39%",
            "34.29%",
            "31.80%"
        ],


        [
            "Deep CNN",
            "46.39%",
            "44.54%",
            "43.51%"
        ],


        [
            "CNN + BatchNorm",
            "52.08%",
            "51.00%",
            "46.71%"
        ],


        [
            "CNN + Dropout",
            "50.01%",
            "49.60%",
            "49.04%"
        ],


        [
            "MobileNetV2",
            "55.15%",
            "53.06%",
            "50.38%"
        ],


        [
            "DenseNet121",
            "54.17%",
            "56.06%",
            "55.89%"
        ],


        [
            "EfficientNetB0",
            "58.35%",
            "59.92%",
            "59.02%"
        ],


        [
            "ResNet50",
            "25.86%",
            "30.49%",
            "31.07%"
        ]

    ]


    table = Table(
        phase4_data
    )


    table.setStyle(
        TableStyle([
            ("GRID",(0,0),(-1,-1),1,None)
        ])
    )


    content.append(table)


    content.append(
        Spacer(1,25)
    )



    # Phase 7

    content.append(
        Paragraph(
            "Phase 7 - Final Model Performance",
            styles["Heading2"]
        )
    )


    phase7_data = [

        [
            "Model",
            "Accuracy",
            "Precision",
            "Recall",
            "F1"
        ],


        [
            "Basic CNN",
            "53.76%",
            "73.58%",
            "53.76%",
            "59.03%"
        ],


        [
            "Deep CNN",
            "66.93%",
            "44.80%",
            "66.93%",
            "53.67%"
        ],


        [
            "CNN + BatchNorm",
            "47.44%",
            "65.76%",
            "47.44%",
            "53.28%"
        ],


        [
            "CNN + Dropout",
            "52.56%",
            "74.03%",
            "52.56%",
            "57.24%"
        ],


        [
            "MobileNetV2",
            "63.67%",
            "70.09%",
            "63.67%",
            "66.26%"
        ],


        [
            "EfficientNetB0",
            "62.93%",
            "44.80%",
            "62.93%",
            "53.67%"
        ],


        [
            "ResNet50",
            "66.93%",
            "44.80%",
            "66.93%",
            "53.67%"
        ],


        [
            "DenseNet121",
            "64.60%",
            "74.43%",
            "64.60%",
            "68.30%"
        ]

    ]


    table2 = Table(
        phase7_data
    )


    table2.setStyle(
        TableStyle([
            ("GRID",(0,0),(-1,-1),1,None)
        ])
    )


    content.append(table2)


    content.append(
        Spacer(1,25)
    )



    # Best Model

    content.append(
        Paragraph(
            "Final Selected Model: ResNet50",
            styles["Heading2"]
        )
    )


    content.append(
        Paragraph(
            """
            The final model selected for deployment is ResNet50.
            The model provides disease classification with explainability
            using Grad-CAM and Saliency Map techniques.
            """,
            styles["BodyText"]
        )
    )


    content.append(
        Spacer(1,20)
    )



    # Add Charts

    charts = [

        (
            "Confusion Matrix",
            "static/charts/confusion_matrix.png"
        ),

        (
            "Accuracy Comparison",
            "static/charts/precision_recall.png"
        ),

        (
            "ROC Curve",
            "static/charts/roc_curve.png"
        )

    ]



    for title, path in charts:


        if os.path.exists(path):

            content.append(
                Paragraph(
                    title,
                    styles["Heading2"]
                )
            )


            content.append(
                Image(
                    path,
                    width=350,
                    height=250
                )
            )


            content.append(
                Spacer(1,20)
            )



    doc.build(
        content
    )