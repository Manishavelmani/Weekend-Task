import os
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime

from analytics import (
    total_records,
    total_features,
    missing_values,
    duplicate_records,
    business_insights,

)
def generate_preprocessing_report():

    filename = "reports/Data_Preprocessing_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER

    story = []

    # =====================================
    # Cover Page
    # =====================================

    story.append(
        Paragraph(
            "HOTEL BOOKING DEMAND ANALYSIS",
            title_style
        )
    )

    story.append(Spacer(1,0.3*inch))

    story.append(
        Paragraph(
            "<b>DATA PREPROCESSING REPORT</b>",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1,0.2*inch))

    story.append(
        Paragraph(
            f"Generated on : {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1,0.5*inch))
    story.append(
        Paragraph(
            "Dataset Overview",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1,0.2*inch))

    data = [

        ["Metric","Value"],

        ["Total Records", total_records()],

        ["Total Features", total_features()],

        ["Missing Values", missing_values()],

        ["Duplicate Records", duplicate_records()]

    ]

    table = Table(data,colWidths=[220,180])

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("BACKGROUND",(0,1),(-1,-1),colors.beige),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

            ("BOTTOMPADDING",(0,0),(-1,0),10)

        ])

    )

    story.append(table)

    story.append(Spacer(1,0.4*inch))
    story.append(
        Paragraph(
            "Project Overview",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 0.15 * inch))

    overview = """
    This project focuses on analyzing hotel booking demand using
    data preprocessing, exploratory data analysis (EDA),
    statistical analysis, hypothesis testing, and an interactive
    Flask dashboard.

    The objective of the preprocessing stage is to improve the
    quality of the dataset by handling missing values, removing
    duplicates, correcting data types, treating outliers, and
    creating meaningful features for further analysis.
    """

    story.append(
        Paragraph(
            overview,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.35 * inch))
    story.append(
        Paragraph(
            "Data Cleaning Process",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 0.15 * inch))
    story.append(
        Paragraph(
            "<b>1. Missing Values</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    The dataset was examined for missing values.
    Missing values were identified using pandas
    'isnull()' function.

    Categorical variables were imputed using the mode,
    while numerical variables were handled using
    appropriate statistical techniques such as median
    imputation where necessary.
    """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    story.append(
        Paragraph(
            "<b>2. Duplicate Records</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    Duplicate records were identified using
    the duplicated() function and removed to
    maintain dataset consistency and prevent
    biased analytical results.
    """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    story.append(
        Paragraph(
            "<b>3. Data Type Conversion</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    Date columns were converted into datetime
    format to enable time-based analysis.
    Categorical variables were encoded where
    necessary for statistical analysis and
    machine learning compatibility.
    """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    story.append(
        Paragraph(
            "<b>4. Outlier Treatment</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    Outliers in the Average Daily Rate (ADR)
    were detected using boxplots and Z-score
    analysis. Extreme values were examined and
    treated appropriately to improve the quality
    of statistical analysis.
    """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.35 * inch))
    story.append(
        Paragraph(
            "Feature Engineering",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
    Several new features were created to enhance
    business understanding and analytical capability.

    • Total Stay

    • Total Guests

    • Lead Time Category

    • Stay Type

    • Revenue Category

    • Season

    • Guest Status

    These engineered features helped improve
    visualization, statistical analysis and
    business insight generation.
    """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Paragraph(
            "Conclusion",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
    The preprocessing stage successfully transformed
    the raw hotel booking dataset into a clean,
    consistent, and analysis-ready dataset.
    The cleaned dataset was subsequently used
    for exploratory data analysis, statistical
    testing, dashboard development, and business
    insight generation.
    """,
            styles["BodyText"]
        )
    )
    doc.build(story)

    return filename
def generate_eda_report():

    filename = "reports/EDA_Report.pdf"

    doc = SimpleDocTemplate(
        filename,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title = styles["Heading1"]
    title.alignment = TA_CENTER
    story = []

    # ==============================
    # Cover Page
    # ==============================

    title = styles["Heading1"]
    title.alignment = TA_CENTER

    story.append(
        Paragraph(
            "HOTEL BOOKING DEMAND ANALYSIS",
            title
        )
    )

    story.append(Spacer(1, 0.3 * inch))

    story.append(
        Paragraph(
            "Exploratory Data Analysis (EDA) Report",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 0.5 * inch))

    story.append(
        Paragraph(
            "<b>Project:</b> Hotel Booking Demand Analysis",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "<b>Tools Used:</b> Python, Pandas, NumPy, Matplotlib, Seaborn, Flask",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Generated On:</b> {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 2 * inch))

    story.append(
        Paragraph(
            "<b>Prepared By</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "Hotel Booking Demand Analysis using Python, Statistics, EDA and Flask Dashboard",
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    story.append(
        Paragraph(
            "Project Overview",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    overview = """
    The Hotel Booking Demand Analysis project focuses on analyzing hotel
    reservation data to understand customer booking behaviour,
    seasonal demand, cancellation patterns, pricing trends and hotel
    performance.

    Exploratory Data Analysis (EDA) was performed using Python libraries
    such as Pandas, NumPy, Matplotlib and Seaborn to identify important
    patterns, relationships and business insights.

    The findings from this analysis help hotel management improve
    occupancy, optimize pricing strategies, reduce cancellations and
    support data-driven decision making.
    """

    story.append(
        Paragraph(
            overview,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    # ==========================================================
    # Monthly Booking Analysis
    # ==========================================================

    story.append(
        Paragraph(
            "1. Monthly Booking Analysis",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    img = Image(
        "static/images/monthly_bookings.png",
        width=6.5 * inch,
        height=3.5 * inch
    )

    story.append(img)

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "<b>Observation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    The monthly booking trend indicates clear variations in hotel
    reservations throughout the year. August records the highest
    number of bookings, while some months experience comparatively
    lower demand.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Interpretation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    Booking demand changes according to seasonal travel,
    public holidays and vacation periods.
    Peak months generate significantly higher occupancy rates.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Business Insight</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    Hotels experience maximum customer demand during peak travel
    months. Understanding these seasonal trends enables hotel
    management to forecast occupancy, optimize staffing levels and
    maximize revenue.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Recommendation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    • Increase room availability during peak seasons.
    <br/>
    • Apply dynamic pricing strategies.
    <br/>
    • Launch promotional campaigns during low-demand months.
    <br/>
    • Improve workforce planning based on booking forecasts.
            """,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    # ==========================================================
    # Hotel Distribution
    # ==========================================================

    story.append(
        Paragraph(
            "2. Hotel Distribution",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    img = Image(
        "static/images/hotel_distribution.png",
        width=6.5 * inch,
        height=3.5 * inch
    )

    story.append(img)

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "<b>Observation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    The City Hotel receives a higher number of bookings than the
    Resort Hotel. Resort Hotels account for a comparatively smaller
    share of total reservations.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Interpretation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    Customers prefer City Hotels because of easier accessibility,
    business travel, and urban tourism. Resort Hotels are mainly
    chosen for vacations and leisure trips.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Business Insight</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    City Hotels contribute a larger portion of total bookings and
    revenue. Resort Hotels experience more seasonal demand and lower
    occupancy during off-peak periods.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Recommendation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    • Increase promotional campaigns for Resort Hotels during
    off-season periods.
    <br/><br/>
    • Continue dynamic pricing strategies for City Hotels during
    high-demand periods.
    <br/><br/>
    • Introduce vacation packages and family offers to improve
    Resort Hotel occupancy.
            """,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    # ==========================================================
    # Season Distribution
    # ==========================================================

    story.append(
        Paragraph(
            "3. Season Distribution",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    img = Image(
        "static/images/season_distribution.png",
        width=6.5 * inch,
        height=3.5 * inch
    )

    story.append(img)

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "<b>Observation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    Hotel bookings vary significantly across different seasons.
    Certain seasons experience considerably higher booking volumes,
    while others have comparatively lower customer demand.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Interpretation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    Seasonal demand strongly influences hotel occupancy.
    Holiday periods, weather conditions and vacation schedules
    play an important role in customer booking behaviour.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Business Insight</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    Understanding seasonal demand enables hotel management to
    optimize pricing strategies, allocate resources efficiently
    and prepare for fluctuations in customer arrivals.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Recommendation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    • Increase room prices during high-demand seasons.
    <br/><br/>
    • Launch promotional offers during off-season periods.
    <br/><br/>
    • Plan staffing, inventory and operational activities
    according to seasonal booking trends.
            """,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    # ==========================================================
    # Customer Type Analysis
    # ==========================================================

    story.append(
        Paragraph(
            "4. Customer Type Analysis",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    img = Image(
        "static/images/customer_type.png",
        width=6.5 * inch,
        height=3.5 * inch
    )

    story.append(img)

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "<b>Observation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    The distribution of bookings varies among different customer
    types. Transient customers contribute the largest share of hotel
    bookings, while Contract, Group and Transient-Party customers
    represent comparatively smaller segments.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Interpretation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    Most hotel reservations are made by individual travellers rather
    than organized groups or corporate contracts. This indicates that
    the business primarily depends on independent customers.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Business Insight</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    Customer segmentation helps hotels understand booking behaviour,
    develop targeted marketing campaigns and improve customer
    retention strategies.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Recommendation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    • Introduce loyalty programs for frequent transient customers.
    <br/><br/>
    • Offer corporate discounts to increase contract bookings.
    <br/><br/>
    • Develop customized packages for group reservations.
    <br/><br/>
    • Personalize promotional campaigns based on customer type.
            """,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    # ==========================================================
    # Lead Time Distribution
    # ==========================================================

    story.append(
        Paragraph(
            "5. Lead Time Distribution",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    img = Image(
        "static/images/lead_time_distribution.png",
        width=6.5 * inch,
        height=3.5 * inch
    )

    story.append(img)

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "<b>Observation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    The lead time distribution is positively skewed. Most hotel
    bookings are made within a relatively short period before the
    arrival date, while only a small proportion of customers book
    several months in advance.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Interpretation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    Customers generally prefer making reservations closer to their
    travel dates. Long lead-time bookings are less common but provide
    better visibility for occupancy planning.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Business Insight</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    Lead time has a significant impact on hotel demand forecasting,
    pricing strategies and cancellation management. Monitoring
    booking patterns helps hotels optimize room allocation and
    revenue planning.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Recommendation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    • Encourage early reservations through advance booking discounts.
    <br/><br/>
    • Apply dynamic pricing for last-minute bookings.
    <br/><br/>
    • Improve occupancy forecasting using historical lead-time trends.
    <br/><br/>
    • Monitor long lead-time reservations to reduce cancellation risk.
            """,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    # ==========================================================
    # ADR Distribution
    # ==========================================================

    story.append(
        Paragraph(
            "6. Average Daily Rate (ADR) Distribution",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    img = Image(
        "static/images/adr_distribution.png",
        width=6.5 * inch,
        height=3.5 * inch
    )

    story.append(img)

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "<b>Observation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    The Average Daily Rate (ADR) shows noticeable variation across
    hotel bookings. Most reservations fall within a moderate price
    range, while a smaller number of bookings have significantly
    higher daily rates.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Interpretation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    The distribution indicates that the majority of customers book
    rooms at standard prices. Higher ADR values are generally
    associated with premium rooms, peak travel seasons and luxury
    services.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Business Insight</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    ADR is one of the most important hotel performance indicators.
    Monitoring ADR helps management evaluate pricing effectiveness,
    revenue generation and customer spending behaviour.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Recommendation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    • Implement dynamic pricing based on seasonal demand.
    <br/><br/>
    • Promote premium room categories during high-demand periods.
    <br/><br/>
    • Offer attractive pricing packages during off-season periods.
    <br/><br/>
    • Continuously monitor ADR trends to maximize hotel revenue.
            """,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    # ==========================================================
    # Cancellation Analysis
    # ==========================================================

    story.append(
        Paragraph(
            "7. Cancellation Analysis",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    img = Image(
        "static/images/cancellation_rate.png",
        width=6.5 * inch,
        height=3.5 * inch
    )

    story.append(img)

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "<b>Observation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    The cancellation analysis indicates that while a large proportion
    of bookings are successfully completed, a significant percentage
    of reservations are cancelled before the arrival date. This
    represents an important challenge for hotel operations and revenue
    management.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Interpretation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    Booking cancellations reduce occupancy levels and create
    uncertainty in demand forecasting. Factors such as long lead
    times, flexible cancellation policies and changes in customer
    travel plans contribute to cancellation behaviour.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Business Insight</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    High cancellation rates negatively affect hotel revenue,
    resource planning and room utilization. Understanding customer
    cancellation patterns enables hotels to improve booking
    management strategies and increase occupancy.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Recommendation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    • Identify customers with a higher probability of cancellation.
    <br/><br/>
    • Introduce attractive non-refundable or partially refundable
    booking options.
    <br/><br/>
    • Apply dynamic overbooking strategies based on historical
    cancellation trends.
    <br/><br/>
    • Send reminder emails and promotional offers before arrival to
    reduce last-minute cancellations.
            """,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    # ==========================================================
    # Correlation Heatmap
    # ==========================================================

    story.append(
        Paragraph(
            "8. Correlation Analysis",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    img = Image(
        "static/images/correlation_heatmap.png",
        width=6.5 * inch,
        height=4.2 * inch
    )

    story.append(img)

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "<b>Observation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    The correlation heatmap illustrates the strength and direction
    of relationships among numerical variables in the hotel booking
    dataset. Most variables exhibit weak to moderate correlations,
    while a few variables show stronger positive or negative
    relationships.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Interpretation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    Correlation analysis helps identify variables that influence one
    another. Highly correlated features may provide valuable insights
    for predictive modeling, while weakly correlated variables may
    contribute independently to hotel booking behaviour.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Business Insight</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    Understanding relationships between variables helps hotel
    management identify the key drivers of booking demand,
    pricing, guest behaviour and operational performance.
    These insights support better strategic and business decisions.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>Recommendation</b>",
            styles["Heading3"]
        )
    )

    story.append(
        Paragraph(
            """
    • Use highly correlated variables for predictive analytics.
    <br/><br/>
    • Monitor relationships between pricing, lead time and
    cancellations to improve forecasting.
    <br/><br/>
    • Apply correlation analysis during feature selection for
    machine learning models.
    <br/><br/>
    • Continuously update correlation analysis as new booking
    data becomes available.
            """,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    # ==========================================================
    # Overall Business Insights
    # ==========================================================

    story.append(
        Paragraph(
            "9. Overall Business Insights",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            """
    The Exploratory Data Analysis provided several valuable insights
    into hotel booking patterns, customer behaviour and operational
    performance. These findings can assist hotel management in making
    strategic business decisions.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "<b>Key Business Insights</b>",
            styles["Heading2"]
        )
    )

    insights = """
    • City Hotels receive significantly more bookings than Resort Hotels, indicating higher demand for urban accommodations.

    <br/><br/>

    • Hotel demand varies across seasons, with peak travel periods generating the highest booking volumes.

    <br/><br/>

    • Most reservations are made by transient customers, highlighting the importance of individual travellers.

    <br/><br/>

    • Lead Time distribution shows that customers generally book closer to their arrival date, while a smaller number make reservations several months in advance.

    <br/><br/>

    • Average Daily Rate (ADR) varies across bookings, reflecting differences in room categories, seasonal pricing and customer preferences.

    <br/><br/>

    • Booking cancellations represent a considerable business challenge and directly affect hotel occupancy and revenue.

    <br/><br/>

    • Correlation analysis indicates that multiple variables contribute to hotel booking behaviour, supporting future predictive analytics and machine learning applications.

    <br/><br/>

    • Overall, customer behaviour, pricing strategy and seasonal demand are the primary drivers of hotel business performance.
    """

    story.append(
        Paragraph(
            insights,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    # ==========================================================
    # Final Recommendations
    # ==========================================================

    story.append(
        Paragraph(
            "10. Final Recommendations",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            """
    Based on the Exploratory Data Analysis, the following
    recommendations are proposed to improve hotel operations,
    customer satisfaction and overall business performance.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "<b>Recommendations</b>",
            styles["Heading2"]
        )
    )

    recommendations = """
    <b>1. Dynamic Pricing Strategy</b>

    Adjust room prices according to seasonal demand,
    occupancy levels and booking trends to maximize revenue.

    <br/><br/>

    <b>2. Reduce Booking Cancellations</b>

    Introduce attractive non-refundable booking options,
    automated reminder emails and loyalty benefits to reduce
    last-minute cancellations.

    <br/><br/>

    <b>3. Improve Occupancy During Off-Seasons</b>

    Launch promotional campaigns, discounted packages and
    family vacation offers to increase bookings during
    low-demand periods.

    <br/><br/>

    <b>4. Strengthen Customer Retention</b>

    Develop loyalty programs, personalized offers and reward
    systems for repeat customers.

    <br/><br/>

    <b>5. Optimize Resource Planning</b>

    Plan staffing levels, room inventory and hotel operations
    based on seasonal booking forecasts and historical demand.

    <br/><br/>

    <b>6. Utilize Data-Driven Decision Making</b>

    Continuously monitor hotel performance using dashboards,
    KPIs and statistical analysis to support strategic
    business decisions.

    <br/><br/>

    <b>7. Future Scope</b>

    The current analysis can be extended by developing machine
    learning models for booking cancellation prediction,
    customer segmentation, demand forecasting and dynamic
    pricing optimization.
    """

    story.append(
        Paragraph(
            recommendations,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.4 * inch))

    story.append(
        Paragraph(
            "<b>Conclusion</b>",
            styles["Heading2"]
        )
    )

    conclusion = """
    The Hotel Booking Demand Analysis successfully explored
    customer booking behaviour, seasonal demand, pricing trends
    and operational performance.

    The insights obtained through Exploratory Data Analysis
    provide valuable support for hotel management in improving
    occupancy, revenue generation and customer satisfaction.

    This report demonstrates the practical application of
    Python, Statistics, Data Analytics and Business Intelligence
    techniques in solving real-world hospitality business
    problems.
    """

    story.append(
        Paragraph(
            conclusion,
            styles["BodyText"]
        )
    )
    doc.build(story)

    return filename
def generate_statistical_report():

    filename = "reports/Statistical_Analysis_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    title = styles["Heading1"]
    title.alignment = TA_CENTER

    story = []
    # ======================================
    # Cover Page
    # ======================================

    story.append(
        Paragraph(
            "HOTEL BOOKING DEMAND ANALYSIS",
            title
        )
    )

    story.append(Spacer(1, 0.3 * inch))

    story.append(
        Paragraph(
            "Statistical Analysis Report",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 0.5 * inch))

    story.append(
        Paragraph(
            "<b>Project:</b> Hotel Booking Demand Analytics Platform",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "<b>Analysis Type:</b> Probability, Inferential Statistics and Assumption Testing",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "<b>Tools Used:</b> Python, Pandas, NumPy, SciPy, Statsmodels, Matplotlib, Seaborn",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Generated On:</b> {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 2 * inch))

    story.append(
        Paragraph(
            "<b>Prepared By</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "Data Analytics Project",
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    # ======================================
    # Project Overview
    # ======================================

    story.append(
        Paragraph(
            "Project Overview",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    overview = """
    This report presents the statistical analysis performed on the
    Hotel Booking Demand dataset.

    The analysis focuses on descriptive statistics, probability,
    inferential statistics, assumption testing and correlation
    analysis to validate business hypotheses and support
    data-driven decision making.

    Statistical techniques were applied to understand customer
    booking behaviour, booking trends, revenue patterns,
    hotel performance and relationships among important variables.
    """

    story.append(
        Paragraph(
            overview,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    # ======================================
    # Descriptive Statistics
    # ======================================

    story.append(
        Paragraph(
            "Descriptive Statistics",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    description = """
    Descriptive statistics provide a summary of the numerical
    characteristics of the dataset. Measures such as mean,
    median, standard deviation, minimum and maximum values
    help understand the distribution and variability of
    hotel booking data.
    """

    story.append(
        Paragraph(
            description,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.3 * inch))
    table_data = [

        ["Statistic", "Value"],

        ["Total Records", str(total_records())],

        ["Total Features", str(total_features())],

        ["Missing Values", str(missing_values())],

        ["Duplicate Records", str(duplicate_records())],

        ["Average Lead Time", "80.09 Days"],

        ["Average ADR", "106.34"],

        ["Average Stay Duration", "3.27 Days"],

        ["Average Guests", "1.98"]

    ]
    table = Table(table_data, colWidths=[250, 180])

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

        ])

    )

    story.append(table)

    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Paragraph(
            "<b>Interpretation</b>",
            styles["Heading2"]
        )
    )

    story.append(

        Paragraph(

            """
            The descriptive statistics indicate that the dataset contains
            a large number of booking records suitable for statistical
            analysis.
        
            Average booking lead time suggests that customers generally
            reserve rooms several weeks before arrival. The Average Daily
            Rate (ADR) provides an estimate of hotel revenue per booking,
            while average stay duration indicates typical customer
            accommodation patterns.
        
            These statistics establish the baseline for subsequent
            probability analysis, assumption testing and hypothesis
            testing.
            """,

            styles["BodyText"]

        )

    )
    story.append(PageBreak())
    # ======================================
    # Probability & Inferential Statistics
    # ======================================

    story.append(
        Paragraph(
            "Probability & Inferential Statistics",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    intro = """
    Probability and inferential statistics help estimate population
    characteristics based on sample data. These techniques allow us
    to make reliable conclusions, quantify uncertainty and support
    business decisions using statistical evidence.

    In this project, probability concepts, sampling theory,
    Central Limit Theorem and confidence intervals were applied
    to understand hotel booking behaviour and revenue patterns.
    """

    story.append(
        Paragraph(
            intro,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.3 * inch))
    table_data = [

        ["Concept", "Purpose"],

        [
            "Probability Distribution",
            "Understand the likelihood of booking-related events."
        ],

        [
            "Sampling Distribution",
            "Estimate population behaviour using sample statistics."
        ],

        [
            "Central Limit Theorem",
            "Approximate the sampling distribution as normal."
        ],

        [
            "Confidence Interval",
            "Estimate the range containing the population parameter."
        ],

        [
            "Inferential Statistics",
            "Draw conclusions about the population using sample data."
        ]

    ]
    table = Table(
        table_data,
        colWidths=[180, 300]
    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("VALIGN", (0, 0), (-1, -1), "TOP"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

        ])

    )

    story.append(table)

    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Paragraph(
            "<b>Business Interpretation</b>",
            styles["Heading2"]
        )
    )

    story.append(

        Paragraph(

            """
            The probability and inferential statistics performed in this
            analysis provide confidence in the reliability of the observed
            booking trends.
        
            By analysing representative samples instead of relying only on
            individual observations, hotel managers can make informed
            decisions regarding pricing, staffing, occupancy planning and
            customer management.
        
            These statistical techniques also establish the foundation for
            assumption testing and hypothesis testing performed in the
            subsequent sections of this report.
            """,

            styles["BodyText"]

        )

    )
    story.append(PageBreak())
    # ======================================
    # Central Limit Theorem
    # ======================================

    story.append(
        Paragraph(
            "Central Limit Theorem",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    clt = """
    The Central Limit Theorem (CLT) states that the sampling
    distribution of the sample mean approaches a normal
    distribution as the sample size becomes sufficiently large,
    regardless of the population's original distribution.

    This principle allows statistical inference and hypothesis
    testing even when the original data is not perfectly
    normally distributed.
    """

    story.append(
        Paragraph(
            clt,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.3 * inch))
    table_data = [

        ["Parameter", "Value"],

        ["Sample Size", "1000"],

        ["Number of Samples", "500"],

        ["Sample Mean (ADR)", "106.34"],

        ["Standard Error", "3.18"],

        ["Distribution", "Approximately Normal"]

    ]
    table = Table(
        table_data,
        colWidths=[220, 220]
    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

        ])

    )

    story.append(table)

    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Image(
            "static/images/clt_distribution.png",
            width=6 * inch,
            height=3.5 * inch
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    story.append(
        Paragraph(
            "<b>Business Interpretation</b>",
            styles["Heading2"]
        )
    )

    story.append(

        Paragraph(

            """
            The Central Limit Theorem confirms that the sampling
            distribution of Average Daily Rate (ADR) is approximately
            normal. This validates the use of inferential statistical
            methods such as confidence intervals and hypothesis testing.
        
            Hotel managers can therefore make reliable business decisions
            based on sample statistics without analysing every booking
            record individually.
            """,

            styles["BodyText"]

        )

    )
    story.append(PageBreak())
    # ======================================
    # Confidence Interval
    # ======================================

    story.append(
        Paragraph(
            "Confidence Interval",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    ci_text = """
    A Confidence Interval (CI) estimates the range within which
    the true population parameter is expected to lie with a
    specified confidence level.

    A 95% confidence interval was calculated for the Average
    Daily Rate (ADR) to estimate the true average revenue
    generated per booking.
    """

    story.append(
        Paragraph(
            ci_text,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.3 * inch))
    table_data = [

        ["Parameter", "Value"],

        ["Sample Mean (ADR)", "106.34"],

        ["Confidence Level", "95%"],

        ["Margin of Error", "2.15"],

        ["Lower Limit", "104.19"],

        ["Upper Limit", "108.49"]

    ]
    table = Table(
        table_data,
        colWidths=[220, 220]
    )

    table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),

        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 1, colors.grey),

        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        ("ALIGN", (0, 0), (-1, -1), "CENTER")

    ]))

    story.append(table)

    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Paragraph(
            "<b>Business Interpretation</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            The 95% confidence interval indicates that the true average
            daily revenue is expected to fall between the lower and
            upper confidence limits. This provides managers with a
            reliable estimate for pricing decisions and revenue planning.
        
            A narrow confidence interval indicates higher estimation
            precision and greater confidence in the statistical analysis.
            """,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    story.append(
        Paragraph(
            "Normality Test (Shapiro-Wilk Test)",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    table_data = [

        ["Statistic", "Value"],

        ["Test", "Shapiro-Wilk"],

        ["Variable", "ADR"],

        ["p-value", "7.338598392923583e-37"],

        ["Decision", "Reject H₀"],

        ["Conclusion", "Data is Not Normally Distributed"]

    ]
    table = Table(
        table_data,
        colWidths=[220, 220]
    )

    table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),

        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 1, colors.grey),

        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        ("ALIGN", (0, 0), (-1, -1), "CENTER")

    ]))

    story.append(table)

    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Paragraph(
            """
            The Shapiro-Wilk test was performed to evaluate whether the
            ADR variable follows a normal distribution.
        
            Since the p-value is less than 0.05, the null hypothesis was
            rejected, indicating that ADR is not normally distributed.
            """,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    story.append(
        Paragraph(
            "Homogeneity of Variance (Levene Test)",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    table_data = [

        ["Statistic", "Value"],

        ["Test", "Levene"],

        ["Groups", "City vs Resort"],

        ["p-value", "0.0"],

        ["Decision", "Reject H₀"],

        ["Conclusion", "Variances are Different"]

    ]
    table = Table(
        table_data,
        colWidths=[220, 220]
    )

    table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),

        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 1, colors.grey),

        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        ("ALIGN", (0, 0), (-1, -1), "CENTER")

    ]))

    story.append(table)

    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Paragraph(
            """
            Levene's Test was conducted to compare the variance of ADR
            between City Hotels and Resort Hotels.
        
            The result indicates unequal variances between the two hotel
            types, suggesting that statistical procedures assuming equal
            variance should be used with caution.
            """,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    # ======================================
    # Correlation Analysis
    # ======================================

    story.append(
        Paragraph(
            "Correlation Analysis",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            """
            Correlation analysis measures the strength and direction of
            the relationship between numerical variables.
        
            Pearson Correlation Coefficient was used to identify
            linear relationships among booking features such as
            Lead Time, ADR, Total Stay and Total Guests.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Image(
            "static/images/correlation_heatmap.png",
            width=6 * inch,
            height=4 * inch
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    story.append(
        Paragraph(
            "<b>Business Interpretation</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            Correlation analysis helps identify variables that move
            together. Strong positive or negative correlations can
            support revenue forecasting, booking prediction and
            customer behaviour analysis.
        
            Understanding these relationships enables hotel managers
            to make informed operational and pricing decisions.
            """,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    # ======================================
    # Statistical Summary
    # ======================================

    story.append(
        Paragraph(
            "Statistical Summary",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    summary = """

    • Descriptive statistics summarized the booking dataset.

    • Probability concepts supported statistical inference.

    • Central Limit Theorem validated sampling analysis.

    • Confidence Intervals estimated the population ADR.

    • Normality testing indicated ADR was not normally distributed.

    • Levene Test showed unequal variance between hotel types.

    • Correlation analysis identified important relationships
    among booking variables.

    """

    story.append(
        Paragraph(
            summary.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    # ======================================
    # Recommendations
    # ======================================

    story.append(
        Paragraph(
            "Recommendations",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    recommendation = """

    • Improve pricing strategies during peak seasons.

    • Monitor cancellation patterns regularly.

    • Encourage early bookings through promotional offers.

    • Use statistical monitoring for revenue forecasting.

    • Apply predictive analytics to improve occupancy planning.

    • Continue collecting customer behaviour data for
    future machine learning models.

    """

    story.append(
        Paragraph(
            recommendation.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    # ======================================
    # Conclusion
    # ======================================

    story.append(
        Paragraph(
            "Conclusion",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    conclusion = """

    The statistical analysis successfully validated important
    characteristics of the Hotel Booking Demand dataset.

    Descriptive statistics, probability theory, inferential
    statistics, assumption testing and correlation analysis
    provided reliable insights into booking behaviour and
    hotel performance.

    These findings support evidence-based decision making for
    pricing, occupancy management, revenue optimization and
    customer relationship management.

    The statistical analysis establishes a strong foundation
    for future predictive analytics and machine learning
    applications within the hotel industry.

    """

    story.append(
        Paragraph(
            conclusion,
            styles["BodyText"]
        )
    )

    doc.build(story)

    return filename
def generate_hypothesis_testing_report():

    filename = "reports/Hypothesis_Testing_Report.pdf"

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    title = styles["Heading1"]
    title.alignment = TA_CENTER

    story = []

    # ======================================
    # Cover Page
    # ======================================

    story.append(
        Paragraph(
            "HOTEL BOOKING DEMAND ANALYSIS",
            title
        )
    )

    story.append(Spacer(1, 0.3 * inch))

    story.append(
        Paragraph(
            "Hypothesis Testing Report",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 0.5 * inch))

    story.append(
        Paragraph(
            "<b>Project :</b> Hotel Booking Demand Analytics Platform",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "<b>Tools :</b> Python, SciPy, Statsmodels, Pandas",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Generated On :</b> {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 2 * inch))

    story.append(
        Paragraph(
            "<b>Prepared By</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "Data Analytics Project",
            styles["BodyText"]
        )
    )

    story.append(PageBreak())

    # ======================================
    # Project Overview
    # ======================================

    story.append(
        Paragraph(
            "Project Overview",
            styles["Heading1"]
        )
    )

    overview = """
Hypothesis testing was performed to determine whether
observed differences and relationships in hotel booking
data are statistically significant.

Both parametric and non-parametric statistical tests
were applied after validating statistical assumptions.
The results provide evidence-based conclusions to support
hotel pricing strategies, customer analysis and revenue
management.
"""

    story.append(
        Paragraph(
            overview,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())

    # ======================================
    # Independent t-Test
    # ======================================

    story.append(
        Paragraph(
            "Independent t-Test",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "<b>Objective</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            The Independent t-Test was performed to determine whether
            the Average Daily Rate (ADR) differs significantly between
            City Hotels and Resort Hotels.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "<b>Null Hypothesis (H₀)</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            There is no significant difference in the Average Daily
            Rate (ADR) between City Hotels and Resort Hotels.
            """,
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "<b>Alternative Hypothesis (H₁)</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            There is a significant difference in the Average Daily
            Rate (ADR) between City Hotels and Resort Hotels.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    table_data = [

        ["Statistic", "Value"],

        ["Test", "Independent t-Test"],

        ["Variable", "ADR"],

        ["t Statistic", "30.287"],

        ["p-value", " 6.153245924852696e-200"],

        ["Significance Level", "0.05"],

        ["Decision", "Reject H₀"]

    ]
    table = Table(
        table_data,
        colWidths=[220, 220]
    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

        ])

    )

    story.append(table)

    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Paragraph(
            "<b>Business Interpretation</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            The p-value is less than 0.05, therefore the null
            hypothesis is rejected.
        
            This indicates that the Average Daily Rate (ADR)
            differs significantly between City Hotels and
            Resort Hotels.
        
            Hotel managers should consider separate pricing
            strategies for different hotel types to maximize
            occupancy and revenue.
            """,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    # ======================================
    # One-Way ANOVA
    # ======================================

    story.append(
        Paragraph(
            "One-Way ANOVA",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "<b>Objective</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            One-Way Analysis of Variance (ANOVA) was performed to
            determine whether the Average Daily Rate (ADR) differs
            significantly among different customer types.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    story.append(
        Paragraph(
            "<b>Null Hypothesis (H₀)</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            There is no significant difference in the Average Daily
            Rate (ADR) among different customer types.
            """,
            styles["BodyText"]
        )
    )
    story.append(
        Paragraph(
            "<b>Alternative Hypothesis (H₁)</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            At least one customer type has a significantly different
            Average Daily Rate (ADR).
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    table_data = [

        ["Statistic", "Value"],

        ["Test", "One-Way ANOVA"],

        ["Variable", "ADR"],

        ["F Statistic", "669.1282713505746"],

        ["p-value", "0.000"],

        ["Alpha", "0.05"],

        ["Decision", "Reject H₀"]

    ]
    table = Table(
        table_data,
        colWidths=[220, 220]
    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

        ])

    )

    story.append(table)

    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Paragraph(
            "<b>Business Interpretation</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            Since the p-value is less than 0.05, the null hypothesis
            is rejected.
        
            This indicates that customer type significantly influences
            the Average Daily Rate (ADR).
        
            Hotels should design pricing strategies based on customer
            segments to improve occupancy and maximize revenue.
            """,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())

    # ======================================
    # Chi-Square Test
    # ======================================

    story.append(
        Paragraph(
            "Chi-Square Test",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "<b>Objective</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            The Chi-Square Test of Independence was performed to
            determine whether there is a significant association
            between Hotel Type and Booking Cancellation.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    story.append(
        Paragraph(
            "<b>Null Hypothesis (H₀)</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            Hotel Type and Booking Cancellation are independent.
            There is no significant association between them.
            """,
            styles["BodyText"]
        )
    )
    story.append(
        Paragraph(
            "<b>Alternative Hypothesis (H₁)</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            Hotel Type and Booking Cancellation are associated.
            There is a significant relationship between them.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    table_data = [

        ["Statistic", "Value"],

        ["Test", "Chi-Square"],

        ["Variables", "Hotel vs Cancellation"],

        ["Chi-Square Statistic", "245.68"],

        ["p-value", "6.905961865776799e-101"],

        ["Alpha", "0.05"],

        ["Decision", "Reject H₀"]

    ]
    table = Table(
        table_data,
        colWidths=[220, 220]
    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkred),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

        ])

    )

    story.append(table)

    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Paragraph(
            "<b>Business Interpretation</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            Since the p-value is less than the significance level
            (0.05), the null hypothesis is rejected.
        
            This indicates a statistically significant association
            between Hotel Type and Booking Cancellation.
        
            The cancellation behaviour differs across hotel types,
            suggesting that cancellation reduction strategies should
            be designed separately for City Hotels and Resort Hotels.
            """,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    # ======================================
    # Mann-Whitney U Test
    # ======================================

    story.append(
        Paragraph(
            "Mann-Whitney U Test",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            "<b>Objective</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            The Mann-Whitney U Test was performed to compare the
            distribution of Average Daily Rate (ADR) between
            City Hotels and Resort Hotels.
        
            Since the data did not satisfy the normality assumption,
            this non-parametric test was selected as an alternative
            to the Independent t-Test.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    story.append(
        Paragraph(
            "<b>Null Hypothesis (H₀)</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            There is no significant difference in the distribution
            of Average Daily Rate (ADR) between City Hotels and
            Resort Hotels.
            """,
            styles["BodyText"]
        )
    )
    story.append(
        Paragraph(
            "<b>Alternative Hypothesis (H₁)</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            There is a significant difference in the distribution
            of Average Daily Rate (ADR) between City Hotels and
            Resort Hotels.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    table_data = [

        ["Statistic", "Value"],

        ["Test", "Mann-Whitney U Test"],

        ["Variable", "ADR"],

        ["U Statistic", "1135645990.0"],

        ["p-value", "0.0"],

        ["Alpha", "0.05"],

        ["Decision", "Reject H₀"]

    ]
    table = Table(
        table_data,
        colWidths=[220, 220]
    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkorange),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

        ])

    )

    story.append(table)

    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Paragraph(
            "<b>Business Interpretation</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            """
            The Mann-Whitney U Test provides a robust comparison of
            ADR between hotel types without assuming normality.
        
            The test result indicates whether the booking revenue
            distribution differs significantly between City Hotels
            and Resort Hotels.
        
            These findings help hotel managers design pricing and
            marketing strategies tailored to each hotel category.
            """,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())
    # ======================================
    # Kruskal-Wallis Test
    # ======================================

    story.append(Paragraph("Kruskal-Wallis Test", styles["Heading1"]))

    story.append(Paragraph("<b>Objective</b>", styles["Heading2"]))

    story.append(Paragraph(
        """
        The Kruskal-Wallis Test was performed to determine whether
        there are significant differences in ADR among different
        customer groups without assuming normality.
        """,
        styles["BodyText"]
    ))

    story.append(Paragraph("<b>Null Hypothesis (H₀)</b>", styles["Heading2"]))

    story.append(Paragraph(
        "No significant difference exists among customer groups.",
        styles["BodyText"]
    ))

    story.append(Paragraph("<b>Alternative Hypothesis (H₁)</b>", styles["Heading2"]))

    story.append(Paragraph(
        "At least one customer group differs significantly.",
        styles["BodyText"]
    ))

    table_data = [
        ["Statistic", "Value"],
        ["Test", "Kruskal-Wallis"],
        ["H Statistic", "2478.85"],
        ["p-value", "0.0"],
        ["Decision", "Reject  H₀"]
    ]

    table = Table(table_data, colWidths=[220, 220])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER")
    ]))

    story.append(table)

    story.append(Paragraph(
        """
        The Kruskal-Wallis test confirms whether booking revenue
        differs significantly across customer groups, helping
        management identify high-value customer segments.
        """,
        styles["BodyText"]
    ))

    story.append(PageBreak())
    story.append(Paragraph("Pearson Correlation", styles["Heading1"]))

    story.append(Paragraph(
        """
        Pearson Correlation measures the strength of linear
        relationships between numerical variables.
        """,
        styles["BodyText"]
    ))

    table_data = [
        ["Statistic", "Value"],
        ["Variables", "Lead Time vs ADR"],
        ["Correlation", "0.0219"],
        ["p-value", "8.997006162842638e-11"],
        ["Decision", "Significant"]
    ]

    table = Table(table_data, colWidths=[220, 220])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey)
    ]))

    story.append(table)

    story.append(Paragraph(
        """
        Pearson correlation helps identify whether two numerical
        variables increase or decrease together.
        """,
        styles["BodyText"]
    ))

    story.append(PageBreak())
    story.append(Paragraph("Spearman Correlation", styles["Heading1"]))

    story.append(Paragraph(
        """
        Spearman Correlation measures monotonic relationships
        between variables without assuming normality.
        """,
        styles["BodyText"]
    ))

    table_data = [
        ["Statistic", "Value"],
        ["Variables", "Lead Time vs ADR"],
        ["Correlation", "0.105"],
        ["p-value", "7.675400161676427e-215"],
        ["Decision", "Significant"]
    ]

    table = Table(table_data, colWidths=[220, 220])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkred),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey)
    ]))

    story.append(table)

    story.append(Paragraph(
        """
        Spearman correlation is useful for identifying monotonic
        relationships when data is not normally distributed.
        """,
        styles["BodyText"]
    ))

    story.append(PageBreak())
    story.append(Paragraph("Overall Statistical Decisions", styles["Heading1"]))

    story.append(Paragraph(
        """
        • Independent t-Test completed
    
        • Chi-Square Test completed
    
        • Mann-Whitney U Test completed
    
        • Kruskal-Wallis Test completed
    
        • Pearson Correlation completed
    
        • Spearman Correlation completed
    
        The statistical analysis indicates significant relationships
        among booking behaviour, hotel type, customer characteristics
        and revenue patterns.
        """,
        styles["BodyText"]
    ))

    story.append(PageBreak())
    story.append(Paragraph("Business Recommendations", styles["Heading1"]))

    story.append(Paragraph(
        """
        • Improve pricing based on hotel type.
    
        • Monitor cancellation behaviour regularly.
    
        • Develop customer-specific marketing strategies.
    
        • Use statistical insights for occupancy forecasting.
    
        • Build predictive models for future booking analysis.
    
        • Continue collecting quality customer data.
        """,
        styles["BodyText"]
    ))

    story.append(PageBreak())
    story.append(Paragraph("Conclusion", styles["Heading1"]))

    story.append(Paragraph(
        """
        Hypothesis testing confirmed statistically significant
        relationships within the Hotel Booking Demand dataset.
    
        The results support data-driven decision making for pricing,
        customer segmentation, revenue optimization and hotel
        management.
    
        This report concludes the statistical validation phase
        of the Hotel Booking Demand Analytics Platform.
        """,
        styles["BodyText"]
    ))

    doc.build(story)

    return filename

