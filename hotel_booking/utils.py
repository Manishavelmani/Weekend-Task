import os
import pandas as pd

# ==========================================
# Project Paths
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(
    BASE_DIR,
    "cleaned",
    "hotel_bookings_final.csv"
)

# ==========================================
# Load Dataset
# ==========================================

def load_dataset():
    """
    Load the final feature-engineered hotel booking dataset.
    """

    df = pd.read_csv(DATASET_PATH)

    # Convert reservation date
    if "reservation_status_date" in df.columns:
        df["reservation_status_date"] = pd.to_datetime(
            df["reservation_status_date"]
        )

    return df


# ==========================================
# Dataset Information
# ==========================================

def dataset_shape():
    """
    Returns number of rows and columns.
    """

    df = load_dataset()

    return df.shape


def column_names():
    """
    Returns all column names.
    """

    df = load_dataset()

    return df.columns.tolist()


def missing_values():
    """
    Returns missing value count.
    """

    df = load_dataset()

    return df.isnull().sum()


def data_types():
    """
    Returns data types.
    """

    df = load_dataset()

    return df.dtypes