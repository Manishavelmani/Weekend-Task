from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet

import os



def generate_diagnosis_report(
        output_path,
        image_path,
        gradcam_path,
        saliency_path,
        disease,
        confidence
):

    doc = SimpleDocTemplate(
        output_path
    )


    styles = getSampleStyleSheet()

    content = []


    title = Paragraph(
        "Skin Disease Diagnosis Report",
        styles["Title"]
    )


    content.append(title)

    content.append(
        Spacer(1,20)
    )


    data = [

        ["Predicted Disease", disease],

        [
            "Confidence",
            f"{confidence*100:.2f}%"
        ]

    ]


    table = Table(
        data
    )


    table.setStyle(
        TableStyle([
            ("GRID",(0,0),(-1,-1),1,None)
        ])
    )


    content.append(table)

    content.append(
        Spacer(1,20)
    )



    for title, img in [

        ("Uploaded Image", image_path),

        ("Grad-CAM", gradcam_path),

        ("Saliency Map", saliency_path)

    ]:

        content.append(
            Paragraph(
                title,
                styles["Heading2"]
            )
        )


        if os.path.exists(img):

            content.append(
                Image(
                    img,
                    width=250,
                    height=250
                )
            )


        content.append(
            Spacer(1,15)
        )


    doc.build(
        content
    )