import os
import pandas as pd

# =====================================================
# PROJECT PATHS
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "cleaned",
    "feature_engineered_dataset.csv"
)

CHART_DIR = os.path.join(
    BASE_DIR,
    "static",
    "charts"
)

os.makedirs(CHART_DIR, exist_ok=True)

# =====================================================
# LOAD DATA
# =====================================================

def load_data():

    df = pd.read_csv(
        DATA_PATH,
        low_memory=False
    )

    # -----------------------------
    # Date Columns
    # -----------------------------

    date_columns = [

        "order_purchase_timestamp",

        "order_approved_at",

        "order_delivered_carrier_date",

        "order_delivered_customer_date",

        "order_estimated_delivery_date",

        "shipping_limit_date",

        "review_creation_date",

        "review_answer_timestamp"

    ]

    for col in date_columns:

        if col in df.columns:

            df[col] = pd.to_datetime(
                df[col],
                errors="coerce"
            )

    # -----------------------------
    # Fill Missing Values
    # -----------------------------

    object_columns = df.select_dtypes(
        include="object"
    ).columns

    for col in object_columns:

        df[col] = df[col].fillna("Unknown")

    numeric_columns = df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    for col in numeric_columns:

        df[col] = df[col].fillna(
            df[col].median()
        )

    return df


# =====================================================
# SAVE CHART
# =====================================================

def chart_path(filename):

    return os.path.join(
        CHART_DIR,
        filename
    )


# =====================================================
# FORMAT MONEY
# =====================================================

def format_currency(value):

    return f"₹ {value:,.2f}"


# =====================================================
# KPI FORMAT
# =====================================================

def format_number(value):

    return f"{int(value):,}"


# =====================================================
# DROPDOWN VALUES
# =====================================================

def dropdown_values():

    df = load_data()

    return {

        "states": sorted(
            df["customer_state"]
            .dropna()
            .unique()
            .tolist()
        ),

        "cities": sorted(
            df["customer_city"]
            .dropna()
            .unique()
            .tolist()
        ),

        "categories": sorted(
            df["product_category_name_english"]
            .dropna()
            .unique()
            .tolist()
        ),

        "payment_types": sorted(
            df["payment_type"]
            .dropna()
            .unique()
            .tolist()
        ),

        "review_scores": sorted(
            df["review_score"]
            .dropna()
            .unique()
            .tolist()
        )

    }


# =====================================================
# DATASET INFO
# =====================================================

def dataset_information():

    df = load_data()

    return {

        "rows": len(df),

        "columns": len(df.columns),

        "missing": int(
            df.isna().sum().sum()
        ),

        "duplicates": int(
            df.duplicated().sum()
        ),

        "memory": round(
            df.memory_usage(deep=True).sum()
            / 1024 / 1024,
            2
        )

    }
#format  id into readable form
def format_display_ids(df):

    df = df.copy()

    if "seller_id" in df.columns:
        df["seller_id"] = [
            f"Seller {i}"
            for i in range(1, len(df) + 1)
        ]

    if "product_id" in df.columns:
        df["product_id"] = [
            f"Product {i}"
            for i in range(1, len(df) + 1)
        ]

    if "order_id" in df.columns:
        df["order_id"] = [
            f"Order {i}"
            for i in range(1, len(df) + 1)
        ]

    return df