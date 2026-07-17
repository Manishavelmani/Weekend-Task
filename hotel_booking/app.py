from flask import Flask, render_template, request, send_file
from report_generator import (generate_preprocessing_report,generate_statistical_report,generate_hypothesis_testing_report,generate_eda_report
)
import os

from analytics import (
    get_total_bookings,
    get_cancellation_rate,
    get_average_adr,
    get_average_stay,
    get_average_guests,
    get_repeat_guest_rate,
    monthly_bookings,
    hotel_distribution,
    season_distribution,
    business_insights,
    customer_type_distribution,
    guest_status_distribution,
    market_segment_distribution,
    top_countries,
    special_requests_distribution,
    adr_by_hotel,
    adr_by_season,
    revenue_category_distribution,
    stay_type_distribution,
    summary_statistics,
    correlation_matrix,
    lead_time_distribution,
    total_records,
    total_features,
    duplicate_records,
    missing_values,
    generate_correlation_heatmap,
    adr_distribution,
    lead_time_category_distribution,
    stay_distribution,
    cancellation_distribution,
    adr_by_customer_type,
    explorer_data,explorer_filters,
)

app = Flask(__name__)

# ==========================================
# HOME DASHBOARD
# ==========================================

@app.route("/")
def dashboard():

    context = {

        "total_bookings": get_total_bookings(),

        "cancellation_rate": get_cancellation_rate(),

        "average_adr": get_average_adr(),

        "average_stay": get_average_stay(),

        "average_guests": get_average_guests(),

        "repeat_guest_rate": get_repeat_guest_rate(),

        "monthly_bookings": monthly_bookings(),

        "hotel_distribution": hotel_distribution(),

        "season_distribution": season_distribution(),

        "business_insights": business_insights()

    }

    return render_template(
        "dashboard/dashboard.html",
        **context
    )


# ==========================================
# BOOKING ANALYTICS
#This method helps to calculate total_bookings,monthly_bookings,
#hotel_distribution,lead_time_distribution,season_distribution
# ==========================================

@app.route("/booking")
def booking():

    return render_template(

        "booking/booking.html",

        total_bookings=get_total_bookings(),

        monthly_bookings=monthly_bookings(),

        hotel_distribution=hotel_distribution(),

        season_distribution=season_distribution(),

        lead_time_distribution=lead_time_distribution()

    )

# ==========================================
# CUSTOMER ANALYTICS
#this method calculate total_bookings,customer_
# type,guest_status,market_segment,countries,special_requests
# ==========================================

@app.route("/customer")
def customer():

    return render_template(

        "customer/customer.html",

        total_bookings=get_total_bookings(),

        customer_type=customer_type_distribution(),

        guest_status=guest_status_distribution(),

        market_segment=market_segment_distribution(),

        countries=top_countries(),

        special_requests=special_requests_distribution()

    )

# ==========================================
# REVENUE ANALYTICS
#avearge_adr,adr_hotel,adr_season,revenue_category,stay_hotel
# ==========================================

@app.route("/revenue")
def revenue():

    return render_template(

        "revenue/revenue.html",

        average_adr=get_average_adr(),

        adr_hotel=adr_by_hotel(),

        adr_season=adr_by_season(),

        revenue_category=revenue_category_distribution(),

        stay_type=stay_type_distribution()

    )


# ==========================================
# STATISTICAL ANALYSIS
#this function calculate statistical operation
# ==========================================

@app.route("/statistics")
def statistics():

    generate_correlation_heatmap()

    return render_template(

        "statistics/statistics.html",

        total_records=total_records(),

        total_features=total_features(),

        missing_values=missing_values(),

        duplicate_records=duplicate_records(),

        summary=summary_statistics(),

        correlation=correlation_matrix(),

        adr_distribution=adr_distribution(),

        lead_distribution=lead_time_category_distribution(),

        stay_distribution=stay_distribution(),

        cancellation_distribution=cancellation_distribution(),

        adr_customer=adr_by_customer_type()

    )
# ==========================================
# DATA EXPLORER
#this method render data filter using pagination
# ==========================================
@app.route("/explorer")
def explorer():

    search = request.args.get("search", "")

    hotel = request.args.get("hotel", "")

    season = request.args.get("season", "")

    customer_type = request.args.get("customer_type", "")

    page = request.args.get("page", 1, type=int)

    per_page = request.args.get("per_page", 10, type=int)

    data, total_records = explorer_data(

        search,

        hotel,

        season,

        customer_type,

        page,

        per_page

    )

    filters = explorer_filters()

    total_pages = (total_records + per_page - 1) // per_page


    return render_template(

        "explorer/explorer.html",

        data=data,

        total_records=total_records,

        hotels=filters["hotels"],

        seasons=filters["seasons"],

        customer_types=filters["customer_types"],

        page=page,

        per_page=per_page,

        total_pages=total_pages


    )
#this function perform download filtered datsets in explorer page
@app.route("/download")
def download():

    search = request.args.get("search", "")

    hotel = request.args.get("hotel", "")

    season = request.args.get("season", "")

    customer_type = request.args.get("customer_type", "")

    # Get filtered data
    data, _ = explorer_data(search,hotel,season,customer_type,page=1,per_page=1000000)

    os.makedirs("downloads", exist_ok=True)

    filepath = os.path.join(
        "downloads",
        "filtered_hotel_bookings.csv"
    )

    data.to_csv(filepath, index=False)

    return send_file(

        filepath,

        as_attachment=True,

        download_name="hotel_bookings.csv"

    )
# ==========================================
# REPORTS
#In report page it has show some details
#about total_recored,total features,miising values,
#duplicate records
# ==========================================

@app.route("/reports")
def reports():

    return render_template(

        "reports/reports.html",

        total_records=total_records(),

        total_features=total_features(),

        missing_values=missing_values(),

        duplicate_records=duplicate_records(),

        business_insights=business_insights()

    )
#this methos download clened csv datasets in report page
@app.route("/download-dataset")
def download_dataset():

    filepath = os.path.join(
        "cleaned",
        "hotel_bookings_final.csv"
    )

    return send_file(
        filepath,
        as_attachment=True,
        download_name="hotel_bookings_final.csv"
    )

#this method download preprocessing,statistical,eda and hypothesis testing reports
#thr report is created by using report lab library in python
@app.route("/download-preprocessing-report")
def download_preprocessing_report():

    filepath = generate_preprocessing_report()

    return send_file(
        filepath,
        as_attachment=True,
        download_name="Hotel_Booking_Preprocessing_Report.pdf"
    )


@app.route("/download-eda-report")
def download_eda_report():

    filepath = generate_eda_report()

    return send_file(
        filepath,
        as_attachment=True,
        download_name="Hotel_Booking_EDA_Report.pdf"
    )


@app.route("/download-statistical-report")
def download_statistical_report():

    filepath = generate_statistical_report()

    return send_file(
        filepath,
        as_attachment=True,
        download_name="Hotel_Booking_Statistical_Report.pdf"
    )


@app.route("/download-hypothesis-report")
def download_hypothesis_report():

    filepath = generate_hypothesis_testing_report()

    return send_file(
        filepath,
        as_attachment=True,
        download_name="Hotel_Booking_Hypothesis_Testing_Report.pdf"
    )

# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )