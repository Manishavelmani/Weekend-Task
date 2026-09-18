from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import joblib
import shap
import os
from assistant_agent import ask_ai
# ============================================================
# FLASK APPLICATION
# ============================================================
app = Flask(__name__)
# ============================================================
# BASE DIRECTORY
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ============================================================
# FILE PATHS
# ============================================================
DATA_PATH = os.path.join(BASE_DIR,"Datasets","WA_Fn-UseC_-Telco-Customer-Churn.csv")
MODEL_PATH = os.path.join(BASE_DIR,"models","final_churn_model.pkl")
PREPROCESSOR_PATH = os.path.join(BASE_DIR,"models","final_preprocessor.pkl")
THRESHOLD_PATH = os.path.join(BASE_DIR,"models","final_churn_threshold.pkl")
# ============================================================
# LOAD CUSTOMER DATA
# ============================================================
try:
    customer_data = pd.read_csv(DATA_PATH)
    if "TotalCharges" in customer_data.columns:
        customer_data["TotalCharges"] = pd.to_numeric(customer_data["TotalCharges"],errors="coerce")
    print("Customer dataset loaded successfully.")
    print("Rows:",len(customer_data))
    print("Columns:",len(customer_data.columns))
except Exception as e:
    customer_data = pd.DataFrame()
    print("Dataset loading error:",e)
# ============================================================
# LOAD MODEL
# ============================================================
try:
    final_churn_model = joblib.load(MODEL_PATH)
    print( "XGBoost model loaded successfully.")
except Exception as e:
    final_churn_model = None
    print("Model loading error:",e)
# ============================================================
# LOAD PREPROCESSOR
# ============================================================
try:
    final_preprocessor = joblib.load( PREPROCESSOR_PATH)
    print("Preprocessor loaded successfully.")
except Exception as e:
    final_preprocessor = None
    print("Preprocessor loading error:",e)
# ============================================================
# LOAD THRESHOLD
# ============================================================
try:
    final_churn_threshold = joblib.load(THRESHOLD_PATH)
    if isinstance(final_churn_threshold,dict):
        final_churn_threshold = (final_churn_threshold.get("threshold",final_churn_threshold.get("best_threshold",0.5)))

    final_churn_threshold = float(final_churn_threshold)
    print("Churn threshold:",final_churn_threshold)
except Exception as e:
    final_churn_threshold = 0.5
    print("Threshold loading error:",e)
# ============================================================
# LOAD SHAP
# ============================================================
shap_explainer = None
try:
    if final_churn_model is not None:
        shap_explainer = shap.TreeExplainer(final_churn_model)
        print("SHAP TreeExplainer loaded successfully.")
except Exception as e:
    print("SHAP initialization error:",e)
# ============================================================
# FEATURE LIST
# ============================================================
numerical_features = [
    "SeniorCitizen",
    "tenure",
    "MonthlyCharges",
    "TotalCharges",
    "NewCustomer",
    "LongTermCustomer",
    "ServiceCount",
    "OptionalServiceCount",
    "HasInternet",
    "FiberOptic",
    "ChargeToTenure",
    "ContractRisk",
    "PaymentMethodRisk",
    "ServiceCombinationRisk",
    "HighValue",
    "HighValueHighRisk"
]
categorical_features = [
    "gender",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "TenureGroup",
    "MonthlyChargeGroup",
    "TotalChargeGroup",
    "ServiceCombination"
]
# ============================================================
# CUSTOMER LOOKUP
# ============================================================
def get_customer(customer_id):
    if customer_data.empty:
        return None
    if "customerID" not in customer_data.columns:
        return None
    customer_id = str(customer_id).strip()
    result = customer_data[customer_data["customerID"].astype(str).str.strip()== customer_id]
    if result.empty:
        return None
    return result.iloc[0]
# ============================================================
# ENGINEERED FEATURES
# ============================================================
def create_engineered_features(customer):
    row = customer.copy()
    # --------------------------------------------------------
    # Numeric conversion
    # --------------------------------------------------------
    row["tenure"] = pd.to_numeric(row.get("tenure",0),errors="coerce")
    row["MonthlyCharges"] = pd.to_numeric(row.get("MonthlyCharges",0),errors="coerce")
    row["TotalCharges"] = pd.to_numeric(row.get("TotalCharges",0),errors="coerce")
    row["SeniorCitizen"] = pd.to_numeric(row.get("SeniorCitizen",0),errors="coerce")
    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------
    for column in ["tenure","MonthlyCharges","TotalCharges","SeniorCitizen"]:
        if pd.isna(row[column]):
            row[column] = 0
    # ========================================================
    # NEW CUSTOMER
    # ========================================================
    row["NewCustomer"] = int(row["tenure"] <= 12)
    # ========================================================
    # LONG TERM CUSTOMER
    # ========================================================
    row["LongTermCustomer"] = int(row["tenure"] >= 36)
    # ========================================================
    # SERVICE COUNT
    # ========================================================
    service_columns = [
        "PhoneService",
        "MultipleLines",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies"
    ]
    service_count = 0
    for column in service_columns:
        if column in row.index:
            value = str(row[column]).strip().lower()
            if value == "yes":
                service_count += 1
    row["ServiceCount"] = (service_count)
    # ========================================================
    # OPTIONAL SERVICE COUNT
    # ========================================================
    optional_columns = [
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies"
    ]
    optional_count = 0
    for column in optional_columns:
        if column in row.index:
            value = str(row[column]).strip().lower()
            if value == "yes":
                optional_count += 1
    row["OptionalServiceCount"] = (optional_count)
    # ========================================================
    # INTERNET
    # ========================================================
    internet_service = str(row.get("InternetService","")).strip().lower()
    row["HasInternet"] = int(internet_service != "no")
    row["FiberOptic"] = int(internet_service == "fiber optic")
    # ========================================================
    # CHARGE TO TENURE
    # ========================================================
    if row["tenure"] > 0:
        row["ChargeToTenure"] = (row["TotalCharges"]/row["tenure"])
    else:
        row["ChargeToTenure"] = (row["MonthlyCharges"])
    # ========================================================
    # CONTRACT RISK
    # ========================================================
    contract = str(row.get("Contract","")).strip().lower()
    contract_risk_map = {
        "month-to-month": 2,
        "one year": 1,
        "two year": 0
    }
    row["ContractRisk"] = (
        contract_risk_map.get(
            contract,
            1
        )
    )
    # ========================================================
    # PAYMENT METHOD RISK
    # ========================================================
    payment_method = str(row.get("PaymentMethod","")).strip().lower()
    payment_risk_map = {
        "electronic check": 2,
        "mailed check": 1,
        "bank transfer (automatic)": 0,
        "credit card (automatic)": 0
    }
    row["PaymentMethodRisk"] = (
        payment_risk_map.get(
            payment_method,
            1
        )
    )
    # ========================================================
    # SERVICE COMBINATION
    # ========================================================
    if row["ServiceCount"] == 0:
        service_combination = ("No Services")
    elif row["ServiceCount"] <= 2:
        service_combination = ("Basic")
    elif row["ServiceCount"] <= 5:
        service_combination = ("Moderate")
    else:
        service_combination = ("High")
    row["ServiceCombination"] = (service_combination)
    # ========================================================
    # SERVICE COMBINATION RISK
    # ========================================================
    service_risk_map = {
        "No Services": 2,
        "Basic": 2,
        "Moderate": 1,
        "High": 0
    }
    row["ServiceCombinationRisk"] = (
        service_risk_map.get(
            service_combination,
            1
        )
    )
    # ========================================================
    # HIGH VALUE
    # ========================================================
    row["HighValue"] = int(row["MonthlyCharges"] >= 70)
    # ========================================================
    # HIGH VALUE + HIGH RISK
    # ========================================================
    row["HighValueHighRisk"] = int(
        row["HighValue"] == 1
        and
        row["ContractRisk"] >= 2
    )
    # ========================================================
    # TENURE GROUP
    # ========================================================
    if row["tenure"] <= 12:
        row["TenureGroup"] = "New"
    elif row["tenure"] <= 36:
        row["TenureGroup"] = "Medium"
    else:
        row["TenureGroup"] = "Long"
    # ========================================================
    # MONTHLY CHARGE GROUP
    # ========================================================
    if row["MonthlyCharges"] < 40:
        row["MonthlyChargeGroup"] = "Low"
    elif row["MonthlyCharges"] < 70:
        row["MonthlyChargeGroup"] = "Medium"
    else:
        row["MonthlyChargeGroup"] = "High"
    # ========================================================
    # TOTAL CHARGE GROUP
    # ========================================================
    if row["TotalCharges"] < 1000:
        row["TotalChargeGroup"] = "Low"
    elif row["TotalCharges"] < 3000:
        row["TotalChargeGroup"] = "Medium"
    else:
        row["TotalChargeGroup"] = "High"
    return row
