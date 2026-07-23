from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime


def create_prediction_report(features, prediction):

    pdf_path = "reports/Prediction_Report.pdf"
    

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "<b><font size=18>House Price Prediction Report</font></b>",
        styles["Title"]
    )

    elements.append(title)
    elements.append(Spacer(1,20))


    date = Paragraph(
        f"<b>Date :</b> {datetime.now().strftime('%d-%m-%Y %H:%M')}",
        styles["Normal"]
    )

    elements.append(date)
    elements.append(Spacer(1,20))


    elements.append(
        Paragraph(
            "<b>Input Features</b>",
            styles["Heading2"]
        )
    )

    data = [["Feature","Value"]]

    for key,value in features.items():
        data.append([key,str(value)])


    table = Table(data,colWidths=[180,180])

    table.setStyle(
        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("BACKGROUND",(0,1),(-1,-1),colors.beige),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

            ("BOTTOMPADDING",(0,0),(-1,0),10),

        ])
    )

    elements.append(table)

    elements.append(Spacer(1,25))


    elements.append(
        Paragraph(
            "<b>Prediction Result</b>",
            styles["Heading2"]
        )
    )


    result = Paragraph(

        f"""
        <font size=16 color='green'>
        Estimated House Price :
        <b>${prediction:,.2f}</b>
        </font>
        """,

        styles["Normal"]

    )

    elements.append(result)

    elements.append(Spacer(1,20))


    summary = Paragraph(

        """
        <b>Summary</b><br/><br/>

        The house price was predicted using the optimized
        CatBoost Regressor model. The prediction is based
        on the user-provided housing characteristics,
        including quality, living area, garage capacity,
        basement area, house age, and other important
        structural features.

        """,

        styles["BodyText"]

    )

    elements.append(summary)

    elements.append(Spacer(1,20))


    model = Paragraph(

        """
        <b>Model Information</b>

        <br/><br/>

        • Algorithm : CatBoost Regressor

        <br/>

        • Dataset : Ames Housing Dataset

        <br/>

        • Target Variable : SalePrice

        <br/>

        • Prediction Type : Regression

        """,

        styles["BodyText"]

    )

    elements.append(model)

    doc.build(elements)

    return pdf_path