# 📊 Advanced Statistical Analysis & Data Analytics Platform – Hotel Booking Demand

## 🚀 Project Overview

The **Advanced Statistical Analysis & Data Analytics Platform** is an end-to-end data analytics project developed using the **Hotel Booking Demand Dataset**.

The project performs complete data analysis workflow starting from data understanding, preprocessing, statistical analysis, hypothesis testing, exploratory data analysis, and finally presents the insights through an interactive **Flask + Bootstrap Analytics Dashboard**.

The objective of this project is to transform raw hotel booking data into meaningful business insights that help understand booking trends, cancellation behavior, customer patterns, and revenue performance.

---

# 📂 Dataset

## Hotel Booking Demand Dataset

Dataset Source:

Kaggle: Hotel Booking Demand Dataset

### Dataset Information

* 119,000+ hotel booking records
* 32 features
* Numerical, categorical, and date-based attributes
* Booking details
* Customer information
* Cancellation information
* Revenue-related metrics

### Main Features

* Hotel type
* Booking status
* Lead time
* Arrival date
* Customer type
* Market segment
* Country
* ADR (Average Daily Rate)
* Number of guests
* Stay duration
* Cancellation status

---

# 🛠️ Technologies Used

## Programming Language

* Python

## Data Analysis

* Pandas
* NumPy

## Statistics

* SciPy
* Statsmodels

## Visualization

* Matplotlib
* Seaborn

## Web Application

* Flask
* HTML5
* CSS3
* Bootstrap 5

## Development Tools

* Jupyter Notebook
* Git
* GitHub

---

# 📁 Project Structure

```
hotel_booking/

│
├── app.py
├── analytics.py
├── utils.py
├── report_generator.py
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── notebooks/
│   └── hotel_booking_analysis.ipynb
│
├── datasets/
│   └── hotel_bookings.csv
│
├── cleaned/
│   ├── hotel_bookings_cleaned.csv
│   └── hotel_bookings_final.csv
│
├── reports/
│   ├── Data_Preprocessing_Report.pdf
│   ├── EDA_Report.pdf
│   ├── Hypothesis_Testing_Report.pdf
│   └── Statistical_Analysis_Report.pdf
│
├── static/
│   ├── css/
│   ├── js/
│   ├── charts/
│   ├── images/
│   └── data/
│
└── templates/

```

---

# 🔎 Data Analysis Workflow

## Phase 1: Data Understanding

Performed:

* Dataset loading
* Shape and structure analysis
* Data type identification
* Numerical and categorical feature analysis
* Missing value analysis
* Duplicate detection
* Statistical summary

Visualizations:

* Missing value heatmap
* Feature distribution plots
* Correlation heatmap
* Summary statistics

---

# Phase 2: Data Preprocessing

Performed:

## Data Cleaning

* Missing value handling
* Duplicate removal
* Data type conversion
* Invalid value correction
* Outlier detection

## Outlier Detection

Methods:

* IQR Method
* Z-Score Method

## Data Transformation

Applied:

* Label Encoding
* One Hot Encoding
* Standardization
* Normalization
* Log Transformation
* Box-Cox Transformation

## Feature Engineering

Created new features:

* Total Stay Duration
* Total Guests
* Booking Lead Time Category
* Weekend Stay
* Weekday Stay
* Revenue Features
* Booking Season

---

# 📈 Statistical Analysis

## Probability & Sampling

Implemented:

* Probability Distribution
* Sampling Distribution
* Central Limit Theorem
* Confidence Interval
* Margin of Error

## Assumption Testing

Performed:

### Normality Testing

* Shapiro-Wilk Test

### Variance Testing

* Levene Test

### Multicollinearity

* Variance Inflation Factor (VIF)

### Correlation Analysis

* Pearson Correlation
* Spearman Correlation

---

# 🧪 Hypothesis Testing

Statistical tests performed:

## Parametric Tests

* Independent T-Test
* Paired T-Test
* One Way ANOVA
* Pearson Correlation

## Non-Parametric Tests

* Chi-Square Test
* Mann Whitney U Test
* Kruskal Wallis Test

Each hypothesis test includes:

* Null Hypothesis
* Alternative Hypothesis
* Assumption Validation
* Test Statistic
* P-Value
* Statistical Decision
* Business Interpretation

---

# 📊 Exploratory Data Analysis

## Booking Analysis

Analyzed:

* Monthly booking trends
* Hotel type performance
* Seasonal patterns
* Lead time behaviour

## Customer Analysis

Analyzed:

* Customer type distribution
* Repeat guests
* Country-wise bookings
* Market segments

## Cancellation Analysis

Analyzed:

* Cancellation rate
* Cancellation by hotel type
* Lead time impact
* Market segment cancellation

## Revenue Analysis

Analyzed:

* ADR distribution
* Revenue trends
* Seasonal revenue
* Stay duration impact

Visualization techniques:

* Bar charts
* Line charts
* Pie charts
* Histograms
* Box plots
* Scatter plots
* Violin plots
* Heatmaps

---

# 🌐 Flask Analytics Dashboard

A web-based interactive dashboard was developed using Flask and Bootstrap.

## Dashboard Modules

## 🏠 Home Dashboard

Displays:

* Total Bookings
* Cancellation Rate
* Average Daily Rate
* Average Stay Duration
* Booking Trends

## 🏨 Booking Analytics

Includes:

* Monthly booking trends
* Hotel comparison
* Market segment analysis
* Country-wise bookings

## 👥 Customer Analytics

Includes:

* Customer categories
* Repeat guest analysis
* Guest demographics

## 💰 Revenue Analytics

Includes:

* ADR analysis
* Revenue trends
* Seasonal performance

## 📊 Statistical Analysis

Displays:

* Distribution analysis
* Hypothesis test results
* Confidence intervals
* Correlation analysis

## 🔍 Data Explorer

Features:

* Search records
* Filter data
* Sorting
* Pagination
* Cleaned dataset exploration

## 📄 Reports

Users can download:

* Cleaned Dataset
* EDA Report
* Statistical Report
* Hypothesis Testing Report

---

# ▶️ How to Run Project

## 1. Clone Repository

```
git clone <repository-url>
```

## 2. Create Virtual Environment

```
python -m venv myenv
```

Activate:

Windows:

```
myenv\Scripts\activate
```

Linux:

```
source myenv/bin/activate
```

## 3. Install Dependencies

```
pip install -r requirements.txt
```

## 4. Run Flask Application

```
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

# 📦 Requirements

Main libraries:

```
pandas
numpy
scipy
statsmodels
matplotlib
seaborn
flask
bootstrap
openpyxl
reportlab
```

---

# 📌 Project Deliverables

✔ Complete Jupyter Notebook
✔ Cleaned Dataset
✔ Feature Engineered Dataset
✔ Data Preprocessing Report
✔ EDA Report
✔ Statistical Analysis Report
✔ Hypothesis Testing Report
✔ Flask Analytics Dashboard
✔ PDF Report Generator
✔ GitHub Repository Documentation



# ⭐ Future Improvements

* Add Machine Learning model for cancellation prediction
* Add user authentication
* Deploy dashboard using cloud platform
* Add automated data pipeline
* Add interactive Plotly visualizations