# ============================================================
# PREPARE CUSTOMER FEATURES
# ============================================================
def prepare_customer_features(customer):
    if final_preprocessor is None:
        raise ValueError("Preprocessor is not loaded.")
    engineered_customer = (create_engineered_features(customer))
    X_customer = pd.DataFrame([engineered_customer])
    X_customer = X_customer.drop(columns=["customerID","Churn"],errors="ignore")
    required_columns = (numerical_features+categorical_features)
    for column in required_columns:
        if column not in X_customer.columns:
            if column in numerical_features:
                X_customer[column] = 0
            else:
                X_customer[column] = "Unknown"
    X_customer = X_customer[required_columns]
    X_processed = (final_preprocessor.transform(X_customer))
    return (X_customer,X_processed)
# ============================================================
# PREDICT CHURN
# ============================================================
def predict_customer_churn(customer):
    if final_churn_model is None:
        raise ValueError("XGBoost model is not loaded.")
    (X_original,X_processed) = prepare_customer_features(customer)
    probability = (final_churn_model.predict_proba(X_processed)[0][1])
    prediction = int(probability>=final_churn_threshold)
    return (probability,prediction,X_original,X_processed)
# ============================================================
# RISK LEVEL
# ============================================================
def get_risk_level(probability):
    probability = float(probability)
    if probability >= 0.75:
        return "High Risk"
    elif probability >= 0.50:
        return "Medium Risk"
    else:
        return "Low Risk"
# ============================================================
# FEATURE NAMES
# ============================================================
def get_feature_names():
    if final_preprocessor is None:
        return []
    try:
        return list(final_preprocessor.get_feature_names_out())
    except Exception as e:
        print("Feature name error:",e)
        return []
# ============================================================
# SHAP
# ============================================================
def explain_customer(customer):
    if shap_explainer is None:
        return [], []
    (X_original,X_processed) = prepare_customer_features(customer)
    try:
        shap_result = (shap_explainer(X_processed))
        shap_values = (shap_result.values)
    except Exception:
        shap_values = (shap_explainer.shap_values(X_processed))
    if isinstance(shap_values,list):
        shap_values = (shap_values[-1])
    shap_values = np.asarray(shap_values)
    if shap_values.ndim == 3:
        shap_values = (shap_values[:, :, -1])
    values = shap_values[0]
    feature_names = (get_feature_names())
    if len(feature_names) != len(values):
        feature_names = [f"Feature_{i}"for i in range(len(values))]
    shap_df = pd.DataFrame({"Feature": feature_names,"SHAP_Value": values})
    positive = (
        shap_df[shap_df["SHAP_Value"] > 0].sort_values("SHAP_Value",ascending=False).head(5))
    negative = (shap_df[shap_df["SHAP_Value"] < 0].sort_values("SHAP_Value",ascending=True).head(5))
    return (positive.to_dict(orient="records"),negative.to_dict(orient="records"))
# ============================================================
# DASHBOARD
# ============================================================
@app.route("/")
def dashboard():
    total_customers = len(customer_data)
    if (not customer_data.empty and "Churn" in customer_data.columns):
        churned_customers = (customer_data["Churn"].astype(str).str.strip().str.lower().eq("yes").sum())
    else:
        churned_customers = 0
    if total_customers > 0:
        churn_rate = (churned_customers/total_customers*100)
    else:
        churn_rate = 0
    active_customers = (total_customers-churned_customers)
    return render_template(
        "dashboard.html",
        total_customers=total_customers,
        churned_customers=churned_customers,
        active_customers=active_customers,
        churn_rate=round(churn_rate,2))
# ============================================================
# CUSTOMER PROFILE
# ============================================================
@app.route("/customer",methods=["GET", "POST"])
def customer():
    customer_info = None
    customer_id = None
    error = None
    if request.method == "POST":
        customer_id = request.form.get("customer_id","").strip()
        if not customer_id:
            error = ("Please enter a Customer ID.")
        else:
            customer_row = get_customer(customer_id)
            if customer_row is None:
                error = ("Customer ID not found.")
            else:
                customer_info = (customer_row.to_dict())
    return render_template(
        "customer.html",
        customer=customer_info,
        customer_id=customer_id,
        error=error)
# ============================================================
# PREDICTION
# ============================================================
@app.route("/prediction",methods=["GET", "POST"])
def prediction():
    customer_info = None
    customer_id = None
    probability = None
    prediction_result = None
    risk_level = None
    error = None
    if request.method == "POST":
        customer_id = request.form.get("customer_id","").strip()
        if not customer_id:
            error = ("Please enter a Customer ID.")
        else:
            customer_row = get_customer(customer_id)
            if customer_row is None:
                error = ("Customer ID not found.")
            else:
                try:
                    (
                        probability,
                        prediction_result,
                        _,
                        _
                    ) = predict_customer_churn(
                        customer_row
                    )
                    risk_level = (get_risk_level(probability))
                    customer_info = (customer_row.to_dict())
                except Exception as e:
                    error = ("Prediction failed.")
                    print("Prediction error:",repr(e))
    return render_template(
        "prediction.html",
        customer=customer_info,
        customer_id=customer_id,
        probability=probability,
        prediction_result=prediction_result,
        risk_level=risk_level,
        threshold=final_churn_threshold,
        error=error
    )
