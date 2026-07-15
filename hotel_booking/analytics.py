from utils import load_dataset
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==========================================
# Load Dataset
# ==========================================

df = load_dataset()

# ==========================================
# KPI FUNCTIONS
# ==========================================

def get_total_bookings():
    return len(df)


def get_cancellation_rate():
    return round(df["is_canceled"].mean() * 100, 2)


def get_average_adr():
    return round(df["adr"].mean(), 2)


def get_average_stay():
    return round(df["total_stay"].mean(), 2)


def get_average_guests():
    return round(df["total_guests"].mean(), 2)


def get_repeat_guest_rate():
    return round(df["is_repeated_guest"].mean() * 100, 2)


# ==========================================
# BOOKING ANALYTICS
# ==========================================

def monthly_bookings():

    month_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    bookings = (
        df["arrival_date_month"]
        .value_counts()
        .reindex(month_order)
        .fillna(0)
        .astype(int)
    )

    return bookings


def hotel_distribution():

    return df["hotel"].value_counts()


def season_distribution():

    return df["season"].value_counts()


def lead_time_distribution():

    return (
        df["lead_time_category"]
        .value_counts()
        .sort_index()
    )

# ==========================================
# CUSTOMER ANALYTICS
# ==========================================

def customer_type_distribution():

    return df["customer_type"].value_counts()


def guest_status_distribution():

    return df["guest_status"].value_counts()


def market_segment_distribution():

    return df["market_segment"].value_counts()


def top_countries(limit=10):

    return df["country"].value_counts().head(limit)


def special_requests_distribution():

    return (
        df["total_of_special_requests"]
        .value_counts()
        .sort_index()
    )


def adr_distribution():

    return (
        df["revenue_category"]
        .value_counts()
        .sort_index()
    )


def lead_time_category_distribution():

    return (
        df["lead_time_category"]
        .value_counts()
        .sort_index()
    )


def stay_distribution():

    return (
        df["stay_type"]
        .value_counts()
        .sort_index()
    )

# ==========================================
# REVENUE ANALYTICS
# ==========================================

def adr_by_hotel():

    return (
        df.groupby("hotel")["adr"]
        .mean()
        .round(2)
    )


def adr_by_season():

    return (
        df.groupby("season")["adr"]
        .mean()
        .round(2)
    )


def revenue_category_distribution():

    return df["revenue_category"].value_counts()


def stay_type_distribution():

    return df["stay_type"].value_counts()


# ==========================================
# STATISTICAL SUMMARY
# ==========================================

def summary_statistics():

    return (
        df.select_dtypes(include="number")
        .describe()
        .round(2)
    )


def correlation_matrix():

    return df.select_dtypes(include="number").corr().round(2)


# ==========================================
# BUSINESS INSIGHTS
# ==========================================

def business_insights():

    return [

        "August recorded the highest booking demand.",

        "City Hotel received more bookings than Resort Hotel.",

        "Transient customers are the largest customer segment.",

        "Summer season generated the highest ADR.",

        "Higher lead time is associated with higher cancellation probability."

    ]
def total_features():

    return df.shape[1]


def total_records():

    return df.shape[0]


def missing_values():

    return int(df.isnull().sum().sum())


def duplicate_records():

    return int(df.duplicated().sum())
# ==========================================
# CANCELLATION DISTRIBUTION
# ==========================================

def cancellation_distribution():

    return (
        df["is_canceled"]
        .replace({
            0: "Not Cancelled",
            1: "Cancelled"
        })
        .value_counts()
    )
# ==========================================
# ADR BY CUSTOMER TYPE
# ==========================================

def adr_by_customer_type():

    return (
        df.groupby("customer_type")["adr"]
        .mean()
        .round(2)
        .sort_values(ascending=False)
    )
# ==========================================
# EXPLORER
# ==========================================

def explorer_data(
    search="",
    hotel="",
    season="",
    customer_type="",
    page=1,
    per_page=10
):

    data = df.copy()

    search = search.strip()
    hotel = hotel.strip()
    season = season.strip()
    customer_type = customer_type.strip()

    if search:
        search = search.lower()

        data = data[
            data.astype(str)
            .apply(lambda x: x.str.lower().str.contains(search))
            .any(axis=1)
        ]

    if hotel:
        data = data[data["hotel"] == hotel]

    if season:
        data = data[data["season"] == season]

    if customer_type:
        data = data[data["customer_type"] == customer_type]

    total_records = len(data)

    start = (page - 1) * per_page
    end = start + per_page

    return data.iloc[start:end], total_records

def explorer_filters():

    return {

        "hotels": sorted(df["hotel"].dropna().unique()),

        "seasons": sorted(df["season"].dropna().unique()),

        "customer_types": sorted(df["customer_type"].dropna().unique())

    }
def generate_correlation_heatmap():

    corr = df.select_dtypes(include="number").corr()

    plt.figure(figsize=(10, 8))

    sns.heatmap(
        corr,
        annot=True,
        cmap="RdBu_r",
        center=0,
        fmt=".2f",
        linewidths=0.5
    )

    plt.title("Correlation Matrix")

    os.makedirs("static/images", exist_ok=True)

    plt.tight_layout()

    plt.savefig(
        "static/images/correlation_heatmap.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


