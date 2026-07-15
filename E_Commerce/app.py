from flask import Flask, render_template, request, send_file

from analytics import (
    dashboard_summary,
    business_insights,
    generate_all_charts,
    top_products,
    top_categories,
    sales_summary,
    customer_summary,
    top_customer_states,
    top_customer_cities,
    product_summary,
    product_table,
    category_table,
    seller_summary,
    seller_table,
    seller_states,
    delivery_summary,
    payment_summary,
    payment_table,
    review_table,
    quality_report,
    explorer_data,
    scorecard
)




app = Flask(__name__)

app.secret_key = "olist_dashboard"




# =====================================================
# HOME
# =====================================================

@app.route("/")
def dashboard():

    return render_template(

        "dashboard.html",

        summary=dashboard_summary(),

        insights=business_insights()

    )


# =====================================================
# SALES
# =====================================================

@app.route("/sales")
def sales():

    return render_template(

        "sales.html",

        summary=dashboard_summary(),

        top_products=top_products().to_dict(
            orient="records"
        ),

        top_categories=top_categories().to_dict(
            orient="records"
        ),

        sales=sales_summary()

    )


# =====================================================
# CUSTOMER
# =====================================================

@app.route("/customers")
def customers():

    return render_template(

        "customers.html",

        summary=customer_summary(),

        states=top_customer_states().to_dict(
            orient="records"
        ),

        cities=top_customer_cities().to_dict(
            orient="records"
        )

    )

# =====================================================
# PRODUCTS
# =====================================================

@app.route("/products")
def products():

    return render_template(

        "products.html",

        summary=product_summary(),

        products=product_table().to_dict(
            orient="records"
        ),

        categories=category_table().to_dict(
            orient="records"
        )

    )


# =====================================================
# SELLERS
# =====================================================

@app.route("/sellers")
def sellers():

    return render_template(

        "sellers.html",

        summary=seller_summary(),

        sellers=seller_table().to_dict(
            orient="records"
        ),

        states=seller_states().to_dict(
            orient="records"
        )

    )


# =====================================================
# DELIVERY
# =====================================================

@app.route("/delivery")
def delivery():

    return render_template(

        "delivery.html",

        summary=delivery_summary()

    )


# =====================================================
# PAYMENTS
# =====================================================

@app.route("/payment-review")
def payments():

    return render_template(

        "payments.html",

        summary=payment_summary(),

        payments=payment_table().to_dict(
            orient="records"
        ),

        reviews=review_table().to_dict(
            orient="records"
        )

    )

# =====================================================
# INSIGHTS
# =====================================================

@app.route("/insights")
def insights():

    return render_template(

        "insights.html",

        data=business_insights()

    )


# =====================================================
# DATA QUALITY
# =====================================================

@app.route("/quality")
def quality():

    return render_template(

        "quality.html",

        report=quality_report()

    )


# =====================================================
# DATASET EXPLORER
# =====================================================

@app.route("/explorer")
def explorer():

    search = request.args.get(

        "search",

        ""

    )

    state = request.args.get(

        "state",

        ""

    )

    payment = request.args.get(

        "payment",

        ""

    )

    page = int(

        request.args.get(

            "page",

            1

        )

    )

    data = explorer_data(

        search,

        state,

        payment,

        page

    )

    return render_template(

        "explorer.html",

        **data,

        search=search,

        state=state,

        payment=payment

    )

# =====================================================
# REPORTS
# =====================================================

@app.route("/reports")
def reports():

    return render_template(

        "reports.html",

        dashboard=dashboard_summary(),

        quality=quality_report(),

        business=business_insights()

    )
# =====================================================
# DOWNLOAD CLEANED DATASET
# =====================================================

@app.route("/download-dataset")
def download_dataset():

    return send_file(
        "cleaned/feature_engineered_dataset.csv",
        as_attachment=True
    )


# =====================================================
# ERROR PAGE
# =====================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(

        "404.html"

    ),404

@app.route("/scorecard")
def scorecard_page():

    return render_template(

        "scorecard.html",

        score=scorecard()

    )


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    generate_all_charts()

    app.run(

        debug=True,



    )