# ============================================================
# EXPLANATION
# ============================================================
@app.route("/explanation",methods=["GET", "POST"])
def explanation():
    customer_info = None
    customer_id = None
    probability = None
    positive_factors = []
    protective_factors = []
    error = None
    if request.method == "POST":
        customer_id = request.form.get("customer_id","").strip()
        if not customer_id:
            error = ("Please enter a Customer ID.")
        else:
            customer_row = get_customer(customer_id)
            if customer_row is None:
                error = ("Customer ID not found.")
            else:
                try:
                    (
                        probability,
                        _,
                        _,
                        _

                    ) = predict_customer_churn(
                        customer_row
                    )
                    (
                        positive_factors,
                        protective_factors) = explain_customer(customer_row)
                    customer_info = (customer_row.to_dict())
                except Exception as e:
                    error = (
                        "Unable to generate "
                        "SHAP explanation.")
                    print("SHAP error:",repr(e))
    return render_template(
        "explanation.html",
        customer=customer_info,
        customer_id=customer_id,
        probability=probability,
        positive_factors=positive_factors,
        protective_factors=protective_factors,
        error=error
    )
# AI ASSISTANT
# ============================================================
@app.route("/assistant",methods=["GET", "POST"])
def assistant():
    question = ""
    answer = None
    error = None
    customer_id = ""
    customer_info = None
    # ========================================================
    # GET
    # ========================================================
    if request.method == "GET":
        customer_id = request.args.get("customer_id","").strip()
        # ----------------------------------------------------
        # Load selected customer
        # ----------------------------------------------------
        if customer_id:
            customer_row = get_customer(customer_id)
            if customer_row is None:
                error = ("Customer ID not found.")
            else:
                customer_info = (customer_row.to_dict())
    # ========================================================
    # POST
    # ========================================================
    elif request.method == "POST":
        customer_id = request.form.get("customer_id","").strip()
        question = request.form.get("question","").strip()
        # ----------------------------------------------------
        # Validate question
        # ----------------------------------------------------
        if not question:
            error = ("Please enter a question.")
        # ----------------------------------------------------
        # Load customer if supplied
        # ----------------------------------------------------
        if (error is None and customer_id):
            customer_row = get_customer(customer_id)
            if customer_row is None:
                error = ("Customer ID not found.")
            else:
                customer_info = (customer_row.to_dict())
        # ----------------------------------------------------
        # Ask AI
        # ----------------------------------------------------
        if error is None:
            try:
                print()
                print("=" * 60)
                print("FLASK ASSISTANT REQUEST")
                print("Customer ID:",customer_id)
                print("Question:",question)
                print("=" * 60)
                answer = ask_ai(question,customer_info=customer_info,top_k=5)
                print("\n>>> ask_ai() STARTED <<<")
            except Exception as e:
                print("Assistant error:",repr(e))
                error = ("Unable to generate AI response.")
    # ========================================================
    # RENDER
    # ========================================================
    return render_template(
        "assistant.html",
        question=question,
        answer=answer,
        error=error,
        customer_id=customer_id,
        customer=customer_info
    )
# ============================================================
# START APPLICATION
# ============================================================
def start_application():
    print()
    print("=" * 60)
    print("AI CUSTOMER INTELLIGENCE APPLICATION")
    print("=" * 60)
    print("Starting Flask application...")
    print("URL: http://127.0.0.1:5000")
    print("=" * 60)
    # --------------------------------------------------------
    # Windows Flask console workaround
    # --------------------------------------------------------
    try:
        import click
        original_echo = click.echo
        def safe_echo(message=None,*args,**kwargs):
            try:
                original_echo(message,*args,**kwargs)
            except OSError:
                pass
        click.echo = safe_echo
    except Exception:
        pass
    try:
        app.run(host="127.0.0.1",port=5000,debug=False,use_reloader=False,use_debugger=False,threaded=True,load_dotenv=False)
    except OSError as e:
        print()
        print("Flask startup error:",repr(e))
        print()
        print("Try opening:")
        print("http://127.0.0.1:5000")
# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    start_application()