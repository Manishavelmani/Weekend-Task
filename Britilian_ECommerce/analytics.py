

import matplotlib
matplotlib.use("Agg")

import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import seaborn as sns

from utils import (
    load_data,
    chart_path,
    format_display_ids
)

# ==========================================================
# LOAD DATA
# ==========================================================

df = load_data()

# ==========================================================
# MODERN SEABORN STYLE
# ==========================================================

sns.set_theme(

    style="whitegrid",

    context="talk",

    palette="crest"

)

plt.rcParams["figure.figsize"] = (12,6)

plt.rcParams["figure.dpi"] = 150

plt.rcParams["savefig.dpi"] = 300

plt.rcParams["axes.spines.top"] = False

plt.rcParams["axes.spines.right"] = False

plt.rcParams["axes.titleweight"] = "bold"

plt.rcParams["axes.titlesize"] = 18

plt.rcParams["axes.labelsize"] = 13




# ==========================================================
# KPI
# ==========================================================

def total_revenue():

    return round(
        df["payment_value"].sum(),
        2
    )


def total_orders():

    return df["order_id"].nunique()


def total_customers():

    return df["customer_unique_id"].nunique()


def total_sellers():

    return df["seller_id"].nunique()


def average_order_value():

    return round(
        df["payment_value"].mean(),
        2
    )


def average_delivery_time():

    return round(
        df["delivery_time"].mean(),
        2
    )


def average_review_score():

    return round(
        df["review_score"].mean(),
        2
    )


def repeat_customers():

    return int(
        df["repeat_customer"].sum()
    )


# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================

def dashboard_summary():

    return {

        "revenue": total_revenue(),

        "orders": total_orders(),

        "customers": total_customers(),

        "sellers": total_sellers(),

        "avg_order": average_order_value(),

        "avg_delivery": average_delivery_time(),

        "avg_review": average_review_score(),

        "repeat": repeat_customers()

    }


# ==========================================================
# MONTHLY SALES CHART
# ==========================================================

def monthly_sales_chart():

    monthly = (

        df.groupby("order_month")["payment_value"]

        .sum()

        .reset_index()

        .sort_values("order_month")

    )

    plt.figure()

    sns.lineplot(

        data=monthly,

        x="order_month",

        y="payment_value",

        linewidth=3,

        marker="o",

        markersize=10,

        color="#2563eb"

    )

    plt.title("Monthly Revenue")

    plt.xlabel("Month")

    plt.ylabel("Revenue")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(

        chart_path("monthly_sales.png"),

        bbox_inches="tight"

    )

    plt.close()


# ==========================================================
# REVENUE BY STATE
# ==========================================================

def revenue_state_chart():

    revenue = (

        df.groupby("customer_state")["payment_value"]

        .sum()

        .sort_values(ascending=False)

        .head(10)

        .reset_index()

    )

    plt.figure()

    sns.barplot(

        data=revenue,

        y="customer_state",

        x="payment_value",

        palette="mako"

    )

    plt.title("Top Revenue States")

    plt.xlabel("Revenue")

    plt.ylabel("State")

    plt.tight_layout()

    plt.savefig(

        chart_path("revenue_state.png"),

        bbox_inches="tight"

    )

    plt.close()


# ==========================================================
# CATEGORY SALES
# ==========================================================

def category_sales_chart():

    category = (

        df.groupby("product_category_name_english")

        ["payment_value"]

        .sum()

        .sort_values(ascending=False)

        .head(10)

        .reset_index()

    )

    plt.figure()

    sns.barplot(

        data=category,

        x="payment_value",

        y="product_category_name_english",

        palette="rocket"

    )

    plt.title("Top Product Categories")

    plt.xlabel("Revenue")

    plt.ylabel("")

    plt.tight_layout()

    plt.savefig(

        chart_path("category_sales.png"),

        bbox_inches="tight"

    )

    plt.close()


# ==========================================================
# PAYMENT DONUT
# ==========================================================

