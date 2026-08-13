from flask import Flask, render_template
import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

app = Flask(__name__)

# ---------------------------------------------------
# Load preprocessed datasets 
# ---------------------------------------------------
data = pd.read_csv(
    'datasets/PJME_preprocessd.csv',
    parse_dates=['Datetime']
)

# Latest demand for predict daily demand
latest_demand = round(data['PJME_MW'].iloc[-1], 2)

# ---------------------------------------------------
# Recreate scalers 
# ---------------------------------------------------

features = [
    'PJME_MW_Scaled',
    'Hour',
    'Day',
    'Week',
    'Month',
    'DayOfWeek',
    'Weekend',
    'Lag_1',
    'Lag_24',
    'Lag_48',
    'Lag_168',
    'RollingMean_24',
    'RollingStd_24',
    'RollingMean_168'
]

feature_scaler = MinMaxScaler()
feature_scaler.fit(data[features])

target_scaler = MinMaxScaler()
target_scaler.fit(data[['PJME_MW']])

# ---------------------------------------------------
# Load best model using the sequential lenght is 168(one week)
# ---------------------------------------------------
best_model = load_model('models/bilstm168_phase6_baseline.keras')

sequence_length = 168

# ---------------------------------------------------
# Dashboard
#show thw overall performance of the timeseries best model 
# ---------------------------------------------------
@app.route('/')
def dashboard():

    metrics = {
        'mae': 1390.79,
        'rmse': 1894.49,
        'mape': 3.53,
        'r2': 0.918
    }

    return render_template(
        'dashboard.html',
        latest_demand=latest_demand,
        best_model='Bidirectional LSTM',
        metrics=metrics
    )

# ---------------------------------------------------
# Forecast Page
#It can show 24 hours forecast details
# ---------------------------------------------------
@app.route('/forecast')
def forecast():

    # Last 168 hours of data
    latest_data = data[features].tail(sequence_length)

    # Scale the input features
    latest_scaled = feature_scaler.transform(latest_data)

    # Create model input
    X_input = np.array([latest_scaled])

    # Predict next 24 hours
    prediction = best_model.predict(X_input, verbose=0)

    # Convert prediction back to MW
    forecast_values = target_scaler.inverse_transform(
        prediction.reshape(-1, 1)
    ).flatten()

    forecast_values = np.round(forecast_values, 2)

    # Last timestamp in the dataset
    last_time = pd.to_datetime(data['Datetime'].iloc[-1])

    # Generate next 24 hourly timestamps
    forecast_times = pd.date_range(
        start=last_time + pd.Timedelta(hours=1),
        periods=24,
        freq='h'
    )

    # Create forecast dataframe
    forecast_df = pd.DataFrame({
        'Datetime': forecast_times,
        'Predicted_Demand': forecast_values
    })

    # Add day name
    forecast_df['Day'] = forecast_df['Datetime'].dt.day_name()

    # Highest demand
    highest = forecast_df.loc[
        forecast_df['Predicted_Demand'].idxmax()
    ]

    # Lowest demand
    lowest = forecast_df.loc[
        forecast_df['Predicted_Demand'].idxmin()
    ]

    # Average demand
    average_demand = round(
        forecast_df['Predicted_Demand'].mean(),
        2
    )

    # Convert dataframe to list for Jinja
    forecast_table = forecast_df.to_dict(orient='records')

    return render_template(
        'forecast.html',
        forecast_table=forecast_table,
        highest_day=highest['Day'],
        highest_value=round(highest['Predicted_Demand'], 2),
        highest_time=highest['Datetime'].strftime('%I:%M %p'),
        lowest_day=lowest['Day'],
        lowest_value=round(lowest['Predicted_Demand'], 2),
        lowest_time=lowest['Datetime'].strftime('%I:%M %p'),
        average_demand=average_demand
    )
# ---------------------------------------------------
# Analytics analysis page show the comparison for model (baseline,deep learning and model improvement table)
#show the validation chart for error,peak demand and actual vs predictes demand
# ---------------------------------------------------
@app.route('/analytics')
def analytics():

    phase4 = pd.read_csv('datasets/baseline_model_comparison.csv')
    phase5 = pd.read_csv('datasets/phase5_comparison.csv')
    phase6 = pd.read_csv('datasets/phase6_comparison.csv')

    return render_template(
        'analytics.html',
        phase4=phase4.to_dict(orient='records'),
        phase5=phase5.to_dict(orient='records'),
        phase6=phase6.to_dict(orient='records')
    )
# ---------------------------------------------------
# Validation
#predict the demand for 60 and 30 days
# ---------------------------------------------------
@app.route('/validation')
def validation():

    metrics = {
        'mae': 1390.79,
        'rmse': 1894.49,
        'mape': 3.53,
        'r2': 0.918
    }

    return render_template(
        'validation.html',
        metrics=metrics
    )

# ---------------------------------------------------
# Run
# ---------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)