def payment_chart():

    payment = (
        df["payment_type"]
        .value_counts()
        .sort_values(ascending=True)
    )

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(8, 5))

    ax = sns.barplot(
        x=payment.values,
        y=payment.index,
        hue=payment.index,
        palette="crest",
        legend=False
    )

    plt.title(
        "Orders by Payment Method",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel("Number of Orders")
    plt.ylabel("Payment Method")

    for i, value in enumerate(payment.values):
        ax.text(
            value + payment.max() * 0.01,
            i,
            f"{value:,}",
            va="center",
            fontsize=10,
            fontweight="bold"
        )

    sns.despine(left=True)

    plt.tight_layout()

    plt.savefig(
        chart_path("payment.png"),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()
# ==========================================================
# REVIEW SCORE DISTRIBUTION
# ==========================================================

def review_chart():

    plt.figure(figsize=(8, 5))

    sns.countplot(
        data=df,
        x="review_score",
        palette="viridis"
    )

    plt.title("Review Score Distribution")
    plt.xlabel("Review Score")
    plt.ylabel("Orders")

    plt.tight_layout()

    plt.savefig(
        chart_path("review_score.png"),
        bbox_inches="tight"
    )

    plt.close()


# ==========================================================
# DELIVERY TIME DISTRIBUTION
# ==========================================================

def delivery_chart():

    plt.figure(figsize=(10, 5))

    sns.histplot(
        data=df,
        x="delivery_time",
        bins=30,
        kde=True,
        color="#2563eb"
    )

    plt.title("Delivery Time Distribution")
    plt.xlabel("Delivery Time (Days)")
    plt.ylabel("Orders")

    plt.tight_layout()

    plt.savefig(
        chart_path("delivery_time.png"),
        bbox_inches="tight"
    )

    plt.close()


# ==========================================================
# CUSTOMER STATE DISTRIBUTION
# ==========================================================

def customer_state_chart():

    customer = (

        df.groupby("customer_state")
        .size()
        .sort_values(ascending=False)
        .head(10)
        .reset_index(name="Customers")

    )

    plt.figure(figsize=(10,6))

    sns.barplot(
        data=customer,
        x="Customers",
        y="customer_state",
        palette="crest"
    )

    plt.title("Top Customer States")

    plt.tight_layout()

    plt.savefig(
        chart_path("customer_states.png"),
        bbox_inches="tight"
    )

    plt.close()


# ==========================================================
# SELLER PERFORMANCE
# ==========================================================

def seller_chart():

    seller = (

        df.groupby("seller_state")[
            "seller_performance_score"
        ]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()

    )

    plt.figure(figsize=(10,6))

    sns.barplot(
        data=seller,
        x="seller_performance_score",
        y="seller_state",
        palette="flare"
    )

    plt.title("Seller Performance")

    plt.tight_layout()

    plt.savefig(
        chart_path("seller_performance.png"),
        bbox_inches="tight"
    )

    plt.close()


# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================

def business_insights():

    return {

        "highest_revenue_month":

        df.groupby("order_month")[
            "payment_value"
        ].sum().idxmax(),

        "best_category":

        df.groupby(
            "product_category_name_english"
        )["payment_value"].sum().idxmax(),

        "best_state":

        df.groupby(
            "customer_state"
        )["payment_value"].sum().idxmax(),

        "best_seller":

        df.groupby(
            "seller_id"
        )["payment_value"].sum().idxmax(),

        "average_review":

        round(
            df["review_score"].mean(),
            2
        ),

        "average_delivery":

        round(
            df["delivery_time"].mean(),
            2
        )

    }


# ==========================================================
# DATA QUALITY
# ==========================================================

def data_quality():

    return {

        "rows": len(df),

        "columns": len(df.columns),

        "missing_values":

        int(df.isna().sum().sum()),

        "duplicate_rows":

        int(df.duplicated().sum()),

        "memory_mb":

        round(
            df.memory_usage(
                deep=True
            ).sum() / 1024 / 1024,
            2
        )

    }


# ==========================================================
# DATASET EXPLORER
# ==========================================================

def dataset(limit=100):

    return df.head(limit)


def search(keyword):

    keyword = keyword.lower()

    return df[

        df.astype(str)

        .apply(

            lambda x:

            x.str.lower()

            .str.contains(keyword)

        )

        .any(axis=1)

    ]

# Add these functions to analytics.py

# ==========================================================
# TOP 10 PRODUCTS
# ==========================================================

def top_products():

    products = (

        df.groupby("product_id")["payment_value"]

        .sum()

        .sort_values(ascending=False)

        .head(10)

        .reset_index()

        .rename(
            columns={
                "payment_value": "Revenue"
            }
        )

    )

    products = format_display_ids(products)

    return products


# ==========================================================
# TOP 10 CATEGORIES
# ==========================================================

def top_categories():

    return (

        df.groupby(
            "product_category_name_english"
        )["payment_value"]

        .sum()

        .sort_values(ascending=False)

        .head(10)

        .reset_index()

        .rename(
            columns={
                "product_category_name_english":"Category",
                "payment_value":"Revenue"
            }
        )

    )


# ==========================================================
# SALES SUMMARY
# ==========================================================

def sales_summary():

    highest_month = (

        df.groupby("order_month")["payment_value"]

        .sum()

        .idxmax()

    )

    highest_category = (

        df.groupby(

            "product_category_name_english"

        )["payment_value"]

        .sum()

        .idxmax()

    )

    highest_state = (

        df.groupby(

            "customer_state"

        )["payment_value"]

        .sum()

        .idxmax()

    )

    return {

        "highest_month":highest_month,

        "highest_category":highest_category,

        "highest_state":highest_state

    }
# ==========================================================
# CUSTOMER ANALYTICS
# ==========================================================

def customer_summary():

    return {

        "customers":

        df["customer_unique_id"].nunique(),

        "repeat":

        int(
            df["repeat_customer"].sum()
        ),

        "average_clv":

        round(
            df["customer_lifetime_value"].mean(),
            2
        ),

        "average_purchase":

        round(
            df["customer_purchase_count"].mean(),
            2
        )

    }


# ==========================================================
# TOP CUSTOMER STATES
# ==========================================================

def top_customer_states():

    return (

        df.groupby("customer_state")

        .agg(

            Customers=("customer_unique_id","nunique"),

            Revenue=("payment_value","sum")

        )

        .sort_values(

            "Customers",

            ascending=False

        )

        .head(10)

        .reset_index()

    )


# ==========================================================
# TOP CUSTOMER CITIES
# ==========================================================

def top_customer_cities():

    return (

        df.groupby("customer_city")

        .agg(

            Customers=("customer_unique_id","nunique"),

            Revenue=("payment_value","sum")

        )

        .sort_values(

            "Customers",

            ascending=False

        )

        .head(10)

        .reset_index()

    )


# ==========================================================
# CUSTOMER STATE CHART
# ==========================================================

def customer_state_chart():

    customer = (

        df.groupby("customer_state")

        ["customer_unique_id"]

        .nunique()

        .sort_values(ascending=False)

        .head(10)

        .reset_index()

    )

    plt.figure(figsize=(11,6))

    sns.barplot(

        data=customer,

        x="customer_unique_id",

        y="customer_state",

        palette="crest"

    )

    plt.title("Top Customer States")

    plt.xlabel("Customers")

    plt.ylabel("")

    plt.tight_layout()

    plt.savefig(

        chart_path(

            "customer_states.png"

        ),

        dpi=300

    )

    plt.close()


# ==========================================================
# CUSTOMER PURCHASE CHART
# ==========================================================

def purchase_count_chart():

    plt.figure(figsize=(10,6))

    sns.histplot(

        data=df,

        x="customer_purchase_count",

        bins=25,

        kde=True,

        color="#2563eb"

    )

    plt.title(

        "Customer Purchase Distribution"

    )

    plt.xlabel(

        "Purchase Count"

    )

    plt.tight_layout()

    plt.savefig(

        chart_path(

            "purchase_distribution.png"

        ),

        dpi=300

    )

    plt.close()


# ==========================================================
# CUSTOMER LIFETIME VALUE
# ==========================================================

def clv_chart():

    plt.figure(figsize=(10,6))

    sns.histplot(

        data=df,

        x="customer_lifetime_value",

        bins=30,

        kde=True,

        color="#16a34a"

    )

    plt.title(

        "Customer Lifetime Value"

    )

    plt.xlabel(

        "Lifetime Value"

    )

    plt.tight_layout()

    plt.savefig(

        chart_path(

            "customer_clv.png"

        ),

        dpi=300

    )

    plt.close()

# ==========================================================
# PRODUCT ANALYTICS
# ==========================================================

def product_summary():

    return {

        "products":

        df["product_id"].nunique(),

        "categories":

        df["product_category_name_english"].nunique(),

        "avg_price":

        round(
            df["price"].mean(),
            2
        ),

        "avg_weight":

        round(
            df["product_weight_g"].mean(),
            2
        )

    }


# ==========================================================
# TOP PRODUCTS
# ==========================================================

def product_table():

    products = (

        df.groupby("product_id")

        .agg(

            Revenue=("payment_value","sum"),

            Orders=("order_id","nunique")

        )

        .sort_values(

            "Revenue",

            ascending=False

        )

        .head(10)

        .reset_index()

    )

    products = format_display_ids(products)

    return products

# ==========================================================
# CATEGORY TABLE
# ==========================================================

def category_table():

    return (

        df.groupby(

            "product_category_name_english"

        )

        .agg(

            Revenue=("payment_value","sum"),

            Orders=("order_id","nunique")

        )

        .sort_values(

            "Revenue",

            ascending=False

        )

        .head(10)

        .reset_index()

    )


# ==========================================================
# PRODUCT PRICE CHART
# ==========================================================

def product_price_chart():

    plt.figure(figsize=(10,6))

    sns.histplot(

        data=df,

        x="price",

        bins=30,

        kde=True,

        palette="crest"

    )

    plt.title(

        "Product Price Distribution"

    )

    plt.tight_layout()

    plt.savefig(

        chart_path(

            "product_price.png"

        ),

        dpi=300

    )

    plt.close()


# ==========================================================
# CATEGORY CHART
# ==========================================================

def category_chart():

    category=(

        df.groupby(

            "product_category_name_english"

        )["payment_value"]

        .sum()

        .sort_values(

            ascending=False

        )

        .head(10)

        .reset_index()

    )

    plt.figure(figsize=(12,6))

    sns.barplot(

        data=category,

        x="payment_value",

        y="product_category_name_english",

        palette="rocket"

    )

    plt.title(

        "Top Product Categories"

    )

    plt.tight_layout()

    plt.savefig(

        chart_path(

            "top_categories.png"

        ),

        dpi=300

    )

    plt.close()


# ==========================================================
# PRODUCT POPULARITY
# ==========================================================
def popularity_chart():

    product = (

        df.groupby("product_id")

        ["order_id"]

        .count()

        .sort_values(

            ascending=False

        )

        .head(10)

        .reset_index()

    )

    product = format_display_ids(product)

    plt.figure(figsize=(12,6))

    sns.barplot(

        data=product,

        x="order_id",

        y="product_id",

        palette="viridis"

    )

    plt.title("Top Selling Products")

    plt.xlabel("Orders")

    plt.ylabel("Products")

    plt.tight_layout()

    plt.savefig(

        chart_path("top_products.png"),

        dpi=300

    )

    plt.close()
# ==========================================================
# SELLER ANALYTICS
# ==========================================================

def seller_summary():

    return {

        "sellers": df["seller_id"].nunique(),

        "avg_score": round(
            df["seller_performance_score"].mean(),
            2
        ),

        "avg_delivery": round(
            df["delivery_time"].mean(),
            2
        ),

        "revenue": round(
            df.groupby("seller_id")["payment_value"]
            .sum()
            .mean(),
            2
        )

    }


# ==========================================================
# TOP SELLERS
# ==========================================================

def seller_table():

    sellers = (

        df.groupby("seller_id")

        .agg(

            Revenue=("payment_value", "sum"),

            Orders=("order_id", "nunique"),

            Rating=("seller_performance_score", "mean")

        )

        .sort_values(

            "Revenue",

            ascending=False

        )

        .head(10)

        .reset_index()

    )

    sellers = format_display_ids(sellers)

    return sellers

# ==========================================================
# SELLER STATES
# ==========================================================

def seller_states():

    return (

        df.groupby("seller_state")

        .agg(

            Sellers=("seller_id","nunique"),

            Revenue=("payment_value","sum")

        )

        .sort_values(

            "Revenue",

            ascending=False

        )

        .head(10)

        .reset_index()

    )



# ==========================================================
# TOP SELLER CHART
# ==========================================================

def seller_chart():

    seller = (

        df.groupby("seller_id")["payment_value"]

        .sum()

        .sort_values(ascending=False)

        .head(10)

        .reset_index()

    )

    seller = format_display_ids(seller)

    plt.figure(figsize=(12,6))

    sns.barplot(

        data=seller,

        x="payment_value",

        y="seller_id",

        palette="crest"

    )

    plt.title("Top Revenue Sellers")

    plt.xlabel("Revenue")

    plt.ylabel("Seller")

    plt.tight_layout()

    plt.savefig(

        chart_path("seller_revenue.png"),

        dpi=300

    )

    plt.close()

# ==========================================================
# SELLER STATE CHART
# ==========================================================

def seller_state_chart():

    state = (

        df.groupby("seller_state")["payment_value"]

        .sum()

        .sort_values(ascending=False)

        .head(10)

        .reset_index()

    )

    plt.figure(figsize=(11,6))

    sns.barplot(

        data=state,

        x="payment_value",

        y="seller_state",

        palette="crest"

    )

    plt.title("Revenue by Seller State")

    plt.tight_layout()

    plt.savefig(

        chart_path("seller_states.png"),

        dpi=300

    )

    plt.close()


# ==========================================================
# SELLER PERFORMANCE
# ==========================================================

def seller_performance_chart():

    plt.figure(figsize=(10,6))

    sns.histplot(

        data=df,

        x="seller_performance_score",

        bins=25,

        kde=True,

        color="#2563eb"

    )

    plt.title("Seller Performance Score")

    plt.tight_layout()

    plt.savefig(

        chart_path("seller_performance.png"),

        dpi=300

    )

    plt.close()
# ==========================================================
# DELIVERY ANALYTICS
# ==========================================================

def delivery_summary():

    return {

        "avg_delivery": round(
            df["delivery_time"].mean(),
            2
        ),

        "avg_shipping": round(
            df["shipping_duration"].mean(),
            2
        ),

        "avg_processing": round(
            df["order_processing_time"].mean(),
            2
        ),

        "delayed": int(
            df["delayed_delivery"].sum()
        )

    }


# ==========================================================
# DELIVERY CHART
# ==========================================================

def delivery_chart():

    plt.figure(figsize=(10,6))

    sns.histplot(

        data=df,

        x="delivery_time",

        bins=30,

        kde=True,

        palette="crest"

    )

    plt.title("Delivery Time Distribution")

    plt.tight_layout()

    plt.savefig(

        chart_path(
            "delivery_distribution.png"
        ),

        dpi=300

    )

    plt.close()


# ==========================================================
# SHIPPING CHART
# ==========================================================

def shipping_chart():

    plt.figure(figsize=(10,6))

    sns.histplot(

        data=df,

        x="shipping_duration",

        bins=30,

        kde=True,

        palette="rocket"

    )

    plt.title("Shipping Duration")

    plt.tight_layout()

    plt.savefig(

        chart_path(
            "shipping_duration.png"
        ),

        dpi=300

    )

    plt.close()


# ==========================================================
# DELAYED DELIVERY
# ==========================================================

def delayed_chart():

    delay = (

        df["delayed_delivery"]

        .value_counts()

        .rename({

            0:"On Time",

            1:"Delayed"

        })

        .reset_index()

    )

    delay.columns=[

        "Status",

        "Orders"

    ]

    plt.figure(figsize=(7,7))

    plt.pie(

        delay["Orders"],

        labels=delay["Status"],

        autopct="%1.1f%%",

        startangle=90

    )

    plt.title(

        "Delayed Deliveries"

    )

    plt.tight_layout()

    plt.savefig(

        chart_path(

            "delayed_delivery.png"

        ),

        dpi=300

    )

    plt.close()
# ==========================================================
# PAYMENT & REVIEW ANALYTICS
# ==========================================================

def payment_summary():

    return {

        "total_payment": round(
            df["payment_value"].sum(),2
        ),

        "average_payment": round(
            df["payment_value"].mean(),2
        ),

        "average_review": round(
            df["review_score"].mean(),2
        ),

        "installments": int(
            df["payment_installments"].sum()
        )

    }


# ==========================================================
# PAYMENT METHODS
# ==========================================================

def payment_table():

    payments= (

        df.groupby("payment_type")

        .agg(

            Orders=("order_id","nunique"),

            Revenue=("payment_value","sum")

        )

        .sort_values(

            "Revenue",

            ascending=False

        )

        .reset_index()

    )
    payments = format_display_ids(payments)

    return payments


# ==========================================================
# REVIEW TABLE
# ==========================================================

def review_table():

    reviews= (

        df.groupby("review_sentiment")

        .agg(

            Reviews=("review_score","count"),

            Average=("review_score","mean")

        )

        .reset_index()

    )
    reviews = format_display_ids(reviews)

    return reviews


# ==========================================================
# PAYMENT CHART
# ==========================================================

def payment_method_chart():

    payment=(

        df.groupby("payment_type")

        ["payment_value"]

        .sum()

        .reset_index()

    )

    plt.figure(figsize=(8,8))

    plt.pie(

        payment["payment_value"],

        labels=payment["payment_type"],

        autopct="%1.1f%%",

        startangle=90

    )

    plt.title("Payment Methods")

    plt.tight_layout()

    plt.savefig(

        chart_path("payment_methods.png"),

        dpi=300

    )

    plt.close()


# ==========================================================
# INSTALLMENTS
# ==========================================================

def installment_chart():

    plt.figure(figsize=(10,6))

    sns.histplot(

        data=df,

        x="payment_installments",

        bins=20,

        kde=True,

        color="#0ea5e9"

    )

    plt.title("Payment Installments")

    plt.tight_layout()

    plt.savefig(

        chart_path("installments.png"),

        dpi=300

    )

    plt.close()


# ==========================================================
# REVIEW SCORE
# ==========================================================

def review_chart():

    plt.figure(figsize=(10,6))

    sns.countplot(

        data=df,

        x="review_score",

        palette="rocket"

    )

    plt.title("Review Score Distribution")

    plt.tight_layout()

    plt.savefig(

        chart_path("review_scores.png"),

        dpi=300

    )

    plt.close()


# ==========================================================
# REVIEW SENTIMENT
# ==========================================================

def sentiment_chart():

    plt.figure(figsize=(8,6))

    sns.countplot(

        data=df,

        x="review_sentiment",

        palette="crest"

    )

    plt.title("Review Sentiment")

    plt.tight_layout()

    plt.savefig(

        chart_path("review_sentiment.png"),

        dpi=300

    )

    plt.close()
# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================

def business_insights():

    highest_month = (

        df.groupby("order_month")["payment_value"]

        .sum()

        .idxmax()

    )

    best_category = (

        df.groupby(

            "product_category_name_english"

        )["payment_value"]

        .sum()

        .idxmax()

    )

    best_state = (

        df.groupby(

            "customer_state"

        )["payment_value"]

        .sum()

        .idxmax()

    )

    best_seller = "Top Revenue Seller"

    return {

        "revenue":

        round(

            df["payment_value"].sum(),

            2

        ),

        "orders":

        df["order_id"].nunique(),

        "customers":

        df["customer_unique_id"].nunique(),

        "highest_month":

        highest_month,

        "best_category":

        best_category,

        "best_state":

        best_state,

        "best_seller":

        best_seller,

        "average_review":

        round(

            df["review_score"].mean(),

            2

        ),

        "average_delivery":

        round(

            df["delivery_time"].mean(),

            2

        )

    }
# ==========================================================
# DATA QUALITY SUMMARY
# ==========================================================

def quality_report():

    return {

        "rows": len(df),

        "columns": len(df.columns),

        "missing": int(df.isna().sum().sum()),

        "duplicates": int(df.duplicated().sum()),

        "customers": df["customer_unique_id"].nunique(),

        "orders": df["order_id"].nunique(),

        "products": df["product_id"].nunique(),

        "sellers": df["seller_id"].nunique(),

        "payment_types": df["payment_type"].nunique(),

        "review_average": round(

            df["review_score"].mean(),

            2

        ),

        "delivery_average": round(

            df["delivery_time"].mean(),

            2

        )

    }
# ==========================================================
# DATASET EXPLORER
# ==========================================================

def explorer_data(
    search="",
    state="",
    payment="",
    page=1,
    per_page=20
):

    data = df.copy()

    # ----------------------------------
    # Search
    # ----------------------------------

    if search:

        search = search.lower()

        data = data[

            data["customer_city"]
            .astype(str)
            .str.lower()
            .str.contains(search)

            |

            data["product_category_name_english"]
            .astype(str)
            .str.lower()
            .str.contains(search)

            |

            data["seller_city"]
            .astype(str)
            .str.lower()
            .str.contains(search)

        ]

    # ----------------------------------
    # State Filter
    # ----------------------------------

    if state:

        data = data[
            data["customer_state"] == state
        ]

    # ----------------------------------
    # Payment Filter
    # ----------------------------------

    if payment:

        data = data[
            data["payment_type"] == payment
        ]

    # ----------------------------------
    # Pagination
    # ----------------------------------

    total = len(data)

    pages = (
        total + per_page - 1
    ) // per_page

    start = (
        page - 1
    ) * per_page

    end = start + per_page

    data = data.iloc[start:end]

    # ----------------------------------
    # Format IDs
    # ----------------------------------

    data = format_display_ids(data)

    # ----------------------------------
    # Return
    # ----------------------------------

    return {

        "records": data.to_dict(
            orient="records"
        ),

        "states": sorted(
            df["customer_state"]
            .dropna()
            .unique()
        ),

        "payments": sorted(
            df["payment_type"]
            .dropna()
            .unique()
        ),

        "page": page,

        "pages": pages,

        "total": total

    }
# ==========================================================
# BUSINESS KPI SCORECARD
# ==========================================================

def scorecard():

    revenue = df["payment_value"].sum()

    avg_review = df["review_score"].mean()

    avg_delivery = df["delivery_time"].mean()

    repeat_rate = (

        df["repeat_customer"].mean()

        * 100

    )

    delayed = (

        df["delayed_delivery"].mean()

        * 100

    )

    payment_methods = (

        df["payment_type"]

        .nunique()

    )

    seller_score = (

        df["seller_performance_score"]

        .mean()

    )

    return {

        "revenue":

        round(revenue,2),

        "review":

        round(avg_review,2),

        "delivery":

        round(avg_delivery,2),

        "repeat":

        round(repeat_rate,2),

        "delay":

        round(delayed,2),

        "payments":

        payment_methods,

        "seller":

        round(seller_score,2)

    }

# ==========================================================
# GENERATE ALL CHARTS
# ==========================================================

def generate_all_charts():

    monthly_sales_chart()

    revenue_state_chart()

    category_sales_chart()

    payment_chart()

    review_chart()

    delivery_chart()

    customer_state_chart()

    seller_chart()

    customer_state_chart()

    purchase_count_chart()

    clv_chart()

    product_price_chart()

    category_chart()

    popularity_chart()

    delivery_chart()

    shipping_chart()

    delayed_chart()

    payment_method_chart()

    installment_chart()

    review_chart()

    sentiment_chart()


